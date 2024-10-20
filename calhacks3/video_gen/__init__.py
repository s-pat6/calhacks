import os
import cv2
import numpy as np
from typing import List
import subprocess
import json


STATIC_FOLDER = "./calhacks3/video_gen/static/"
PHOTO_FOLDER = "./photodatabase/"


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
        ColorFilter.make_pink,
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
        out = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                video_filename,
                "-i",
                f"{STATIC_FOLDER}smile.wav",
                "-map",
                "0:v",
                "-map",
                "1:a",
            "-c:v", "libx264",  # Encode video with H.264, widely supported by browsers
            "-c:a", "aac",       # Encode audio with AAC
                "-movflags",
                "+faststart",
                out_file,
            ],
            capture_output= False, #True

        )
        print("ffmpeg ran", out)


class PictureSelector:
    pictures = {}

    def __init__(self, meta_data) -> "PictureSelector":
        self.pictures = meta_data

    @staticmethod
    def calculate_happiness_metric(meta_data) -> float:
        return (
            meta_data["emotion"][meta_data["dominant_emotion"]] * 3
            + meta_data["emotion"]["happy"] * 2
            - meta_data["emotion"]["sad"]
            - meta_data["emotion"]["angry"]
            - meta_data["emotion"]["neutral"]
        )

    def select(self, num=5):
        ratings = [PictureSelector.calculate_happiness_metric(x) for x in self.pictures]
        selection = []

        sorted_list = [x for _, x in sorted(zip(ratings, self.pictures))]

        for i in range(num):
            index: int = int((len(self.pictures) / (num + 1)) * i)
            print("Rating:", ratings[index], "Index:", index)
            selected = sorted_list[index]
            selected["rating"] = PictureSelector.calculate_happiness_metric(selected)
            selection.append(selected)
        self.pictures = selection
        return selection

    def load_pictures(self):
        for pic in self.pictures:
            self.files.append(pic["path"])


class VideoGenerator:
    meta_data = {}

    def _load_meta_data(self, name: str):
        with open(f"{PHOTO_FOLDER}/{name}/meta.json") as f:
            self.meta_data[name] = json.loads(f.read())

    @staticmethod
    def insertion_sort(selected, extra):
        for e in extra:
            rating = PictureSelector.calculate_happiness_metric(e)
            inserted: bool = False

            for i, s in enumerate(selected):
                if s["rating"] >= rating:
                    selected.insert(i, e)
                    inserted: bool = True
                    break

            if not inserted:
                selected.append(e)

        return selected

    async def precious_smile_for(self, name: str, extra, out_file: str):
        if name not in self.meta_data:
            self._load_meta_data(name)

        picture_selector = PictureSelector(self.meta_data[name])
        selected = picture_selector.select(num=5 - min(len(extra), 5))
        selected_and_extra = VideoGenerator.insertion_sort(selected, extra)
        paths = [value["path"] for value in selected_and_extra]

        print(paths)

        vid_gen = PreciousSmileGenerator()
        vid_gen.load_pictures(paths)
        vid_gen.render("/tmp/temp.mp4")
        vid_gen.add_audio_track("/tmp/temp.mp4", "/tmp/tempaudio.mp4")
        os.rename("/tmp/tempaudio.mp4", out_file)
        


video_generator = VideoGenerator()

if __name__ == "__main__":
    video_generator.precious_smile_for(
        "Karmanyaah",
        [
            {
                "emotion": {
                    "angry": 3.577738496661068e-06,
                    "disgust": 7.95996562674417e-10,
                    "fear": 0.6826502212226523,
                    "happy": 1000.003607538234449408,
                    "sad": 10.322486479430586,
                    "surprise": 6.189664705563807e-08,
                    "neutral": 88.99125391192757,
                },
                "dominant_emotion": "happy",
                "region": {"x": 67, "y": 26, "w": 228, "h": 228, "left_eye": [147, 125], "right_eye": [146, 120]},
                "face_confidence": 0.98,
                "path": "./photodatabase/Tassilo/1.png",
            }
        ],
        "with_audio.mp4",
    )
