import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QLabel, QPushButton, QGridLayout, QWidget, QMessageBox
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from datetime import datetime
from ClassOPC import Coneccao_Opc

class JanelaPrincipal(QMainWindow):
    def __init__(self, opc_ua):
        super().__init__()
        self.opc_ua = opc_ua  # Conexão OPC UA
        self.setWindowTitle("Situação 1")  # Título
        self.setFont(QFont('Arial', 20))  # Fonte
        
        # Botões e entradas
        self.botao_temperatura = QPushButton("Ajustar Temperatura do Processo")  # Botão ajustar temperatura
        self.botao_velocidade = QPushButton("Ajustar Velocidade da Esteira")  # Botão ajustar velocidade
        self.botao_exportar = QPushButton("Exportar Dados para Qualidade")  # Botão exportar dados
        self.botao_atualizar = QPushButton("Atualizar Indicadores")  # Botão atualizar indicadores
        self.entrada_velocidade = QLineEdit()  # Campo de entrada - velocidade
        self.entrada_temperatura = QLineEdit()  # Campo de entrada - temperatura
        
        # Labels
        self.label_producao = QLabel(f"Produção:")  # Produçãoução
        self.label_temperatura = QLabel(f"Temperatura:")  # Temperatura
        self.label_velocidade = QLabel(f"Velolidade:")  # Velocidade
        self.label_defeitos = QLabel(f"Defeitos:")  # Defeitos
        #esse valores delevem ser forçados no clp

        # Layout da interface
        self.layout = QGridLayout()
        self.layout.addWidget(self.botao_temperatura, 0, 0)  # Botão
        self.layout.addWidget(self.botao_velocidade, 1, 0)
        self.layout.addWidget(self.botao_exportar, 2, 0)
        self.layout.addWidget(self.botao_atualizar, 3, 0)
        self.layout.addWidget(self.entrada_temperatura, 0, 1)  # Campos
        self.layout.addWidget(self.entrada_velocidade, 1, 1)
        self.layout.addWidget(self.label_producao, 2, 1)  # Label
        self.layout.addWidget(self.label_temperatura, 3, 1)
        self.layout.addWidget(self.label_velocidade, 4, 1)
        self.layout.addWidget(self.label_defeitos, 5, 1)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centraliza
        
        # Widget
        self.custom_widget = QWidget()
        self.custom_widget.setLayout(self.layout) 
        self.setCentralWidget(self.custom_widget)

        # Conectando os botões às funções
        self.botao_temperatura.clicked.connect(self.ajustar_temperatura)
        self.botao_velocidade.clicked.connect(self.ajustar_velocidade)
        self.botao_exportar.clicked.connect(self.exportar_dados)
        self.botao_atualizar.clicked.connect(self.atualizar_indicadores)

        # Timer para atualizar os indicadores a cada 1 segundo
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_indicadores)
        self.timer.start(1000)

    def ajustar_temperatura(self):
        # Ajusta a temperatura no CLP
        valor = float(self.entrada_temperatura.text())
        self.opc_ua.escrita_valor_float("ns=4;s=|var|NEXTO PLC.Application.OPC_UA.ajuste_temp", valor)

    def ajustar_velocidade(self):
        # Ajusta a velocidade no CLP
        valor = float(self.entrada_velocidade.text())
        self.opc_ua.escrita_valor_float("ns=4;s=|var|NEXTO PLC.Application.OPC_UA.ajuste_velocidade", valor)

    def exportar_dados(self):
        # Exporta os dados para um arquivo CSV
        with open('dados_qualidade.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Temperatura (°C)", "Velocidade Esteira (m/s)", "Defeitos", "Produtos por Hora", "Data e Hora"])
            writer.writerow([self.label_temperatura.text(), self.label_velocidade.text(), self.label_defeitos.text(), self.label_producao.text(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    def atualizar_indicadores(self):
        # Atualiza os indicadores lendo os valores do CLP
        self.label_temperatura.setText(f"Temperatura: {self.opc_ua.leitura_valor('ns=4;s=|var|NEXTO PLC.Application.OPC_UA.temperatura_processo')}")
        self.label_velocidade.setText(f"Velocidade: {self.opc_ua.leitura_valor('ns=4;s=|var|NEXTO PLC.Application.OPC_UA.velocidade_esteira')}")
        self.label_defeitos.setText(f"Defeitos: {self.opc_ua.leitura_valor('ns=4;s=|var|NEXTO PLC.Application.OPC_UA.defeitos_detectados')}")
        self.label_producao.setText(f"Produção: {self.opc_ua.leitura_valor('ns=4;s=|var|NEXTO PLC.Application.OPC_UA.produtos_por_hora')}")

# URL do CLP
clp_bancada_5 = 'opc.tcp://192.168.15.52:4840'
# Conectando ao servidor OPC UA
opc_ua = Coneccao_Opc(url=clp_bancada_5)
opc_ua.conectar_opc()
# Inicializando a aplicação PyQt
app = QApplication(sys.argv)
window = JanelaPrincipal(opc_ua)  # Passando a conexão OPC UA para a janela principal
window.show()
app.exec()
# Desconectando do servidor OPC UA ao fechar a aplicação
opc_ua.desconectar_opc()
