import cv2

from filters.filter import Filter
from filters.filter_color import FilterColor
from PIL import ImageFont, ImageDraw, Image  


class FilterAddText(Filter):
    def __init__(self, text):
        super(FilterAddText, self).__init__(duration=0)
        self.text = text
        self.do_stop = False

    def draw(self, frame):
        frame = FilterColor.add_color(frame, (255, 178, 0))
        cv2_im_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
	pil_im = Image.fromarray(cv2_im_rgb)
        
        frame = ImageDraw.Draw(pil_im)  
        font = ImageFont.truetype("Ubuntu-R.ttf", 80)  
        frame.text((10, 700), text, font=font)  
#        font = cv2.FONT_HERSHEY_SIMPLEX
#        fontScale = 1
#        color = (255, 255, 255)
#        thickness = 3
#        textsize = cv2.getTextSize(self.text, font, 1, 2)[0]
#        x = (frame.shape[1] - textsize[0]) // 2
#        y = (frame.shape[0] + textsize[1]) // 2 - 10
#        frame = cv2.putText(frame, self.text, (x, y), font_new, fontScale, color, thickness, cv2.LINE_AA)
        return frame
