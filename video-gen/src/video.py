import os
import cv2
import numpy as np
from typing import List
import subprocess


STATIC_FOLDER = "./video-gen/static/"


def add_transparent_image(background, foreground, x_offset=None, y_offset=None):
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    if x_offset is None:
        x_offset = (bg_w - fg_w) // 2
    if y_offset is None:
        y_offset = (bg_h - fg_h) // 2

    w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
    h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

    if w < 1 or h < 1:
        return

    bg_x = max(0, x_offset)
    bg_y = max(0, y_offset)
    fg_x = max(0, x_offset * -1)
    fg_y = max(0, y_offset * -1)
    foreground = foreground[fg_y : fg_y + h, fg_x : fg_x + w]
    background_subsection = background[bg_y : bg_y + h, bg_x : bg_x + w]

    foreground_colors = foreground[:, :, :3]
    alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0
    alpha_mask = alpha_channel[:, :, np.newaxis]

    composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

    background[bg_y : bg_y + h, bg_x : bg_x + w] = composite


class YouAreSoOverlay:
    text = cv2.imread(f"{STATIC_FOLDER}/you_are_so.png", cv2.IMREAD_UNCHANGED)

    x_align = 50
    y_align = 600

    @staticmethod
    def generate(background):
        add_transparent_image(background, YouAreSoOverlay.text, YouAreSoOverlay.x_align, YouAreSoOverlay.y_align)


class PreciousOverlay:
    text = cv2.imread(f"{STATIC_FOLDER}/precious.png", cv2.IMREAD_UNCHANGED)

    x_align = 75
    y_align = 600

    @staticmethod
    def generate(background):
        add_transparent_image(background, PreciousOverlay.text, PreciousOverlay.x_align, PreciousOverlay.y_align)


class WhenYouOverlay:
    text = cv2.imread(f"{STATIC_FOLDER}/when_you.png", cv2.IMREAD_UNCHANGED)

    x_align = 75
    y_align = 600

    @staticmethod
    def generate(background):
        add_transparent_image(background, WhenYouOverlay.text, WhenYouOverlay.x_align, WhenYouOverlay.y_align)


class SmileOverlay:
    text = cv2.imread(f"{STATIC_FOLDER}/overlay_smile.png", cv2.IMREAD_UNCHANGED)

    x_align = 0
    y_align = 0

    @staticmethod
    def generate(background):
        add_transparent_image(background, SmileOverlay.text, SmileOverlay.x_align, SmileOverlay.y_align)


class Renderer:

    out_file = "out.mp4"
    codec = None
    vid_writer = None

    def create(out_file, h, w):
        renderer = Renderer()
        renderer.out_file = out_file
        renderer.codec = cv2.VideoWriter_fourcc(*"mp4v")
        renderer.vid_writer = cv2.VideoWriter(out_file, renderer.codec, 80, (w, h))
        return renderer

    def stand_still(self, img, frames=40):
        for _ in range(frames):
            self.vid_writer.write(img)

    def release(self):
        self.vid_writer.release()


class Transition:
    @staticmethod
    def calculate_coordinates(i, step_size, direction, h, w):
        if direction == 0:
            return (i * step_size, h), (0, 0)
        if direction == 1:
            return (h, i * step_size), (0, 0)
        if direction == 2:
            return (h, w - i * step_size), (0, w)
        if direction == 3:
            return (0, i * step_size), (h, 0)

    @staticmethod
    def generate(current_img, next_img, renderer, frames, direction):
        h, w, _ = current_img.shape
        step_size = int(w / frames)
        for i in range(frames - 1):
            i = i + 1
            shapes = np.zeros_like(current_img, np.uint8)
            x, y = Transition.calculate_coordinates(i, step_size, direction, h, w)
            cv2.rectangle(shapes, x, y, (255, 255, 255), cv2.FILLED)
            alpha_mask = shapes / 255.0

            composite = current_img * (1 - alpha_mask) + next_img * alpha_mask

            current_img[0:h, 0:w] = composite

            renderer.stand_still(current_img, 1)


class ColorFilter:
    @staticmethod
    def brighten(image):
        maxIntensity = 255.0  # depends on dtype of image data

        image = cv2.multiply(image, 1.2)
        return image

    @staticmethod
    def make_pink(image):
        image = ColorFilter.brighten(image)
        image = np.uint8(cv2.add(image, (50, 0, 50)))
        return image

    @staticmethod
    def no_modification(image):
        return image


class PreciousSmileGenerator:

    image_manipulations = [
        YouAreSoOverlay.generate,
        PreciousOverlay.generate,
        WhenYouOverlay.generate,
        SmileOverlay.generate,
        SmileOverlay.generate,
    ]
    transitions = [0, 1, 2, 3, 0]
    color_enhancements = [
        ColorFilter.no_modification,
        ColorFilter.no_modification,
        ColorFilter.no_modification,
        ColorFilter.brighten,
        ColorFilter.make_pink,
    ]
    files: List[str] = []
    loaded_files = []
    folder: str = ""

    def load_pictures(self, paths: List[str]):
        for img_file in paths:
            if img_file.endswith((".jpg", ".jpeg", ".png")):
                print("reading: ", img_file)
                self.files.append(img_file)

                img = cv2.imread(img_file)
                h, w, _ = img.shape
                print(h, w, min(h, w))
                crop = img[0 : min(h, w), 0 : min(h, w)]
                print(crop.shape)
                crop = cv2.resize(crop, (800, 800))
                print(crop.shape)

                self.loaded_files.append(crop)

    def render(self, video_filename: str):
        print(self.files)
        first_image = self.loaded_files[0]
        h, w, _ = first_image.shape

        renderer = Renderer.create(video_filename, h, w)

        for i, loaded_img in enumerate(self.loaded_files):
            self.image_manipulations[i](loaded_img)
            loaded_img = self.color_enhancements[i](loaded_img)
            renderer.stand_still(loaded_img, 120)
            if i <= len(self.files) - 2:
                Transition.generate(loaded_img, self.loaded_files[i + 1], renderer, 10, self.transitions[i])

        renderer.release

    def add_audio_track(self, video_filename: str, out_file: str):
        # ffmpeg -i <sourceVideoFile> -i <sourceAudioFile> -map 0:0 -map 1:0 -c:v copy -c:a copy <outputVideoFile>
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                video_filename,
                "-i",
                "video-gen/static/smile.wav",
                "-map",
                "0:0",
                "-map",
                "1:0",
                "-c:v",
                "copy",
                out_file,
            ]
        )


class PictureSelector:
    pictures = {}

    @staticmethod
    def calculate_happiness_metric(meta_data) -> float:
        return (
            meta_data["emotion"][meta_data["dominant_emotion"]] * 3
            + meta_data["emotion"]["happy"]
            - meta_data["emotion"]["sad"]
            - meta_data["emotion"]["angry"]
        )

    def select(self):
        ratings = [PictureSelector.calculate_happiness_metric(x) for x in self.pictures]
        selection = []
        self.pictures = [x for _, x in sorted(zip(ratings, self.pictures))]

        for i in range(5):
            selection.append(self.pictures[int(len(self.pictures) / (6 - i))]["path"])

        return selection

    def load_pictures(self):
        for pic in self.pictures:
            self.files.append(pic["path"])


def generate_precious_smiles(pictures, out_file):
    picture_selector = PictureSelector()
    picture_selector.pictures = pictures
    paths = picture_selector.select()

    print(paths)

    vid_gen = PreciousSmileGenerator()
    vid_gen.load_pictures(paths)
    vid_gen.render("/tmp/temp.mp4")
    vid_gen.add_audio_track("/temp/temp.mp4", out_file)


generate_precious_smiles(
    [
        {
            "emotion": {
                "angry": 3.577738496661068e-06,
                "disgust": 7.95996562674417e-10,
                "fear": 0.6826502212226523,
                "happy": 0.003607538234449408,
                "sad": 10.322486479430586,
                "surprise": 6.189664705563807e-08,
                "neutral": 88.99125391192757,
            },
            "dominant_emotion": "neutral",
            "region": {"x": 67, "y": 26, "w": 228, "h": 228, "left_eye": [147, 125], "right_eye": [146, 120]},
            "face_confidence": 0.98,
            "path": "./photodatabase/Karmanyaah/8.png",
        },
        {
            "emotion": {
                "angry": 99.67702627182007,
                "disgust": 1.7249597007240272e-14,
                "fear": 0.006090241004130803,
                "happy": 0.0002496213028280181,
                "sad": 0.3154019359499216,
                "surprise": 5.827532900681831e-10,
                "neutral": 0.0012251732186996378,
            },
            "dominant_emotion": "angry",
            "region": {"x": 0, "y": 0, "w": 261, "h": 316, "left_eye": None, "right_eye": None},
            "face_confidence": 0,
            "path": "./photodatabase/Karmanyaah/3.png",
        },
        {
            "emotion": {
                "angry": 2.9455176786541415e-05,
                "disgust": 4.2401935708793505e-13,
                "fear": 0.30625953804701567,
                "happy": 96.2863564491272,
                "sad": 0.0009006215805129614,
                "surprise": 0.0007496195848943898,
                "neutral": 3.405703231692314,
            },
            "dominant_emotion": "happy",
            "region": {"x": 93, "y": 110, "w": 332, "h": 332, "left_eye": [316, 340], "right_eye": [194, 265]},
            "face_confidence": 0.92,
            "path": "./photodatabase/Karmanyaah/6.png",
        },
        {
            "emotion": {
                "angry": 97.81807065010071,
                "disgust": 0.0015355975847342052,
                "fear": 0.6448905915021896,
                "happy": 0.0010533173735893797,
                "sad": 1.5098375268280506,
                "surprise": 0.010167976142838597,
                "neutral": 0.01443585060769692,
            },
            "dominant_emotion": "angry",
            "region": {"x": 0, "y": 0, "w": 498, "h": 736, "left_eye": None, "right_eye": None},
            "face_confidence": 0,
            "path": "./photodatabase/Karmanyaah/9.png",
        },
        {
            "emotion": {
                "angry": 1.1587784384953046,
                "disgust": 4.547175754404264e-09,
                "fear": 0.02599086010681004,
                "happy": 0.004819748133620136,
                "sad": 3.850822380234145,
                "surprise": 8.129668090337807e-07,
                "neutral": 94.95958655831734,
            },
            "dominant_emotion": "neutral",
            "region": {"x": 93, "y": 281, "w": 669, "h": 669, "left_eye": [551, 546], "right_eye": [291, 541]},
            "face_confidence": 0.92,
            "path": "./photodatabase/Karmanyaah/13.png",
        },
        {
            "emotion": {
                "angry": 0.17245898488909006,
                "disgust": 9.359465735769845e-06,
                "fear": 35.769492387771606,
                "happy": 0.022007033112458885,
                "sad": 63.139575719833374,
                "surprise": 8.959391095686442e-06,
                "neutral": 0.8964443579316139,
            },
            "dominant_emotion": "sad",
            "region": {"x": 14, "y": 26, "w": 183, "h": 187, "left_eye": [70, 95], "right_eye": [75, 93]},
            "face_confidence": 0.91,
            "path": "./photodatabase/Karmanyaah/14.png",
        },
        {
            "emotion": {
                "angry": 0.0001519658644240143,
                "disgust": 4.9935508307110896e-05,
                "fear": 0.003782362407838175,
                "happy": 94.79567377541505,
                "sad": 0.004847574307578388,
                "surprise": 0.0004220074767151182,
                "neutral": 5.195077445809689,
            },
            "dominant_emotion": "happy",
            "region": {"x": 52, "y": 72, "w": 278, "h": 278, "left_eye": [235, 186], "right_eye": [150, 277]},
            "face_confidence": 0.92,
            "path": "./photodatabase/Karmanyaah/7.png",
        },
        {
            "emotion": {
                "angry": 5.363109335303307,
                "disgust": 0.00029208008527348284,
                "fear": 1.700773648917675,
                "happy": 0.2793072024360299,
                "sad": 17.069654166698456,
                "surprise": 0.41635623201727867,
                "neutral": 75.17050504684448,
            },
            "dominant_emotion": "neutral",
            "region": {"x": 165, "y": 239, "w": 545, "h": 545, "left_eye": [541, 454], "right_eye": [328, 447]},
            "face_confidence": 0.92,
            "path": "./photodatabase/Karmanyaah/12.png",
        },
        {
            "emotion": {
                "angry": 3.229910135269165,
                "disgust": 8.433391762707743e-07,
                "fear": 2.973117120563984,
                "happy": 0.0075160460255574435,
                "sad": 65.15405178070068,
                "surprise": 0.2275398001074791,
                "neutral": 28.40786576271057,
            },
            "dominant_emotion": "sad",
            "region": {"x": 200, "y": 111, "w": 535, "h": 535, "left_eye": [570, 324], "right_eye": [372, 318]},
            "face_confidence": 0.94,
            "path": "./photodatabase/Karmanyaah/11.png",
        },
        {
            "emotion": {
                "angry": 0.6456318777054548,
                "disgust": 6.327834922714715e-08,
                "fear": 3.007810562849045,
                "happy": 0.006339864921756089,
                "sad": 3.77948060631752,
                "surprise": 0.010034332808572799,
                "neutral": 92.55070686340332,
            },
            "dominant_emotion": "neutral",
            "region": {"x": 42, "y": 32, "w": 221, "h": 226, "left_eye": [198, 120], "right_eye": [112, 119]},
            "face_confidence": 0.92,
            "path": "./photodatabase/Karmanyaah/5.png",
        },
        {
            "emotion": {
                "angry": 0.29618008993566036,
                "disgust": 5.349957987732523e-06,
                "fear": 0.006057786958990619,
                "happy": 79.73145842552185,
                "sad": 0.47962418757379055,
                "surprise": 0.0007819285201549064,
                "neutral": 19.485892355442047,
            },
            "dominant_emotion": "happy",
            "region": {"x": 177, "y": 149, "w": 307, "h": 307, "left_eye": [382, 283], "right_eye": [279, 369]},
            "face_confidence": 0.95,
            "path": "./photodatabase/Karmanyaah/4.png",
        },
        {
            "emotion": {
                "angry": 0.15653809070296176,
                "disgust": 1.1296847027819316e-07,
                "fear": 0.0007223160034076529,
                "happy": 99.5154380220697,
                "sad": 0.063439547661936,
                "surprise": 0.002534478273627552,
                "neutral": 0.26133077540466493,
            },
            "dominant_emotion": "happy",
            "region": {"x": 89, "y": 76, "w": 210, "h": 252, "left_eye": [253, 173], "right_eye": [162, 174]},
            "face_confidence": 0.96,
            "path": "./photodatabase/Karmanyaah/10.png",
        },
    ],
    "vid.mp4",
)
