from flask import Flask
from flask_restful import Api
from resources.fruta import Frutas, Fruta

app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

api= Api(app)

@app.before_first_request
def cria_branco():
    banco.create_all()

api.add_resource(Frutas, '/fruit/all')      
api.add_resource(Fruta, '/fruit/<string:name_fruit>')      


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
