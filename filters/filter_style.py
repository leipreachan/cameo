import cv2
import numpy as np

from filters.filter import Filter


class FilterStyle(Filter):
    def __init__(self, model_path):
        self.model = cv2.dnn.readNetFromTorch(model_path)
        super(FilterStyle, self).__init__(duration=0)

    def predict(self, img, h, w):
        blob = cv2.dnn.blobFromImage(img, 1.0, (w, h),
                                    (103.939, 116.779, 123.680), swapRB=False, crop=False)

        print ('[INFO] Setting the input to the model')
        self.model.setInput(blob)

        print ('[INFO] Starting Inference!')
        out = self.model.forward()
        print ('[INFO] Inference Completed successfully!')

        # Reshape the output tensor and add back in the mean subtraction, and
        # then swap the channel ordering
        out = out.reshape((3, out.shape[2], out.shape[3]))
        out[0] += 103.939
        out[1] += 116.779
        out[2] += 123.680
        out /= 255.0
        out = out.transpose(1, 2, 0)
        return out

    def render(self, frame):
        (h, w) = frame.shape[:2]
        output = self.predict(frame, h, w)
        return output

    def draw(self, frame):
        if self.do_stop:
            return frame

        frame = self.render(frame)
        return frame
