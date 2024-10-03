import mysql.connector

#db_t_mquina
class banco:
    def __init__(self) -> None:
        self.status = False
        self.conexao = mysql.connector.connect(
            host='doce-gelato.cfey060w0r7y.us-east-2.rds.amazonaws.com',
            database='doce_gelato',
            user='astrodocegelato',
            password='Doce-gelato226')

        self.bancoo = "ONLINE"
        # self.conexao = mysql.connector.connect(
        #     host='localhost',
        #     database='doce_gelato',
        #     user='root',
        #     password='Gestor226@')
        


        self.cursor = self.conexao.cursor()
    def mostrar(self):
        
        if self.conexao.is_connected():
            print('conectado')

    def open_Banco(self):
        print('Banco Aberto')
        self.status = False
        
        self.conexao = mysql.connector.connect(
            host='doce-gelato.cfey060w0r7y.us-east-2.rds.amazonaws.com',
            database='doce_gelato',
            user='astrodocegelato',
            password='Doce-gelato226')
        self.cursor = self.conexao.cursor()

    
    
    def buscar_Banco(self, tabela, valor_buscado=None):
        #Codigo SQL
        codigo_sql = f"""Select * from {tabela}"""
        
        self.cursor.execute(codigo_sql)
        tabela_banco = self.cursor.fetchall()
        lista_valor = []
        #Busca dentro da tabela
        if valor_buscado != None:
            for valor in tabela_banco:
                if valor_buscado == valor[1]:
                    return valor[1]
            return lista_valor
        else:
            for valor in tabela_banco:
                lista_valor.append(valor)
            return lista_valor

    def autenthicar_Banco(self, usuario, senha, tabela):
        #Codigo SQL
        codigo_sql = f"""Select * from {tabela}"""
        
        self.cursor.execute(codigo_sql)
        tabela = self.cursor.fetchall()
        
        flag_login = False

        #Busca dentro da tabela
        for valor in tabela:
            print(f'DEBIG SQL-------------------- {valor}  ----  usuario [{usuario}]  senha [{senha}]')
            if valor[1] == usuario and valor[2] == senha:
                flag_login = True
                print('logado')
        

        return flag_login
        

    def cadastrar_maquina_Banco(self, list_valores):
        
        self.cursor.execute(f"""insert into t_equipamentos
            (tag,rg,sta,voltagem,largura,altura,comprimento,capacidade,modelo,usuario) 
            values
            ("{list_valores[0]}","{list_valores[1]}","{list_valores[2]}",
            "{list_valores[3]}","{list_valores[4]}","{list_valores[5]}",
            "{list_valores[6]}","{list_valores[7]}","{list_valores[8]}","{list_valores[9]}");""")

        self.conexao.commit()

    def close_Banco(self):
        self.conexao.close()
        self.cursor.close()
        self.status = False      
        print('Banco encerrado!')
        return self.status
