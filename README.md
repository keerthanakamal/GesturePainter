🖐️ Gesture Painter – Real-Time Hand Gesture Drawing App 🎨
Gesture Painter is a real-time computer vision application that lets you draw on a virtual canvas using just your hand gestures — no mouse or touchscreen needed! Built using MediaPipe and OpenCV, it supports gesture-based drawing, color selection, erasing, and shape detection — all through your webcam.

✨ Features
✍️ Draw with One Finger
Raise your index finger to draw on the canvas in real-time.

🖐️ Pause Drawing with Five Fingers
Show all fingers to pause drawing immediately.

🧽 Eraser Mode
Toggle eraser on/off using the 'e' key or by selecting the black color box.

🎨 Color Palette
Choose from multiple colors using a clickable palette (by pointing your finger at the boxes).

🔲 Shape Detection
Press 'd' to detect and classify the shape you’ve drawn (Circle, Triangle, Rectangle, etc.).

🧼 Auto Clear After Detection
Automatically clears the canvas after shape detection so you can start fresh.

🖼️ Live Webcam Feedback
Merged canvas with live video feed using OpenCV's bitwise operations.

🛠️ Technologies Used
Python

OpenCV

MediaPipe

NumPy

🚀 How to Run
Clone the repository:

bash
Copy code
git clone https://github.com/keerthanakamal/GesturePainter.git
cd GesturePainter
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the app:

bash
Copy code
python main.py
🎮 Controls
Action	Control
Draw	Raise index finger
Pause	Raise all five fingers
Toggle Eraser	Press e or select black color
Detect Shape	Press d
Manual Pause Toggle	Press p
Quit	Press q

📂 Project Structure
css
Copy code
GesturePainter/
├── main.py
├── utils/
│   ├── hand_detector.py
│   └── gesture_controller.py
├── README.md
└── requirements.txt
