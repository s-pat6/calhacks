
import asyncio
from typing import Dict, List, Optional, Tuple
import cv2
from os import getenv,getcwd
from ..voice.main import generate_and_speak

print(cv2.__file__)
cv2.__file__ = getcwd() + "/haarcascades/"
print(cv2.__file__)


import numpy as np

from deepface import DeepFace
import deepface.modules.streaming as ds
import time

from deepface.commons.logger import Logger
logger = Logger()
from PIL import Image


def get_emotions(f):
     return DeepFace.analyze(
        img_path=f,
        actions=("emotion"), #"age", "gender"
        detector_backend="opencv",
        enforce_detection=False,
        silent=True,
    )



latestimg = [None]

model_name = 'VGG-Face'
db_path = './photodatabase'
detector_backend="opencv"
distance_metric="cosine"
source=0
time_threshold=1
frame_threshold=4
anti_spoofing: bool = False
IDENTIFIED_IMG_SIZE = 112

frozen = [False]

emote = False
emotes = 0

def publish_detection(img, faces_in_image):
    global latestimg, emote, emotes, frozen
    #print("Found:")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    latestimg[0] = Image.fromarray(img)
    #latestimg[0] = 'a'
    #print('set an mi', latestimg == None)
    if faces_in_image is not None:
        # frozen = True
        print(faces_in_image)
        for name, faceattrs in faces_in_image.items():
            print(faceattrs)
            if (faceattrs["dominant_emotion"] != 'neutral' and faceattrs["dominant_emotion"] != 'happy' and faceattrs["emotion"][faceattrs["dominant_emotion"]] > 20):
                frozen[0] = True
                if (emote == False and emotes > 1):
                    generate_and_speak('emotion.wav', 'Inform the user that the other person is ' + faceattrs['dominant_emotion'])
                    emote = True
                else:
                    emotes += 1
            print(name + ": ", faceattrs["emotion"])
            print(str(faceattrs))

def search_identity(
    detected_face: np.ndarray,
    db_path: str,
    model_name: str,
    detector_backend: str,
    distance_metric: str,
) -> Tuple[Optional[str], Optional[np.ndarray]]:
    """
    Search an identity in facial database.
    Args:
        detected_face (np.ndarray): extracted individual facial image
        db_path (string): Path to the folder containing image files. All detected faces
            in the database will be considered in the decision-making process.
        model_name (str): Model for face recognition. Options: VGG-Face, Facenet, Facenet512,
            OpenFace, DeepFace, DeepID, Dlib, ArcFace, SFace and GhostFaceNet (default is VGG-Face).
        detector_backend (string): face detector backend. Options: 'opencv', 'retinaface',
            'mtcnn', 'ssd', 'dlib', 'mediapipe', 'yolov8', 'centerface' or 'skip'
            (default is opencv).
        distance_metric (string): Metric for measuring similarity. Options: 'cosine',
            'euclidean', 'euclidean_l2' (default is cosine).
    Returns:
        result (tuple): result consisting of following objects
            identified image path (str)
            identified image itself (np.ndarray)
    """
    target_path = None
    try:
        dfs = DeepFace.find(
            img_path=detected_face,
            db_path=db_path,
            model_name=model_name,
            detector_backend=detector_backend,
            distance_metric=distance_metric,
            enforce_detection=False,
            silent=True,
        )
    except ValueError as err:
        if f"No item found in {db_path}" in str(err):
            logger.warn(
                f"No item is found in {db_path}."
                "So, no facial recognition analysis will be performed."
            )
            dfs = []
        else:
            raise err
    if len(dfs) == 0:
        # you may consider to return unknown person's image here
        return None, None

    # detected face is coming from parent, safe to access 1st index
    df = dfs[0]

    if df.shape[0] == 0:
        return None, None

    candidate = df.iloc[0]
    target_path = candidate["identity"]
    logger.info(f"Hello, {target_path}")

    # load found identity image - extracted if possible
    target_objs = DeepFace.extract_faces(
        img_path=target_path,
        detector_backend=detector_backend,
        enforce_detection=False,
        align=True,
    )

    # extract facial area of the identified image if and only if it has one face
    # otherwise, show image as is
    if len(target_objs) == 1:
        # extract 1st item directly
        target_obj = target_objs[0]
        target_img = target_obj["face"]
        target_img = cv2.resize(target_img, (IDENTIFIED_IMG_SIZE, IDENTIFIED_IMG_SIZE))
        target_img *= 255
        target_img = target_img[:, :, ::-1]
    else:
        target_img = cv2.imread(target_path)

    #print("path", target_path)
    return target_path.split("/")[-2], target_img

def perform_facial_recognition(
    img: np.ndarray,
    detected_faces: List[np.ndarray],
    faces_coordinates: List[Tuple[int, int, int, int, bool, float]],
    db_path: str,
    detector_backend: str,
    distance_metric: str,
    model_name: str,
) -> Tuple[np.ndarray, Dict[str,Dict[str, any] ]]:
    """
    Perform facial recognition
    Args:
        img (np.ndarray): image itself
        detected_faces (list): list of extracted detected face images as numpy
        faces_coordinates (list): list of facial area coordinates as tuple with
            x, y, w and h values also is_real and antispoof_score keys
        db_path (string): Path to the folder containing image files. All detected faces
            in the database will be considered in the decision-making process.
        detector_backend (string): face detector backend. Options: 'opencv', 'retinaface',
            'mtcnn', 'ssd', 'dlib', 'mediapipe', 'yolov8', 'centerface' or 'skip'
            (default is opencv).
        distance_metric (string): Metric for measuring similarity. Options: 'cosine',
            'euclidean', 'euclidean_l2' (default is cosine).
        model_name (str): Model for face recognition. Options: VGG-Face, Facenet, Facenet512,
            OpenFace, DeepFace, DeepID, Dlib, ArcFace, SFace and GhostFaceNet (default is VGG-Face).
    Returns:
        img (np.ndarray): image with identified face informations
    """
    faces_in_img: Dict[str, Dict[str, any]] = {}
    for idx, (x, y, w, h, is_real, antispoof_score) in enumerate(faces_coordinates):
        detected_face = detected_faces[idx]
        target_label, target_img = search_identity(
            detected_face=detected_face,
            db_path=db_path,
            detector_backend=detector_backend,
            distance_metric=distance_metric,
            model_name=model_name,
        )
        demographies = DeepFace.analyze(
            img_path=detected_face,
            actions=("emotion"), #"age", "gender"
            detector_backend="skip",
            enforce_detection=False,
            silent=True,
        )

        if target_label is None:
            continue
        # todo, combine the two logics more properly
        if len(demographies) == 0:
            continue
        
        #faces_in_img.append(target_label)
        #print("YOOOOO", faces_in_img)

        # safe to access 1st index because detector backend is skip
        demography = demographies[0]
        faces_in_img[target_label] = demography

        img = ds.overlay_emotion(img=img, emotion_probas=demography["emotion"], x=x, y=y, w=w, h=h)
        #img = ds.overlay_age_gender(
        #    img=img,
        #    apparent_age=demography["age"],
        #    gender=demography["dominant_gender"][0:1],  # M or W
        #    x=x,
        #    y=y,
        #    w=w,
        #    h=h,
        #)
        img = ds.overlay_identified_face(
            img=img,
            target_img=target_img,
            label=target_label,
            x=x,
            y=y,
            w=w,
            h=h,
        )

    return img, faces_in_img

def build_demography_models(enable_face_analysis: bool) -> None:
    """
    Build demography analysis models
    Args:
        enable_face_analysis (bool): Flag to enable face analysis (default is True).
    Returns:
        None
    """
    if enable_face_analysis is False:
        return
    DeepFace.build_model(task="facial_attribute", model_name="Age")
    logger.info("Age model is just built")
    DeepFace.build_model(task="facial_attribute", model_name="Gender")
    logger.info("Gender model is just built")
    DeepFace.build_model(task="facial_attribute", model_name="Emotion")
    logger.info("Emotion model is just built")
async def stuff():
    global frozen
    # initialize models
    build_demography_models(enable_face_analysis=True)
    ds.build_facial_recognition_model(model_name=model_name)
    # call a dummy find function for db_path once to create embeddings before starting webcam
    _ = ds.search_identity(
        detected_face=np.zeros([224, 224, 3]),
        db_path=db_path,
        detector_backend=detector_backend,
        distance_metric=distance_metric,
        model_name=model_name,
    )

    freezed_img = None
    freeze = False
    num_frames_with_faces = 0
    tic = time.time()
    print("1")

    cap = cv2.VideoCapture(source)  # webcam
    print("1")

    while True:
        #print(frozen)
        await asyncio.sleep(0.01)

        if frozen[0]:
            continue

        has_frame, img = cap.read()
        
        if not has_frame:
            break

        # we are adding some figures into img such as identified facial image, age, gender
        # that is why, we need raw image itself to make analysis
        raw_img = img.copy()

        faces_coordinates = []

        if freeze is False:
            faces_coordinates = ds.grab_facial_areas(
                img=img, detector_backend=detector_backend, anti_spoofing=anti_spoofing
            )

            # we will pass img to analyze modules (identity, demography) and add some illustrations
            # that is why, we will not be able to extract detected face from img clearly
            detected_faces = ds.extract_facial_areas(img=img, faces_coordinates=faces_coordinates)

            img = ds.highlight_facial_areas(img=img, faces_coordinates=faces_coordinates)
            img = ds.countdown_to_freeze(
                img=img,
                faces_coordinates=faces_coordinates,
                frame_threshold=frame_threshold,
                num_frames_with_faces=num_frames_with_faces,
            )

            num_frames_with_faces = num_frames_with_faces + 1 if len(faces_coordinates) else 0

            freeze = num_frames_with_faces > 0 and num_frames_with_faces % frame_threshold == 0
            if freeze:
                # add analyze results into img - derive from raw_img
                img = ds.highlight_facial_areas(
                    img=raw_img, faces_coordinates=faces_coordinates, anti_spoofing=anti_spoofing
                )

                # age, gender and emotion analysis
                img = ds.perform_demography_analysis(
                    enable_face_analysis=True,
                    img=raw_img,
                    faces_coordinates=faces_coordinates,
                    detected_faces=detected_faces,
                )
                # facial recogntion analysis
                img, faces_in_image = perform_facial_recognition(
                    img=img,
                    faces_coordinates=faces_coordinates,
                    detected_faces=detected_faces,
                    db_path=db_path,
                    detector_backend=detector_backend,
                    distance_metric=distance_metric,
                    model_name=model_name,
                )

                publish_detection(img, faces_in_image)

                # freeze the img after analysis
                freezed_img = img.copy()

                # start counter for freezing
                tic = time.time()
                logger.info("freezed")

        elif freeze is True and time.time() - tic > time_threshold:
            freeze = False
            freezed_img = None
            # reset counter for freezing
            tic = time.time()
            logger.info("freeze released")

        freezed_img = ds.countdown_to_release(img=freezed_img, tic=tic, time_threshold=time_threshold)

        publish_detection(img if freezed_img is None else freezed_img, None)
        #cv2.imshow("img", img if freezed_img is None else freezed_img)

        #if cv2.waitKey(1) & 0xFF == ord("q"):  # press q to quit
        #    break

    # kill open cv things
    cap.release()
    cv2.destroyAllWindows()

    return data

if __name__ == '__main__':
    print(get_emotions("./photodatabase/Karmanyaah/3.png"))
    stuff()