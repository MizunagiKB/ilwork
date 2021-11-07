from typing import cast, List
from PyQt5 import Qt, QtCore, QtGui, QtWidgets

import cv2

import numpy as np
import image_data
import image_view
import ui.frm_watershed

DEFAULT_COLOR_LIST = [
    Qt.QColorConstants.White,
    Qt.QColorConstants.Red,
    Qt.QColorConstants.Green,
    Qt.QColorConstants.Blue,
]


class CLayerProperty(object):
    color: Qt.QColor = None

    def __init__(self, _color: Qt.QColor):

        self.m_pin_pen = Qt.QPen()
        self.m_pin_pen.setStyle(QtCore.Qt.SolidLine)
        self.m_pin_pen.setColor(Qt.QColorConstants.White)

        self.m_pin_brush = Qt.QBrush()
        self.m_pin_brush.setStyle(QtCore.Qt.SolidPattern)

        self.set_color(_color)

    def set_color(self, _color: Qt.QColor):
        self.color = _color
        self.m_pin_brush.setColor(self.color)


class CGPinItem(QtWidgets.QGraphicsRectItem):
    widget = None

    def mousePressEvent(self, event):
        super(CGPinItem, self).mousePressEvent(event)

        o_gitem = self.widget.get_current_tree_item(self)
        if o_gitem is not None:
            o_widget = self.widget.ui.treewidget_layer
            o_widget.setCurrentItem(o_gitem)

    def mouseReleaseEvent(self, event):
        super(CGPinItem, self).mouseReleaseEvent(event)

        self.widget.update_color()
        self.widget.update_pin()
        self.widget.watershed()

    def keyPressEvent(self, event):
        super(CGPinItem, self).keyPressEvent(event)

        if event.key() in (QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace):
            self.widget.remove_pin()


class CWidget(QtWidgets.QWidget):
    view: image_view.CView = None
    watershed_mark: np.ndarray = None
    __disable_event: bool = True

    def __init__(self, _view: image_view.CView):
        super(CWidget, self).__init__()

        self.view = _view

        self.ui = ui.frm_watershed.Ui_Form()
        self.ui.setupUi(self)

        self.ui.group_layer_property.setEnabled(False)

        self.ui.slider_transparent.valueChanged.connect(self.evt_changed)
        self.ui.slider_r.valueChanged.connect(self.evt_color)
        self.ui.slider_g.valueChanged.connect(self.evt_color)
        self.ui.slider_b.valueChanged.connect(self.evt_color)

        self.ui.treewidget_layer.currentItemChanged.connect(
            self.evt_current_item_changed
        )

    def custom_init(self):

        self.view.set_display(image_view.DISPLAY_SRC)

        self.view.clear_marker()

        widget = self.ui.treewidget_layer
        widget.clear()
        widget.setColumnCount(2)

        for idx, o_color in enumerate(DEFAULT_COLOR_LIST):
            o_layer = QtWidgets.QTreeWidgetItem()
            o_layer.setText(0, "")
            if idx == 0:
                o_layer.setText(1, "Base")
                o_layer.setData(0, QtCore.Qt.UserRole, None)
            else:
                layer_prop = CLayerProperty(o_color)
                o_layer.setText(1, "Area {:d}".format(idx))
                o_layer.setData(0, QtCore.Qt.UserRole, layer_prop)

                o_pixmap = QtGui.QPixmap(16, 16)
                o_pixmap.fill(layer_prop.color)
                o_layer.setIcon(0, QtGui.QIcon(o_pixmap))

            widget.addTopLevelItem(o_layer)

        self.update_color()

        widget.setCurrentItem(widget.topLevelItem(1))

        self.clear_mark()

        self.watershed()

        self.view.pix_item.event_reciever = self

    def custom_term(self):
        self.view.pix_item.event_reciever = None

    def custom_mousePressEvent(self, event) -> bool:
        if event.button() == QtCore.Qt.LeftButton:
            o_layer = self.get_current_layer()
            self.append_pin(o_layer, event.pos())
            self.update_pin()
            self.watershed()

    def custom_mouseReleaseEvent(self, event) -> bool:
        pass

    def keyPressEvent(self, evt: QtGui.QKeyEvent) -> None:

        if evt.key() in (QtCore.Qt.Key_Delete, QtCore.Qt.Key_Backspace):
            self.remove_pin()

    def evt_changed(self):
        alpha = self.ui.slider_transparent.value() / 100.0
        self.view.set_display(image_view.DISPLAY_DST, alpha)

    def evt_current_item_changed(self, item_curr, item_prev):

        enable = False

        for witem_area in self.iter_layer():
            for witem_pin in self.iter_pin(witem_area):
                _data = witem_pin.data(0, QtCore.Qt.UserRole)
                if isinstance(_data, CGPinItem) is True:
                    pin = cast(CGPinItem, _data)
                    pin.setSelected(False)

        if item_curr is not None:
            _data = item_curr.data(0, QtCore.Qt.UserRole)
            if _data is not None:
                if isinstance(_data, CLayerProperty) is True:
                    layer_data = cast(CLayerProperty, _data)

                    self.ui.text_layer_name.setText(item_curr.text(1))

                    self.__disable_event = True
                    self.ui.slider_r.setValue(layer_data.color.red())
                    self.ui.slider_g.setValue(layer_data.color.green())
                    self.ui.slider_b.setValue(layer_data.color.blue())
                    self.__disable_event = False
                    enable = True

                elif isinstance(_data, CGPinItem) is True:
                    pin = cast(CGPinItem, _data)
                    pin.setSelected(True)

        self.ui.group_layer_property.setEnabled(enable)

    def evt_color(self):

        if self.__disable_event is True:
            return

        layer_item = self.get_current_layer()

        if layer_item is not None:
            _data = layer_item.data(0, QtCore.Qt.UserRole)
            if _data is not None:
                if isinstance(_data, CLayerProperty) is True:
                    layer_data = cast(CLayerProperty, _data)

                    color = Qt.QColor(
                        self.ui.slider_r.value(),
                        self.ui.slider_g.value(),
                        self.ui.slider_b.value(),
                    )
                    layer_data.set_color(color)

                    self.update_color()
                    self.update_pin()
                    self.watershed()

    def clear_mark(self):
        result, cv2_image = self.view.src_image_data.get_image(
            image_data.IMAGE_TYPE_OPENCV
        )
        if result is True:
            self.watershed_mark = np.zeros(cv2_image.shape[0:2], np.int32)

    def iter_layer(self):

        widget = self.ui.treewidget_layer

        for idx in range(widget.topLevelItemCount()):
            yield widget.topLevelItem(idx)

    def iter_pin(self, o_layer):
        for idx in range(o_layer.childCount()):
            yield o_layer.child(idx)

    def iter_selected_pin(self):

        widget = self.ui.treewidget_layer

        for o_item in widget.selectedItems():
            gitem = o_item.data(0, QtCore.Qt.UserRole)
            if isinstance(gitem, CGPinItem) is True:
                yield o_item

    # ------------------------------------------------------------------------
    def append_pin(self, o_layer, o_pos):

        if o_layer is None:

            return None

        else:
            o_layer_info = o_layer.data(0, QtCore.Qt.UserRole)

            o_gitem = CGPinItem(o_pos.x() - 8, o_pos.y() - 8, 16, 16)
            o_gitem.widget = self
            o_gitem.setPen(o_layer_info.m_pin_pen)
            o_gitem.setBrush(o_layer_info.m_pin_brush)
            o_gitem.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
            o_gitem.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
            o_gitem.setFlag(QtWidgets.QGraphicsItem.ItemIsFocusable, True)

            o_gitem.setParentItem(self.view.marker_root)

            o_pin = QtWidgets.QTreeWidgetItem()
            o_pin.setText(1, "Pin")
            o_pin.setData(0, QtCore.Qt.UserRole, o_gitem)

            o_layer.addChild(o_pin)

            self.update_color()
            self.update_pin()
            self.watershed()

    def remove_pin(self):

        list_remove_item: List[QtWidgets.QTreeWidgetItem] = []

        for item in self.ui.treewidget_layer.selectedItems():
            _data = item.data(0, QtCore.Qt.UserRole)
            if isinstance(_data, CGPinItem) is True:
                pin = cast(CGPinItem, _data)
                pin.setParentItem(None)
                self.view.scene().removeItem(pin)

                item.setData(0, QtCore.Qt.UserRole, None)

                list_remove_item.append(item)

        for item in list_remove_item:
            item.parent().removeChild(item)

        self.update_color()
        self.update_pin()
        self.watershed()

    def update_pin(self):

        self.clear_mark()

        n_layer_index = 0
        for o_layer in self.iter_layer():
            for o_pin in self.iter_pin(o_layer):
                o_gitem = o_pin.data(0, QtCore.Qt.UserRole)

                o_point = o_gitem.mapToParent(
                    o_gitem.rect().x() + 8, o_gitem.rect().y() + 8
                )

                o_pin.setText(
                    1, "Pin(%(x)d, %(y)d)" % {"x": o_point.x(), "y": o_point.y()}
                )

                self.marker_set(o_point.x(), o_point.y(), n_layer_index)
            n_layer_index += 1

    def update_color(self):

        list_color = []

        for o_layer in self.iter_layer():
            layer_prop = o_layer.data(0, QtCore.Qt.UserRole)
            if layer_prop is None:
                list_color.append(Qt.QColor(0, 0, 0))
            else:
                list_color.append(layer_prop.color)

                o_pixmap = QtGui.QPixmap(16, 16)
                o_pixmap.fill(layer_prop.color)
                o_layer.setIcon(0, QtGui.QIcon(o_pixmap))

                for o_pin in self.iter_pin(o_layer):
                    o_gitem = o_pin.data(0, QtCore.Qt.UserRole)
                    o_gitem.setPen(layer_prop.m_pin_pen)
                    o_gitem.setBrush(layer_prop.m_pin_brush)

        self.update_ary_color(list_color)

    # ------------------------------------------------------------------------
    def get_current_layer(self) -> QtWidgets.QTreeWidgetItem:

        widget = self.ui.treewidget_layer

        o_item = widget.currentItem()
        if o_item is not None:
            o_item_data = o_item.data(0, QtCore.Qt.UserRole)
            if o_item_data is None:
                pass
            elif isinstance(o_item_data, CLayerProperty) is True:
                return o_item
            elif isinstance(o_item_data, CGPinItem) is True:
                return o_item.parent()

        return None

    def get_current_tree_item(self, o_gitem):
        if o_gitem is not None:
            for o_layer in self.iter_layer():
                for o_pin in self.iter_pin(o_layer):
                    if o_pin.data(0, QtCore.Qt.UserRole) == o_gitem:
                        return o_pin
        return None

    def update_ary_color(self, list_color):

        list_ndarray = [
            np.array([col.blue(), col.green(), col.red()]) for col in list_color
        ]
        self.m_ary_color = np.int32(list_ndarray)

    def marker_set(self, xpos, ypos, marker_index):

        cv2.rectangle(
            self.watershed_mark,
            (int(xpos) - 1, int(ypos) - 1),
            (int(xpos) + 1, int(ypos) + 1),
            marker_index,
        )

    def watershed(self, alpha=0.5):

        if self.watershed_mark is None:
            return

        _, cv_image = self.view.src_image_data.get_image(
            image_data.IMAGE_TYPE_OPENCV, color_order=image_data.COLOR_ORDER_BGR
        )

        cvimage_mark = self.watershed_mark.copy()
        cv2.watershed(cv_image, cvimage_mark)
        cvimage_overlay = self.m_ary_color[np.maximum(cvimage_mark, 0)]

        cvimage_result = cv2.addWeighted(
            cv_image,
            0.0,
            cvimage_overlay,
            1.0,
            0.0,
            dtype=cv2.CV_8UC3,
        )

        alpha = self.ui.slider_transparent.value() / 100.0

        self.view.dst_image_data.set_image(
            cvimage_result, color_order=image_data.COLOR_ORDER_BGR
        )
        self.view.set_display(image_view.DISPLAY_DST, alpha)
