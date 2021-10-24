import io
from PyQt5 import QtWidgets, QtSvg

import ui.frm_potrace
from lib.potrace import Bitmap
from lib.potrace import backend_svg

import image_data
import image_view


class CWidget(QtWidgets.QWidget):
    view: QtWidgets.QGraphicsView

    def __init__(self, _view: QtWidgets.QGraphicsScene):
        super(CWidget, self).__init__()

        self.view = _view

        self.ui = ui.frm_potrace.Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.pressed.connect(self.evt_trace)

    def custom_init(self):
        pass

    def custom_term(self):
        pass

    def evt_trace(self):

        _, pil_image = self.view.src_image_data.get_image(image_data.IMAGE_TYPE_PIL)

        bm = Bitmap(pil_image, 0.5)

        plist = bm.trace(
            turdsize=2,
            turnpolicy="minority",
            alphamax=1,
            opticurve=False,
            opttolerance=0.2,
        )

        data = backend_svg.backend_svg(pil_image, plist)

        self.view.dst_image_data.from_svg(data)
        self.view.set_display(image_view.DISPLAY_DST)
