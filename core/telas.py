from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QPushButton, QStackedWidget, QTextEdit, QComboBox,
    QInputDialog, QFrame, QScrollArea, QLineEdit, QDateEdit
)
from PySide6.QtGui import QPixmap, QFont, QIcon, QImage
from PySide6.QtCore import Qt, QDate
from core.funcionalidades import Funcionalidades
from core.google_auth import GoogleAuthenticator
from core.image_processor import ImageProcessor
from core.calibration_manager import CalibrationManager
from core.analysis_engine import AnalysisEngine


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
            icon_label.setStyleSheet("""
                QLabel {
                    font-size: 32px;
                    color: #00bcd4;
                    font-weight: bold;
                }
            """)
            layout.addWidget(icon_label)

        if title:
            title_label = QLabel(title)
            title_label.setAlignment(Qt.AlignCenter)
            title_label.setStyleSheet("""
                QLabel {
                    font-size: 18px;
                    font-weight: bold;
                    color: #ffffff;
                    margin: 5px 0;
                    background-color: transparent;
                }
            """)
            layout.addWidget(title_label)

        if description:
            desc_label = QLabel(description)
            desc_label.setAlignment(Qt.AlignCenter)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("""
                QLabel {
                    font-size: 14px;
                    color: #b0b0b0;
                    line-height: 1.4;
                    background-color: transparent;
                }
            """)
            layout.addWidget(desc_label)

        self.setStyleSheet("""
            ModernCard {
                background-color: #3a404a;
                border-radius: 12px;
                border: 1px solid #4a5568;
            }
            ModernCard:hover {
                background-color: #434a56;
                border: 1px solid #00bcd4;
            }
        """)


class SidebarButton(QPushButton):
    def __init__(self, text, icon_text="", parent=None):
        super().__init__(parent)
        self.setText(f"  {icon_text}  {text}")
        self.setCheckable(True)
        self.setup_style()

    def setup_style(self):
        self.setStyleSheet("""
            SidebarButton {
                text-align: left;
                padding: 15px 20px;
                font-size: 14px;
                font-weight: 500;
                color: #b0b0b0;
                background-color: transparent;
                border: none;
                border-radius: 8px;
                margin: 2px 8px;
            }
            SidebarButton:hover {
                background-color: #3a404a;
                color: #ffffff;
            }
            SidebarButton:checked {
                background-color: #00bcd4;
                color: #ffffff;
                font-weight: bold;
            }
        """)


class SmashMetricsUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.funcionalidades = Funcionalidades()
        self.google_authenticator = GoogleAuthenticator()
        self.image_processor = ImageProcessor(self)
        self.calibration_manager = CalibrationManager(self, self.image_processor)
        self.analysis_engine = AnalysisEngine(self, self.image_processor)
        self.funcionalidades.analysis_engine = self.analysis_engine

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
        sidebar.setStyleSheet("""
            QWidget {
                background-color: #1e2328;
                border-right: 1px solid #4a5568;
            }
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 20, 0, 20)
        sidebar_layout.setSpacing(5)

        logo_label = QLabel("SmashMetrics")
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: #00bcd4;
                padding: 20px 0;
                margin-bottom: 20px;
            }
        """)
        sidebar_layout.addWidget(logo_label)

        self.nav_buttons = []

        buttons_data = [
            ("📊", "Início", self.show_dashboard),
            ("📈", "Análise", self.show_analysis),
            ("📋", "Relatório", self.show_report),
            ("⚙️", "Sobre", self.show_about),
        ]

        for icon, text, handler in buttons_data:
            btn = SidebarButton(text, icon)
            btn.clicked.connect(handler)
            self.nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        exit_btn = SidebarButton("Sair", "🚪")
        exit_btn.clicked.connect(self.handle_exit_and_logout)
        sidebar_layout.addWidget(exit_btn)

        main_layout.addWidget(sidebar)

    def handle_exit_and_logout(self):
        self.google_authenticator.logout(self)

        self.close()

        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)

    def setup_screens(self):
        self.dashboard_widget = self.create_dashboard_screen()
        self.stacked_widget.addWidget(self.dashboard_widget)

        self.analysis_widget = self.create_analysis_screen()
        self.stacked_widget.addWidget(self.analysis_widget)

        self.report_widget = self.create_report_screen()
        self.stacked_widget.addWidget(self.report_widget)

        self.about_widget = self.create_about_screen()
        self.stacked_widget.addWidget(self.about_widget)

    def show_dashboard(self):
        self.stacked_widget.setCurrentWidget(self.dashboard_widget)
        for btn in self.nav_buttons:
            btn.setChecked(False)
        self.nav_buttons[0].setChecked(True)

    def show_analysis(self):
        self.stacked_widget.setCurrentWidget(self.analysis_widget)
        for btn in self.nav_buttons:
            btn.setChecked(False)
        self.nav_buttons[1].setChecked(True)

    def show_report(self):
        self.stacked_widget.setCurrentWidget(self.report_widget)
        for btn in self.nav_buttons:
            btn.setChecked(False)
        self.nav_buttons[2].setChecked(True)

    def show_about(self):
        self.stacked_widget.setCurrentWidget(self.about_widget)
        for btn in self.nav_buttons:
            btn.setChecked(False)
        self.nav_buttons[3].setChecked(True)


    def create_dashboard_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(30)

        title = QLabel("SmashMetrics")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 48px;
                font-weight: bold;
                color: #00bcd4;
                margin-bottom: 10px;
            }
        """)
        layout.addWidget(title)

        subtitle = QLabel(
            "Sistema de análise forense de colisões veiculares desenvolvido\nno IFCE - Campus Maracanaú"
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #b0b0b0;
                margin-bottom: 30px;
                line-height: 1.5;
            }
        """)
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
            "⚡"
        )
        nova_analise_card.mousePressEvent = lambda e: self.show_analysis()
        cards_layout.addWidget(nova_analise_card)

        relatorios_card = ModernCard(
            "Relatórios",
            "Acesse os relatórios gerados das análises realizadas",
            "📋"
        )
        relatorios_card.mousePressEvent = lambda e: self.show_report()
        cards_layout.addWidget(relatorios_card)

        sobre_card = ModernCard(
            "Sobre",
            "Saiba mais sobre o sistema e a metodologia utilizada",
            "ℹ️"
        )
        sobre_card.mousePressEvent = lambda e: self.show_about()
        cards_layout.addWidget(sobre_card)

        layout.addLayout(cards_layout)

        iniciar_btn = QPushButton("Iniciar Análise →")
        iniciar_btn.clicked.connect(self.show_analysis)
        iniciar_btn.setStyleSheet("""
            QPushButton {
                background-color: #00bcd4;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #00acc1;
            }
            QPushButton:pressed {
                background-color: #0097a7;
            }
        """)
        layout.addWidget(iniciar_btn, alignment=Qt.AlignCenter)

        layout.addStretch()
        return widget

    def create_report_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        title = QLabel("Relatórios")
        title.setStyleSheet("""
              QLabel {
                  font-size: 32px;
                  font-weight: bold;
                  color: #ffffff;
                  margin-bottom: 20px;
              }
          """)
        layout.addWidget(title)

        report_text = QTextEdit()
        report_text.setReadOnly(True)
        report_text.setText("Conteúdo do relatório será exibido aqui.")
        report_text.setStyleSheet("""
              QTextEdit {
                  background-color: #3a404a;
                  border: 1px solid #4a5568;
                  border-radius: 8px;
                  color: #ffffff;
                  font-size: 14px;
                  padding: 10px;
              }
          """)
        layout.addWidget(report_text)

        layout.addStretch()
        return widget

    def create_about_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        title = QLabel("Sobre o SmashMetrics")
        title.setStyleSheet("""
              QLabel {
                  font-size: 32px;
                  font-weight: bold;
                  color: #ffffff;
                  margin-bottom: 20px;
              }
          """)
        layout.addWidget(title)

        about_text = QLabel(
            "<p>O SmashMetrics é um sistema desenvolvido para auxiliar na análise forense de colisões veiculares, "
            "utilizando técnicas de processamento digital de imagens para medir deformações e estimar a velocidade "
            "de impacto.</p>"
            "<p>Desenvolvido no IFCE - Campus Maracanaú.</p>"
            "<p>Versão: 1.0</p>"
        )
        about_text.setWordWrap(True)
        about_text.setStyleSheet("""
              QLabel {
                  font-size: 14px;
                  color: #b0b0b0;
                  line-height: 1.5;
              }
          """)
        layout.addWidget(about_text)

        layout.addStretch()
        return widget

    def create_analysis_screen(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        title = QLabel("Análise de Imagem de Colisão")
        title.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: #ffffff;
                margin-bottom: 20px;
            }
        """)
        layout.addWidget(title)

        image_container = QWidget()
        image_container_layout = QVBoxLayout(image_container)
        image_container_layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumHeight(400)
        self.image_label.setText("Nenhuma imagem carregada\nClique em \'Importar Imagem\' para começar")
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #3a404a;
                border: 2px dashed #00bcd4;
                border-radius: 12px;
                color: #b0b0b0;
                font-size: 16px;
                padding: 20px;
            }
        """)
        image_container_layout.addWidget(self.image_label)

        self.remove_image_button = QPushButton("X")
        self.remove_image_button.setFixedSize(30, 30)
        self.remove_image_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #c0392b;
            }
        """)
        self.remove_image_button.clicked.connect(self.image_processor.remove_image)
        self.remove_image_button.setVisible(False)

        self.remove_image_button.move(self.image_label.width() - self.remove_image_button.width() - 10,
                                       10)
        self.image_label.installEventFilter(self)

        layout.addWidget(image_container)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setAlignment(Qt.AlignCenter)

        button_style = """
            QPushButton {
                background-color: #3a404a;
                color: #ffffff;
                border: 1px solid #4a5568;
                border-radius: 8px;
                padding: 8px 15px;
                font-size: 12px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #434a56;
                border-color: #00bcd4;
            }
            QPushButton:pressed {
                background-color: #2d3339;
            }
        """

        import_btn = QPushButton("📷 Importar")
        import_btn.clicked.connect(self.image_processor.import_image)
        import_btn.setStyleSheet(button_style.replace("background-color: #3a404a;", "background-color: #00bcd4;"))
        buttons_layout.addWidget(import_btn)

        buttons_data = [
            ("🔄", "8-bit", self.image_processor.convert_to_gray),
            ("⚡", "Segmentar", self.image_processor.apply_watershed),
            ("🎯", "Calibrar", self.calibration_manager.calibrate_image),
        ]

        for icon, text, handler in buttons_data:
            btn = QPushButton(f"{icon} {text}")
            btn.clicked.connect(lambda _, h=handler: h())
            btn.setStyleSheet(button_style)
            buttons_layout.addWidget(btn)

        calc_btn = QPushButton("📊 Calcular")
        calc_btn.clicked.connect(lambda: self.funcionalidades.handle_velocity_calculation(self, self.image_processor))
        calc_btn.setStyleSheet(button_style.replace("background-color: #3a404a;", "background-color: #00bcd4;"))
        buttons_layout.addWidget(calc_btn)

        layout.addLayout(buttons_layout)

        return widget

    def eventFilter(self, obj, event):
        if obj == self.image_label and event.type() == event.Type.Resize:
            self.remove_image_button.move(self.image_label.width() - self.remove_image_button.width() - 10,
                                           10)
        return super().eventFilter(obj, event)

    def display_image(self, image):
        if len(image.shape) == 2:
            height, width = image.shape
            bytes_per_line = width
            q_image = QImage(image.data, width, height,
                             bytes_per_line, QImage.Format_Grayscale8)
        else:
            height, width, channel = image.shape
            bytes_per_line = 3 * width
            q_image = QImage(image.data, width, height,
                             bytes_per_line, QImage.Format_BGR888)

        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(
            pixmap.scaled(self.image_label.size(),
                          Qt.KeepAspectRatio,
                          Qt.SmoothTransformation)
        )
        self.remove_image_button.setVisible(True)

    def remove_image(self):
        self.original_image = None
        self.processed_image = None
        self.image_label.clear()
        self.image_label.setText("Nenhuma imagem carregada\nClique em \'Importar Imagem\' para começar")
        self.remove_image_button.setVisible(False)

    def apply_global_styles(self):
        try:
            with open("assets/styles.css", "r") as f:
                self.setStyleSheet(self.styleSheet() + f.read())
        except FileNotFoundError:
            print("⚠ Arquivo \'styles.css\' não encontrado. O aplicativo usará o estilo padrão.")


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
        title.setStyleSheet("""
            QLabel {
                font-size: 36px;
                font-weight: bold;
                color: #00bcd4;
            }
        """)
        layout.addWidget(title, alignment=Qt.AlignCenter)

        subtitle = QLabel("Faça login para continuar")
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 18px;
                color: #b0b0b0;
            }
        """)
        layout.addWidget(subtitle, alignment=Qt.AlignCenter)

        google_login_btn = QPushButton("Entrar com Google")
        google_login_btn.setStyleSheet("""
            QPushButton {
                background-color: #4285F4;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #357ae8;
            }
            QPushButton:pressed {
                background-color: #2d67cb;
            }
        """)
        google_login_btn.clicked.connect(self.handle_google_login)
        layout.addWidget(google_login_btn, alignment=Qt.AlignCenter)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            QLabel {
                color: red;
                font-size: 14px;
            }
        """)
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        self.setStyleSheet("""
            QWidget {
                background-color: #282c34;
            }
        """)

    def handle_google_login(self):
        if self.google_authenticator.login_google(self):
            self.status_label.setStyleSheet("color: green;")
            self.status_label.setText("Login realizado com sucesso!")
            self.main_window.show()
            self.close()
        else:
            self.status_label.setStyleSheet("color: red;")
            self.status_label.setText("Falha no login. Tente novamente.")


    def apply_global_styles(self):
        try:
            with open("assets/styles.css", "r") as f:
                self.setStyleSheet(self.styleSheet() + f.read())
        except FileNotFoundError:
            print("⚠ Arquivo \'styles.css\' não encontrado. O aplicativo usará o estilo padrão.")


