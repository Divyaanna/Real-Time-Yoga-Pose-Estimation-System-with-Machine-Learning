import mediapipe as mp
import pandas as pd
import numpy as np
import cv2
import pickle
from flask import Flask, render_template, Response
app = Flask('pose_detect')

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

columns = ["class"]

for i in range(0, 33):
    columns.append(f"x{i}")
    columns.append(f"y{i}")
    columns.append(f"z{i}")
    columns.append(f"v{i}")


with open("gbmodel.pkl", "rb") as f:
    model = pickle.load(f)

cap = cv2.VideoCapture(0)
counter = 0
current_stage = ""

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        image.flags.writeable = False

        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

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

        except Exception as e:
            pass

        cv2.imshow("window", image)

        if cv2.waitKey(10) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
