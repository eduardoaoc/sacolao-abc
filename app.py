from flask import Flask, jsonify
from flask_restful import Api
from blacklist import BLACKLIST
from resources.fruta import Frutas, Fruta
from resources.user import User, UserLogin, UserRegister, UserLogout
from flask_jwt_extended import JWTManager


app= Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False

app.config['JWT_SECRET_KEY']= 'SecretKey'
app.config['JWT_BLACKLIST_ENABLED']= True

api= Api(app)
jwt= JWTManager(app)

@app.before_first_request
def cria_branco():
    banco.create_all()

@jwt.token_in_blocklist_loader
def verifica_blacklist(self, token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalidade(jwt_header, jwt_payload):
    return jsonify({'Message': 'You have been logged out.'}), 401 #UNATHORIZED

#produtos
api.add_resource(Frutas, '/fruit/all')      
api.add_resource(Fruta, '/fruit/<string:name_fruit>')     
#usuários 
api.add_resource(User, '/users/<int:user_id>')      
api.add_resource(UserRegister, '/register')      
api.add_resource(UserLogin, '/login')      
api.add_resource(UserLogout, '/logout')      


if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(app)
    app.run(debug=True)
