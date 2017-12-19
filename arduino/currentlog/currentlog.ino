
#include <SoftReset.h> 	//https://github.com/WickedDevice/SoftReset
#include <EmonLib.h>   	// https://github.com/openenergymonitor/EmonLib

int DELAY_BTW_PACKET = 40; 
int NB_ADC = 3; // nombre de mesures pour faire une moyenne de courant

const byte num_capteurs = 2;
int currents[num_capteurs] = {0};

EnergyMonitor emon[num_capteurs];
CRC32 crc;

const byte buffSize = 40;
char inputBuffer[buffSize] = {0};
const char startMarker = '<';
const char endMarker = '>';
const char delimiterMarker = ',';
const char crcMarker = ';';

byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromRPI = false;
boolean receivedACK = false;

char messageFromRPI[buffSize] = {0};
int newFlashInterval = 0;

unsigned long curMillis;

double getCurrentByIndex(byte i) {
	int n = 0;
	double curr = 0;
	curr = emon[i].calcIrms(1480);  // Calculate Irms only
	return(234 * curr); // Apparent power
//	return 111;
}

void executeCommands(){
	if (newDataFromRPI) {
		newDataFromRPI = false;
		if (strcmp(messageFromRPI, "ISREADY") == 0) {
			sendResponse("<READY>");
		}
		if (strcmp(messageFromRPI, "VALUES") == 0) {
			sendValues();
		}
		if (strcmp(messageFromRPI, "v") == 0) {
			sendValues();
		}
		if (strcmp(messageFromRPI, "UPTIME") == 0) {
			sendUptime();
		}
		if (strcmp(messageFromRPI, "REBOOT") == 0) {
			sendResponse("<REBOOTING>");
			soft_restart();
		}
	}
}

void sendUptime(){
	char uptime[32];
	long curMillis = millis();
	sprintf(uptime,"<UPTIME=%0ld>", curMillis / 1000);
	Serial.println(uptime);
	delay(DELAY_BTW_PACKET);
	Serial.println(uptime);
}

//concatene un char dans une string
void appendChar(char* s, char c) {
	int len = strlen(s);
	s[len] = c;
	s[len+1] = '\0';
}
	
void sendValues(){
	char crcbuff[32] = "";
	char trame[32] = "";
	char buff[16] = "";
	int i;
	int checksum = 0;
	Serial.print(startMarker);
	for(i=0; i<num_capteurs; i++) {
		currents[i] = (int)getCurrentByIndex(i);
		checksum += currents[i];
		sprintf(buff,"%i", currents[i]);
		strcat(trame, buff);
		if (i != num_capteurs-1){
			appendChar(trame, delimiterMarker);
		}
	}
	Serial.print(trame);
	Serial.print(crcMarker);
	sprintf(crcbuff,"%i", checksum);
	Serial.print(crcbuff);
	Serial.println(endMarker);
//<v>
}
void sendResponse(char response[]) {
	Serial.println(response);
	delay(DELAY_BTW_PACKET);
	Serial.println(response);
}

//=============
// receive data from RPI and save it into inputBuffer
void getDataFromRPI() {    
  if(Serial.available() > 0) {
    char x = Serial.read();

    if (x == endMarker) {
      readInProgress = false;
      newDataFromRPI = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}

//=============
// split the data into its parts
//trame ack : <ACK>
void parseData() {
  char * strtokIndx; // this is used by strtok() as an index
  
  strtokIndx = strtok(inputBuffer,","); // get the first part of the string
  strcpy(messageFromRPI, strtokIndx); // copy it to messageFromRPI
  
  strtokIndx = strtok(NULL, ","); // this continues where the previous call left off
  newFlashInterval = atoi(strtokIndx);     // convert this part to an integer
}

void setup() {
	Serial.begin(9600);
	emon[1].current(5, 111.1); //100A inconsistent value on boot
	emon[0].current(4, 28); //30A
//	getCurrent to avoid inconsistent readings after boot
	for(byte n=0; n<10; n++) {
		for(byte i=0; i<num_capteurs; i++) {
			currents[i] = (int)getCurrentByIndex(i);
		}
	}
}

//=============
void loop() {
	getDataFromRPI();
	executeCommands();
}
