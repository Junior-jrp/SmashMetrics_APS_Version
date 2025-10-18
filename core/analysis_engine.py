import numpy as np
from PySide6.QtWidgets import QMessageBox, QInputDialog
from core.database import DatabaseManager, AnaliseCRUD


class AnalysisEngine:
    def __init__(self, ui_context, image_processor):
        self.ui = ui_context
        self.image_processor = image_processor

    def measure_deformation(self):
        if self.ui.processed_image is None:
            QMessageBox.warning(self.ui, "Erro", "Nenhuma imagem processada para medir a deformação.")
            return None

        image_copy = self.ui.processed_image.copy()
        points = self.image_processor.select_points(image_copy)
        if len(points) != 2:
            QMessageBox.warning(self.ui, "Erro", "Selecione exatamente dois pontos para medir a deformação.")
            return None

        pixel_distance = self.image_processor.calculate_pixel_distance(points[0], points[1])
        if self.ui.scale_factor is None:
            QMessageBox.warning(self.ui, "Erro", "Calibre a imagem primeiro!")
            return None

        real_distance = pixel_distance * self.ui.scale_factor
        QMessageBox.information(self.ui, "Medição de Deformação",
                                f"Deformação medida: {real_distance:.2f} cm")
        return real_distance

    def calculate_energy_and_velocity(self, deformation_cm):
        mass, ok_mass = QInputDialog.getDouble(self.ui, "Massa", "Insira a massa do veículo (kg):", decimals=2)
        if not ok_mass or mass <= 0:
            QMessageBox.warning(self.ui, "Erro", "Massa inválida.")
            return
        deformation_m = deformation_cm / 100.0
        F_eff = 2.621e6
        Edef = F_eff * (deformation_m ** 2)

        velocity = np.sqrt((2 * Edef) / mass)
        velocity_kmh = velocity * 3.6

        report_content = (
            f"**Resultados da Análise (Método Ajustado)**\n"
            f"- Deformação medida: {deformation_cm:.2f} cm\n"
            f"- Edef: {Edef:.2f} Joules\n"
            f"- Velocidade: {velocity_kmh:.2f} km/h"
        )
        QMessageBox.information(self.ui, "Resultados da Análise", report_content)


        db = DatabaseManager()
        analise_crud = AnaliseCRUD(db)
