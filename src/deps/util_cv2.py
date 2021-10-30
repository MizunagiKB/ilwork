from typing import Tuple
import numpy as np


def brightness(
    _cv2_image: np.ndarray, size: Tuple[int, int] = (16, 16)
) -> Tuple[int, int]:
    # 画像の中でどこが最も明るいかを調べる関数
    # https://watlab-blog.com/2019/07/27/movie-saliency/

    cv2_image = _cv2_image.copy()
    h, w = cv2_image.shape[:2]

    x_step = w // size[0]
    x_adjust = (w % size[0]) // 2
    y_step = h // size[1]
    y_adjust = (h % size[1]) // 2

    latest = 0  # 最新の平均輝度値
    coordinate = [0, 0]  # 最も明るい領域の座標値

    for y in range(0, h, y_step):
        for x in range(0, w, x_step):

            x0 = x + x_adjust
            y0 = y + y_adjust
            x1 = x + x_adjust + x_step
            y1 = y + y_adjust + y_step

            roi = cv2_image[y0:y1, x0:x1]
            f_mean = np.average(roi).astype("uint8")

            if latest < f_mean:
                latest = f_mean
                coordinate = [x, y]
            else:
                pass

            cv2_image[y0:y1, x0:x1] = np.full(roi.shape, f_mean)

    px = coordinate[0] + (x_step // 2 + x_adjust)
    py = coordinate[1] + (y_step // 2 + y_adjust)

    return px, py, cv2_image
