from opcua import Client, ua

class Coneccao_Opc():
    def __init__(self, url):
        # Endereço do servidor de OPC UA
        self.url = url
        # Definindo o URL para conexão
        self.client = Client(self.url)
    def conectar_opc(self):
        self.client.connect()
        print("Conectado ao servidor OPC UA")
    def desconectar_opc(self):
        self.client.disconnect()
        print("Desconectado do servidor OPC UA")
    def leitura_valor(self, node):
        no_leitura = self.client.get_node(node)
        valor = no_leitura.get_value()
        return valor
    def escrita_valor_booleano(self, node, valor):
        no_escrita = self.client.get_node(node)
        no_escrita.set_value(ua.DataValue(ua.Variant(valor, ua.VariantType.Boolean)))
    def escrita_valor_float(self, node, valor):
        # Escreve um valor float no nó especificado
        no_escrita = self.client.get_node(node)
        no_escrita.set_value(ua.DataValue(ua.Variant(valor, ua.VariantType.Float)))
