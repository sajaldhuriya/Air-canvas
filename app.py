import cv2  # type: ignore
import mediapipe as mp # type: ignore
import numpy as np # type: ignore
from flask import Flask, render_template, Response # type: ignore
from PIL import Image # type: ignore
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore
import os # type: ignore

# Load environment variables from .env file
load_dotenv()

# Google Generative AI Setup
api_key = os.getenv("GENAI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    raise ValueError("API key for Google Generative AI is not set. Please check the .env file.")

# Brush and Eraser Sizes
brushThickness = 25
eraserThickness = 100

# Initialize Webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)  # Height

#header iamge
image_folder_path = "Air_canavs_images"  
header = cv2.imread(f'{image_folder_path}/1.png')

# Mediapipe Hands Setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(min_detection_confidence=0.85)
mpDraw = mp.solutions.drawing_utils
drawColor = (255, 0, 255)  # Initial drawing color: Magenta

# Brush thickness options
brush_options = {
    "Thin": 10,
    "Medium": 25,
    "Thick": 50,
    "Thicker": 75
}
selected_thickness = "Medium"

# Color selection boxes coordinates
color_boxes = {
    "Magenta": ((325, 21), (476, 70), (255, 0, 255)),
    "Blue": ((581, 21), (731, 70), (255, 0, 0)),
    "Green": ((837, 21), (988, 70), (0, 255, 0)),
    "Eraser": ((1093, 21), (1243, 70), (0, 0, 0))
}
selected_color = "Magenta"
selected_color_rgb = (255, 0, 255)  # Default color

# Brush thickness selection boxes coordinates
thickness_boxes = {
    "Thin": ((1093, 200), (1243, 280)),
    "Medium": ((1093, 330), (1243, 410)),
    "Thick": ((1093, 460), (1243, 540)),
    "Thicker": ((1093, 590), (1243, 670))
}

# Initialize Flask app
app = Flask(__name__)

# Initialize variables for drawing
xp, yp = 0, 0
imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # Canvas for drawing
ai_response_text = ""


@app.route('/')
def index():
    return render_template('index.html')


def gen_frames():
    global xp, yp, brushThickness, selected_color, selected_thickness, ai_response_text, selected_color_rgb
    while True:
        success, img = cap.read()
        if not success:
            break

        img = cv2.flip(img, 1)  # Flip horizontally for mirror effect
        img[0:160, 0:1280] = header
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        lmList = []
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1], lmList[8][2]  # Index finger tip
            x2, y2 = lmList[12][1], lmList[12][2]  # Middle finger tip
            
            #selection mode
            if y1 < lmList[7][2] and y2 < lmList[11][2]:
                xp, yp = 0, 0
                cv2.rectangle(img, (min(x1, x2), min(y1, y2)), (max(x1, x2), max(y1, y2)), selected_color_rgb, cv2.FILLED)

                # Color selection logic
                for color_name, ((x_start, y_start), (x_end, y_end), color) in color_boxes.items():
                    if x_start < x1 < x_end and y_start < y1 < y_end:
                        selected_color = color_name
                        selected_color_rgb = color
                        cv2.rectangle(img, (x_start, y_start), (x_end, y_end), color, cv2.FILLED)

                        #tested

                # Brush thickness selection logic with borders
                for thickness_name, (box_start, box_end) in thickness_boxes.items():
                    border_thickness = 6 if selected_thickness == thickness_name else 2
                    cv2.rectangle(img, box_start, box_end, (255, 255, 255), border_thickness)  # White border
                    cv2.putText(img, thickness_name, (box_start[0] + 10, box_start[1] + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                (0, 0, 0), 2)
                    # Set selected thickness if inside the box
                    if box_start[0] < x1 < box_end[0] and box_start[1] < y1 < box_end[1]:
                        selected_thickness = thickness_name
                        brushThickness = brush_options[selected_thickness]

            if y1 < lmList[12][2]:  # Drawing condition
                cv2.circle(img, (x1, y1), 15, selected_color_rgb, cv2.FILLED)
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                cv2.line(img, (xp, yp), (x1, y1), selected_color_rgb, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), selected_color_rgb, brushThickness)
                xp, yp = x1, y1

            # Thumbs Up Gesture Detection (Thumb is extended, other fingers are folded)
            thumb_up = (
                lmList[4][2] < lmList[3][2] and  # Thumb is extended (Thumb tip is above the base)
                lmList[8][2] > lmList[6][2] and  # Index finger is folded
                lmList[12][2] > lmList[10][2] and  # Middle finger is folded
                lmList[16][2] > lmList[14][2] and  # Ring finger is folded
                lmList[20][2] > lmList[18][2]     # Pinky finger is folded
            )

            if thumb_up:  # If thumbs up gesture is detected
                pil_image = Image.fromarray(cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2RGB))
                response = model.generate_content(["Solve this math problem", pil_image])
                ai_response_text = response.text
            else:
                if ai_response_text == "":
                    ai_response_text = "Please draw to trigger AI response..."

        # Merging canvas with frame
        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        # Add text to image (Reverted back to original position)
        cv2.putText(img, ai_response_text, (50, 650), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Encode frame as JPEG and yield it
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)