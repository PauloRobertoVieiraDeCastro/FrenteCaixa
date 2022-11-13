from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask import Response
from flask import make_response
from flask import send_from_directory,send_file
from flask_mysqldb import MySQL
from flask_bcrypt import check_password_hash
from produtos import*
from dao_produtos import*
from compras import*
from dao_compras import*
from clientes import*
from dao_clientes import*
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import io


app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "cimento1"
app.config['MYSQL_DB'] = "Venda_GET"
app.config['MYSQL_PORT'] = 3306
app.secret_key = 'cimento1' #ela é essencial para deletar dados do banco
db = MySQL(app)
atividade_dao = DAO(db)
atividade_dao_compras = DAO_COMPRAS(db)
atividade_dao_clientes = DAO_CLIENTES(db)


@app.route("/",methods=['GET','POST'])
def teste():
    lista = atividade_dao.listar()
    #numeros = [i for i in range(1,len(lista)+1)]
    return render_template('main.html',lista=lista,n=len(lista))

@app.route('/deletar/<int:ide>')
def deletar(ide):
    atividade_dao.apagar(ide)
    flash("A tarefa foi removida com sucesso")
    return redirect(url_for('teste'))


@app.route('/pagar', methods=['POST',])
def pagar():
    cod_cliente = request.form['cod_cliente']
    tipo_pagamento = request.form['pagamento_forma']
    sku = [i for i in request.form.getlist('sku')]
    preco = [float(i) for i in request.form.getlist('preco')]
    produto = [i for i in request.form.getlist('produto')]
    if cod_cliente:
        for i in range(len(sku)):
            lista = Compra(cod_cliente,sku[i],produto[i],preco[i],tipo_pagamento)
            atividade_dao_compras.salvar_compras(lista)
    else:
        for i in range(len(sku)):
            lista = Compra(0,sku[i],produto[i],preco[i],tipo_pagamento)
            atividade_dao_compras.salvar_compras(lista)
    
    return redirect(url_for('teste'))

#-----------------------------------------------------página com as vendas realizadas-------------------------------------------------
@app.route('/vendas')
def vendas():
    listar = atividade_dao_compras.listar_compras()
    return render_template('vendas.html',listar=listar)

#-----------------------------------------------------página para inserir clientes no banco de dados-----------------------------------
@app.route('/clientes')
def clientes():
    lista = atividade_dao_clientes.listar_clientes()
    return render_template('inserir_cliente.html',lista=lista)

#-----------------------------------------------------inserir clientes no banco de dados-----------------------------------
@app.route('/criar_cliente', methods=['POST',])
def criar_cliente():
    cupom = request.form['cupom']
    cpf = request.form['cpf']
    nome = request.form['nome']
    tel = request.form['tel']
    logradouro = request.form['logradouro']
    cidade = request.form['cidade']
    estado = request.form['estado']
    lista = Clientes(cupom,cpf,nome,tel,logradouro,cidade,estado)
    atividade_dao_clientes.salvar_clientes(lista)
    return redirect(url_for('teste'))

#-----------------------------------------------------página para inserir produtos no banco de dados-----------------------------------
@app.route('/inserir_produto')
def inserir_produto():
    return render_template("inserir_produto.html")

#-----------------------------------------------------página para atualizar produtos no banco de dados-----------------------------------
@app.route('/editar/<int:ide>')
def editar(ide):
    lista = atividade_dao.busca_por_id(ide)
    return render_template('editar_produto.html', lista=lista)

#-----------------------------------------------------atualizar cadastro de produtos no banco de dados-----------------------------------
@app.route('/atualizar_produto', methods=['POST',])
def atualizar_produto():
    sku_produto = request.form['sku_produto']
    nome_produto = request.form['nome_produto']
    preco_produto = request.form['preco_produto']
    quantidade_produto = request.form['quantidade_produto']
    lista = Produtos(sku_produto,nome_produto,preco_produto,quantidade_produto,ide=request.form['ide'])
    atividade_dao.salvar(lista)
    return redirect(url_for('teste'))

#-----------------------------------------------------inserir cadastro de produtos no banco de dados-----------------------------------
@app.route('/criar', methods=['POST',])
def criar():
    sku_produto = request.form['sku_produto']
    nome_produto = request.form['nome_produto']
    preco_produto = request.form['preco_produto']
    quantidade_produto = request.form['quantidade_produto']
    lista = Produtos(sku_produto,nome_produto,preco_produto,quantidade_produto)
    atividade_dao.salvar(lista)
    return redirect(url_for('teste'))


#------------------------------------------------------------dashboards--------------------------------------------------

@app.route('/estatistica',methods=['POST','GET'])
def estatistica():
    lista_count = atividade_dao.dash_count()
    lista_soma = atividade_dao.dash_soma_vendas()
    lista_max = atividade_dao.dash_max()
    lista = atividade_dao_compras.relatorio_vendas()
    a,b,c,d,e,f,g,h = [],[],[],[],[],[],[],[]
    for i,j,k,l,m,n,o in lista:
        a.append(i)
        b.append(j)
        c.append(k)
        d.append(l)
        e.append(m)
        f.append(n)
        g.append(o)
       
    dff=pd.DataFrame([a,b,c,d,e,f,g]).T
    dff.columns = ["Contagem","Cupom","SKU","Produto","Preço","Pagamento","Data"]
    dff["Dia"]=[i.day_name() for i in dff['Data']]
    def custo(x,y):
        if(int(x)==0):
            return y
        elif(int(x)>=20000):
            return float(y)*0.9
        else:
            return float(y)*0.95
        
    dff['Valor_efetivo'] = [float(custo(dff.iloc[i,1],dff.iloc[i,4])) for i in range(0,len(dff['Contagem']))]
    precos = dff.groupby('Produto')['Preço'].sum()
    dfff = pd.DataFrame(precos).sort_values(by='Preço', ascending=False).head()
    dfff.reset_index(inplace=True)

    moldes = pd.DataFrame(dff[dff['Produto'].str.contains('Molde')]['Produto'].value_counts())
    moldes.reset_index(inplace=True)
    moldes.columns = ['Produto','Quantidade']
    moldes.sort_values(by='Quantidade',inplace=True,ascending=False)

    final = dff['Valor_efetivo'].sum()
    #print(final)


    lista1 = atividade_dao_clientes.relatorio_clientes()
    a1,b1,c1,d1,e1,f1,g1,x1,y1,z1 = [],[],[],[],[],[],[],[],[],[]
    for h1,i1,j1,k1,l1,m1,n1,o1,p1,q1 in lista1:
        a1.append(h1)
        b1.append(i1)
        c1.append(j1)
        d1.append(k1)
        e1.append(l1)
        f1.append(m1)
        g1.append(n1)
        x1.append(o1)
        y1.append(p1)
        z1.append(q1)
       
    dff1=pd.DataFrame([a1,b1,c1,d1,e1,f1,g1,x1,y1,z1]).T
    dff1.columns = ["Cupom","CPF","Nome","Telefone","Logradouro","Cidade","Estado","SKU","produto","preco"]
    
    
    config = {'responsive': True}
    fig1 = px.bar(dfff, y='Preço', x='Produto',title="Valor obtido nos produtos mais vendidos")
    fig2 = px.pie(dff, values="Contagem", names="Pagamento", title='Proporção das vendas')
    fig3 = px.pie(dff, values="Contagem", names="Dia", title='Proporção das vendas por dia')
    fig4 = px.bar(moldes.head(6),x='Produto',y='Quantidade',title='Moldes mais vendidos',color='Produto',text_auto=True,color_discrete_sequence=[
                 "orange","red","yellow","green", "blue", "purple"],)#px.histogram(dff1.sort_values(by='preco').head(), y='preco', x='Nome',title="Valor comprado por cliente")
    graphJSON1 = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON4 = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("dashboard_vendas.html",contagem = lista_count[0][0], soma = round(final,2), maximo = lista_max[0][0],
                           graphJSON=[graphJSON1,graphJSON2,graphJSON3,graphJSON4])

#-------------------------------------------trecho para download de relatórios-----------------------------------------------------------


@app.route('/download/report/excel')
def download_report():
    lista = atividade_dao_compras.relatorio_vendas()
    a,b,c,d,e,f,g = [],[],[],[],[],[],[]
    for h,i,j,k,l,m,n in lista:
        a.append(h)
        b.append(i)
        c.append(j)
        d.append(k)
        e.append(l)
        f.append(m)
        g.append(n)
       
    dff=pd.DataFrame([a,b,c,d,e,f,g]).T
    dff.columns = ["Id","Cupom","SKU","Produto","Preço","Pagamento","Data da compra"]
    
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')
    dff.to_excel(excel_writer=writer, index=False, sheet_name='Sheet1')
    writer.save()
    writer.close()
    # Flask create response 
    r = make_response(out.getvalue())

    # Defining correct excel headers
    r.headers["Content-Disposition"] = "attachment; filename=relatorio_vendas.xlsx"
    r.headers["Content-type"] = "application/x-xls"
    return r#Response(dfff, mimetype="application/ms-excel", headers={"Content-Disposition":"attachment;filename=relatorio_vendas.xls"})


@app.route('/download/clientes/excel_clientes')
def download_clientes():
    lista = atividade_dao_clientes.relatorio_clientes()
    a,b,c,d,e,f,g,x,y,z = [],[],[],[],[],[],[],[],[],[]
    for h,i,j,k,l,m,n,o,p,q in lista:
        a.append(h)
        b.append(i)
        c.append(j)
        d.append(k)
        e.append(l)
        f.append(m)
        g.append(n)
        x.append(o)
        y.append(p)
        z.append(q)
       
    dff=pd.DataFrame([a,b,c,d,e,f,g,x,y,z]).T
    dff.columns = ["Cupom","CPF","Nome","Telefone","Logradouro","Cidade","Estado","SKU","produto","preco"]
    
    out = io.BytesIO()
    writer = pd.ExcelWriter(out, engine='xlsxwriter')
    dff.to_excel(excel_writer=writer, index=False, sheet_name='Sheet1')
    writer.save()
    writer.close()
    # Flask create response 
    r = make_response(out.getvalue())

    # Defining correct excel headers
    r.headers["Content-Disposition"] = "attachment; filename=relatorio_clientes.xlsx"
    r.headers["Content-type"] = "application/x-xls"
    return r

if __name__=="__main__":
    app.run(debug=True)
