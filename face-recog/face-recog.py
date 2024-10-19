import cv2
from deepface import DeepFace
from os import getenv

print(cv2.__file__)
cv2.__file__ = getenv("OPENCV_DATA_PATH", None)
print(cv2.__file__)

DeepFace.stream(db_path = "./face-recog/photodatabase", model_name="Facenet512", enable_face_analysis=True, time_threshold=3, frame_threshold=3)