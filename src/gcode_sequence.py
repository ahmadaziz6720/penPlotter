import serial
import os

serial_port = "COM5"
baud_rate = 115200 

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
except serial.SerialException:
    print(f"Failed to open {serial_port}")
    exit()


def send_gcode(gcode_command):
    print(f"- {gcode_command}")
    ser.write((gcode_command + '\n').encode())
    ser.flush()
    # print(f"Sent: {gcode_command}")

    response = ""
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            response += line + "\n"
        if "ok" in line.lower():
            break
    # print(f"Respons: {response}")

# start gcode
send_gcode("G28")
send_gcode("M220 S1000")
send_gcode("G0 X0 Y0 Z2")  

send_gcode("M300 S200 P200") # beep
send_gcode("G0 X45 Y130 Z2") # home for pen
send_gcode("G92 X0 Y0")

while 1:
    x_cursor = 0

    string = input("Enter a string: ")
    font_size = float(input("Enter font size: "))
    spacing = font_size

    send_gcode(f"G0 Y-{str(font_size*10+1)}")
    send_gcode("G92 X0 Y0")

    # define array for each letter
    letters = []
    # read coordinates from file
    coordinates_folder = 'src/coordinates'
    for letter in string:
        if letter == ' ':
            letters.append('s')
            continue
        with open(os.path.join(coordinates_folder, f'{letter}.txt'), 'r') as file:
            letter_width = 0
            letter_coordinates = []
            for line in file:
                line = line.strip()
                if line == 'z':
                    letter_coordinates.append('z')
                else:
                    x, y = line.split(',')
                    letter_coordinates.append((float(x)*font_size, float(y)*font_size))
                    if float(x)*font_size > letter_width:
                        letter_width = float(x)*font_size
            # letter_coordinates.append("w")
            letter_coordinates.append(letter_width)
            letters.append(letter_coordinates)

    z = True
    for letter in letters:
        #check if letter is space
        if letter == 's':
            send_gcode("G0 Z1")
            send_gcode(f"G0 X{str(font_size*5)} Y0")
            send_gcode("G92 X0 Y0")
            z = True
            x_cursor += font_size*5
        else:
            letter_width = letter[-1]
            for coordinate in letter:
                if coordinate == 'z':
                    send_gcode("G0 Z1")
                    z = True
                        
                elif type(coordinate) == tuple:
                    x, y = coordinate
                    send_gcode(f"G0 X{x} Y{y}")
                    if z:
                        send_gcode("G0 Z0")
                        z = False
                else:
                    continue
                
        # print("------------next letter-----------")
        if letters.index(letter) != len(letters)-1 and letter != 's':
            send_gcode("G0 Z1")
            z = True
            send_gcode(f"G0 X{str(letter_width+spacing)} Y0")
            x_cursor += letter_width + spacing
            send_gcode("G92 X0 Y0")

    send_gcode("M300 S440 P200")
    # send_gcode("M300 S200 P200")  # beep
    # send_gcode("M300 S300 P500")

    send_gcode("G0 Z2")
    send_gcode(f"G0 X-{x_cursor}")
