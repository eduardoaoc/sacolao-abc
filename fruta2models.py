from sql_alchemy import banco 
class FruitModel(banco.Model):
    __tablename__='produtos'
    
    name_fruit= banco.Column(banco.String(80), primary_key=True)
    genus= banco.Column(banco.String(50))
    id= banco.Column(banco.Integer)
    family=banco.Column(banco.String(50))
    order=banco.Column(banco.String(50))
    carbohydrates= banco.Column(banco.Float(precision=2))
    protein= banco.Column(banco.Float(precision=2))
    fat= banco.Column(banco.Float(precision=2))
    calories= banco.Column(banco.Float(precision=2))
    sugar= banco.Column(banco.Float(precision=2))
 
    def __init__(self, name_fruit, genus, id, family, order, carbohydrates, protein, fat, calories, sugar):
        self.name_fruit= name_fruit 
        self.genus= genus
        self.id= id 
        self.family= family
        self.order= order
        self.carbohydrates= carbohydrates
        self.protein= protein
        self.fat= fat 
        self.calories= calories
        self.sugar= sugar

    def json(self):
        return {
            'genus': self.genus,
            'name_fruit': self.name_fruit,
            'id': self.id,
            'family': self.family,
            'order': self.order,
            'carbohydrates': self.carbohydrates,
            'protein': self.protein,
            'fat': self.fat,
            'calories': self.calories,
            'sugar': self.sugar
        } 

    @classmethod         
    def find_fruit(cls, name_fruit):
        fruta= cls.query.filter_by(name_fruit=name_fruit).first()
        if fruta:
            return fruta
        return None

    def save_fruit(self):
        #adiciona objeto ao banco de dados
        banco.session.add(self)        
        banco.session.commit()


    #atualiza o objeto, não da pra modificar apenas o name_fruit
    def update_fruta(self, name_fruit, genus, id, family, order, carbohydrates, protein, fat, calories, sugar):
        self.name_fruit= name_fruit 
        self.genus= genus
        self.id= id 
        self.family= family
        self.order= order
        self.carbohydrates= carbohydrates
        self.protein= protein
        self.fat= fat 
        self.calories= calories
        self.sugar= sugar

    def delete_fruta(self):
        banco.session.delete(self)        
        banco.session.commit()