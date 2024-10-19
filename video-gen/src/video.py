import os
import cv2
import numpy as np
from typing import List


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
    text = cv2.imread("./static/you_are_so.png", cv2.IMREAD_UNCHANGED)

    x_align = 50
    y_align = 600

    @staticmethod
    def generate(background):
        add_transparent_image(background, YouAreSoOverlay.text, YouAreSoOverlay.x_align, YouAreSoOverlay.y_align)


class PreciousOverlay:
    text = cv2.imread("./static/precious.png", cv2.IMREAD_UNCHANGED)

    x_align = 75
    y_align = 600

    @staticmethod
    def generate(background):
        add_transparent_image(background, PreciousOverlay.text, PreciousOverlay.x_align, PreciousOverlay.y_align)


class WhenYouOverlay:
    text = cv2.imread("./static/when_you.png", cv2.IMREAD_UNCHANGED)

    x_align = 75
    y_align = 600

    @staticmethod
    def generate(background):
        add_transparent_image(background, WhenYouOverlay.text, WhenYouOverlay.x_align, WhenYouOverlay.y_align)


class SmileOverlay:
    text = cv2.imread("./static/overlay_smile.png", cv2.IMREAD_UNCHANGED)

    x_align = 0
    y_align = 0

    @staticmethod
    def generate(background):
        add_transparent_image(background, SmileOverlay.text, SmileOverlay.x_align, SmileOverlay.y_align)


class PreciousSmileGenerator:

    image_manipulations = [
        YouAreSoOverlay.generate,
        PreciousOverlay.generate,
        WhenYouOverlay.generate,
        SmileOverlay.generate,
        SmileOverlay.generate,
    ]
    files: List[str] = []
    folder: str = ""

    def load_pictures(self, path: str):
        self.folder = path
        contents = os.listdir(path)
        contents.sort()
        for img_file in contents:
            if img_file.endswith((".jpg", ".jpeg", ".png")):
                print("reading: ", img_file)
                self.files.append(os.path.join(path, img_file))
                print(cv2.imread(os.path.join(path, img_file)).shape)

    def render(self, video_filename: str):
        print(self.files)
        first_image = cv2.imread(self.files[0])
        h, w, _ = first_image.shape

        codec = cv2.VideoWriter_fourcc(*"mp4v")
        vid_writer = cv2.VideoWriter(video_filename, codec, 30, (w, h))

        for i, img in enumerate(self.files):
            loaded_img = cv2.imread(img)
            self.image_manipulations[i](loaded_img)
            for _ in range(40):
                vid_writer.write(loaded_img)
        vid_writer.release()


vid_gen = PreciousSmileGenerator()
vid_gen.load_pictures("./pictures")
vid_gen.render("out.mp4")
