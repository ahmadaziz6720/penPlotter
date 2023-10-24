current_z = 0

with open("coordinates.txt", "r") as file:
    gcode_lines = []
    
    for line in file:
        line = line.strip()
        if line == 'z':
            gcode_lines.append("G1 Z1\n")
        else:
            x, y = line.split(',')
            gcode = "G1 X{} Y{} Z0\n".format(x, y)
            gcode_lines.append(gcode)

with open("output.gcode", "w") as output_file:
    output_file.writelines(gcode_lines)

print("G-code generation complete.")
