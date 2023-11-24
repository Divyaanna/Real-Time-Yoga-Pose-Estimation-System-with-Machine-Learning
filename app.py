import pickle

import cv2
import mediapipe as mp
import numpy as np
import pandas as pd
from flask import Flask, Response, render_template
from flask_socketio import SocketIO
from gtts import gTTS

app = Flask(__name__)
socketio = SocketIO(app)

enable_voice_guidance = True
def speak(text):
    if enable_voice_guidance:
        tts = gTTS(text=text, lang='en')
        tts.save("static/voice_guidance.mp3")

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

columns = ["class"]

for i in range(0, 33):
    columns.append(f"x{i}")
    columns.append(f"y{i}")
    columns.append(f"z{i}")
    columns.append(f"v{i}")

with open("rfmodel_32.pkl", "rb") as f:
    model = pickle.load(f)

cap = cv2.VideoCapture(0)
counter = 0
current_stage = ""
current_body_language_class = ""
current_body_language_prob = ""

def emit_pose_data():
                global current_body_language_class, current_body_language_prob
                while True:
                    socketio.emit(
                        'update_pose',
                        {
                            'body_language_class': current_body_language_class,
                            'body_language_prob': current_body_language_prob
                        }
                    )
                    socketio.sleep(1)

def generate_frames():
    global current_body_language_class, current_body_language_prob, enable_voice_guidance
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while True:
            ret, frame = cap.read()

            image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            image.flags.writeable = False

            results = pose.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2),
            )

            try:
                row = (
                    np.array(
                        [
                            [res.x, res.y, res.z, res.visibility]
                            for res in results.pose_landmarks.landmark
                        ]
                    )
                    .flatten()
                    .tolist()
                )
                X = pd.DataFrame([row], columns=columns[1:])
                body_language_class = model.predict(X)[0]
                body_language_prob = model.predict_proba(X)[0]
                print(body_language_class)
                current_body_language_class = body_language_class
                current_body_language_prob = round(body_language_prob[np.argmax(body_language_prob)], 2)


                cv2.rectangle(image, (0, 0), (250, 60), (245, 117, 16), -1)

                cv2.putText(
                    image,
                    "CLASS",
                    (95, 12),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    image,
                    body_language_class.split(" ")[0],
                    (90, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )

                cv2.putText(
                    image,
                    "PROB",
                    (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 0),
                    1,
                    cv2.LINE_AA,
                )
                cv2.putText(
                    image,
                    str(round(body_language_prob[np.argmax(body_language_prob)], 2)),
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2,
                    cv2.LINE_AA,
                )
                # Provide voice guidance when the camera is initialized, only if enabled
                if counter == 0 and enable_voice_guidance:
                    speak("Initializing camera. Please wait.")
                    counter += 1

            except Exception as e:
                pass

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


            

@app.route('/')
def index():
    #return render_template('index.html', body_language_class=current_body_language_class, body_language_prob=current_body_language_prob)
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Add a new route for handling settings changes
@app.route('/settings', methods=['POST'])
def update_settings():
    global enable_voice_guidance
    # You can use Flask request to get data from the client
    enable_voice_guidance = request.form.get('enable_voice_guidance') == 'true'
    return 'Settings updated successfully'

if __name__ == "__main__":
    #app.run(debug=True, port=5000)
    socketio.start_background_task(emit_pose_data)
    socketio.run(app, debug=True, port=5000)
