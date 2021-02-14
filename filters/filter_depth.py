import cv2

from filters.filter import Filter


class FilterVideo(Filter):
    def __init__(self, path):
        super(FilterVideo, self).__init__(duration=0)
        self.video = cv2.VideoCapture(path)
        self.frame_counter = 0
        if not self.video.isOpened():
            self.logger.error(f"video file '{path}' doesn't exist")
            self.do_stop = True

    def draw(self, frame):
        if self.do_stop:
            return frame

        height, width, _ = frame.shape
        ret, frame = self.video.read()
        self.frame_counter += 1
        if self.frame_counter == self.video.get(cv2.CAP_PROP_FRAME_COUNT):
            self.frame_counter = 0 #Or whatever as long as it is the same as next line
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame = cv2.resize(frame, (width, height))
        return frame
