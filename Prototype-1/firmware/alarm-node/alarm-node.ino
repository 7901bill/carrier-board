#include <RCSwitch.h>

RCSwitch mySwitch = RCSwitch();

const int buzzerPin = 3;  // passive buzzer connected to D3

void setup() {
  Serial.begin(9600);
  mySwitch.enableReceive(0);  // interrupt 0 → pin 2 on Uno
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  if (mySwitch.available()) {
    long received = mySwitch.getReceivedValue();

    Serial.print("Received: ");
    Serial.println(received);

    if (received == 22222) {   // cat
      Serial.println("MATCH: Received 22222 (cat)");
      playBeepPattern();
    }
    else if (received == 11111) { // dog
      Serial.println("MATCH: Received 11111 (dog)");
      playBeepPattern();
    }
    else if (received == 12345) { // default
      Serial.println("MATCH: Received 12345 (default)");
      playBeepPattern();
    }

    mySwitch.resetAvailable();
  }
}

void playBeepPattern() {
  // triple short beeps
  for (int i = 0; i < 3; i++) {
    tone(buzzerPin, 1000);   // play 1kHz tone
    delay(200);              // tone duration
    noTone(buzzerPin);       // stop tone
    delay(150);              // gap
  }
}
