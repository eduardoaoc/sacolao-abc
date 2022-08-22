from flask_restful import Resource, reqparse
from models.fruta import FruitModel

"""todas_frutas=[{
  "url_fruit": "abacaxi",
  "name": "abacaxi",
  "genus": "Ananas",
  "id": 1,
  "family": "Bromeliaces",
  "order": "Poales",
  "nutritions": {
      "carbohydrates": 12,
      "protein": 0,
      "fat": 0,
      "calories": 49,
      "sugar": 9.26
  }
},
{
  "name": "Acerola",
  "genus": "Malpighia",
  "id": 2,
  "family": "Malpighiaceae",
  "order": "Malpighiales",
  "nutritions": {
      "carbohydrates": 7.69,
      "protein": 0.4,
      "fat": 0.3,
      "calories": 32,
      "sugar": 0
  }
},
{
  "name": "Ameixa",
  "genus": "Prunus",
  "id": 3,
  "family": "Rosaceae",
  "order": "Rosales",
  "nutritions": {
      "carbohydrates": 11.42,
      "protein": 0.7,
      "fat": 0.30,
      "calories": 46,
      "sugar": 9.92
  }
},
{
  "name": "Banana",
  "genus": "Musa",
  "id": 4,
  "family": "Musaceae",
  "order": "Zingiberales",
  "nutritions": {
      "carbohydrates": 22.84,
      "protein": 1.09,
      "fat": 0.33,
      "calories": 89,
      "sugar": 12.23
  }
},
{
  "name": "Caju",
  "genus": "Anacardium",
  "id": 5,
  "family": "Anacardiaceae",
  "order": "Sapindales",
  "nutritions": {
      "carbohydrates": 11.41,
      "protein": 0.21,
      "fat": 0.14,
      "calories": 43,
      "sugar": 8.59
  }
},
{
  "name": "Damascos",
  "genus": "Prunus",
  "id": 6,
  "family": "Rosaceae",
  "order": "Rosales",
  "nutritions": {
      "carbohydrates": 11.12,
      "protein": 1.4,
      "fat": 0.39,
      "calories": 48,
      "sugar": 9.24
  }
}]"""


class Frutas(Resource):
    def get(self):#transforma o objeto em json e em cada obj dentro do banco de dados serão retornados
        return {'frutas': [fruta.json() for fruta in FruitModel.query.all()]}  #SELECT * FROM 

class Fruta(Resource):
    argumentos= reqparse.RequestParser()

    argumentos.add_argument('name', type=str, required=True, help='The field "NAME" cannot be left.')
    argumentos.add_argument('genus')
    argumentos.add_argument('id', type=int, required=True, help='The field "ID" cannot be left.')
    argumentos.add_argument('family')
    argumentos.add_argument('order')
    argumentos.add_argument('carbohydrates')
    argumentos.add_argument('protein')
    argumentos.add_argument('fat')
    argumentos.add_argument('calories')
    argumentos.add_argument('sugar')

    #todas as frutas/produtos 
    def get(self, name_fruit):
        fruta= FruitModel.find_fruit(name_fruit)
        if fruta:
            return fruta.json()
        return {'Message': 'Fruit not found.'}, 404     

    #adiciona uma nova fruta
    def post(self, name_fruit):
        #se existir uma furta com esse id ele fala que ja existe.
        if FruitModel.find_fruit(name_fruit):
            return {"Message": f"Fruit id '{name_fruit}' already exists."}, 400 #bad request
        dados= Fruta.argumentos.parse_args()
        fruit= FruitModel(name_fruit, **dados)
        try:    
            fruit.save_fruit()
        except:
            return{'Message':'An internal error ocurred trying to save fruit.'}, 500 #internal server error     
        return fruit.json()

    #atualizar dsdos de uma fruta
    def put(self, name_fruit):
        dados= Fruta.argumentos.parse_args()
        fruta_encontrada= FruitModel.find_fruit(name_fruit)
        if fruta_encontrada:
            fruta_encontrada.update_fruta(**dados)
            fruta_encontrada.save_fruit()
            return fruta_encontrada.json(), 200
        fruta= FruitModel(name_fruit, **dados)
        try:    
            fruta.save_fruit()
        except:
            return{'Message':'An internal error ocurred trying to save fruit.'}, 500 #internal server error  
        return fruta.json(), 201 

    def delete(self, name_fruit):
        fruta= FruitModel.find_fruit(name_fruit)
        if fruta:
            try:
                fruta.delete_fruta()
            except:
                return{'Message':'An error ocurred trying to delete fruit.'}, 500     
            return{'Message':'Fruit deleted.'}
        return{'Message': 'Fruit not found'}, 404
