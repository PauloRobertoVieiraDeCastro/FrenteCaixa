from produtos import*
SQL_BUSCA = 'SELECT ide, SKU, produto, preco, quantidade FROM precos_get'
SQL_CRIA = 'INSERT INTO precos_get (SKU, produto, preco, quantidade) VALUES (%s, %s, %s, %s)'
SQL_ATUALIZAR = 'UPDATE precos_get SET SKU = %s, produto=%s, preco=%s, quantidade=%s WHERE ide = %s'
SQL_DELETA = 'DELETE FROM precos_get WHERE ide = %s'
SQL_POR_ID = 'SELECT ide, SKU, produto, preco, quantidade FROM precos_get WHERE ide = %s'
SQL_COUNT = 'SELECT COUNT(ident) AS total FROM vendas_get'
SQL_VENDAS = 'SELECT SUM(preco) AS vendas FROM vendas_get'
SQL_MAX = 'SELECT produto, COUNT(produto) AS cont FROM vendas_get GROUP BY produto ORDER BY cont DESC;'

class DAO:
    def __init__(self, db):
        self.__db = db

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA)
        atividade = traduz_atividade(cursor.fetchall())
        return atividade

    def apagar(self,ide):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_DELETA, (ide,))
        self.__db.connection.commit()

    def busca_por_id(self, ide):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_POR_ID, (ide,))
        tupla = cursor.fetchone()
        return Produtos(tupla[1],tupla[2],tupla[3], tupla[4], ide=tupla[0])

    def salvar(self,lista):
        cursor = self.__db.connection.cursor() #cursor para acessar o db
        if lista.ide:
            cursor.execute(SQL_ATUALIZAR,(lista.sku,lista.produto,lista.preco,lista.quantidade,lista.ide))
        else:
            cursor.execute(SQL_CRIA, (lista.sku, lista.produto, lista.preco, lista.quantidade))
        self.__db.connection.commit()
        return lista

    def dash_count(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_COUNT)
        atividade_count = cursor.fetchall()
        return atividade_count

    def dash_soma_vendas(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_VENDAS)
        atividade_select = cursor.fetchall()
        return atividade_select

    def dash_max(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_MAX)
        atividade_max = cursor.fetchall()
        return atividade_max

   

def traduz_atividade(atividades):
    def cria_atividade_com_tupla(tupla):
        return Produtos(tupla[1],tupla[2],tupla[3], tupla[4], ide=tupla[0])
        
    return list(map(cria_atividade_com_tupla, atividades))   
