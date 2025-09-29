import numpy as np
from PySide6.QtWidgets import QMessageBox, QInputDialog

class CalibrationManager:
    def __init__(self, ui_context, image_processor):
        self.ui = ui_context
        self.image_processor = image_processor

    def calibrate_image(self):
        if self.ui.original_image is not None:
            image_copy = self.ui.original_image.copy()
            scale_factors = []

            for i in range(3):
                QMessageBox.information(self.ui, "Calibração", f"Selecione os pontos para a calibração {i + 1}/3.")

                points = self.image_processor.select_points(image_copy)
                if len(points) != 2:
                    QMessageBox.warning(self.ui, "Erro", "Selecione exatamente dois pontos.")
                    return

                pixel_distance = self.image_processor.calculate_pixel_distance(points[0], points[1])
                if pixel_distance == 0:
                    QMessageBox.warning(self.ui, "Erro", "A distância entre os pontos não pode ser zero.")
                    return

                real_distance, ok = QInputDialog.getDouble(
                    self.ui, "Calibração",
                    f"Insira a distância real para a calibração {i + 1}/3 (em cm):",
                    decimals=2
                )
                if not ok or real_distance <= 0:
                    QMessageBox.warning(self.ui, "Erro", "Distância real inválida ou não fornecida.")
                    return

                scale_factor = real_distance / pixel_distance
                scale_factors.append(scale_factor)

            self.ui.scale_factor = np.mean(scale_factors)

            QMessageBox.information(
                self.ui, "Calibração",
                f"Escala calibrada com sucesso!\n"
                f"Fator médio: {self.ui.scale_factor:.4f} cm/px\n"
                f"(Baseado em 3 medições)"
            )
        else:
            QMessageBox.warning(self.ui, "Erro", "Nenhuma imagem carregada para calibrar.")
