
import pyodbc
from time import sleep
import os
import win32api
import psycopg2
import psutil

from datetime import datetime

class DataBaseNuvem:

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="masterkey",
            host="dbthiago.cpoye04a2pvx.us-east-1.rds.amazonaws.com",
            port="5432"
        )
        self.cursor = self.conn.cursor()


    def buscar(self, sql_query):
        self.sql_query = sql_query
        self.cursor.execute(self.sql_query)
        row = self.cursor.fetchall()
        return row

    def alterar(self,sql_query):
        self.sql_query = sql_query
        self.cursor.execute(self.sql_query)
        self.conn.commit()

    def desconectar(self):
        self.cursor.close()
        self.conn.close()

class DataBase:

    def __init__(self, database):

        self.database = database

        drive_odbc = '{Firebird/InterBase(r) driver}'
        str_connect = f'DRIVER={drive_odbc}; Database={caminho};User=sysdba;Password=masterkey;'
        self.cnxn = pyodbc.connect(str_connect)
        self.cursor = self.cnxn.cursor()


    def buscar(self, sql_query):
        self.sql_query = sql_query
        self.cursor.execute(self.sql_query)
        row = self.cursor.fetchall()
        return row

    def alterar(self,sql_query):
        self.sql_query = sql_query
        self.cursor.execute(self.sql_query)
        self.cursor.commit()

    def desconectar(self):
        self.cursor.close()
        self.cnxn.close()


def arquivo_mais_novo():
    pasta = "C:/Backup Internews"

    # Lista todos os arquivos na pasta e subpastas
    arquivos = []
    for root, dirs, files in os.walk(pasta):
        for file in files:
            arquivos.append(os.path.join(root, file))

    # Obtém o arquivo mais recente pela data de modificação
    arquivo_mais_recente = max(arquivos, key=os.path.getmtime)

    # Obtém a data de modificação do arquivo mais recente
    data_modificacao_timestamp = os.path.getmtime(arquivo_mais_recente)
    data_modificacao = datetime.fromtimestamp(data_modificacao_timestamp).date()

    return data_modificacao


def versao():
    # Caminho para o arquivo executável
    file_path = "C:/internews/internews.exe"

    # Verifica se o arquivo existe
    if os.path.exists(file_path):
        # Obtém a versão do arquivo executável
        version_info = win32api.GetFileVersionInfo(file_path, '\\')

        # Extrai a versão principal, secundária, revisão e build
        major_version = version_info['FileVersionMS'] >> 16
        minor_version = version_info['FileVersionMS'] & 0xFFFF
        revision = version_info['FileVersionLS'] >> 16
        build = version_info['FileVersionLS'] & 0xFFFF

        # Imprime a versão
        versao = f"{major_version}.{minor_version}.{revision}.{build}"
        return versao
    else:
        return f"Não exite"

def verificaMega():
    caminho_arquivo = (r"C:\Users\User\AppData\Local\MEGAsync",
    "C:\Internews\Interfire\MEGAsyncSetup32.exe")
    # Verifica se o arquivo existe
    msg = "N"
    for file in caminho_arquivo:
        if os.path.exists(file):
            msg = "S"
    return msg


def SistemaAberto():
    process_name = "InterNews.exe"
    # Itera por todos os processos ativos
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            # Verifica se o nome do processo ou o caminho do executável bate com o esperado
            if process_name.lower() in (proc.info['name'] or '').lower() or \
               process_name.lower() in (proc.info['exe'] or '').lower():
                return 'S'
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return 'N'

caminho = 'c:/internews/banco de dados/dados.fdb'


# Scripts SQL banco de dados
empresaNome = """SELECT NOME FROM EMPRESAS"""
countEmprersa = """SELECT count(*) FROM EMPRESAS"""
organizaDb = """SELECT  (CURRENT_DATE-ULT_REINDEX) AS ULT_ORGANIZACAO, DURACAO_REINDEX, ULT_REINDEX
FROM CONFIG"""
nfceNfe = """select count(*) from nota_fiscal
                WHERE STATUS_NFE <> 'T' and
                current_date - DT_EMISSAO < 30 """

# Declaração de variáveis Globais


class Dados:
    # Dados do Cliente
    def __init__(self):
        self.db = DataBase(caminho)

    def empresa(self):
        return str(self.db.buscar(empresaNome)[0][0]).upper()

    def cnpj(self):
        return self.db.buscar('select cnpj from empresas')[0][0]

    def empresaQuantidade(self):
        return self.db.buscar(countEmprersa)[0][0]

    def diasDB(self):
        return self.db.buscar(organizaDb)[0][0]

    def tempoDB(self):
        return self.db.buscar(organizaDb)[0][1]

    def dataDB(self):
        return self.db.buscar(organizaDb)[0][2]

    def notasNaoTransmitida(self):
        return self.db.buscar(nfceNfe)[0][0]

    def ultimoBackup(self):
        return arquivo_mais_novo()

    def diasUltBackup(self):
        return (datetime.now().date() - self.ultimoBackup()).days

    def mega(self):
        return verificaMega()

    def versao(self):
        return versao()
    def mostrarDados(self):
        print(f"CNPJ: {self.cnpj()}")
        print(f"Empresa: {self.empresa()}, Quantidade: {self.empresaQuantidade()}")
        print(f"Versão: {self.versao()}")
        print(f'Ultimo backup: {self.ultimoBackup()}, Dias: {self.diasUltBackup()}')
        print(f"Mega: {self.mega()}")
        print(f'Dias Organiza DB: {self.diasDB()} ')
        print(f'NFCe e NFe pendentes: {self.notasNaoTransmitida()}')

    def desconectar(self):
        self.db.desconectar()


while True:
    try:
        dbNuvem = DataBaseNuvem()
        break
    except psycopg2.OperationalError:
        print('Sem conexão de rede')
        sleep(2)

def ColetaDados():
    dadosCliente = dict()
    empresa = Dados()
    dadosCliente['VERSAO'] = empresa.versao()
    dadosCliente['ULT_BACKUP'] = empresa.ultimoBackup()
    dadosCliente['ULT_ORGDB'] = empresa.dataDB()
    dadosCliente['MEGA'] = empresa.mega()
    dadosCliente['NF_PENDENTE'] = empresa.notasNaoTransmitida()
    dadosCliente['NUM_EMPRESAS'] = empresa.empresaQuantidade()
    dadosCliente['ULT_ENVIO'] = 0
    dadosCliente['ALERTA'] = ''
    dadosCliente['CNPJ'] = empresa.cnpj()
    dadosCliente['ONLINE'] = SistemaAberto()
    # print(dadosCliente)
    return dadosCliente

def AtualizaNuvem(cliente):
    # cria o cliente caso não exista a faz a alteração
    countCnpj = int(dbNuvem.buscar(f"SELECT COUNT(*) CNPJ FROM USUARIOS WHERE CNPJ = '{cliente['CNPJ']}'")[0][0])
    # print(countCnpj)

    if countCnpj == 0:
        empresa = Dados()
        scriptcriarCliente = (f"""INSERT INTO USUARIOS (NOME, CNPJ,ATUALIZAR, ALERTA)
                                    VALUES ('{empresa.empresa()}','{cliente['CNPJ']}','N', 'N')""")
        print(scriptcriarCliente)
        dbNuvem.alterar(scriptcriarCliente)

    # Altera Dados
    scriptAtualizarDados = f"""UPDATE USUARIOS SET VERSAO = '{cliente['VERSAO']}',
                                    ULT_BACKUP = '{cliente['ULT_BACKUP']}',
                                    ULT_ORGDB = '{cliente['ULT_ORGDB']}',
                                    MEGA = '{cliente['MEGA']}',
                                    NF_PENDENTE = '{cliente['NF_PENDENTE']}',
                                    NUM_EMPRESAS = '{cliente['NUM_EMPRESAS']}',
                                    ULT_ENVIO = '{cliente['ULT_ENVIO']}',
                                    ATUALIZAR = 'N', 
                                    ALERTA = '{cliente['ALERTA']}',
                                    ONLINE = '{cliente['ONLINE']}'   
                                    WHERE CNPJ = '{cliente['CNPJ']}'
                                    """
    # print(scriptAtualizarDados)
    dbNuvem.alterar(scriptAtualizarDados)


cliente = ColetaDados()
cliente['ULT_ENVIO'] = datetime.now()

# Comando para banco

# print(dbNuvem.alterar("ALTER TABLE USUARIOS ADD COLUMN online CHAR(1);"))
# print(dbNuvem.buscar("select * from USUARIOS where nome like '%Teste%' "))

while True:
    try:
        dbNuvem = DataBaseNuvem()
        cliente_novo = ColetaDados()
        cliente_novo['ALERTA'] = cliente['ALERTA']
        print('cliente',cliente)
        print('novo',cliente_novo)

        if cliente_novo != cliente:
            cliente = cliente_novo.copy()
            cliente['ULT_ENVIO'] = datetime.now()
            # Verifica Alerta
            if ((datetime.now().date() - cliente['ULT_BACKUP']).days > 7 or
                 'N' in cliente['MEGA'] or
                 (datetime.now().date() - cliente['ULT_ORGDB']).days > 30 or
                 cliente['NF_PENDENTE'] > 10):
                print('Sistema em Alerta')
                cliente['ALERTA'] = 'S'

            else:
                print('Sistema OK')
                cliente['ALERTA'] = 'N'

            AtualizaNuvem(cliente)
            cliente['ULT_ENVIO'] = 0
            print('Atualizado')

        else:
            print('Dados ')

        sleep(10)
    except Exception as e:
        print(e)
        sleep(1)

