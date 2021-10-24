import io
import re
from typing import Any, Tuple

import PIL.Image
import numpy as np
import cv2

from PyQt5 import Qt, QtSvg, QtWidgets

INTERNAL_IMAGE_FORMAT = "bmp"

IMAGE_TYPE_PIL = 1
IMAGE_TYPE_OPENCV = 2
IMAGE_TYPE_NNABLA = 3
IMAGE_TYPE_QTITEM = 4

COLOR_ORDER_RGB = 1
COLOR_ORDER_BGR = 2


class CImageData(object):
    pil_image: PIL.Image.Image = None
    svg_image: str = None

    def from_file(self, fp, mode="r", formats=None) -> None:
        self.pil_image = PIL.Image.open(fp, mode=mode, formats=formats)
        self.svg_image = None

    def from_svg(self, svg: str) -> None:
        self.pil_image = None
        self.svg_image = svg

    def get_image(
        self,
        image_type: int,
        channel_first: bool = False,
        color_order: int = COLOR_ORDER_RGB,
    ) -> Tuple[bool, Any]:

        if self.pil_image is None:
            return False, None

        rgb_image = self.pil_image.convert("RGB")

        if image_type == IMAGE_TYPE_PIL:
            return True, self.pil_image

        elif image_type == IMAGE_TYPE_OPENCV:
            np_image = np.asarray(self.pil_image.convert("RGB"))
            if color_order == COLOR_ORDER_BGR:
                np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
            return True, np_image

        elif image_type == IMAGE_TYPE_NNABLA:
            rgb_image = self.pil_image.convert("RGB")
            np_image = np.asarray(rgb_image)
            if color_order == COLOR_ORDER_BGR:
                np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
            if channel_first is True:
                np_image = np_image.transpose((2, 0, 1))
            return True, np_image

    def set_image(
        self,
        image: Any,
        channel_first: bool = False,
        color_order: int = COLOR_ORDER_RGB,
    ):

        self.pil_image = None
        self.svg_image = None

        if isinstance(image, PIL.Image.Image) is True:
            self.pil_image = image

        elif isinstance(image, np.ndarray) is True:
            np_image = image
            if color_order == COLOR_ORDER_BGR:
                np_image = cv2.cvtColor(np_image, cv2.COLOR_BGR2RGB)
            if channel_first is True:
                np_image = np_image.transpose((1, 2, 0))
            self.pil_image = PIL.Image.fromarray(np_image)

        elif isinstance(image, str) is True:
            self.svg_image = image

    def get_size(self) -> Tuple[int, int]:
        if self.pil_image is not None:
            return self.pil_image.width, self.pil_image.height
        elif self.svg_image is not None:
            found = re.search('width="(.*)" height="(.*)"', self.svg_image)
            if found is not None:
                return int(found.group(1)), int(found.group(2))
        else:
            return None, None

    def get_pixmap(self) -> Any:

        if self.pil_image is not None:
            io_bytes = io.BytesIO()
            self.pil_image.save(io_bytes, INTERNAL_IMAGE_FORMAT)
            io_bytes.seek(0)
            item = Qt.QPixmap()
            item.loadFromData(io_bytes.read())

        elif self.svg_image is not None:
            item = self.svg_image

        else:
            item = None

        return item
