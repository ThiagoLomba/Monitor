import os
import psycopg2
from time import sleep

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')
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



campos = [['NOME', 30], ['ALERTA', 6], ['VERSAO', 6], ['BK', 2],
          ['ORG', 3], ['MEGA', 4], ['NFE', 3],['EMP',3],['ONL',3], ['ENVIO', 10]]


def mostrarResultado(dados):
    for descricao in campos:
        print(descricao[0].ljust(descricao[1]), end='\t')

    print()

    for cliente in dados:
        for num, i in enumerate(cliente):
            #print(num, i, campos[num][1])
            print(str(i).ljust(campos[num][1]), end='\t')

        print()


alerta = ''
busca = ''
ordem = 1
while True:

    print('MONITOR INTERNEWS')

    try:
        db = DataBaseNuvem()
    except psycopg2.OperationalError:
        print('Sem conexão de rede')
        exit()

    resultados = db.buscar("SELECT left(NOME,30),ALERTA, left(VERSAO,6), CURRENT_DATE - ULT_BACKUP,"
                           "  CURRENT_DATE - ULT_ORGDB, MEGA, "
                           "NF_PENDENTE, NUM_EMPRESAS, ONLINE, TO_CHAR(ULT_ENVIO, 'DD/MM HH24:MI')"
                           f"FROM USUARIOS WHERE ALERTA not like '{alerta}' and nome like '%{busca.upper()}%' "
                           f"ORDER BY {ordem} ")
    db.desconectar()
    mostrarResultado(resultados)
    print('\n')
    print(f'1 - Alerta ({alerta})\n'
          '2 - Buscar\n' 
          f'3 - Ordem {ordem}')
    opc = input('Opcao: ')

    print(opc)
    if opc == '1':
        if alerta == '':
            alerta = 'N'
        else:
            alerta = ''
    if opc == '2':
        busca = input('Digite o nome: ')
    if opc == '3':
        for num, i in enumerate(campos):
            print(num + 1, i[0])

        ordem = int(input('Numero da coluna: '))
        if ordem < 1 or ordem > len(campos):
            print('Coluna Inexistente')
            ordem = 1


    limpar_tela()















