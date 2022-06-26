import serial
import sys

# list the serials
# python3 -m serial.tools.list_ports

def main(file_to_print):

    # ser = serial.Serial('/dev/ttyACM0')  # open serial port
    ser = serial.Serial('/dev/cu.usbmodem123451')
    print(ser.name)         # check which port was really used

    # open the file
    with open(file_to_print) as fp:
        # increase the punch speed
        ser.write("**p30".encode('utf-8'))
        ser.write("**d100".encode('utf-8'))
        # test the punches
        ser.write("**t4".encode('utf-8'))
        # advance the tape 400mm
        ser.write("**f125".encode('utf-8'))

        # start sending
        for line in fp:
            ser.write(line.encode('utf-8'))

        # advance the tape
        ser.write("**f125".encode('utf-8'))
        ser.write("**t4".encode('utf-8'))
        ser.write("**f63".encode('utf-8'))

    ser.flush()
    ser.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Please pass the filename to send on the commandline")
    else:
        main(sys.argv[1])
