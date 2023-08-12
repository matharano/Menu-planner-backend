from flask_restx import Api, fields
from flask_restx import Model as FlaskModel

class Model(FlaskModel):
    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
    
    def to_sql(self, data:dict) -> list:
        """Parse data into sql format - as tuple. id is always ignored. Example:
        ```
        >>> my_model = Model({"id":fields.Integer, "name":fields.String, "observation":fields.String})
        >>> my_model.to_sql({"name":"Cuiabaninho"})
        ('Cuiabaninho', '')"""
        formatted = []
        for key in self.keys():
            if key == 'id': continue
            if key in data.keys():
                formatted.append(data[key])
            else:
                formatted.append(self[key].default)
        return tuple(formatted)
    
    def from_sql(self, data:list) -> dict:
        """Parse data from sql format to json. Example:
        ```
        >>> my_model = Model('dishes', {'dishes':fields.List(fields.Nested({"id":fields.Integer, "name":fields.String, "observation":fields.String}))})
        >>> my_model.from_sql([(1, 'Cuiabaninho', ''), (2, 'Estrogonofe', 'Com cebola')])
        {"dishes":[{"id":0, "name":'Cuiabaninho', "observation":''}, {"id":2, "name":'Estrogonofe', "observation":'Com cebola'}]}"""
        return {self.name: [dict(zip(self.keys(), inst)) for inst in data]}

message = Model("message", {
   "message": fields.String(default='')
})

id = Model("id", {
    "id": fields.Integer
})

dish = Model('dish', {
    'id' : fields.Integer,
    'category': fields.String(required=True),
    'name': fields.String(required=True),
    'cost': fields.Integer(required=True),
    'observation': fields.String(default='')
})

dishes = Model('dishes', {
    'dishes':fields.List(fields.Nested(dish))
})