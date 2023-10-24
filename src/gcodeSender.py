import serial
import time

serial_port = "COM5"
baud_rate = 115200 

try:
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
except serial.SerialException:
    print(f"Gagal membuka koneksi ke {serial_port}. Pastikan port serial yang benar.")
    exit()

def send_gcode(gcode_command):
    ser.write((gcode_command + '\n').encode())
    ser.flush()
    print(f"Sent: {gcode_command}")

    response = ""
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            response += line + "\n"
        if "ok" in line.lower():
            break

    print(f"Respons: {response}")

# Command List
"""
X50 Y10 Z0          # home for pen
G0 X10 Y10 Z0       # linear move
G28 X Y             # Homeing
M300 S440 P200      # Play buzzer
M220 S500           # Set speed
"""
# send_gcode("G28")
# send_gcode("M220 S500")
# send_gcode("G0 Z1")
# send_gcode("G92 X0 Y0 Z0")
# send_gcode("M300 S440 P200")
# send_gcode("M300 S200 P200")
send_gcode("G0 X50 Y170 Z1")
# send_gcode("G0 X50 Y110 Z0")
# send_gcode("G0 X150 Y110 Z0")
# send_gcode("G0 X150 Y10 Z0")
# send_gcode("G0 X50 Y10 Z0")
# send_gcode("G0 X150 Y110 Z0")
# send_gcode("G0 X50 Y110 Z0")
# send_gcode("G0 X150 Y10 Z0")
# send_gcode("G0 X50 Y10 Z0")

# gcode_file = open("output.gcode", "r")

# for line in gcode_file:
#     print(line.strip())
#     send_gcode(line.strip())
    
send_gcode("M300 S440 P200")
send_gcode("M300 S200 P200")

ser.close()
