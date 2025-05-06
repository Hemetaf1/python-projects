from deepface import DeepFace
import cv2

img_path = "your_image_path"

img = cv2.imread(img_path)

results = DeepFace.analyze(img_path=img_path, actions=['emotion'])

for face in results:
    region = face['region']
    x, y, w, h = region['x'], region['y'], region['w'], region['h']
    emotion = face['dominant_emotion']

    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(img, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

cv2.imshow("Emotion Detection", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
