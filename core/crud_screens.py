"""
Telas de CRUD para Seguradoras e Análises
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QTextEdit,
    QDialog, QFormLayout, QDateEdit, QComboBox,
    QMessageBox, QHeaderView, QDialogButtonBox, QScrollArea,
    QFrame, QSizePolicy, QSpacerItem
)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QFont
from core.database import DatabaseManager, SeguradoraCRUD, AnaliseCRUD
from core.theme import Styles, Colors, Typography, BorderRadius


# ==================== DIÁLOGOS ====================

class SeguradoraDialog(QDialog):
    """Diálogo para criar/editar seguradora"""

    def __init__(self, parent=None, seguradora_data=None, db_manager=None):
        super().__init__(parent)
        self.seguradora_data = seguradora_data
        self.db_manager = db_manager
        self.setWindowTitle("Nova Seguradora" if not seguradora_data else "Editar Seguradora")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)
        self.setup_ui()

        if seguradora_data:
            self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel("Nova Seguradora" if not self.seguradora_data else "Editar Seguradora")
        title.setStyleSheet(Styles.label_title())
        layout.addWidget(title)

        # Scroll area para o formulário
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(Styles.scrollarea())

        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # Campos do formulário
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Ex: Porto Seguro")
        form_layout.addRow("Nome:*", self.nome_input)

        self.cnpj_input = QLineEdit()
        self.cnpj_input.setPlaceholderText("00.000.000/0000-00")
        self.cnpj_input.setMaxLength(18)
        form_layout.addRow("CNPJ:", self.cnpj_input)

        self.telefone_input = QLineEdit()
        self.telefone_input.setPlaceholderText("(85) 99999-9999")
        self.telefone_input.setMaxLength(20)
        form_layout.addRow("Telefone:", self.telefone_input)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("contato@seguradora.com.br")
        form_layout.addRow("Email:", self.email_input)

        self.endereco_input = QTextEdit()
        self.endereco_input.setMaximumHeight(80)
        self.endereco_input.setPlaceholderText("Endereço completo da seguradora")
        form_layout.addRow("Endereço:", self.endereco_input)

        self.contato_input = QLineEdit()
        self.contato_input.setPlaceholderText("Nome do responsável")
        form_layout.addRow("Contato Responsável:", self.contato_input)

        self.observacoes_input = QTextEdit()
        self.observacoes_input.setMaximumHeight(100)
        self.observacoes_input.setPlaceholderText("Observações adicionais sobre a seguradora")
        form_layout.addRow("Observações:", self.observacoes_input)

        scroll.setWidget(form_widget)
        layout.addWidget(scroll)

        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet(Styles.secondary_button())
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Salvar")
        save_btn.setStyleSheet(Styles.primary_button())
        save_btn.clicked.connect(self.validate_and_accept)
        buttons_layout.addWidget(save_btn)

        layout.addLayout(buttons_layout)

        # Aplicar estilos
        self.setStyleSheet(Styles.dialog() + Styles.input_field())

    def load_data(self):
        """Carrega dados da seguradora para edição"""
        self.nome_input.setText(self.seguradora_data.get('nome', ''))
        self.cnpj_input.setText(self.seguradora_data.get('cnpj', '') or '')
        self.telefone_input.setText(self.seguradora_data.get('telefone', '') or '')
        self.email_input.setText(self.seguradora_data.get('email', '') or '')
        self.endereco_input.setText(self.seguradora_data.get('endereco', '') or '')
        self.contato_input.setText(self.seguradora_data.get('contato_responsavel', '') or '')
        self.observacoes_input.setText(self.seguradora_data.get('observacoes', '') or '')

    def validate_and_accept(self):
        """Valida os dados antes de aceitar"""
        if not self.nome_input.text().strip():
            QMessageBox.warning(self, "Erro", "O campo Nome é obrigatório!")
            self.nome_input.setFocus()
            return

        # Validação básica de CNPJ (se preenchido)
        cnpj = self.cnpj_input.text().strip()
        if cnpj and len(cnpj.replace('.', '').replace('/', '').replace('-', '')) != 14:
            QMessageBox.warning(self, "Erro", "CNPJ inválido! Use o formato: 00.000.000/0000-00")
            self.cnpj_input.setFocus()
            return

        # Validação básica de email (se preenchido)
        email = self.email_input.text().strip()
        if email and '@' not in email:
            QMessageBox.warning(self, "Erro", "Email inválido!")
            self.email_input.setFocus()
            return

        self.accept()

    def get_data(self):
        """Retorna os dados do formulário"""
        return {
            'nome': self.nome_input.text().strip(),
            'cnpj': self.cnpj_input.text().strip() or None,
            'telefone': self.telefone_input.text().strip() or None,
            'email': self.email_input.text().strip() or None,
            'endereco': self.endereco_input.toPlainText().strip() or None,
            'contato_responsavel': self.contato_input.text().strip() or None,
            'observacoes': self.observacoes_input.toPlainText().strip() or None
        }


class AnaliseDialog(QDialog):
    """Diálogo para criar/editar análise"""

    def __init__(self, parent=None, analise_data=None, db_manager=None):
        super().__init__(parent)
        self.analise_data = analise_data
        self.db_manager = db_manager
        self.setWindowTitle("Nova Análise" if not analise_data else "Editar Análise")
        self.setMinimumWidth(700)
        self.setMinimumHeight(600)
        self.setup_ui()

        if analise_data:
            self.load_data()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        title = QLabel("Nova Análise" if not self.analise_data else "Editar Análise")
        title.setStyleSheet(Styles.label_title())
        layout.addWidget(title)

        # Scroll area para o formulário
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet(Styles.scrollarea())

        form_widget = QWidget()
        form_layout = QFormLayout(form_widget)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(0, 0, 0, 0)

        # === DADOS DO SINISTRO ===
        sinistro_label = QLabel("Dados do Sinistro")
        sinistro_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Typography.SIZE_MEDIUM};
                font-weight: {Typography.WEIGHT_BOLD};
                color: {Colors.CYAN_PRIMARY};
                margin-top: 10px;
                margin-bottom: 5px;
            }}
        """)
        form_layout.addRow(sinistro_label)

        self.titulo_input = QLineEdit()
        self.titulo_input.setPlaceholderText("Ex: Colisão Frontal - Av. Principal")
        form_layout.addRow("Título:*", self.titulo_input)

        # Carregar seguradoras
        self.seguradora_combo = QComboBox()
        self.seguradora_combo.addItem("Nenhuma seguradora", None)
        if self.db_manager:
            seguradora_crud = SeguradoraCRUD(self.db_manager)
            seguradoras = seguradora_crud.read_all(apenas_ativas=True)
            for seg in seguradoras:
                self.seguradora_combo.addItem(seg['nome'], seg['id'])
        form_layout.addRow("Seguradora:", self.seguradora_combo)

        self.numero_sinistro_input = QLineEdit()
        self.numero_sinistro_input.setPlaceholderText("Número do sinistro/processo")
        form_layout.addRow("Nº Sinistro:", self.numero_sinistro_input)

        self.data_acidente_input = QDateEdit()
        self.data_acidente_input.setCalendarPopup(True)
        self.data_acidente_input.setDate(QDate.currentDate())
        self.data_acidente_input.setDisplayFormat("dd/MM/yyyy")
        form_layout.addRow("Data do Acidente:", self.data_acidente_input)

        self.segurado_input = QLineEdit()
        self.segurado_input.setPlaceholderText("Nome do segurado/envolvido")
        form_layout.addRow("Segurado:", self.segurado_input)

        self.apolice_input = QLineEdit()
        self.apolice_input.setPlaceholderText("Número da apólice")
        form_layout.addRow("Nº Apólice:", self.apolice_input)

        # === DADOS DA COLISÃO ===
        colisao_label = QLabel("Dados da Colisão")
        colisao_label.setStyleSheet(f"""
            QLabel {{
                font-size: {Typography.SIZE_MEDIUM};
                font-weight: {Typography.WEIGHT_BOLD};
                color: {Colors.CYAN_PRIMARY};
                margin-top: 20px;
                margin-bottom: 5px;
            }}
        """)
        form_layout.addRow(colisao_label)

        self.local_input = QLineEdit()
        self.local_input.setPlaceholderText("Ex: Av. Bezerra de Menezes, 1000")
        form_layout.addRow("Local:", self.local_input)

        self.tipo_combo = QComboBox()
        self.tipo_combo.addItems([
            "Não especificado", "Frontal", "Traseira", "Lateral",
            "Capotamento", "Atropelamento", "Choque com objeto fixo", "Outro"
        ])
        form_layout.addRow("Tipo:", self.tipo_combo)

        self.status_combo = QComboBox()
        self.status_combo.addItems([
            "Em andamento", "Concluída", "Arquivada", "Cancelada"
        ])
        form_layout.addRow("Status:", self.status_combo)

        self.observacoes_input = QTextEdit()
        self.observacoes_input.setMaximumHeight(120)
        self.observacoes_input.setPlaceholderText("Observações sobre a análise")
        form_layout.addRow("Observações:", self.observacoes_input)

        scroll.setWidget(form_widget)
        layout.addWidget(scroll)

        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet(Styles.secondary_button())
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        save_btn = QPushButton("Salvar")
        save_btn.setStyleSheet(Styles.primary_button())
        save_btn.clicked.connect(self.validate_and_accept)
        buttons_layout.addWidget(save_btn)

        layout.addLayout(buttons_layout)

        # Aplicar estilos
        self.setStyleSheet(Styles.dialog() + Styles.input_field())

    def load_data(self):
        """Carrega dados da análise para edição"""
        self.titulo_input.setText(self.analise_data.get('titulo', ''))

        # Selecionar seguradora
        seg_id = self.analise_data.get('seguradora_id')
        if seg_id:
            for i in range(self.seguradora_combo.count()):
                if self.seguradora_combo.itemData(i) == seg_id:
                    self.seguradora_combo.setCurrentIndex(i)
                    break

        self.numero_sinistro_input.setText(self.analise_data.get('numero_sinistro', '') or '')

        # Data do acidente
        data_acidente = self.analise_data.get('data_acidente')
        if data_acidente:
            self.data_acidente_input.setDate(QDate.fromString(str(data_acidente), "yyyy-MM-dd"))

        self.segurado_input.setText(self.analise_data.get('segurado', '') or '')
        self.apolice_input.setText(self.analise_data.get('numero_apolice', '') or '')
        self.local_input.setText(self.analise_data.get('local_colisao', '') or '')

        # Tipo de colisão
        tipo = self.analise_data.get('tipo_colisao')
        if tipo:
            index = self.tipo_combo.findText(tipo)
            if index >= 0:
                self.tipo_combo.setCurrentIndex(index)

        # Status
        status = self.analise_data.get('status')
        if status:
            index = self.status_combo.findText(status)
            if index >= 0:
                self.status_combo.setCurrentIndex(index)

        self.observacoes_input.setText(self.analise_data.get('observacoes', '') or '')

    def validate_and_accept(self):
        """Valida os dados antes de aceitar"""
        if not self.titulo_input.text().strip():
            QMessageBox.warning(self, "Erro", "O campo Título é obrigatório!")
            self.titulo_input.setFocus()
            return

        self.accept()

    def get_data(self):
        """Retorna os dados do formulário"""
        seguradora_id = self.seguradora_combo.currentData()
        tipo = self.tipo_combo.currentText()

        data_dict = {
            'titulo': self.titulo_input.text().strip(),
            'seguradora_id': seguradora_id,
            'numero_sinistro': self.numero_sinistro_input.text().strip() or None,
            'data_acidente': self.data_acidente_input.date().toString("yyyy-MM-dd"),
            'segurado': self.segurado_input.text().strip() or None,
            'numero_apolice': self.apolice_input.text().strip() or None,
            'local_colisao': self.local_input.text().strip() or None,
            'tipo_colisao': tipo if tipo != "Não especificado" else None,
            'status': self.status_combo.currentText(),
            'observacoes': self.observacoes_input.toPlainText().strip() or None
        }

        return data_dict


# ==================== TELAS PRINCIPAIS ====================

class SeguradorasCRUDScreen(QWidget):
    """Tela de gerenciamento de seguradoras"""

    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager or DatabaseManager()
        self.seguradora_crud = SeguradoraCRUD(self.db_manager)
        self.setup_ui()
        self.load_seguradoras()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # === CABEÇALHO ===
        header_layout = QHBoxLayout()

        title = QLabel("Seguradoras")
        title.setStyleSheet(Styles.label_title())
        header_layout.addWidget(title)

        header_layout.addStretch()

        novo_btn = QPushButton("Nova Seguradora")
        novo_btn.clicked.connect(self.nova_seguradora)
        novo_btn.setStyleSheet(Styles.primary_button())
        header_layout.addWidget(novo_btn)

        layout.addLayout(header_layout)

        # === BUSCA ===
        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por nome, CNPJ ou email...")
        self.search_input.textChanged.connect(self.buscar_seguradoras)
        self.search_input.setStyleSheet(Styles.input_field())
        search_layout.addWidget(self.search_input)

        layout.addLayout(search_layout)

        # === TABELA ===
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nome", "CNPJ", "Telefone", "Email", "Ações"
        ])

        # Configurar largura das colunas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        header.setSectionResizeMode(5, QHeaderView.Fixed)
        self.table.setColumnWidth(5, 200)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(Styles.table())

        layout.addWidget(self.table)

        # Status bar
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(Styles.label_normal())
        layout.addWidget(self.status_label)

    def load_seguradoras(self, seguradoras=None):
        """Carrega seguradoras na tabela"""
        if seguradoras is None:
            seguradoras = self.seguradora_crud.read_all(apenas_ativas=True)

        self.table.setRowCount(0)

        for seg in seguradoras:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(seg['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(seg['nome']))
            self.table.setItem(row, 2, QTableWidgetItem(seg.get('cnpj') or '-'))
            self.table.setItem(row, 3, QTableWidgetItem(seg.get('telefone') or '-'))
            self.table.setItem(row, 4, QTableWidgetItem(seg.get('email') or '-'))

            # Botões de ação
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(5)

            editar_btn = QPushButton("Editar")
            editar_btn.setStyleSheet(Styles.secondary_button())
            editar_btn.clicked.connect(lambda _, s=seg: self.editar_seguradora(s))
            actions_layout.addWidget(editar_btn)

            excluir_btn = QPushButton("Excluir")
            excluir_btn.setStyleSheet(Styles.danger_button())
            excluir_btn.clicked.connect(lambda _, s=seg: self.excluir_seguradora(s))
            actions_layout.addWidget(excluir_btn)

            self.table.setCellWidget(row, 5, actions_widget)

        self.status_label.setText(f"Total: {len(seguradoras)} seguradora(s)")

    def nova_seguradora(self):
        """Abre diálogo para nova seguradora"""
        dialog = SeguradoraDialog(self, db_manager=self.db_manager)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.seguradora_crud.create(**data)
                QMessageBox.information(self, "Sucesso", "Seguradora cadastrada com sucesso!")
                self.load_seguradoras()
            except ValueError as e:
                QMessageBox.warning(self, "Erro", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao cadastrar seguradora: {e}")

    def editar_seguradora(self, seguradora):
        """Abre diálogo para editar seguradora"""
        dialog = SeguradoraDialog(self, seguradora_data=seguradora, db_manager=self.db_manager)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.seguradora_crud.update(seguradora['id'], **data)
                QMessageBox.information(self, "Sucesso", "Seguradora atualizada com sucesso!")
                self.load_seguradoras()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar seguradora: {e}")

    def excluir_seguradora(self, seguradora):
        """Exclui seguradora (soft delete)"""
        resposta = QMessageBox.question(
            self, "Confirmar Exclusão",
            f"Deseja realmente excluir a seguradora '{seguradora['nome']}'?\n\n"
            "Esta ação apenas desativará a seguradora, sem remover os dados.",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                self.seguradora_crud.delete(seguradora['id'], soft_delete=True)
                QMessageBox.information(self, "Sucesso", "Seguradora desativada com sucesso!")
                self.load_seguradoras()
            except ValueError as e:
                QMessageBox.warning(self, "Erro", str(e))
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir seguradora: {e}")

    def buscar_seguradoras(self):
        """Busca seguradoras pelo termo digitado"""
        termo = self.search_input.text().strip()
        if termo:
            try:
                seguradoras = self.seguradora_crud.search(termo)
                self.load_seguradoras(seguradoras)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao buscar: {e}")
        else:
            self.load_seguradoras()


class AnaliseCRUDScreen(QWidget):
    """Tela de gerenciamento de análises"""

    # Signal para notificar que uma análise foi selecionada
    analise_selecionada = Signal(dict)

    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager or DatabaseManager()
        self.analise_crud = AnaliseCRUD(self.db_manager)
        self.seguradora_crud = SeguradoraCRUD(self.db_manager)
        self.setup_ui()
        self.load_analises()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(25)

        # === CABEÇALHO ===
        header_layout = QHBoxLayout()

        title = QLabel("Análises")
        title.setStyleSheet(Styles.label_title())
        header_layout.addWidget(title)

        header_layout.addStretch()

        nova_btn = QPushButton("Nova Análise")
        nova_btn.clicked.connect(self.nova_analise)
        nova_btn.setStyleSheet(Styles.primary_button())
        header_layout.addWidget(nova_btn)

        layout.addLayout(header_layout)

        # === FILTROS ===
        filtros_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar por título, sinistro, segurado ou local...")
        self.search_input.textChanged.connect(self.buscar_analises)
        self.search_input.setStyleSheet(Styles.input_field())
        filtros_layout.addWidget(self.search_input, 3)

        self.filtro_status = QComboBox()
        self.filtro_status.addItems([
            "Todos os status", "Em andamento", "Concluída", "Arquivada", "Cancelada"
        ])
        self.filtro_status.currentTextChanged.connect(self.aplicar_filtros)
        self.filtro_status.setStyleSheet(Styles.input_field())
        filtros_layout.addWidget(self.filtro_status, 1)

        self.filtro_seguradora = QComboBox()
        self.filtro_seguradora.addItem("Todas as seguradoras", None)
        seguradoras = self.seguradora_crud.read_all(apenas_ativas=True)
        for seg in seguradoras:
            self.filtro_seguradora.addItem(seg['nome'], seg['id'])
        self.filtro_seguradora.currentIndexChanged.connect(self.aplicar_filtros)
        self.filtro_seguradora.setStyleSheet(Styles.input_field())
        filtros_layout.addWidget(self.filtro_seguradora, 1)

        layout.addLayout(filtros_layout)

        # === TABELA ===
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Título", "Seguradora", "Nº Sinistro", "Data", "Status", "Velocidade", "Ações"
        ])

        # Configurar largura das colunas
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.Fixed)
        self.table.setColumnWidth(7, 250)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(Styles.table())

        layout.addWidget(self.table)

        # Status bar
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(Styles.label_normal())
        layout.addWidget(self.status_label)

    def load_analises(self, analises=None):
        """Carrega análises na tabela"""
        if analises is None:
            analises = self.analise_crud.read_all()

        self.table.setRowCount(0)

        for analise in analises:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(analise['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(analise['titulo']))
            self.table.setItem(row, 2, QTableWidgetItem(analise.get('seguradora_nome') or '-'))
            self.table.setItem(row, 3, QTableWidgetItem(analise.get('numero_sinistro') or '-'))

            # Formatar data
            data_analise = analise.get('data_analise')
            if data_analise:
                data_str = str(data_analise).split()[0]  # Pega só a data
                self.table.setItem(row, 4, QTableWidgetItem(data_str))
            else:
                self.table.setItem(row, 4, QTableWidgetItem('-'))

            # Status com cor
            status_item = QTableWidgetItem(analise.get('status', '-'))
            status = analise.get('status', '')
            if status == 'Concluída':
                status_item.setForeground(Qt.green)
            elif status == 'Em andamento':
                status_item.setForeground(Qt.yellow)
            elif status == 'Arquivada':
                status_item.setForeground(Qt.gray)
            self.table.setItem(row, 5, status_item)

            # Velocidade
            velocidade = analise.get('velocidade_kmh')
            vel_str = f"{velocidade:.2f} km/h" if velocidade else '-'
            self.table.setItem(row, 6, QTableWidgetItem(vel_str))

            # Botões de ação
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            actions_layout.setSpacing(5)

            visualizar_btn = QPushButton("Ver")
            visualizar_btn.setStyleSheet(Styles.secondary_button())
            visualizar_btn.clicked.connect(lambda _, a=analise: self.visualizar_analise(a))
            actions_layout.addWidget(visualizar_btn)

            editar_btn = QPushButton("Editar")
            editar_btn.setStyleSheet(Styles.secondary_button())
            editar_btn.clicked.connect(lambda _, a=analise: self.editar_analise(a))
            actions_layout.addWidget(editar_btn)

            excluir_btn = QPushButton("Excluir")
            excluir_btn.setStyleSheet(Styles.danger_button())
            excluir_btn.clicked.connect(lambda _, a=analise: self.excluir_analise(a))
            actions_layout.addWidget(excluir_btn)

            self.table.setCellWidget(row, 7, actions_widget)

        # Estatísticas
        stats = self.analise_crud.get_statistics()
        total = stats.get('total_analises', 0)
        concluidas = stats.get('concluidas', 0)
        em_andamento = stats.get('em_andamento', 0)

        self.status_label.setText(
            f"Total: {total} análise(s) | "
            f"Concluídas: {concluidas} | "
            f"Em andamento: {em_andamento}"
        )

    def nova_analise(self):
        """Abre diálogo para nova análise"""
        dialog = AnaliseDialog(self, db_manager=self.db_manager)
        if dialog.exec():
            data = dialog.get_data()
            try:
                analise_id = self.analise_crud.create(**data)
                QMessageBox.information(self, "Sucesso", f"Análise cadastrada com sucesso! ID: {analise_id}")
                self.load_analises()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao cadastrar análise: {e}")

    def editar_analise(self, analise):
        """Abre diálogo para editar análise"""
        dialog = AnaliseDialog(self, analise_data=analise, db_manager=self.db_manager)
        if dialog.exec():
            data = dialog.get_data()
            try:
                self.analise_crud.update(analise['id'], **data)
                QMessageBox.information(self, "Sucesso", "Análise atualizada com sucesso!")
                self.load_analises()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao atualizar análise: {e}")

    def visualizar_analise(self, analise):
        """Visualiza detalhes da análise"""
        # Buscar dados completos
        analise_completa = self.analise_crud.read(analise['id'])

        # Criar diálogo de visualização
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Análise #{analise['id']}")
        dialog.setMinimumWidth(600)
        dialog.setMinimumHeight(500)

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        titulo = QLabel(analise_completa['titulo'])
        titulo.setStyleSheet(Styles.label_title())
        layout.addWidget(titulo)

        # Criar texto com todos os detalhes
        detalhes = QTextEdit()
        detalhes.setReadOnly(True)

        texto = f"""
<h3 style="color: {Colors.CYAN_PRIMARY};">Dados do Sinistro</h3>
<p><b>Seguradora:</b> {analise_completa.get('seguradora_nome') or 'Não informada'}</p>
<p><b>Número do Sinistro:</b> {analise_completa.get('numero_sinistro') or 'Não informado'}</p>
<p><b>Data do Acidente:</b> {analise_completa.get('data_acidente') or 'Não informada'}</p>
<p><b>Segurado:</b> {analise_completa.get('segurado') or 'Não informado'}</p>
<p><b>Número da Apólice:</b> {analise_completa.get('numero_apolice') or 'Não informado'}</p>

<h3 style="color: {Colors.CYAN_PRIMARY};">Dados da Colisão</h3>
<p><b>Local:</b> {analise_completa.get('local_colisao') or 'Não informado'}</p>
<p><b>Tipo:</b> {analise_completa.get('tipo_colisao') or 'Não informado'}</p>

<h3 style="color: {Colors.CYAN_PRIMARY};">Resultados Técnicos</h3>
<p><b>Deformação:</b> {analise_completa.get('deformacao_cm') or '-'} cm</p>
<p><b>Velocidade:</b> {analise_completa.get('velocidade_kmh') or '-'} km/h</p>
<p><b>Energia:</b> {analise_completa.get('energia_joules') or '-'} J</p>
<p><b>Massa do Veículo:</b> {analise_completa.get('massa_veiculo') or '-'} kg</p>
<p><b>Fator de Escala:</b> {analise_completa.get('scale_factor') or '-'}</p>

<h3 style="color: {Colors.CYAN_PRIMARY};">Informações Adicionais</h3>
<p><b>Status:</b> {analise_completa.get('status')}</p>
<p><b>Data da Análise:</b> {analise_completa.get('data_analise')}</p>
<p><b>Observações:</b><br>{analise_completa.get('observacoes') or 'Nenhuma observação'}</p>
        """

        detalhes.setHtml(texto)
        detalhes.setStyleSheet(f"""
            QTextEdit {{
                background-color: {Colors.BG_CARD};
                border: 1px solid {Colors.BORDER_DEFAULT};
                border-radius: {BorderRadius.MEDIUM};
                color: {Colors.TEXT_PRIMARY};
                padding: 15px;
                font-size: {Typography.SIZE_NORMAL};
            }}
        """)
        layout.addWidget(detalhes)

        # Botão fechar
        fechar_btn = QPushButton("Fechar")
        fechar_btn.setStyleSheet(Styles.secondary_button())
        fechar_btn.clicked.connect(dialog.accept)
        layout.addWidget(fechar_btn, alignment=Qt.AlignRight)

        dialog.setStyleSheet(Styles.dialog())
        dialog.exec()

    def excluir_analise(self, analise):
        """Exclui análise permanentemente"""
        resposta = QMessageBox.question(
            self, "Confirmar Exclusão",
            f"Deseja realmente excluir a análise '{analise['titulo']}'?\n\n"
            "Esta ação não pode ser desfeita!",
            QMessageBox.Yes | QMessageBox.No
        )

        if resposta == QMessageBox.Yes:
            try:
                self.analise_crud.delete(analise['id'])
                QMessageBox.information(self, "Sucesso", "Análise excluída com sucesso!")
                self.load_analises()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao excluir análise: {e}")

    def buscar_analises(self):
        """Busca análises pelo termo digitado"""
        termo = self.search_input.text().strip()
        if termo:
            try:
                analises = self.analise_crud.search(termo)
                self.load_analises(analises)
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao buscar: {e}")
        else:
            self.aplicar_filtros()

    def aplicar_filtros(self):
        """Aplica filtros de status e seguradora"""
        if self.search_input.text().strip():
            return  # Se há busca ativa, não aplica filtros

        try:
            status = self.filtro_status.currentText()
            filtro_status = None if status == "Todos os status" else status

            seguradora_id = self.filtro_seguradora.currentData()

            analises = self.analise_crud.read_all(
                filtro_status=filtro_status,
                filtro_seguradora=seguradora_id
            )
            self.load_analises(analises)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao aplicar filtros: {e}")


# -*- coding: utf-8 -*-
"""
Diálogos em grade (3 colunas) com dark mode, labels à esquerda e scroll.
Requer: core.theme (Styles, Colors, Typography, BorderRadius)
"""

from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QLineEdit,
    QTextEdit, QComboBox, QDateEdit, QPushButton, QScrollArea, QMessageBox
)
from PySide6.QtCore import Qt, QDate

from core.theme import Styles, Colors, Typography
from core.database import SeguradoraCRUD


# ---------- util ----------
def _label(text: str) -> QLabel:
    """Label do campo (alinhada à esquerda, fonte maior)."""
    lbl = QLabel(text)
    lbl.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    lbl.setStyleSheet(
        f"color:{Colors.TEXT_SECONDARY};"
        f"font-size:{Typography.SIZE_MEDIUM};"
        f"font-weight:{Typography.WEIGHT_MEDIUM};"
        "margin-bottom: 6px;"
    )
    return lbl


def _std_height(w):
    try:
        w.setMinimumHeight(44)
    except Exception:
        pass
    return w


def _wrap_field(title: str, widget: QWidget) -> QWidget:
    """Empacota label acima e input abaixo para usar em uma célula da grade."""
    box = QWidget()
    v = QVBoxLayout(box)
    v.setContentsMargins(0, 0, 0, 0)
    v.setSpacing(0)
    v.addWidget(_label(title))
    v.addWidget(_std_height(widget))
    return box


# ---------- base dialog (grid 3 colunas) ----------

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QLineEdit, QTextEdit, QDialog, QDateEdit, QComboBox,
    QMessageBox, QHeaderView, QScrollArea, QFrame, QGridLayout
)

class _BaseGridDialog(QDialog):
    COLS = 3
    def _build_shell(self, title_text: str, max_w: int = 200):
        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)
        title = QLabel(title_text)
        title.setStyleSheet(Styles.label_title())
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        root.addWidget(title)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet(Styles.scrollarea())
        root.addWidget(self.scroll)
        root.setStretch(1, 1)
        viewport = QWidget()
        vlay = QHBoxLayout(viewport)
        vlay.setContentsMargins(0, 0, 0, 0)
        self.card = QWidget(objectName="FormCard")
        self.card.setStyleSheet(Styles.form_card())
        self.card.setMinimumWidth(1200)
        self.card.setMaximumWidth(2000)
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(28, 28, 28, 28)
        card_layout.setSpacing(16)
        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(18)
        self.grid.setVerticalSpacing(14)
        for i in range(self.COLS):
            self.grid.setColumnStretch(i, 1)
        card_layout.addLayout(self.grid)
        vlay.addStretch(1)
        vlay.addWidget(self.card, 0, Qt.AlignTop)
        vlay.addStretch(1)
        self.scroll.setWidget(viewport)
        footer = QHBoxLayout()
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.setStyleSheet(Styles.secondary_button())
        footer.addWidget(self.btn_cancel, 0, Qt.AlignLeft)
        footer.addStretch(1)
        self.btn_save = QPushButton("Salvar")
        self.btn_save.setStyleSheet(Styles.primary_button())
        footer.addWidget(self.btn_save, 0, Qt.AlignRight)
        root.addLayout(footer)
        self.setStyleSheet(Styles.dialog() + Styles.input_field() + Styles.combo_popup() + Styles.calendar())
        self._col = 0
        self._row = 0
    def _add_cell(self, widget: QWidget, span: int = 1):
        span = max(1, min(span, self.COLS))
        if self._col + span > self.COLS:
            self._row += 1
            self._col = 0
        self.grid.addWidget(widget, self._row, self._col, 1, span)
        self._col += span
        if self._col >= self.COLS:
            self._row += 1
            self._col = 0

class SeguradoraDialog(_BaseGridDialog):
    def __init__(self, parent=None, seguradora_data=None, db_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.seguradora_data = seguradora_data
        self.setMinimumSize(854, 480)
        self._build_shell("Nova Seguradora" if not seguradora_data else "Editar Seguradora")
        self._build_form()
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.validate_and_accept)
        if seguradora_data:
            self.load_data()
    def _build_form(self):
        self.in_nome = QLineEdit(); self.in_nome.setPlaceholderText("Ex: Porto Seguro")
        self.in_cnpj = QLineEdit(); self.in_cnpj.setPlaceholderText("00.000.000/0000-00"); self.in_cnpj.setMaxLength(18)
        self.in_telefone = QLineEdit(); self.in_telefone.setPlaceholderText("(85) 99999-9999"); self.in_telefone.setMaxLength(20)
        self.in_email = QLineEdit(); self.in_email.setPlaceholderText("contato@seguradora.com.br")
        self.in_endereco = QTextEdit(); self.in_endereco.setPlaceholderText("Endereço completo da seguradora"); self.in_endereco.setMaximumHeight(120)
        self.in_contato = QLineEdit(); self.in_contato.setPlaceholderText("Nome do responsável")
        self.in_obs = QTextEdit(); self.in_obs.setPlaceholderText("Observações adicionais"); self.in_obs.setMaximumHeight(140)
        def cell(lbl, w):
            box = QWidget()
            v = QVBoxLayout(box); v.setContentsMargins(0, 0, 0, 0); v.setSpacing(6)
            lab = QLabel(lbl); lab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            lab.setStyleSheet(f"color:{Colors.TEXT_SECONDARY};font-size:{Typography.SIZE_MEDIUM};font-weight:{Typography.WEIGHT_MEDIUM};")
            v.addWidget(lab); v.addWidget(w)
            try: w.setMinimumHeight(48)
            except: pass
            return box
        self._add_cell(cell("Nome*", self.in_nome), span=2)
        self._add_cell(cell("CNPJ", self.in_cnpj), span=1)
        self._add_cell(cell("Telefone", self.in_telefone), span=1)
        self._add_cell(cell("Email", self.in_email), span=2)
        self._add_cell(cell("Endereço", self.in_endereco), span=2)
        self._add_cell(cell("Contato Responsável", self.in_contato), span=1)
        self._add_cell(cell("Observações", self.in_obs), span=3)
    def validate_and_accept(self):
        if not self.in_nome.text().strip():
            QMessageBox.warning(self, "Erro", "O campo Nome é obrigatório!")
            self.in_nome.setFocus()
            return
        self.accept()
    def get_data(self):
        return {
            "nome": self.in_nome.text().strip(),
            "cnpj": self.in_cnpj.text().strip(),
            "telefone": self.in_telefone.text().strip(),
            "email": self.in_email.text().strip(),
            "endereco": self.in_endereco.toPlainText().strip(),
            "contato_responsavel": self.in_contato.text().strip(),
            "observacoes": self.in_obs.toPlainText().strip(),
        }
    def load_data(self):
        d = self.seguradora_data
        self.in_nome.setText(d.get("nome", ""))
        self.in_cnpj.setText(d.get("cnpj", ""))
        self.in_telefone.setText(d.get("telefone", ""))
        self.in_email.setText(d.get("email", ""))
        self.in_endereco.setText(d.get("endereco", ""))
        self.in_contato.setText(d.get("contato_responsavel", ""))
        self.in_obs.setText(d.get("observacoes", ""))

class AnaliseDialog(_BaseGridDialog):
    def __init__(self, parent=None, analise_data=None, db_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.analise_data = analise_data
        self.setMinimumSize(1280, 720)
        self._build_shell("Nova Análise" if not analise_data else "Editar Análise", max_w=1360)
        self._build_form()
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_save.clicked.connect(self.validate_and_accept)
        if analise_data:
            self.load_data()
    def _build_form(self):
        self.in_titulo = QLineEdit(); self.in_titulo.setPlaceholderText("Ex: Colisão Frontal - Av. Principal")
        self.cb_seguradora = QComboBox(); self.cb_seguradora.addItem("Nenhuma seguradora", None)
        if self.db_manager:
            for seg in SeguradoraCRUD(self.db_manager).read_all(apenas_ativas=True):
                self.cb_seguradora.addItem(seg["nome"], seg["id"])
        self.in_num_sinistro = QLineEdit(); self.in_num_sinistro.setPlaceholderText("Número do sinistro/processo")
        self.in_data = QDateEdit(); self.in_data.setCalendarPopup(True); self.in_data.setDate(QDate.currentDate()); self.in_data.setDisplayFormat("dd/MM/yyyy")
        self.in_segurado = QLineEdit(); self.in_segurado.setPlaceholderText("Nome do segurado/envolvido")
        self.in_apolice = QLineEdit(); self.in_apolice.setPlaceholderText("Número da apólice")
        self.in_local = QLineEdit(); self.in_local.setPlaceholderText("Ex: Av. Bezerra de Menezes, 1000")
        self.cb_tipo = QComboBox(); self.cb_tipo.addItems(["Não especificado","Frontal","Traseira","Lateral","Capotamento","Atropelamento","Choque com objeto fixo","Outro"])
        self.cb_status = QComboBox(); self.cb_status.addItems(["Em andamento","Concluída","Arquivada","Cancelada"])
        self.in_obs = QTextEdit(); self.in_obs.setPlaceholderText("Observações sobre a análise"); self.in_obs.setMaximumHeight(160)
        def cell(lbl, w):
            box = QWidget()
            v = QVBoxLayout(box); v.setContentsMargins(0, 0, 0, 0); v.setSpacing(6)
            lab = QLabel(lbl); lab.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            lab.setStyleSheet(f"color:{Colors.TEXT_SECONDARY};font-size:{Typography.SIZE_MEDIUM};font-weight:{Typography.WEIGHT_MEDIUM};")
            v.addWidget(lab); v.addWidget(w)
            try: w.setMinimumHeight(48)
            except: pass
            return box
        self._add_cell(cell("Título*", self.in_titulo), span=2)
        self._add_cell(cell("Seguradora", self.cb_seguradora), span=1)
        self._add_cell(cell("Nº Sinistro", self.in_num_sinistro), span=1)
        self._add_cell(cell("Data do Acidente", self.in_data), span=1)
        self._add_cell(cell("Segurado", self.in_segurado), span=1)
        self._add_cell(cell("Nº Apólice", self.in_apolice), span=1)
        self._add_cell(cell("Local", self.in_local), span=2)
        self._add_cell(cell("Tipo", self.cb_tipo), span=1)
        self._add_cell(cell("Status", self.cb_status), span=2)
        self._add_cell(cell("Observações", self.in_obs), span=3)
    def validate_and_accept(self):
        if not self.in_titulo.text().strip():
            QMessageBox.warning(self, "Erro", "O campo Título é obrigatório!")
            self.in_titulo.setFocus()
            return
        self.accept()
    def get_data(self):
        return {
            "titulo": self.in_titulo.text().strip(),
            "seguradora_id": self.cb_seguradora.currentData(),
            "numero_sinistro": self.in_num_sinistro.text().strip(),
            "data_acidente": self.in_data.date().toString("yyyy-MM-dd"),
            "segurado": self.in_segurado.text().strip(),
            "numero_apolice": self.in_apolice.text().strip(),
            "local_colisao": self.in_local.text().strip(),
            "tipo_colisao": self.cb_tipo.currentText(),
            "status": self.cb_status.currentText(),
            "observacoes": self.in_obs.toPlainText().strip(),
        }
    def load_data(self):
        d = self.analise_data
        self.in_titulo.setText(d.get("titulo", ""))
        if d.get("seguradora_id"):
            for i in range(self.cb_seguradora.count()):
                if self.cb_seguradora.itemData(i) == d["seguradora_id"]:
                    self.cb_seguradora.setCurrentIndex(i)
                    break
        self.in_num_sinistro.setText(d.get("numero_sinistro", ""))
        if d.get("data_acidente"):
            self.in_data.setDate(QDate.fromString(str(d["data_acidente"]), "yyyy-MM-dd"))
        self.in_segurado.setText(d.get("segurado", ""))
        self.in_apolice.setText(d.get("numero_apolice", ""))
        self.in_local.setText(d.get("local_colisao", ""))
        t = d.get("tipo_colisao", "Não especificado")
        idx = self.cb_tipo.findText(t)
        if idx >= 0:
            self.cb_tipo.setCurrentIndex(idx)
        s = d.get("status", "Em andamento")
        idx2 = self.cb_status.findText(s)
        if idx2 >= 0:
            self.cb_status.setCurrentIndex(idx2)
        self.in_obs.setText(d.get("observacoes", ""))
