from PyQt5 import QtWidgets


import image_data
import image_view


class CWidget(QtWidgets.QWidget):
    view: image_view.CView

    def __init__(self, _view: image_view.CView):
        super(CWidget, self).__init__()

        self.view = _view

        # Designerで作成したWidgetがMainFrameのDockWidgetに格納される前提です。
        # self.ui = ui.frm_x_demo.Ui_Form()
        # self.ui.setupUi(self)

    def custom_init(self):
        # 開始化処理
        # ツールが切り替わる毎に呼び出されます。

        # マウスイベントの受け取り開始（適当）
        self.view.pix_item.event_reciever = self

    def custom_term(self):
        # 終了処理
        # ツールが切り替わる毎に呼び出されます。

        # マウスイベントの受け取り終了（適当）
        self.view.pix_item.event_reciever = None

    def custom_mousePressEvent(self, event) -> None:
        pass

    def custom_mouseReleaseEvent(self, event) -> None:
        pass

    def dummy_function(self):
        # 読み込んだ画像は以下の方法で取得します。
        result, pil_image = self.view.src_image_data.get_image(
            image_data.IMAGE_TYPE_PIL
        )
        result, cv2_image = self.view.dst_image_data.get_image(
            image_data.IMAGE_TYPE_OPENCV
        )
