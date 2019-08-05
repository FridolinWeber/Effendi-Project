#include "I2Cdev.h"
#include "MPU6050_6Axis_MotionApps20.h"

#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif

MPU6050 mpu;

#define OUTPUT_READABLE_YAWPITCHROLL

#define LED_PIN 13 // (Arduino is 13, Teensy is 11, Teensy++ is 6)
bool blinkState = false;

// MPU control/status vars
bool dmpReady = false;  // set true if DMP init was successful
uint8_t mpuIntStatus;   // holds actual interrupt status byte from MPU
uint8_t devStatus;      // return status after each device operation (0 = success, !0 = error)
uint16_t packetSize;    // expected DMP packet size (default is 42 bytes)
uint16_t fifoCount;     // count of all bytes currently in FIFO
uint8_t fifoBuffer[64]; // FIFO storage buffer

// orientation/motion vars
Quaternion q;           // [w, x, y, z]         quaternion container
VectorInt16 aa;         // [x, y, z]            accel sensor measurements
VectorInt16 aaReal;     // [x, y, z]            gravity-free accel sensor measurements
VectorInt16 aaWorld;    // [x, y, z]            world-frame accel sensor measurements
VectorFloat gravity;    // [x, y, z]            gravity vector
float euler[3];         // [psi, theta, phi]    Euler angle container
float ypr[3];           // [yaw, pitch, roll]   yaw/pitch/roll container and gravity vector

// packet structure for InvenSense teapot demo
uint8_t teapotPacket[14] = { '$', 0x02, 0,0, 0,0, 0,0, 0,0, 0x00, 0x00, '\r', '\n' };

volatile bool mpuInterrupt = false;     // indicates whether MPU interrupt pin has gone high
void dmpDataReady() {
    mpuInterrupt = true;
}
int Xdeger, Ydeger;
char veri[30];
void setup() {
    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
        TWBR = 24; // 400kHz I2C clock (200kHz if CPU is 8MHz)
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif
    
    Serial.begin(38400);
    //while (!Serial); // wait for Leonardo enumeration, others continue immediately

    // initialize device
    Serial.println(F("Initializing I2C devices..."));
    mpu.initialize();

    // verify connection
    Serial.println(F("Testing device connections..."));
    //Serial.println(mpu.testConnection() ? F("MPU6050 connection successful") : F("MPU6050 connection failed"));
    
    // load and configure the DMP
    Serial.println(F("Initializing DMP..."));
    devStatus = mpu.dmpInitialize();

    // supply your own gyro offsets here, scaled for min sensitivity
    mpu.setXGyroOffset(220);
    mpu.setYGyroOffset(76);
    mpu.setZGyroOffset(-10);
    mpu.setZAccelOffset(1788); // 1688 factory default for my test chip

    // make sure it worked (returns 0 if so)
    if (devStatus == 0) {
        // turn on the DMP, now that it's ready
        Serial.println(F("Enabling DMP..."));
        mpu.setDMPEnabled(true);

        // enable Arduino interrupt detection
        //Serial.println(F("Enabling interrupt detection (Arduino external interrupt 0)..."));
        attachInterrupt(0, dmpDataReady, RISING);
        mpuIntStatus = mpu.getIntStatus();

        // set our DMP Ready flag so the main loop() function knows it's okay to use it
        Serial.println(F("DMP ready! Waiting for first interrupt..."));
        dmpReady = true;

        // get expected DMP packet size for later comparison
        packetSize = mpu.dmpGetFIFOPacketSize();
    } else {
        Serial.print(F("DMP Initialization failed (code "));
        Serial.print(devStatus);
        Serial.println(F(")"));
    }

    // configure LED for output
    pinMode(LED_PIN, OUTPUT);
}

void loop() {
    // if programming failed, don't try to do anything
    if (!dmpReady) return;

    // wait for MPU interrupt or extra packet(s) available
    while (!mpuInterrupt && fifoCount < packetSize) {
    }

    // reset interrupt flag and get INT_STATUS byte
    mpuInterrupt = false;
    mpuIntStatus = mpu.getIntStatus();

    // get current FIFO count
    fifoCount = mpu.getFIFOCount();

    // check for overflow (this should never happen unless our code is too inefficient)
    if ((mpuIntStatus & 0x10) || fifoCount == 1024) {
        // reset so we can continue cleanly
        mpu.resetFIFO();
        Serial.println(F("FIFO overflow!"));

    // otherwise, check for DMP data ready interrupt (this should happen frequently)
    } else if (mpuIntStatus & 0x02) {
        // wait for correct available data length, should be a VERY short wait
        while (fifoCount < packetSize) fifoCount = mpu.getFIFOCount();

        // read a packet from FIFO
        mpu.getFIFOBytes(fifoBuffer, packetSize);
        
        // track FIFO count here in case there is > 1 packet available
        // (this lets us immediately read more without waiting for an interrupt)
        fifoCount -= packetSize;
        
      if(Serial.available()){
        
        char rx_char;
        rx_char = Serial.read();
          if (rx_char == '.'){       //only when the program in python on the computer sends a "." to the Arduino, the current angles are transmitted. Otherwise, too many data are transmitted that the program cannot handle in an appropriate time
                 #ifdef OUTPUT_READABLE_YAWPITCHROLL
                    // display Euler angles in degrees
                    mpu.dmpGetQuaternion(&q, fifoBuffer);
                    mpu.dmpGetGravity(&gravity, &q);
                    mpu.dmpGetYawPitchRoll(ypr, &q, &gravity);
                    
                   /* analogRead(0);
                    int pressureValue0 = analogRead(0);
                    
                    analogRead(1); //trashanalogreadings due to impedance when Arduino switches to multiplexer readout.
                    int pressureValue1 = analogRead(1);

                    analogRead(2);
                    int pressureValue2 = analogRead(2);

                    analogRead(3);
                    int pressureValue3 = analogRead(3);

                    analogRead(4);
                    int pressureValue4 = analogRead(4);
                    
                    analogRead(5);
                    int pressureValue5 = analogRead(5);

                    analogRead(6);
                    int pressureValue6 = analogRead(6);
                    
                    analogRead(7);
                    int pressureValue7 = analogRead(7);
                    
                    analogRead(8);
                    int pressureValue8 = analogRead(8);
                    
                    analogRead(9);
                    int pressureValue9 = analogRead(9);
                    
                    //analogRead(10);
                    //int pressureValue10 = analogRead(10);
*/
                    

                    
                    //Serial.print(ypr[0] * 180/M_PI);
                    Xdeger = ypr[0] * 180/M_PI;
                    Ydeger = ypr[1] * 180/M_PI;
                    //Serial.print(";");
                    //Serial.print(ypr[1] * 180/M_PI);
                    //Serial.println(";");
                    //Serial.print(ypr[2] * 180/M_PI);
                    //Serial.print(";");





                    sprintf(veri, "%d, %d", Xdeger, Ydeger);

                    //Son olarak elimizdekileri Serial e yazdırdık
                     Serial.println(veri);
                  /*  
                    Serial.print(pressureValue0);
                    Serial.print(";");
                    Serial.print(pressureValue1);
                    Serial.print(";");
                    Serial.print(pressureValue2);
                    Serial.print(";");
                    Serial.print(pressureValue3);
                    Serial.print(";");
                    Serial.print(pressureValue4);
                    Serial.print(";");
                    Serial.print(pressureValue5);
                    Serial.print(";");
                    Serial.print(pressureValue6);
                    Serial.print(";");
                    Serial.print(pressureValue7);
                    Serial.print(";");
                    Serial.print(pressureValue8);
                    Serial.print(";");
                    Serial.print(pressureValue9);
                    Serial.println(";");
                    
       */
                #endif
          }
      }
      
        // blink LED to indicate activity
        blinkState = !blinkState;
        digitalWrite(LED_PIN, blinkState);
    }
}
