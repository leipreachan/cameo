import cv2
import numpy as np
import emoji

from filters.filter import Filter
from PIL import ImageFont, ImageDraw, Image, ImageFilter


class FilterBlurText(Filter):
    def __init__(self, text):
        super(FilterBlurText, self).__init__(duration=0)
        self.text = text
        self.do_stop = False

    def draw(self, frame):
        cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im_rgb)
        pil_im = pil_im.filter(ImageFilter.GaussianBlur(30))
        draw = ImageDraw.Draw(pil_im)
        font = ImageFont.truetype("Ubuntu-L.ttf", 80)
        proper_text = emoji.emojize(self.text)
        w, h = draw.textsize(proper_text, font)
        height, width, _ = frame.shape
        xy = ((width - w) / 2, (height - h) / 2)
        draw.text(xy, proper_text, font=font)
        frame = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        return frame
