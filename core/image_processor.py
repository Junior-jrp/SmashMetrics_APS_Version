import cv2
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QImage, QPixmap, Qt
from scipy.ndimage import distance_transform_edt
from skimage import morphology, measure, segmentation, filters, color
from scipy import ndimage as ndi

class ImageProcessor:
    def __init__(self, ui_context):
        self.ui = ui_context

    def import_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self.ui, "Importar Imagem", "",
            "Imagens (*.png *.jpg *.bmp *.tiff)"
        )
        if file_path:
            self.ui.original_image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            if self.ui.original_image is not None:
                self.ui.display_image(self.ui.original_image)
                QMessageBox.information(
                    self.ui, "Imagem Importada",
                    f"Imagem {file_path} carregada com sucesso."
                )
            else:
                QMessageBox.warning(self.ui, "Erro", "Falha ao carregar a imagem.")

    def remove_image(self):
        self.ui.remove_image()

    def convert_to_gray(self):
        if self.ui.original_image is not None:
            if len(self.ui.original_image.shape) == 3:
                gray_image = cv2.cvtColor(self.ui.original_image, cv2.COLOR_BGR2GRAY)
            else:
                gray_image = self.ui.original_image

            gray_image = cv2.normalize(gray_image, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)

            self.ui.processed_image = gray_image
            self.ui.display_image(gray_image)
            QMessageBox.information(
                self.ui, "Conversão",
                "Imagem convertida para escala de cinza 8-bit."
            )
        else:
            QMessageBox.warning(self.ui, "Erro", "Nenhuma imagem carregada.")

    def imposemin(self, img, minima):
        marker = np.full(img.shape, np.inf)
        marker[minima == 1] = 0
        mask = np.minimum(img + 1, marker)
        return morphology.reconstruction(marker, mask, method='erosion')

    def apply_watershed(self):
        if self.ui.processed_image is not None:
            try:
                if len(self.ui.processed_image.shape) == 3:
                    gray = cv2.cvtColor(self.ui.processed_image, cv2.COLOR_BGR2GRAY)
                else:
                    gray = self.ui.processed_image.copy()
                cv2.imshow("1. Imagem em Escala de Cinza", gray)
                cv2.waitKey(0)

                blurred = cv2.GaussianBlur(gray, (7, 7), 3)
                cv2.imshow("2. Filtro Gaussiano", blurred)
                cv2.waitKey(0)

                _, binary = cv2.threshold(blurred, 0, 255,
                                          cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
                cv2.imshow("3. Binarização Invertida", binary)
                cv2.waitKey(0)

                se_disk = morphology.disk(1)
                opening_bool = morphology.opening(binary.astype(bool), se_disk)
                opening = opening_bool.astype(np.uint8) * 255
                cv2.imshow("4. Abertura Morfológica", opening)
                cv2.waitKey(0)

                opening_uint8 = opening_bool.astype(np.uint8) * 255
                kernel_cv2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
                sure_bg = cv2.dilate(opening_uint8, kernel_cv2, iterations=1)
                sure_bg = cv2.dilate(sure_bg, kernel_cv2, iterations=1)
                sure_bg = cv2.dilate(sure_bg, kernel_cv2, iterations=1)
                cv2.imshow("5. Área de Fundo (Dilatação)", sure_bg)
                cv2.waitKey(0)

                D = ndi.distance_transform_edt(np.logical_not(opening_bool))
                dist_display = cv2.normalize(D, None, 0, 255,
                                             cv2.NORM_MINMAX).astype(np.uint8)
                cv2.imshow("6. Transformada de Distância", dist_display)
                cv2.waitKey(0)
                maxD = D.max()
                sure_fg_bool = D > 0.5 * maxD
                sure_fg = sure_fg_bool.astype(np.uint8) * 255
                cv2.imshow("7. Foreground Seguro", sure_fg)
                cv2.waitKey(0)

                unknown = np.logical_and(sure_bg > 0, sure_fg == 0)
                unknown_uint8 = (unknown.astype(np.uint8)) * 255
                cv2.imshow("8. Regiões Desconhecidas", unknown_uint8)
                cv2.waitKey(0)

                markers = measure.label(sure_fg_bool, connectivity=2)
                markers = markers + 1
                markers[unknown] = 0
                markers_vis = color.label2rgb(markers, bg_label=0, bg_color=(1, 1, 1))
                markers_vis = (markers_vis * 255).astype(np.uint8)
                cv2.imshow("9. Marcadores (Markers)", markers_vis)
                cv2.waitKey(0)

                gradmag = filters.sobel(gray.astype(float) / 255)
                grad_norm = cv2.normalize(gradmag, None, 0, 255,
                                          cv2.NORM_MINMAX).astype(np.uint8)
                cv2.imshow("10. Gradiente da Imagem", grad_norm)
                cv2.waitKey(0)

                minima = (markers > 0).astype(np.uint8)
                markers_imposed = self.imposemin(gradmag, minima)
                L_ws = segmentation.watershed(
                    markers_imposed,
                    connectivity=2,
                    watershed_line=False
                )

                L_ws_vis = color.label2rgb(L_ws, bg_label=0, bg_color=(1, 1, 1))
                L_ws_vis = (L_ws_vis * 255).astype(np.uint8)

                cv2.imshow("Segmentação via Watershed", L_ws_vis)
                cv2.waitKey(0)

                boundary = morphology.dilation(L_ws) != morphology.erosion(L_ws)

                if len(self.ui.original_image.shape) == 2:
                    I_color = cv2.cvtColor(self.ui.original_image, cv2.COLOR_GRAY2BGR)
                else:
                    I_color = self.ui.original_image.copy()

                I_overlay = I_color.copy()
                I_overlay[boundary] = [0, 0, 255]

                cv2.imshow("12. Segmentação por Watershed (Overlay)", I_overlay)
                cv2.waitKey(0)
                cv2.destroyAllWindows()

                self.ui.processed_image = I_overlay
                self.ui.display_image(I_overlay)

                QMessageBox.information(self.ui, "Watershed",
                                        "Segmentação concluída com:\n"
                                        "- Contornos em vermelho")
            except Exception as e:
                QMessageBox.critical(self.ui, "Erro", f"Erro no processamento:\n{str(e)}")
        else:
            QMessageBox.warning(self.ui, "Erro", "Nenhuma imagem processada.")

    def select_points(self, image):
        points = []
        zoom_scale = 3
        zoom_size = 100

        draw_image = image.copy()
        zoom_window = None

        def click_event(event, x, y, flags, param):
            nonlocal draw_image, zoom_window
            if event == cv2.EVENT_LBUTTONDOWN:
                if len(points) == 0:
                    points.append((x, y))
                    cv2.circle(draw_image, (x, y), 5, (0, 255, 0), -1)
                    cv2.imshow("Seleção de Pontos", draw_image)
                elif len(points) == 1:
                    points.append((x, y))
                    cv2.line(draw_image, points[0], points[1], (0, 255, 0), 2)
                    cv2.imshow("Seleção de Pontos", draw_image)
            elif event == cv2.EVENT_MOUSEMOVE:
                x_start = max(x - zoom_size // 2, 0)
                y_start = max(y - zoom_size // 2, 0)
                x_end = min(x + zoom_size // 2, image.shape[1])
                y_end = min(y + zoom_size // 2, image.shape[0])
                zoom_region = image[y_start:y_end, x_start:x_end].copy()
                cv2.circle(zoom_region, (zoom_size // 2, zoom_size // 2), 3, (0, 0, 255), -1)
                zoom_resized = cv2.resize(zoom_region, (zoom_size * zoom_scale, zoom_size * zoom_scale),
                                          interpolation=cv2.INTER_LINEAR)
                cv2.imshow("Zoom", zoom_resized)
                if len(points) == 1:
                    temp_image = draw_image.copy()
                    cv2.line(temp_image, points[0], (x, y), (255, 0, 0), 1)
                    cv2.imshow("Seleção de Pontos", temp_image)

        cv2.imshow("Seleção de Pontos", draw_image)
        cv2.setMouseCallback("Seleção de Pontos", click_event)

        while len(points) < 2:
            if cv2.waitKey(100) == 27:
                break

        cv2.destroyWindow("Zoom")
        cv2.destroyWindow("Seleção de Pontos")
        return points

        while len(points) < 2:
            if cv2.waitKey(100) == 27:
                break

        cv2.destroyAllWindows()
        return points

    def calculate_pixel_distance(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
