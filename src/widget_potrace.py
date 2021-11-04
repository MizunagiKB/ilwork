from PyQt5 import QtCore, QtGui, QtWidgets
from numpy import result_type

import ui.frm_potrace

from deps.potrace import Bitmap
from deps.potrace import backend_svg

import image_data
import image_view


class CWidget(QtWidgets.QWidget):
    view: image_view.CView = None
    prev_background_brush: QtGui.QBrush = None

    def __init__(self, _view: image_view.CView):
        super(CWidget, self).__init__()

        self.view = _view

        self.ui = ui.frm_potrace.Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButton.pressed.connect(self.evt_trace)

    def custom_init(self):

        self.prev_background_brush = self.view.backgroundBrush()

        color_w = QtGui.QColor(255, 255, 255)
        color_g = QtGui.QColor(220, 220, 220)

        tilePixmap = QtGui.QPixmap(64, 64)
        tilePixmap.fill(color_w)

        tilePainter = QtGui.QPainter(tilePixmap)
        tilePainter.fillRect(0, 0, 32, 32, color_g)
        tilePainter.fillRect(32, 32, 32, 32, color_g)
        tilePainter.end()

        self.view.setBackgroundBrush(QtGui.QBrush(tilePixmap))

    def custom_term(self):
        if self.prev_background_brush is not None:
            self.view.setBackgroundBrush(self.prev_background_brush)

    def evt_trace(self):

        result, pil_image = self.view.src_image_data.get_image(image_data.IMAGE_TYPE_PIL)
        if result is False:
            return

        blacklevel = (
            self.ui.slider_blacklevel.value() / self.ui.slider_blacklevel.maximum()
        )
        bm = Bitmap(pil_image, blacklevel)

        plist = bm.trace(
            turdsize=self.ui.spin_turdsize.value(),
            turnpolicy=self.ui.combo_turnpolicy.currentIndex(),
            alphamax=self.ui.spin_alphamax.value() / 10.0,
            opticurve=self.ui.check_opticurve.isChecked(),
            opttolerance=0.2,
        )

        data = backend_svg.backend_svg(pil_image, plist)

        self.view.dst_image_data.from_svg(data)
        self.view.set_display(image_view.DISPLAY_DST)
