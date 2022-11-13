class Compra:
    def __init__(self,cupom,sku1,produto1,compra,forma_pagamento,data_compra=None,ident=None):
        self.cupom = cupom
        self.sku1 = sku1
        self.produto1 = produto1
        self.compra = compra
        self.forma_pagamento = forma_pagamento
        self.data_compra = data_compra
        self.ident = ident
