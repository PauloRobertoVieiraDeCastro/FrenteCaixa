from compras import*
SQL_BUSCA = 'SELECT ident, cupom, SKU, produto, preco, forma_pagamento, data_compra FROM vendas_get'
SQL_CRIA = 'INSERT INTO vendas_get (cupom, SKU, produto, preco, forma_pagamento) VALUES (%s, %s, %s, %s, %s)'

class DAO_COMPRAS:
    def __init__(self, db):
        self.__db = db

    def listar_compras(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA)
        atividade = traduz_atividade(cursor.fetchall())
        return atividade

    def salvar_compras(self,lista):
        cursor = self.__db.connection.cursor() #cursor para acessar o db
        cursor.execute(SQL_CRIA, (lista.cupom, lista.sku1, lista.produto1, lista.compra, lista.forma_pagamento))
        self.__db.connection.commit()
        return lista

    def relatorio_vendas(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA)
        atividade = cursor.fetchall()
        return atividade


def traduz_atividade(atividades):
    def cria_atividade_com_tupla(tupla):
        return Compra(tupla[1],tupla[2],tupla[3], tupla[4], tupla[5], tupla[6], ident=tupla[0])
        
    return list(map(cria_atividade_com_tupla, atividades))   

