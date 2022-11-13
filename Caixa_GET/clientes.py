class Clientes:
    def __init__(self,codigo,cpf,nome,telefone=None,logradouro=None,cidade=None,estado=None):
        self.codigo = codigo
        self.cpf = cpf
        self.nome = nome
        self.telefone = telefone
        self.logradouro = logradouro
        self.cidade = cidade
        self.estado = estado
