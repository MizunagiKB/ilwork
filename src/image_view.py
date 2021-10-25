import os
import io
from typing import cast

import PIL.Image
from PyQt5 import Qt, QtCore, QtGui, QtSvg, QtWidgets

import image_data

DISPLAY_SRC = 1
DISPLAY_DST = 2


class CGraphicsItem(QtWidgets.QGraphicsPixmapItem):
    event_reciever = None
    view = None

    def __init__(self, _view):
        super(CGraphicsItem, self).__init__()

        self.view = _view

    def mousePressEvent(self, event):
        if self.event_reciever is None:
            super(CGraphicsItem, self).mousePressEvent(event)
        else:
            if self.view.hand_dragging is True:
                super(CGraphicsItem, self).mousePressEvent(event)
            else:
                self.event_reciever.custom_mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if self.event_reciever is None:
            super(CGraphicsItem, self).mouseReleaseEvent(event)
        else:
            if self.view.hand_dragging is True:
                super(CGraphicsItem, self).mousePressEvent(event)
            else:
                self.event_reciever.custom_mouseReleaseEvent(event)


class CScene(QtWidgets.QGraphicsScene):
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list") is True:
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list") is True:
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasFormat("text/uri-list") is True:
            for url in event.mimeData().urls():
                pathname = url.toLocalFile()
                _, ext = os.path.splitext(pathname)
                if ext.lower() in (".bmp", ".png", ".jpg", ".jpeg", ".webp"):
                    self.parent().open(url.toLocalFile())
                    event.acceptProposedAction()
                    break


class CView(QtWidgets.QGraphicsView):
    __main_window: QtWidgets.QMainWindow = None
    __src_image_data: image_data.CImageData = None
    __dst_image_data: image_data.CImageData = None
    __pix_item: CGraphicsItem = None
    __svg_item: QtSvg.QGraphicsSvgItem = None
    pixmap_root: QtWidgets.QGraphicsItem = None
    marker_root: QtWidgets.QGraphicsItem = None

    hand_dragging: bool = False

    def __init__(self, _main_window: QtWidgets.QMainWindow):
        super(CView, self).__init__()

        self.__main_window = _main_window

        self.__main_window.ui.ac_image_src.triggered.connect(self.evt_image_src)
        self.__main_window.ui.ac_image_dst.triggered.connect(self.evt_image_dst)

        self.__main_window.ui.ac_zoom_reset.triggered.connect(self.evt_zoom_reset)
        self.__main_window.ui.ac_zoom_out.triggered.connect(self.evt_zoom_out)
        self.__main_window.ui.ac_zoom_in.triggered.connect(self.evt_zoom_in)

        self.__src_image_data = image_data.CImageData()
        self.__dst_image_data = image_data.CImageData()

        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QtWidgets.QGraphicsView.FullViewportUpdate)

        self.setScene(CScene(self))

        self.__pix_item = CGraphicsItem(self)
        self.__pix_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
        self.__pix_item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)

        self.__svg_item = QtSvg.QGraphicsSvgItem()
        self.__svg_item.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, False)
        self.__svg_item.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, False)

        self.pixmap_root = QtWidgets.QGraphicsRectItem()
        self.scene().addItem(self.pixmap_root)
        self.marker_root = QtWidgets.QGraphicsRectItem()
        self.scene().addItem(self.marker_root)

        o_pixmap = QtGui.QPixmap(64, 64)
        o_pixmap.fill(QtGui.QColor(64, 64, 64))
        self.setBackgroundBrush(QtGui.QBrush(o_pixmap))

        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.set_display(DISPLAY_SRC)

    @property
    def src_image_data(self) -> image_data.CImageData:
        return self.__src_image_data

    @property
    def dst_image_data(self) -> image_data.CImageData:
        return self.__dst_image_data

    @property
    def pix_item(self) -> CGraphicsItem:
        return self.__pix_item

    def keyPressEvent(self, event):
        super(CView, self).keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Space:
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self.hand_dragging = True

    def keyReleaseEvent(self, event):
        super(CView, self).keyReleaseEvent(event)

        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.hand_dragging = False

    def evt_image_src(self):
        self.set_display(DISPLAY_SRC)

    def evt_image_dst(self):
        self.set_display(DISPLAY_DST)

    def evt_zoom_reset(self):
        self.resetTransform()

    def evt_zoom_in(self):
        self.scale(2.0, 2.0)

    def evt_zoom_out(self):
        self.scale(0.5, 0.5)

    def clear_pixmap(self):
        for o in self.pixmap_root.childItems():
            o.setParentItem(None)
            self.scene().removeItem(o)

    def clear_marker(self):
        for o in self.marker_root.childItems():
            o.setParentItem(None)
            self.scene().removeItem(o)

    def open(self, pathname: str) -> bool:

        if os.path.exists(pathname) is False:
            return False

        self.__src_image_data.from_file(pathname)
        self.__dst_image_data.from_file(pathname)

        self.clear_pixmap()

        self.resetTransform()
        w, h = self.__src_image_data.get_size()
        self.scene().setSceneRect(0, 0, w, h)
        self.set_display(DISPLAY_SRC)

        return True

    def export(self, pathname: str) -> bool:
        result, pil_image = self.__dst_image_data.get_image(image_data.IMAGE_TYPE_PIL)
        if result is True:
            cast(PIL.Image.Image, pil_image).save(pathname)
        return result

    def set_display(self, display: int, alpha: float = 0.5):
        self.clear_pixmap()

        check_src = False
        check_dst = False

        if display == DISPLAY_SRC:
            data = self.__src_image_data.get_pixmap()
            if data is None:
                pass
            else:
                self.__pix_item.setPixmap(data)
                self.__pix_item.setParentItem(self.pixmap_root)
                check_src = True

        elif display == DISPLAY_DST:
            res_src, im_src = self.__src_image_data.get_image(image_data.IMAGE_TYPE_PIL)
            res_dst, im_dst = self.__dst_image_data.get_image(image_data.IMAGE_TYPE_PIL)
            if all([res_src, res_dst]) is False:

                pix_data = self.__dst_image_data.get_pixmap()
                if pix_data is not None:
                    renderer = QtSvg.QSvgRenderer(pix_data.encode("utf-8"))
                    self.__svg_item.setSharedRenderer(renderer)
                    self.__svg_item.setFlags(QtWidgets.QGraphicsItem.ItemClipsToShape)
                    self.__svg_item.setCacheMode(QtWidgets.QGraphicsItem.NoCache)
                    self.__svg_item.setZValue(0)
                    self.__svg_item.setParentItem(self.pixmap_root)
                    check_dst = True

            elif isinstance(im_dst, PIL.Image.Image) is True:

                im = PIL.Image.blend(im_src, im_dst, alpha)

                io_bytes = io.BytesIO()
                im.save(io_bytes, "bmp")
                io_bytes.seek(0)
                item = Qt.QPixmap()
                item.loadFromData(io_bytes.read())

                self.__pix_item.setPixmap(item)
                self.__pix_item.setParentItem(self.pixmap_root)
                check_dst = True

        enabled = any([check_src, check_dst])
        self.__main_window.ui.ac_zoom_reset.setEnabled(enabled)
        self.__main_window.ui.ac_zoom_out.setEnabled(enabled)
        self.__main_window.ui.ac_zoom_in.setEnabled(enabled)

        self.__main_window.ui.ac_image_src.setEnabled(enabled)
        self.__main_window.ui.ac_image_dst.setEnabled(enabled)

        self.__main_window.ui.ac_image_src.setChecked(check_src)
        self.__main_window.ui.ac_image_dst.setChecked(check_dst)

        self.setFocus()
