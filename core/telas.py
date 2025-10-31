from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QPushButton, QStackedWidget, QTextEdit, QComboBox,
    QInputDialog, QFrame, QScrollArea, QLineEdit, QDateEdit
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QImage
from PySide6.QtCore import Qt, QDate

from core.database import DatabaseManager
from core.funcionalidades import Funcionalidades
from core.google_auth import GoogleAuthenticator
from core.image_processor import ImageProcessor
from core.calibration_manager import CalibrationManager
from core.analysis_engine import AnalysisEngine
from core.crud_screens import SeguradorasCRUDScreen, AnaliseCRUDScreen
from core.theme import Styles, Colors, Icons, BorderRadius, Typography


class ModernCard(QFrame):
    def __init__(self, title="", description="", icon_text="", parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        self.setup_ui(title, description, icon_text)

    def setup_ui(self, title, description, icon_text):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)

        if icon_text:
            icon_label = QLabel(icon_text)
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setStyleSheet(f"""
                QLabel {{
                    font-size: {Typography.SIZE_XLARGE};
                    color: {Colors.CYAN_PRIMARY};
                    font-weight: {Typography.WEIGHT_BOLD};
                    background-color: transparent;
                }}
            """)
            layout.addWidget(icon_label)

        if title:
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet(Styles.label_normal())
            layout.addWidget(title_label)

        if description:
            desc_label = QLabel(description)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet(f"""
                QLabel {{
                    font-size: {Typography.SIZE_NORMAL};
                    color: {Colors.TEXT_SECONDARY};
                    line-height: 1.4;
                    background-color: transparent;
                }}
            """)
            layout.addWidget(desc_label)

        self.setStyleSheet(Styles.card())


class SidebarButton(QPushButton):
    def __init__(self, text, icon_text="", parent=None):
        super().__init__(parent)
        self.setText(f"  {icon_text}  {text}")
        self.setCheckable(True)
        self.setStyleSheet(Styles.sidebar_button())


class SmashMetricsUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.funcionalidades = Funcionalidades()
        self.google_authenticator = GoogleAuthenticator()
        self.image_processor = ImageProcessor(self)
        self.calibration_manager = CalibrationManager(self, self.image_processor)
        self.analysis_engine = AnalysisEngine(self, self.image_processor)
        self.funcionalidades.analysis_engine = self.analysis_engine

        self.db_manager = DatabaseManager()

        self.setWindowTitle("SmashMetrics - Análise Forense de Colisões")
        self.setGeometry(100, 100, 1400, 900)

        self.original_image = None
        self.processed_image = None
        self.scale_factor = None
        self.selected_stiffness = None

        self.setup_ui()
        self.apply_global_styles()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.create_sidebar(main_layout)

        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget, 1)

        self.setup_screens()

    def create_sidebar(self, main_layout):
        sidebar = QWidget()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet(Styles.sidebar())

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(5)

        logo_label = QLabel("SmashMetrics")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Typography.SIZE_LARGE};
                font-weight: {Typography.WEIGHT_BOLD};
                color: {Colors.CYAN_PRIMARY};
                padding: 20px 0;
                margin-bottom: 20px;
                background-color: transparent;
            }}
        """)
        sidebar_layout.addWidget(logo_label)

        self.nav_buttons = []

        buttons_data = [
            ("Início", self.show_dashboard),
            ("Análise", self.show_analysis),
            ("Seguradoras", self.show_seguradoras),
            ("Gerenciar Análises", self.show_analises),
            ("Relatório", self.show_report),
            ("Sobre", self.show_about),
        ]

        for text, handler in buttons_data:
            btn = SidebarButton(text)
            btn.clicked.connect(handler)
            self.nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        exit_btn = SidebarButton("Sair", Icons.EXIT)
        exit_btn.clicked.connect(self.handle_exit_and_logout)
        sidebar_layout.addWidget(exit_btn)

        main_layout.addWidget(sidebar)

    def handle_exit_and_logout(self):
        self.close()
        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)

    def closeEvent(self, event):

        if hasattr(self, "google_authenticator"):
            self.google_authenticator.logout(self)
        event.accept()

    def setup_screens(self):
        self.dashboard_widget = self.create_dashboard_screen()
        self.stacked_widget.addWidget(self.dashboard_widget)

        self.analysis_widget = self.create_analysis_screen()
        self.stacked_widget.addWidget(self.analysis_widget)

        self.report_widget = self.create_report_screen()
        self.stacked_widget.addWidget(self.report_widget)

        self.about_widget = self.create_about_screen()
        self.stacked_widget.addWidget(self.about_widget)

        self.seguradoras_widget = SeguradorasCRUDScreen(self, self.db_manager)
        self.stacked_widget.addWidget(self.seguradoras_widget)

        self.analises_widget = AnaliseCRUDScreen(self, self.db_manager)
        self.stacked_widget.addWidget(self.analises_widget)

    def show_dashboard(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_widget)
        self._update_nav(0)

    def show_analysis(self):
        self.stacked_widget.setCurrentWidget(self.analysis_widget)
        self._update_nav(1)

    def show_report(self):
        self.stacked_widget.setCurrentWidget(self.report_widget)
        self._update_nav(4)

    def show_about(self):
        self.stacked_widget.setCurrentWidget(self.about_widget)
        self._update_nav(5)

    def show_seguradoras(self):
        self.stacked_widget.setCurrentWidget(self.seguradoras_widget)
        self._update_nav(2)

    def show_analises(self):
        self.stacked_widget.setCurrentWidget(self.analises_widget)
        self._update_nav(3)

    def _update_nav(self, active_index):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == active_index)

    def create_dashboard_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        title = QLabel("SmashMetrics")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(Styles.label_title())
        layout.addWidget(title)

        subtitle = QLabel(
            "Sistema de análise forense de colisões veiculares desenvolvido\nno IFCE - Campus Maracanaú"
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(Styles.label_subtitle())
        layout.addWidget(subtitle)

        icon_label = QLabel()
        try:
            icon_pixmap = QPixmap("logo_smashmetrics-removebg-preview.png")
            if not icon_pixmap.isNull():
                icon_pixmap = icon_pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                icon_label.setPixmap(icon_pixmap)
                icon_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(icon_label)
        except:
            pass

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(25)

        nova_analise_card = ModernCard(
            "Nova Análise",
            "Importe uma imagem e inicie o processo de análise forense",
            Icons.LIGHTNING if hasattr(Icons, 'LIGHTNING') else "⚡"
        )
        nova_analise_card.mousePressEvent = lambda e: self.show_analysis()
        cards_layout.addWidget(nova_analise_card)

        relatorios_card = ModernCard(
            "Relatórios",
            "Acesse os relatórios gerados das análises realizadas",
            Icons.REPORT
        )
        relatorios_card.mousePressEvent = lambda e: self.show_report()
        cards_layout.addWidget(relatorios_card)

        sobre_card = ModernCard(
            "Sobre",
            "Saiba mais sobre o sistema e a metodologia utilizada",
            Icons.INFO
        )
        sobre_card.mousePressEvent = lambda e: self.show_about()
        cards_layout.addWidget(sobre_card)

        layout.addLayout(cards_layout)

        iniciar_btn = QPushButton("Iniciar Análise →")
        iniciar_btn.clicked.connect(self.show_analysis)
        iniciar_btn.setStyleSheet(Styles.primary_button())
        layout.addWidget(iniciar_btn, alignment=Qt.AlignCenter)

        layout.addStretch()
        return widget

    def create_report_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        title = QLabel("Relatórios")
        title.setStyleSheet(Styles.label_title())
        layout.addWidget(title)

        report_text = QTextEdit()
        report_text.setReadOnly(True)
        report_text.setText("Conteúdo do relatório será exibido aqui.")
        report_text.setStyleSheet(Styles.input_field())
        layout.addWidget(report_text)

        layout.addStretch()
        return widget

    def create_about_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        title = QLabel("Sobre o SmashMetrics")
        title.setStyleSheet(Styles.label_title())
        layout.addWidget(title)

        about_text = QLabel(
            "<p>O SmashMetrics é um sistema desenvolvido para auxiliar na análise forense de colisões veiculares, "
            "utilizando técnicas de processamento digital de imagens para medir deformações e estimar a velocidade "
            "de impacto.</p>"
            "<p>Desenvolvido no IFCE - Campus Maracanaú.</p>"
            "<p>Versão: 1.0</p>"
        )
        about_text.setWordWrap(True)
        about_text.setStyleSheet(Styles.label_normal())
        layout.addWidget(about_text)

        layout.addStretch()
        return widget

    def create_analysis_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        title = QLabel("Análise de Imagem de Colisão")
        title.setStyleSheet(Styles.label_title())
        layout.addWidget(title)

        image_container = QWidget()
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(400)
        self.image_label.setText("Nenhuma imagem carregada\nClique em 'Importar Imagem' para começar")
        self.image_label.setStyleSheet(Styles.image_placeholder())
        image_container_layout.addWidget(self.image_label)

        self.remove_image_button = QPushButton(Icons.DELETE)
        self.remove_image_button.setFixedSize(30, 30)
        self.remove_image_button.setStyleSheet(Styles.danger_button())
        self.remove_image_button.clicked.connect(self.image_processor.remove_image)
        self.remove_image_button.setVisible(False)
        self.remove_image_button.move(self.image_label.width() - self.remove_image_button.width() - 10, 10)
        self.image_label.installEventFilter(self)

        layout.addWidget(image_container)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setAlignment(Qt.AlignCenter)

        import_btn = QPushButton("📷 Importar")
        import_btn.clicked.connect(self.image_processor.import_image)
        import_btn.setStyleSheet(Styles.primary_button())
        buttons_layout.addWidget(import_btn)

        actions = [
            ("🔄 8-bit", self.image_processor.convert_to_gray),
            ("⚡ Segmentar", self.image_processor.apply_watershed),
            ("🎯 Calibrar", self.calibration_manager.calibrate_image),
        ]

        for text, handler in actions:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            btn.setStyleSheet(Styles.secondary_button())
            buttons_layout.addWidget(btn)

        calc_btn = QPushButton("📊 Calcular")
        calc_btn.clicked.connect(lambda: self.funcionalidades.handle_velocity_calculation(self, self.image_processor))
        calc_btn.setStyleSheet(Styles.primary_button())
        buttons_layout.addWidget(calc_btn)

        layout.addLayout(buttons_layout)

        return widget

    def eventFilter(self, obj, event):
        if obj == self.image_label and event.type() == event.Type.Resize:
            self.remove_image_button.move(self.image_label.width() - self.remove_image_button.width() - 10, 10)
        return super().eventFilter(obj, event)

    def display_image(self, image):
        if len(image.shape) == 2:
            height, width = image.shape
            bytes_per_line = width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        else:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_BGR888)

        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.remove_image_button.setVisible(True)

    def remove_image(self):
        self.original_image = None
        self.processed_image = None
        self.image_label.clear()
        self.image_label.setText("Nenhuma imagem carregada\nClique em 'Importar Imagem' para começar")
        self.remove_image_button.setVisible(False)

    def apply_global_styles(self):
        self.setStyleSheet(Styles.main_window())

    def closeEvent(self, event):

        if hasattr(self, "google_authenticator"):
            self.google_authenticator.logout(self)
        event.accept()


class LoginScreen(QWidget):
    def __init__(self, main_window, google_authenticator):
        super().__init__()
        self.main_window = main_window
        self.google_authenticator = google_authenticator
        self.setWindowTitle("Login - SmashMetrics")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()
        self.apply_global_styles()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        title = QLabel("Bem-vindo ao SmashMetrics")
        title.setStyleSheet(Styles.label_title())
        layout.addWidget(title, alignment=Qt.AlignCenter)

        subtitle = QLabel("Faça login para continuar")
        subtitle.setStyleSheet(Styles.label_subtitle())
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        google_login_btn = QPushButton("Entrar com Google")
        google_login_btn.setStyleSheet(Styles.primary_button())
        google_login_btn.clicked.connect(self.handle_google_login)
        layout.addWidget(google_login_btn, alignment=Qt.AlignCenter)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"color: {Colors.ERROR}; font-size: {Typography.SIZE_NORMAL};")
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        self.setStyleSheet(f"QWidget {{ background-color: {Colors.BG_PRIMARY}; }}")

    def handle_google_login(self):
        if self.google_authenticator.login_google(self):
            self.status_label.setStyleSheet(f"color: {Colors.SUCCESS};")
            self.status_label.setText("Login realizado com sucesso!")
            self.main_window.show()
            self.close()
        else:
            self.status_label.setStyleSheet(f"color: {Colors.ERROR};")
            self.status_label.setText("Falha no login. Tente novamente.")

    def apply_global_styles(self):
        self.setStyleSheet(Styles.main_window())
