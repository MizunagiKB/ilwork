from typing import Any
from PyQt5 import Qt, QtWidgets

import numpy as np
import cv2
import PIL.Image
import PIL.ImageFilter

import nnabla as nn

from nnabla.models.imagenet import VGG16

import image_data
import image_view
import ui.frm_check


class CWidget(QtWidgets.QWidget):
    view: image_view.CView = None
    model: VGG16 = None

    def __init__(self, _view: image_view.CView):
        super(CWidget, self).__init__()

        self.view = _view

        self.ui = ui.frm_check.Ui_Form()
        self.ui.setupUi(self)

        self.ui.slider_transparent.valueChanged.connect(self.evt_changed)

        self.ui.push_saliency_sr.pressed.connect(self.evt_saliency_sr)
        self.ui.push_saliency_fg.pressed.connect(self.evt_saliency_fg)
        self.ui.push_kmeans.pressed.connect(self.evt_kmean)
        self.ui.push_gradcam.pressed.connect(self.evt_gradcam)

    def custom_init(self):
        pass

    def custom_term(self):
        pass

    def evt_changed(self):
        alpha = self.ui.slider_transparent.value() / 100.0
        self.view.set_display(image_view.DISPLAY_DST, alpha)

    def evt_saliency_sr(self):
        self.processing_saliency(cv2.saliency.StaticSaliencySpectralResidual_create())

    def evt_saliency_fg(self):
        self.processing_saliency(cv2.saliency.StaticSaliencyFineGrained_create())

    def processing_saliency(self, saliency: Any):

        color_order = image_data.COLOR_ORDER_BGR

        _, cv2_image = self.view.src_image_data.get_image(
            image_data.IMAGE_TYPE_OPENCV, color_order=color_order
        )

        _, saliency_map = saliency.computeSaliency(cv2_image)

        im_gray = (saliency_map * 255).astype("uint8")
        cv2_image_heatmap = cv2.applyColorMap(im_gray, cv2.COLORMAP_JET)

        if False:
            h, w = cv2_image.shape[:2]
            px, py, _ = brightness(im_gray)
            # cv2_image_heatmap = cv2.circle(cv2_image, (px, py), 100, (255, 0, 0), 20)
            cv2_image_heatmap = cv2.circle(
                cv2_image, (px, py), w // 10, (0, 0, 0), (w // 50)
            )
            cv2_image_heatmap = cv2.circle(
                cv2_image_heatmap, (px, py), w // 10, (0, 0, 255), (w // 100)
            )

        alpha = self.ui.slider_transparent.value() / 100.0

        self.view.dst_image_data.set_image(cv2_image_heatmap, color_order=color_order)
        self.view.set_display(image_view.DISPLAY_DST, alpha)

    def evt_kmean(self):

        _, pil_image = self.view.src_image_data.get_image(image_data.IMAGE_TYPE_PIL)

        img3groups = pil_image.convert("L").quantize(
            colors=self.ui.spinbox_colors.value(), kmeans=100
        )
        img_filterd = img3groups.convert("RGB")

        for _ in range(self.ui.spinbox_number_of_times.value()):
            img_filterd = img_filterd.filter(PIL.ImageFilter.MaxFilter())
        for _ in range(self.ui.spinbox_number_of_times.value()):
            img_filterd = img_filterd.filter(PIL.ImageFilter.MinFilter())

        alpha = self.ui.slider_transparent.value() / 100.0

        self.view.dst_image_data.set_image(img_filterd)
        self.view.set_display(image_view.DISPLAY_DST, alpha)

    def evt_gradcam(self):

        if self.model is None:
            self.model = VGG16()

        _, pil_image = self.view.src_image_data.get_image(image_data.IMAGE_TYPE_PIL)

        export_image = nnabla_gradcam(self.model, pil_image)

        alpha = self.ui.slider_transparent.value() / 100.0

        self.view.dst_image_data.set_image(export_image)
        self.view.set_display(image_view.DISPLAY_DST, alpha)


def nnabla_gradcam(model, pil_image: PIL.Image.Image):

    batch_size = 1
    x = nn.Variable((batch_size,) + model.input_shape)
    # set training True since gradient of variable is necessary for Grad-CAM
    vgg = model(x, training=True, returns_net=True)
    vgg_variables = vgg.variables

    target_label_indices = {}
    for idx, name in enumerate(model.category_names):
        target_label_indices[name] = idx

    # target_label_indices = {
    #    "comic book":
    #    "butterfly": 326,
    #    "flower": 985,
    #    "spider": 74,
    # }
    input_name = list(vgg.inputs.keys())[0]

    resize_image = pil_image.convert("RGB").resize((224, 224))
    img = np.asarray(resize_image).astype(np.uint8)
    img = img.transpose((2, 0, 1))

    vgg_variables[input_name].d = img
    middle_layer = vgg_variables["VGG16/ReLU_13"]
    pred = vgg_variables["VGG16/Affine_3"]
    selected = pred[:, target_label_indices["comic book"]]

    selected.forward()

    predicted_labels = np.argsort(-pred.d[0])
    for i, predicted_label in enumerate(predicted_labels[:15]):
        # print(
        #     "Top {:d}, Label index: {:d},  Label name: {:s}".format(
        #         i + 1, predicted_label, model.category_names[predicted_label]
        #     )
        # )
        pass

    for k, v in vgg_variables.items():
        if "VGG16/" in k:
            v.grad.zero()

    selected = pred[:, target_label_indices["comic book"]]
    selected.backward()

    heatmap = gradcam(middle_layer)

    resize_image = pil_image.convert("RGB")
    base_img = np.asarray(resize_image).astype(np.uint8)

    img_filterd = overlay_images(base_img, heatmap, 1.0)

    return img_filterd


def gradcam(middle_layer):
    conv_layer_output = middle_layer.d
    conv_layer_grad = middle_layer.g
    pooled_grad = conv_layer_grad.mean(axis=(0, 2, 3), keepdims=True)
    heatmap = pooled_grad * conv_layer_output
    # ReLU
    heatmap = np.maximum(heatmap, 0)
    heatmap = heatmap.mean(axis=(0, 1))
    max_v, min_v = np.max(heatmap), np.min(heatmap)
    if max_v != min_v:
        heatmap = (heatmap - min_v) / (max_v - min_v)
    return heatmap


def overlay_images(base_img, overlay_img, overlay_coef=1.0):
    # resize
    _overlay_img = cv2.resize(overlay_img, (base_img.shape[1], base_img.shape[0]))
    # normalize
    _overlay_img = 255 * _overlay_img / _overlay_img.max()
    _overlay_img = _overlay_img.astype("uint8")
    # color adjust
    _overlay_img = cv2.applyColorMap(_overlay_img, cv2.COLORMAP_JET)
    base_img = cv2.cvtColor(base_img, cv2.COLOR_BGR2RGB)
    # overlay
    alpha1 = overlay_coef
    alpha2 = 1.0 - overlay_coef
    ret_img = _overlay_img * alpha1 + base_img * alpha2
    ret_img = 255 * ret_img / ret_img.max()
    ret_img = ret_img.astype("uint8")
    ret_img = cv2.cvtColor(ret_img, cv2.COLOR_BGR2RGB)
    return ret_img


# 画像の中でどこが最も明るいかを調べる関数
# https://watlab-blog.com/2019/07/27/movie-saliency/
def brightness(img):
    h, w = img.shape[:2]  # グレースケール画像のサイズ取得（カラーは3）
    x = int(w / 20)  # 領域の横幅
    y = int(h / 20)  # 領域の高さ
    x_step = x  # 領域の横方向へのずらし幅
    y_step = y  # 領域の縦方向へのずらし幅
    x0 = 0  # 領域の初期値x成分
    y0 = 0  # 領域の初期値y成分
    j = 0  # 縦方向のループ指標を初期化

    latest = 0  # 最新の平均輝度値
    coordinate = [0, 0]  # 最も明るい領域の座標値

    # 縦方向の走査を行うループ
    while y + (j * y_step) < h:
        i = 0  # 横方向の走査が終わる度にiを初期化
        ys = y0 + (j * y_step)  # 高さ方向の始点位置を更新
        yf = y + (j * y_step)  # 高さ方向の終点位置を更新

        # 横方向の走査をするループ
        while x + (i * x_step) < w:
            roi = img[ys:yf, x0 + (i * x_step) : x + (i * x_step)]  # 元画像から領域をroiで抽出

            # ここからが領域に対する画像処理
            # 領域毎に平均輝度を算出し、これまでの平均値と比べ大きかったらlatestを更新
            ave = np.mean(roi).astype("uint8")
            if latest < ave:
                latest = ave
                coordinate = [i, j]
            else:
                pass
            img[ys:yf, x0 + (i * x_step) : x + (i * x_step)] = np.full(roi.shape, ave)
            # ここまでが領域に対する画像処理

            i = i + 1  # whileループの条件がFalse（横方向の端になる）まで、iを増分
        j = j + 1  # whileループの条件がFalse（縦方向の端になる）まで、jを増分
    # 最も明るい領域の中心座標を計算
    px = int(coordinate[0] * x_step + (x / 2))
    py = int(coordinate[1] * y_step + (y / 2))
    return px, py, img
