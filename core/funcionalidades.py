import numpy as np
from PySide6.QtWidgets import QMessageBox, QInputDialog
from core.calibration_manager import CalibrationManager
from core.analysis_engine import AnalysisEngine

class Funcionalidades:
    def __init__(self):
        self.scale_factor = None
        self.calibration_manager = None # Será instanciado na UI
        self.analysis_engine = None # Será instanciado na UI

    def handle_velocity_calculation(self, ui, image_processor):
        if self.analysis_engine is None:
            QMessageBox.critical(ui, "Erro", "AnalysisEngine não inicializado.")
            return

        deformation_cm = self.analysis_engine.measure_deformation()
        if deformation_cm is not None:
            self.analysis_engine.calculate_energy_and_velocity(deformation_cm)
