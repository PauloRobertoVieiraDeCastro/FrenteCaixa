from clientes import*
SQL_BUSCA = 'SELECT cupom, CPF, nome, Telefone, Logradouro, Cidade, Estado FROM clientes_get3'
SQL_CRIA = 'INSERT INTO clientes_get3 (cupom, CPF, nome, Telefone, Logradouro, Cidade, Estado) VALUES (%s, %s, %s, %s, %s, %s, %s)'
SQL_JUNCAO = 'SELECT clientes_get3.cupom, clientes_get3.CPF, clientes_get3.Nome,clientes_get3.Telefone, clientes_get3.Logradouro, clientes_get3.Cidade,clientes_get3.Estado,vendas_get.SKU, vendas_get.produto, vendas_get.preco FROM clientes_get3 JOIN vendas_get ON clientes_get3.cupom = vendas_get.cupom'

class DAO_CLIENTES:
    def __init__(self, db):
        self.__db = db

    def listar_clientes(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA)
        atividade = traduz_atividade(cursor.fetchall())
        return atividade

    def salvar_clientes(self,lista):
        cursor = self.__db.connection.cursor() #cursor para acessar o db
        cursor.execute(SQL_CRIA, (lista.codigo, lista.cpf, lista.nome, lista.telefone, lista.logradouro, lista.cidade, lista.estado))
        self.__db.connection.commit()
        return lista

    def relatorio_clientes(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_JUNCAO)
        atividade = cursor.fetchall()
        return atividade

def traduz_atividade(atividades):
    def cria_atividade_com_tupla(tupla):
        return Clientes(tupla[0],tupla[1],tupla[2],tupla[3],tupla[4],tupla[5],tupla[6])
        
    return list(map(cria_atividade_com_tupla, atividades))   
