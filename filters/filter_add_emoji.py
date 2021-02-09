import cv2
import numpy as np
import emoji

from filters.filter import Filter
from PIL import ImageFont, ImageDraw, Image


class FilterAddEmoji(Filter):
    def __init__(self, text):
        super(FilterAddEmoji, self).__init__(duration=0)
        self.text = text
        self.do_stop = False

    def draw(self, frame):
        cv2_im_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(cv2_im_rgb)
        draw = ImageDraw.Draw(pil_im)
        font = ImageFont.truetype("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf", size=109, layout_engine=ImageFont.LAYOUT_RAQM)
        proper_text = emoji.emojize(self.text, use_aliases=True)
        w, h = draw.textsize(proper_text, font=font)
        height, width, _ = frame.shape
        xy = (int((width - w) / 2), int((height - h) / 2))
        draw.text(xy, proper_text, fill="white", embedded_color=True, font=font)
        frame = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)
        return frame
