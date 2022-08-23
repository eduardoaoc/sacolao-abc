from flask_restful import Resource, reqparse
from models.user import UserModel
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp 
from blacklist import BLACKLIST

argumentos= reqparse.RequestParser()
argumentos.add_argument('login', type=str, required=True, help='The field "LOGIN" cannot be left.')
argumentos.add_argument('password', type=str, required=True, help='The field "PASSWORD" cannot be left.')

class User(Resource):
    #/users/user_id
    def get(self, user_id):
        user= UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'Message': 'User not found.'}, 404     
    @jwt_required()
    def delete(self, user_id):
        user= UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return{'Message':'An error ocurred trying to delete user.'}, 500     
            return{'Message':'User deleted.'}
        return{'Message': 'User not found'}, 404

class UserRegister(Resource):
    #/register
    def post(self):

        dados= argumentos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return{'Message':f"The login '{dados['login']}' already exists."}

        user= UserModel(**dados)
        user.save_user()
        return{'Message':'User created successfully.'}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados= argumentos.parse_args()
        user= UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.password, dados['password']):
            token_acess= create_access_token(identity=user.user_id)
            return {'Acess_token': token_acess}, 200
        return{'Message':'The username or password is incorrect.'}, 401    


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jwt_id= get_jwt()['jti']  #JWT Token Identifier 
        BLACKLIST.add(jwt_id)
        return{'Message':'Logged out successfuly!'}, 200