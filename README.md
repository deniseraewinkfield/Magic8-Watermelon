MicroPython I2C driver for SSD1306 OLED displays. Supports 128x64 and 128x32 monochrome displays with text rendering, graphics, and power management features. 
This library is needed to make the screen accessible in micropython. (ssd1306.py)
For (magic_8_glove.py), this file was saved onto the microcontroller. 
To begin, pins 22 and 21 handle, SDA and SCL respectively, both are used by the screen and the accelerator through 12C on different buses.
SDA = Serial Data 
SCL = Serial Clock 
Project Goal = Measure and display real-time g-force readings using an ADXL375 accelerometer and SSD1306 OLED display for a "Magic 8 Watermelon" wearable device.
