import time
import serial

HOST="WINDOWS"
PORT_LINUX='/dev/ttyUSB0'
PORT_WINDOWS='COM3'
BAUDRATE = 115200

#configuração da Serial
if HOST=="LINUX" :
    serialPort = serial.Serial(
        port=PORT_LINUX, baudrate=BAUDRATE , bytesize=serial.EIGHTBITS, timeout=2, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE,
    )
elif HOST=="WINDOWS" :
    serialPort = serial.Serial(
        port=PORT_WINDOWS, baudrate=BAUDRATE, bytesize=serial.EIGHTBITS, timeout=2, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE,
    )


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    serialString = ""  # Used to hold data coming over UART

    serialPort.write(b"Hello! Serial Test \r\n")
    #serialPort.write(b"Hi How are you \r\n")

    while 1:
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found
            serialString = serialPort.readline()

            # Print the contents of the serial data
            try:
                print(serialString.decode("Ascii"))
            except:
                pass
