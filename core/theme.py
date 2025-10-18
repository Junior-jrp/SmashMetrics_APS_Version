"""
Sistema de Design Unificado - SmashMetrics
Define todas as cores, estilos e componentes visuais
"""


class Colors:
    # Backgrounds
    BG_PRIMARY = "#1a1d23"
    BG_SECONDARY = "#252933"
    BG_TERTIARY = "#2d3139"
    BG_CARD = "#2d3139"
    BG_HOVER = "#353b47"

    # Ciano (cor principal)
    CYAN_PRIMARY = "#00d9ff"
    CYAN_HOVER = "#00b8d4"
    CYAN_PRESSED = "#0097a7"
    CYAN_DISABLED = "#004d5a"

    # Textos
    TEXT_PRIMARY = "#e8eaed"
    TEXT_SECONDARY = "#a0a4a8"
    TEXT_DISABLED = "#5a5f6a"
    TEXT_ON_CYAN = "#ffffff"

    # Bordas
    BORDER_DEFAULT = "#3a3f4a"
    BORDER_FOCUS = "#00d9ff"
    BORDER_ERROR = "#ff5252"

    # Estados
    SUCCESS = "#00e676"
    ERROR = "#ff5252"
    WARNING = "#ffd740"
    INFO = "#00d9ff"

    # Sombras
    SHADOW_LIGHT = "rgba(0, 0, 0, 0.1)"
    SHADOW_MEDIUM = "rgba(0, 0, 0, 0.2)"
    SHADOW_HEAVY = "rgba(0, 0, 0, 0.4)"


class Typography:
    FONT_FAMILY = "'Segoe UI', 'Inter', 'Roboto', sans-serif"

    # Tamanhos
    SIZE_XLARGE = "32px"
    SIZE_LARGE = "24px"
    SIZE_MEDIUM = "18px"
    SIZE_NORMAL = "14px"
    SIZE_SMALL = "12px"

    # Pesos
    WEIGHT_BOLD = "bold"
    WEIGHT_SEMIBOLD = "600"
    WEIGHT_MEDIUM = "500"
    WEIGHT_REGULAR = "400"


class Spacing:
    XS = "4px"
    SM = "8px"
    MD = "16px"
    LG = "24px"
    XL = "32px"
    XXL = "48px"


class BorderRadius:
    SMALL = "4px"
    MEDIUM = "8px"
    LARGE = "12px"
    XLARGE = "16px"
    ROUND = "50%"


class Styles:
    """Estilos prontos para componentes Qt"""

    @staticmethod
    def main_window():
        return f"""
            QMainWindow {{
                background-color: {Colors.BG_PRIMARY};
                color: {Colors.TEXT_PRIMARY};
                font-family: {Typography.FONT_FAMILY};
            }}
        """

    @staticmethod
    def sidebar():
        return f"""
            QWidget {{
                background-color: {Colors.BG_SECONDARY};
                border-right: 1px solid {Colors.BORDER_DEFAULT};
            }}
        """

    @staticmethod
    def scrollarea():
        return f"""
                QScrollArea {{
                    background-color: transparent;
                    border: none;
                }}
                QScrollArea > QWidget > QWidget {{
                    background-color: transparent;
                }}
                QScrollBar:vertical {{
                    background-color: {Colors.BG_SECONDARY};
                    width: 12px;
                    border-radius: 6px;
                }}
                QScrollBar::handle:vertical {{
                    background-color: {Colors.BORDER_DEFAULT};
                    border-radius: 6px;
                    min-height: 20px;
                }}
                QScrollBar::handle:vertical:hover {{
                    background-color: {Colors.CYAN_PRIMARY};
                }}
                QScrollBar::add-line:vertical, 
                QScrollBar::sub-line:vertical {{
                    height: 0px;
                }}
            """

    @staticmethod
    def sidebar_button():
        return f"""
            QPushButton {{
                text-align: left;
                padding: 12px 20px;
                font-size: {Typography.SIZE_NORMAL};
                font-weight: {Typography.WEIGHT_MEDIUM};
                color: {Colors.TEXT_SECONDARY};
                background-color: transparent;
                border: none;
                border-radius: {BorderRadius.MEDIUM};
                margin: 2px 8px;
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_HOVER};
                color: {Colors.TEXT_PRIMARY};
            }}
            QPushButton:checked {{
                background-color: {Colors.CYAN_PRIMARY};
                color: {Colors.TEXT_ON_CYAN};
                font-weight: {Typography.WEIGHT_BOLD};
            }}
            QPushButton:disabled {{
                color: {Colors.TEXT_DISABLED};
            }}
        """

    @staticmethod
    def primary_button():
        return f"""
            QPushButton {{
                background-color: {Colors.CYAN_PRIMARY};
                color: {Colors.TEXT_ON_CYAN};
                border: none;
                padding: 12px 24px;
                border-radius: {BorderRadius.MEDIUM};
                font-size: {Typography.SIZE_NORMAL};
                font-weight: {Typography.WEIGHT_SEMIBOLD};
            }}
            QPushButton:hover {{
                background-color: {Colors.CYAN_HOVER};
            }}
            QPushButton:pressed {{
                background-color: {Colors.CYAN_PRESSED};
            }}
            QPushButton:disabled {{
                background-color: {Colors.CYAN_DISABLED};
                color: {Colors.TEXT_DISABLED};
            }}
        """

    @staticmethod
    def secondary_button():
        return f"""
            QPushButton {{
                background-color: {Colors.BG_CARD};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_DEFAULT};
                padding: 10px 20px;
                border-radius: {BorderRadius.MEDIUM};
                font-size: {Typography.SIZE_NORMAL};
                font-weight: {Typography.WEIGHT_MEDIUM};
            }}
            QPushButton:hover {{
                background-color: {Colors.BG_HOVER};
                border-color: {Colors.CYAN_PRIMARY};
            }}
            QPushButton:pressed {{
                background-color: {Colors.BG_SECONDARY};
            }}
            QPushButton:disabled {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_DISABLED};
                border-color: {Colors.BORDER_DEFAULT};
            }}
        """

    @staticmethod
    def danger_button():
        return f"""
            QPushButton {{
                background-color: {Colors.ERROR};
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: {BorderRadius.MEDIUM};
                font-size: {Typography.SIZE_NORMAL};
                font-weight: {Typography.WEIGHT_SEMIBOLD};
            }}
            QPushButton:hover {{
                background-color: #e64545;
            }}
            QPushButton:pressed {{
                background-color: #d32f2f;
            }}
        """

    @staticmethod
    def card():
        return f"""
            QFrame {{
                background-color: {Colors.BG_CARD};
                border-radius: {BorderRadius.LARGE};
                border: 1px solid {Colors.BORDER_DEFAULT};
            }}
            QFrame:hover {{
                border-color: {Colors.CYAN_PRIMARY};
                background-color: {Colors.BG_HOVER};
            }}
        """

    @staticmethod
    def input_field():
        return f"""
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
                background-color: {Colors.BG_TERTIARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_DEFAULT};
                border-radius: {BorderRadius.MEDIUM};
                padding: 10px;
                font-size: {Typography.SIZE_NORMAL};
                selection-background-color: {Colors.CYAN_PRIMARY};
            }}
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, 
            QDoubleSpinBox:focus, QComboBox:focus {{
                border: 2px solid {Colors.CYAN_PRIMARY};
                background-color: {Colors.BG_SECONDARY};
            }}
            QLineEdit:disabled, QTextEdit:disabled, QSpinBox:disabled,
            QDoubleSpinBox:disabled, QComboBox:disabled {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_DISABLED};
                border-color: {Colors.BORDER_DEFAULT};
            }}
        """

    @staticmethod
    def table():
        return f"""
            QTableWidget {{
                background-color: {Colors.BG_CARD};
                border: 1px solid {Colors.BORDER_DEFAULT};
                border-radius: {BorderRadius.MEDIUM};
                color: {Colors.TEXT_PRIMARY};
                gridline-color: {Colors.BORDER_DEFAULT};
                font-size: {Typography.SIZE_NORMAL};
            }}
            QTableWidget::item {{
                padding: 8px;
                border: none;
            }}
            QTableWidget::item:selected {{
                background-color: {Colors.CYAN_PRIMARY};
                color: {Colors.TEXT_ON_CYAN};
            }}
            QTableWidget::item:hover {{
                background-color: {Colors.BG_HOVER};
            }}
            QHeaderView::section {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                padding: 12px;
                border: none;
                border-bottom: 2px solid {Colors.CYAN_PRIMARY};
                font-weight: {Typography.WEIGHT_SEMIBOLD};
                font-size: {Typography.SIZE_NORMAL};
            }}
            QScrollBar:vertical {{
                background-color: {Colors.BG_SECONDARY};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {Colors.BORDER_DEFAULT};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {Colors.CYAN_PRIMARY};
            }}
        """

    @staticmethod
    def label_title():
        return f"""
            QLabel {{
                font-size: {Typography.SIZE_XLARGE};
                font-weight: {Typography.WEIGHT_BOLD};
                color: {Colors.TEXT_PRIMARY};
                background-color: transparent;
            }}
        """

    @staticmethod
    def label_subtitle():
        return f"""
            QLabel {{
                font-size: {Typography.SIZE_MEDIUM};
                font-weight: {Typography.WEIGHT_MEDIUM};
                color: {Colors.TEXT_SECONDARY};
                background-color: transparent;
            }}
        """

    @staticmethod
    def label_normal():
        return f"""
            QLabel {{
                font-size: {Typography.SIZE_NORMAL};
                color: {Colors.TEXT_PRIMARY};
                background-color: transparent;
            }}
        """

    @staticmethod
    def dialog():
        return f"""
            QDialog {{
                background-color: {Colors.BG_PRIMARY};
            }}
            QLabel {{
                color: {Colors.TEXT_PRIMARY};
                font-size: {Typography.SIZE_NORMAL};
            }}
            QDialogButtonBox {{
                dialogbuttonbox-buttons-have-icons: 0;
            }}
        """

    @staticmethod
    @staticmethod
    def dialog():
        # >>> substitua seu método dialog() por este, para cobrir o fundo do QDialog e filhos
        return f"""
               QDialog {{
                   background-color: {Colors.BG_PRIMARY};
                   color: {Colors.TEXT_PRIMARY};
                   font-family: {Typography.FONT_FAMILY};
               }}
               QLabel {{
                   color: {Colors.TEXT_PRIMARY};
                   font-size: {Typography.SIZE_NORMAL};
                   background-color: transparent;
               }}
               QDialogButtonBox {{
                   dialogbuttonbox-buttons-have-icons: 0;
               }}
           """

    @staticmethod
    def combo_popup():
        return f"""
            QComboBox QAbstractItemView {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER_FOCUS};
                color: {Colors.TEXT_PRIMARY};
                selection-background-color: {Colors.CYAN_PRIMARY};
                selection-color: {Colors.TEXT_ON_CYAN};
            }}
        """

    @staticmethod
    def calendar():
        return f"""
            QCalendarWidget {{
                background-color: {Colors.BG_CARD};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER_DEFAULT};
                border-radius: {BorderRadius.MEDIUM};
            }}
            QCalendarWidget QAbstractItemView:enabled {{
                selection-background-color: {Colors.CYAN_PRIMARY};
                selection-color: {Colors.TEXT_ON_CYAN};
            }}
        """

    @staticmethod
    def scrollarea():
        from .theme import Colors, BorderRadius  # se estiver no mesmo arquivo, remova esta linha
        return f"""
                QScrollArea {{
                    background-color: transparent;
                    border: none;
                }}
                QScrollArea > QWidget > QWidget {{
                    background-color: transparent;
                }}
                QScrollBar:vertical {{
                    background-color: {Colors.BG_SECONDARY};
                    width: 12px;
                    border-radius: 6px;
                }}
                QScrollBar::handle:vertical {{
                    background-color: {Colors.BORDER_DEFAULT};
                    border-radius: 6px;
                    min-height: 20px;
                }}
                QScrollBar::handle:vertical:hover {{
                    background-color: {Colors.CYAN_PRIMARY};
                }}
                QScrollBar::add-line:vertical, 
                QScrollBar::sub-line:vertical {{
                    height: 0px;
                }}
            """

    @staticmethod
    def form_label():
        return f"""
               QLabel {{
                   color: {Colors.TEXT_SECONDARY};
                   font-size: {Typography.SIZE_NORMAL};
               }}
           """

    @staticmethod
    def form_card():
        return f"""
            QWidget#FormCard {{
                background-color: {Colors.BG_CARD};
                border-radius: {BorderRadius.LARGE};
                border: 1px solid {Colors.BORDER_DEFAULT};
            }}
        """

    @staticmethod
    def image_placeholder():
        return f"""
            QLabel {{
                background-color: {Colors.BG_CARD};
                border: 2px dashed {Colors.CYAN_PRIMARY};
                border-radius: {BorderRadius.LARGE};
                color: {Colors.TEXT_SECONDARY};
                font-size: {Typography.SIZE_MEDIUM};
                padding: 40px;
            }}
        """


class Icons:
    """Ícones SVG ou Unicode para uso na interface"""

    # Navegação
    HOME = "🏠"
    ANALYSIS = "📊"
    INSURANCE = "🏢"
    REPORT = "📋"
    SETTINGS = "⚙️"
    EXIT = "🚪"

    # Ações
    ADD = "➕"
    EDIT = "✏️"
    DELETE = "🗑️"
    SAVE = "💾"
    CANCEL = "❌"
    SEARCH = "🔍"
    FILTER = "🔽"

    # Status
    SUCCESS = "✓"
    ERROR = "✗"
    WARNING = "⚠"
    INFO = "ℹ"

    # Ferramentas
    IMPORT = "📥"
    EXPORT = "📤"
    CAMERA = "📷"
    CALIBRATE = "🎯"
    CALCULATE = "🧮"

    @staticmethod
    def get_svg_icon(name, color=Colors.TEXT_PRIMARY, size=24):
        """Retorna código SVG para ícones personalizados"""
        # Aqui você pode adicionar ícones SVG customizados se quiser
        pass