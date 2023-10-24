import matplotlib.pyplot as plt
import cv2
import numpy as np
import os

def generate_coordinates(input_image_path, output_coordinates_path):
    input_image = cv2.imread(input_image_path)
    input_image = cv2.rotate(input_image, cv2.ROTATE_180)
    input_image = cv2.flip(input_image, 1)

    # Convert to array
    input_array = np.array(input_image)
    input_array = cv2.cvtColor(input_array, cv2.COLOR_RGBA2RGB)

    # Convert to grayscale
    gray_image = cv2.cvtColor(input_array, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray_image, 127, 255, 0)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Array of approx contours
    approx_contours = []

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.001 * cv2.arcLength(contour, True), True)
        for i in range(len(approx)):
            x1, y1 = approx[i][0]
            x2, y2 = approx[(i + 1) % len(approx)][0]
        approx_contours.append(approx)

    approx_leftmost = float('inf')
    approx_bottommost = float('inf')

    for i in range(len(approx_contours)):
        for j in range(len(approx_contours[i])):
            x, y = approx_contours[i][j][0]
            approx_leftmost = min(approx_leftmost, x)
            approx_bottommost = min(approx_bottommost, y)

    # Shift to 0, 0
    approx_shift_x = -approx_leftmost
    approx_shift_y = -approx_bottommost

    for i in range(len(approx_contours)):
        for j in range(len(approx_contours[i])):
            approx_contours[i][j][0][0] += approx_shift_x
            approx_contours[i][j][0][1] += approx_shift_y

    # Scaling
    approx_y_max = -float('inf')
    for i in range(len(approx_contours)):
        for j in range(len(approx_contours[i])):
            x, y = approx_contours[i][j][0]
            approx_y_max = max(approx_y_max, y)

    approx_scaling_factor = 10.0 / approx_y_max

    lines = []
    for i in range(len(approx_contours)):
        line_segment = []
        for j in range(len(approx_contours[i])):
            x = approx_contours[i][j][0][0] * approx_scaling_factor
            y = approx_contours[i][j][0][1] * approx_scaling_factor
            line_segment.append((x, y))
        lines.append(line_segment)

    # Export to coordinates text file
    with open(output_coordinates_path, 'w') as file:
        file.write('z\n')
        for line in lines:
            for point in line:
                x, y = point
                file.write(f'{x},{y}\n')
            x, y = line[0]
            file.write(f'{x},{y}\n')
            if line != lines[-1]:
                file.write('z\n')
            else:
                continue
            
# folder
font_folder = './img/font'
output_folder = 'src/coordinates'

os.makedirs(output_folder, exist_ok=True)

for font_name in 'abcdefghijklmnopqrstuvwxyz':
    input_image_path = os.path.join(font_folder, f'{font_name}.png')
    output_coordinates_path = os.path.join(output_folder, f'{font_name}.txt')
    generate_coordinates(input_image_path, output_coordinates_path)
    print(f'Generated coordinates for font: {font_name}')
