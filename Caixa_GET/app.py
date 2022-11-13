from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask import send_from_directory,send_file
from flask_mysqldb import MySQL
from flask_bcrypt import check_password_hash
from produtos import*
from dao_produtos import*
import json
import plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


app = Flask(__name__)
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "cimento1"
app.config['MYSQL_DB'] = "Venda_GET"
app.config['MYSQL_PORT'] = 3306
app.secret_key = 'cimento1' #ela é essencial para deletar dados do banco
db = MySQL(app)
atividade_dao = DAO(db)

@app.route("/",methods=['GET','POST'])
def teste():
    lista = atividade_dao.listar()
    return render_template('main.html',lista=lista)
