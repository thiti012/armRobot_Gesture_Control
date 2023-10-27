#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#define I2CAdd 0x41  // Define the I2C address here
#define SERVOMIN 150  // Minimum PWM value for 0 degrees
#define SERVOMAX 600  // Maximum PWM value for 180 degrees

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(I2CAdd);  // Use the I2C address

int default_angle[4] = {75, 90, 90, 60};

void setup() {
  pwm.begin();
  pwm.setPWMFreq(60);  // Set the PWM frequency to 60 Hz (adjust as needed)
  Serial.begin(115200);

  for (size_t i = 0; i < 4; i++) {
    int pwmValue = map(default_angle[i], 0, 180, SERVOMIN, SERVOMAX);
    pwm.setPWM(i, 0, pwmValue);
  }
}

byte angle[4];
byte pre_angle[4];
long t = millis();

void loop() {
  if (Serial.available()) {
    Serial.readBytes(angle, 4);
    for (size_t i = 0; i < 4; i++) {
      if (angle[i] != pre_angle[i]) {
        int pwmValue = map(angle[i], 0, 180, SERVOMIN, SERVOMAX);
        pwm.setPWM(i, 0, pwmValue);
        pre_angle[i] = angle[i];
      }
    }
    t = millis();
  }

  if (millis() - t > 2000) {
    for (size_t i = 0; i < 4; i++) {
      int pwmValue = map(default_angle[i], 0, 180, SERVOMIN, SERVOMAX);
      pwm.setPWM(i, 0, pwmValue);
      pre_angle[i] = default_angle[i];
    }
  }
}

