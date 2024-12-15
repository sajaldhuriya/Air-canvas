import cv2
import mediapipe as mp
import numpy as np
import os

# Brush and Eraser Sizes
brushThickness = 25
eraserThickness = 100

# Initialize Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)  # Height
image_folder_path = "Air_canavs_images"  # Overlay images folder
myList =os.listdir(image_folder_path)
print(myList)

overlay = []
for impath in myList:
    image=cv2.imread(f'{image_folder_path}/{impath}')
    overlay.append(image)

header= overlay[0]

# Path to save the output video on Desktop
output_file = "C:\\Users\\sajal dhuriya\\OneDrive\\Desktop\\output.mp4"
drawing_save_path = "C:\\Users\\sajal dhuriya\\OneDrive\\Desktop\\air_image\\im.png"  # Save path for the drawing

# Initialize VideoWriter for recording (MP4 format)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(output_file, fourcc, 20.0, (1280, 720))

# Check if VideoWriter opened successfully
if not out.isOpened():
    print("Error: Could not open video file for writing. Please check the path and codec.")
else:
    print("Video file opened successfully.")

xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # Canvas for drawing

# Mediapipe Hands Setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.85)
mpDraw = mp.solutions.drawing_utils
drawColor = (255, 0, 255)  # Initial drawing color: Magenta

# Brush thickness options with increased box size and spacing
brush_options = {
    "Thin": 10,
    "Medium": 25,
    "Thick": 50,
    "Thicker": 75
}
selected_thickness = "Medium"

# Adjusted thickness selection boxes coordinates with increased size and spacing
thickness_boxes = {
    "Thin": ((1093, 200), (1243, 280)),
    "Medium": ((1093, 330), (1243, 410)),
    "Thick": ((1093, 460), (1243,540)),
    "Thicker": ((1093, 590),(1243,670))
}

# Color selection boxes coordinates
color_boxes = {
    "Magenta": ((325, 21), (476, 70), (255, 0, 255)),
    "Blue": ((581, 21), (731, 70), (255, 0, 0)),
    "Green": ((837, 21), (988, 70), (0, 255, 0)),
    "Eraser": ((1093, 21), (1243, 70), (0, 0, 0))
}
selected_color = "Magenta"


while True:
    # Read Frame
    success, img = cap.read()


    if not success:
        break

    img = cv2.flip(img, 1)  # Flip horizontally for a mirror effect
    img[0:160, 0:1280] = header
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for Mediapipe
    results = hands.process(imgRGB)  # Process the frame for hand landmarks

    lmList = []
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)  # Convert coordinates to pixels
                lmList.append([id, cx, cy])
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

    if len(lmList) != 0:
        # Tip of index and middle fingers
        x1, y1 = lmList[8][1], lmList[8][2]  # Index finger tip
        x2, y2 = lmList[12][1], lmList[12][2]  # Middle finger tip

        # Selection Mode
        if y1 < lmList[7][2] and y2 < lmList[11][2]:  # Both fingers are above their respective joints
            xp, yp = 0, 0

            # Draw colored rectangle between the two fingers
            cv2.rectangle(img, (min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2)), drawColor, cv2.FILLED)

            # Set color based on selection in the color box area
            for color_name, ((x_start, y_start), (x_end, y_end), color) in color_boxes.items():
                if x_start < x1 < x_end and y_start < y1 < y_end:
                    drawColor = color
                    selected_color = color_name

            # Check if brush thickness selection area is selected
            for thickness_name, (box_start, box_end) in thickness_boxes.items():
                if box_start[0] < x1 < box_end[0] and box_start[1] < y1 < box_end[1]:
                    selected_thickness = thickness_name
                    brushThickness = brush_options[selected_thickness]

        # Drawing Mode
        if y1 < lmList[12][2]:  # Drawing condition
            # Draw colored circle at index finger tip
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
            if drawColor == (0, 0, 0):  # Eraser
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:  # Drawing with color
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)
            xp, yp = x1, y1

    # Merging the canvas and current frame
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Draw color selection boxes with a highlight for the selected color
    for color_name, ((x_start, y_start), (x_end, y_end), color) in color_boxes.items():
        border_thickness = 6 if selected_color == color_name else 2
        cv2.rectangle(img, (x_start, y_start), (x_end, y_end), color, border_thickness)

    # Draw brush thickness selection boxes with a highlight for the selected thickness
    for thickness_name, (box_start, box_end) in thickness_boxes.items():
        border_thickness = 6 if selected_thickness == thickness_name else 2
        cv2.rectangle(img, box_start, box_end, (255, 255, 255), border_thickness)
        cv2.putText(img, thickness_name, (box_start[0] + 10, box_start[1] + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow("Image", img)

    # Write the frame to the video file if opened
    if out.isOpened():
        out.write(img)

    # Save drawing if 's' is pressed
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.imwrite(drawing_save_path, imgCanvas)
        print(f"Drawing saved to {drawing_save_path}")

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything when done
cap.release()
out.release()
cv2.destroyAllWindows()
