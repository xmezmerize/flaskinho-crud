from flask import Flask, render_template, request, redirect, url_for
from db import db
from models import Contato

# cria a aplicação flask
app = Flask(__name__)
# config do BD
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///dados.db"
# liga o bd à aplicação flask
db.init_app(app)


# read
@app.route("/")
def home():
    contatos = db.session.query(Contato).all()
    return render_template("home.html", contatos=contatos)

# create
@app.route("/registrar", methods=['GET', 'POST'])
def registrar():
    if request.method == 'GET':
        return render_template("/register.html")
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        telefone = request.form['telefoneForm']
        
        novo_contato = Contato(nome=nome, telefone=telefone)
        db.session.add(novo_contato)
        db.session.commit()
        
        return redirect(url_for('home'))
    
# delete
@app.route("/deletar/<int:id>")
def delete(id):
    contato = db.session.query(Contato).filter_by(id=id).first()
    db.session.delete(contato)
    db.session.commit()
    
    return redirect(url_for('home'))

# editar
@app.route("/editar/<int:id>", methods=['GET', 'POST'])
def editar(id):
    contato = db.session.query(Contato).filter_by(id=id).first()
    if request.method == "GET":
        return render_template('editar.html', contato=contato)
    elif request.method == 'POST':
        nome = request.form['nomeForm']
        telefone = request.form['telefoneForm']
        
        contato.nome = nome
        contato.telefone = telefone
        db.session.commit()
        
        return redirect(url_for('home'))

# servidor
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)