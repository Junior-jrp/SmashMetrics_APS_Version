import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from PySide6.QtWidgets import QMessageBox

class GoogleAuthenticator:
    def __init__(self):
        self.SCOPES = ['openid', 'https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile']
        self.TOKEN_FILE = 'token.json'
        self.CREDENTIALS_FILE = 'credentials.json'

    def login_google(self, ui_context):
        creds = None
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.CREDENTIALS_FILE, self.SCOPES)
                    creds = flow.run_local_server(port=0)
                except FileNotFoundError:
                    QMessageBox.critical(ui_context, "Erro de Configuração",
                                         "O arquivo \'credentials.json\' não foi encontrado.\n" \
                                         "Por favor, siga as instruções para configurar as credenciais do Google.")
                    return False
                except Exception as e:
                    QMessageBox.critical(ui_context, "Erro de Autenticação",
                                         f"Ocorreu um erro durante a autenticação: {e}")
                    return False
            with open(self.TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)

        if creds and creds.valid:
            QMessageBox.information(ui_context, "Login Bem-Sucedido", "Login com Google realizado com sucesso!")
            return True
        else:
            QMessageBox.warning(ui_context, "Login Falhou", "Não foi possível fazer login com o Google.")
            return False

    def logout(self, ui_context):
        if os.path.exists(self.TOKEN_FILE):
            os.remove(self.TOKEN_FILE)
            QMessageBox.information(ui_context, "Logout", "Logout realizado com sucesso. As credenciais foram removidas.")
        else:
            QMessageBox.information(ui_context, "Logout", "Nenhuma sessão ativa para fazer logout.")

    def is_logged_in(self):
        creds = None
        if os.path.exists(self.TOKEN_FILE):
            with open(self.TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        return creds is not None and creds.valid
