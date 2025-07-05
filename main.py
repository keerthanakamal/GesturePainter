import cv2
import numpy as np
from utils.hand_detector import HandDetector
from utils.gesture_controller import fingers_up

# Function to detect shape
def detect_shape(canvas):
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return "No Shape"

    largest = max(contours, key=cv2.contourArea)
    if cv2.contourArea(largest) < 100:
        return "Too Small"

    approx = cv2.approxPolyDP(largest, 0.04 * cv2.arcLength(largest, True), True)
    sides = len(approx)

    if sides == 3:
        return "Triangle"
    elif sides == 4:
        return "Rectangle"
    elif sides > 4:
        area = cv2.contourArea(largest)
        perimeter = cv2.arcLength(largest, True)
        circularity = 4 * np.pi * area / (perimeter * perimeter)
        if 0.7 < circularity < 1.2:
            return "Circle"
        else:
            return "Polygon"
    else:
        return "Unknown"

# State variables
is_drawing = False
eraser_mode = False
drawing_color = (0, 0, 255)
brush_thickness = 7
eraser_thickness = 50
color_selected = False
manual_pause = False

# Colors
colors = {
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "blue": (255, 0, 0),
    "yellow": (0, 255, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}

# Color palette layout
color_buttons = []
x_offset = 20
box_width = 60
box_height = 60
spacing = 20

for i, (name, color) in enumerate(colors.items()):
    x1 = x_offset + i * (box_width + spacing)
    y1 = 10
    x2 = x1 + box_width
    y2 = y1 + box_height
    color_buttons.append((x1, y1, x2, y2, color, name))

# Video setup
cap = cv2.VideoCapture(0)
detector = HandDetector(detection_confidence=0.8)
ret, frame = cap.read()
h, w, _ = frame.shape
canvas = np.zeros((h, w, 3), dtype=np.uint8)
prev_x, prev_y = 0, 0

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    output = frame.copy()

    frame = detector.find_hands(frame)
    lm_list = detector.find_position(frame)

    if lm_list:
        x, y = lm_list[8][1], lm_list[8][2]
        fingers = fingers_up(lm_list)

        # Color selection
        for (x1, y1, x2, y2, color, name) in color_buttons:
            if x1 < x < x2 and y1 < y < y2:
                drawing_color = color
                eraser_mode = (name == "black")
                is_drawing = False
                color_selected = True
                cv2.putText(output, f"{name.upper()} SELECTED", (10, 130),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        # Drawing gesture
        if fingers == [0, 1, 0, 0, 0]:
            is_drawing = True
            cv2.putText(output, "Drawing Mode", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Pause gesture
        if fingers == [1, 1, 1, 1, 1]:
            is_drawing = False
            manual_pause = True
            prev_x, prev_y = 0, 0
            cv2.putText(output, "Paused", (10, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 128), 2)

        # Drawing / Erasing
        if is_drawing and color_selected and not manual_pause:
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x, y

            if eraser_mode:
                cv2.line(canvas, (prev_x, prev_y), (x, y), (0, 0, 0), eraser_thickness)
                cv2.putText(output, "Eraser ON", (10, 80),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            else:
                cv2.line(canvas, (prev_x, prev_y), (x, y), drawing_color, brush_thickness)

            prev_x, prev_y = x, y
        else:
            prev_x, prev_y = 0, 0

        cv2.circle(output, (x, y), 10, drawing_color, cv2.FILLED)
    else:
        prev_x, prev_y = 0, 0

    # Draw color palette
    for (x1, y1, x2, y2, color, name) in color_buttons:
        cv2.rectangle(output, (x1, y1), (x2, y2), color, -1)
        if drawing_color == color:
            cv2.rectangle(output, (x1, y1), (x2, y2), (0, 0, 0), 3)

    # Merge canvas
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray_canvas, 20, 255, cv2.THRESH_BINARY)
    inv_mask = cv2.bitwise_not(mask)
    frame_bg = cv2.bitwise_and(output, output, mask=inv_mask)
    canvas_fg = cv2.bitwise_and(canvas, canvas, mask=mask)
    final_output = cv2.add(frame_bg, canvas_fg)

    cv2.imshow("Gesture Painter", final_output)

    key = cv2.waitKey(1)

    # Keyboard controls
    if key & 0xFF == ord('e'):
        eraser_mode = not eraser_mode
    if key & 0xFF == ord('p'):
        manual_pause = not manual_pause
        print("Paused" if manual_pause else "Resumed")
    if key & 0xFF == ord('d'):
        shape = detect_shape(canvas)
        print(f"Detected Shape: {shape}")
        cv2.putText(final_output, f"Detected Shape: {shape}", (10, h - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Gesture Painter", final_output)
        cv2.waitKey(2000)
        canvas = np.zeros((h, w, 3), dtype=np.uint8)  # 🔥 Auto-clear canvas
    if key & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
