# Use serial communication
# Source: https://stm32python.gitlab.io/en/docs/Micropython/STARTWB55/uart

# https://docs.micropython.org/en/latest/esp32/quickref.html#uart-serial-bus
# Changed: input only
# default pins are listed below
#    | UART0 | UART1 | UART2
#    -----------------------
# tx | 1     | 10     | 17
# rx | 3     | 9      | 16

from time import sleep, sleep_ms, time
from machine import unique_id
from machine import UART
from machine import Pin
from binascii import hexlify

# Set up the LED on pin26 as an output pin
led = Pin(26, Pin.OUT)

# obtain unigue board identifier, gives a UTF8 coded text representation
id_board = hexlify(unique_id()).decode("utf-8")
print("Board Identifier: " + id_board)

# UART Initialization
uart = UART(2, baudrate=115200, timeout=100)

# First reading to empty UART RX receive queue
uart.read()

# counter
counter = 0

while True:

    # Timestamp
    timestamp = time()
    

    # Receiving a possible message
    # Reading bytes/characters in the RX receive queue
    message_received = uart.read() # Read the received characters to the end
    
    # If there was indeed a pending message in the Rx ...
    if not (message_received is None):

        try:
            # debug message
            # print("\ndebug: " + message_received.decode("utf-8") + "\n")
            # split received message_received in list of messages
            messages = message_received.split()
            # minimum content is one board_id plus one counter
            if len(messages) >= 2:
                # access last board_id and last_counter
                last_message = messages[-2] + " " + messages[-1]
                # Interprets bytes read as a string encoded in UTF8
                message_decode = last_message.decode("utf-8")
                # Displays the received message on the serial port of the USB User
                print(str(timestamp) + " received message: " + message_decode)

        except UnicodeError:
            print("UnicodeError")
        
    # toggle LED
    led.toggle()
    
    # increment counter
    counter += 1

    # timeout
    sleep(5)
    