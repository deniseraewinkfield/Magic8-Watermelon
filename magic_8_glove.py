from machine import Pin, I2C
import ssd1306
import time
import math

# I2C setup
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=400000)

# Initialize OLED (128x64)
oled = ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# ADXL375 setup
ADXL375_ADDR = 0x53
POWER_CTL = 0x2D
DATA_FORMAT = 0x31
DATAX0 = 0x32

# Glove mass constant
GLOVE_MASS_KG = 0.244  # 8.6 oz converted to kg

class ADXL375:
    def __init__(self, i2c, address=0x53):
        self.i2c = i2c
        self.address = address
        
        # Wake up the sensor
        self.i2c.writeto_mem(self.address, POWER_CTL, b'\x08')
        time.sleep_ms(10)
        
        # Set data format
        self.i2c.writeto_mem(self.address, DATA_FORMAT, b'\x0B')
        time.sleep_ms(10)
        
    def read_accel(self):
        # Read 6 bytes starting from DATAX0
        data = self.i2c.readfrom_mem(self.address, DATAX0, 6)
        
        # Convert to signed 16-bit values
        x = int.from_bytes(data[0:2], 'little')
        if x > 32767:
            x -= 65536
            
        y = int.from_bytes(data[2:4], 'little')
        if y > 32767:
            y -= 65536
            
        z = int.from_bytes(data[4:6], 'little')
        if z > 32767:
            z -= 65536
        
        # Scale for ADXL375
        scale = 0.61
        
        return x * scale, y * scale, z * scale

# Initialize sensor
try:
    accel = ADXL375(i2c, ADXL375_ADDR)
    oled.fill(0)
    oled.text("ADXL375 Ready!", 0, 0)
    oled.show()
    time.sleep(1)
    print("ADXL375 initialized successfully!")
except Exception as e:
    oled.fill(0)
    oled.text("Sensor Error!", 0, 0)
    oled.show()
    print("Error:", e)
    raise

# Main loop
print("Starting readings...")
while True:
    try:
        # Read acceleration
        x, y, z = accel.read_accel()
        
        # Calculate magnitude in g's
        mag_g = math.sqrt(x*x + y*y + z*z)
        
        # Convert to Newtons: F = m * a
        # where a = mag_g * 9.81 m/s²
        force_n = GLOVE_MASS_KG * mag_g * 9.81
        
        # Clear display
        oled.fill(0)
        
        # Display title at top
        oled.text("Magic8Watermelon", 0, 0)
        
        # Display both g-force and Newtons
        oled.text("G-Force:", 10, 20)
        oled.text("{:.1f} g".format(mag_g), 20, 32)
        
        oled.text("Force:", 10, 45)
        oled.text("{:.2f} N".format(force_n), 20, 57)
        
        oled.show()
        
        # Print to console
        print("G-Force: {:.1f} g | Force: {:.2f} N".format(mag_g, force_n))
        
        time.sleep_ms(1000)  # Update every 1.5 seconds
        
    except KeyboardInterrupt:
        print("Stopped by user")
        break
    except Exception as e:
        print("Error:", e)
        time.sleep(1)
