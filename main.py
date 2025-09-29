import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from core.telas import SmashMetricsUI, LoginScreen
from core.funcionalidades import Funcionalidades
from core.google_auth import GoogleAuthenticator

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon_path = "assets/logos/logo_smashmetrics_removebg_preview_CD6_icon.ico"
    app.setWindowIcon(QIcon(icon_path))

    try:
        with open("assets/styles.css", "r") as f:
            app.setStyleSheet(f.read())
    except FileNotFoundError:
        print("⚠ Arquivo \'styles.css\' não encontrado. O aplicativo usará o estilo padrão.")

    google_authenticator = GoogleAuthenticator()

    main_window = SmashMetricsUI()
    main_window.setWindowIcon(QIcon(icon_path))

    login_screen = LoginScreen(main_window, google_authenticator)

    login_screen.show()

    sys.exit(app.exec())
