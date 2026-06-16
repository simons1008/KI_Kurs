# Use parallel input
# Source: https://stm32python.gitlab.io/en/docs/Micropython/STARTWB55/uart
# Changed: use parallel input


from time import sleep, sleep_ms, time
from machine import unique_id
from machine import UART
from machine import Pin
from binascii import hexlify

# define output pin on GPIO26
led = Pin(26, Pin.OUT)

# obtain unigue board identifier, gives a UTF8 coded text representation
id_board = hexlify(unique_id()).decode("utf-8")
print("Board Identifier: " + id_board)

# define input pin on GPIO18
p18 = Pin(18, Pin.IN)
# define input pin on GPIO19
p19 = Pin(19, Pin.IN)

while True: 
    
    # Timestamp
    timestamp = time()
    
    # make label_code
    bit0 = p18.value()
    bit1 = p19.value()
    label_code = (bit1 << 1) | bit0

    # Displays the status of the input pins on the serial port of the USB User
    # print(str(timestamp) + " status of input pins " + str(label) + "\n")
    
    # decode labe
    if label_code == 0:
        label = "letter_S"
    elif label_code == 1:
        label = "letter_F"
    elif label_code == 2:
        label = "letter_Z"
    elif label_code == 3:
        label = "unknown"
    else:
        label = "unsupported label"
  
    print(str(timestamp) + " parallel message: " + label + "\n")

    # toggle LED
    led.toggle()
    
    # timeout
    sleep(5)
