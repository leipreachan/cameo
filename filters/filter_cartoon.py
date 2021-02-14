import cv2

from filters.filter import Filter


class FilterCartoon(Filter):
    def __init__(self):
        super(FilterCartoon, self).__init__(duration=0)

    # https://subscription.packtpub.com/book/application_development/9781785282690/1/ch01lvl1sec12/cartoonizing-an-image
    def render(self, img_rgb):
        numDownSamples = 3 # number of downscaling steps
        numBilateralFilters = 7  # number of bilateral filtering steps

        # -- STEP 1 --
        # downsample image using Gaussian pyramid
        img_color = img_rgb
        for _ in range(numDownSamples):
            img_color = cv2.pyrDown(img_color)

        # repeatedly apply small bilateral filter instead of applying
        # one large filter
        for _ in range(numBilateralFilters):
            img_color = cv2.bilateralFilter(img_color, 9, 9, 9)

        # upsample image to original size
        for _ in range(numDownSamples):
            img_color = cv2.pyrUp(img_color)

        # -- STEPS 2 and 3 --
        # convert to grayscale and apply median blur
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.medianBlur(img_gray, 7)

        # -- STEP 4 --
        # detect and enhance edges
        img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                         cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 2)

        # -- STEP 5 --
        # convert back to color so that it can be bit-ANDed
        # with color image
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)

        return cv2.bitwise_and(img_color, img_edge)

    def draw(self, frame):
        if self.do_stop:
            return frame

        frame = self.render(frame)
        return frame
