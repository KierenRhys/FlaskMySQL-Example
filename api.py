from flask import Flask
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL

app = Flask(__name__)
api = Api(app)

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'ItemListDb'
app.config['MYSQL_DATABSE_HOST'] = 'localhost'

mysql.init_app(app)

class CreateUser(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = args['password']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spCreateUser', (_userEmail, _userPassword))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return {'status': 200, 'Message': 'User creation success'}
            else:
                return {'status': 100, 'Message': str(data[0])}

        except Exception as e:
            return {'error': str(e)}

class AuthenticateUser(Resource):
    def post(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('email', type=str, help='Email address to create user')
            parser.add_argument('password', type=str, help='Password to create user')
            args = parser.parse_args()

            _userEmail = args['email']
            _userPassword = args['password']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spAuthenticateUser', (_userEmail,))
            data = cursor.fetchall()

            if len(data) > 0:
                if(str(data[0][2])==_userPassword):
                    return {'status': 200, 'UserId': str(data[0][0])}
                else:
                    return {'status': 100, 'Message': 'Authentication failure'}

        except Exception as e:
            return {'error': str(e)}

class AddItem(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            parser.add_argument('item', type=str)
            args = parser.parse_args()

            _userId = args['id']
            _item = args['item']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spAddItems', (_userId, _item))
            data = cursor.fetchall()

            conn.commit()
            return {'status': 200, 'Message': 'Success'}
    
        except Exception as e:
            return {'error': str(e)}

class GetAllItems(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            args = parser.parse_args()

            _userId = args['id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spGetAllItems', (_userId,))
            data = cursor.fetchall()

            items_list=[]
            for item in data:
                i = {
                    'Id': item[0],
                    'Item': item[1]
                }
                items_list.append(i)

            return {'status': 200, 'Items': items_list}

        except Exception as e:
            return {'error': str(e)}

class GetOneItem(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int)
            args = parser.parse_args()

            _itemId = args['id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spGetOneItem', (_itemId,))
            data = cursor.fetchall()

            item = {
                'Id': data[0][0],
                'IdUser': data[0][1],
                'ItemName': data[0][2]
            }

            if len(data) > 0:
                return {'status': 200, 'Item': item}
            else:
                return {'status': 100, 'Message': 'Item does\'nt exist'}

        except Exception as e:
            return {'error': str(e)}

class UpdateItem(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int)
            parser.add_argument('item', type=str)
            args = parser.parse_args()

            _itemId = args['id']
            _itemName = args['item']
           
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spUpdateItem', (_itemId, _itemName))

            conn.commit()
            return {'status': 200, 'Message': 'Item updated'}

        except Exception as e:
            return {'error': str(e)}

class DeleteItem(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=int)
            args = parser.parse_args()

            _itemId = args['id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('spDeleteItem', (_itemId,))

            conn.commit()
            return {'status': 200, 'Message': 'Item deleted'}

        except Exception as e:
            return {'error': str(e)}

api.add_resource(CreateUser, '/CreateUser')
api.add_resource(AuthenticateUser, '/AuthenticateUser')
api.add_resource(AddItem, '/AddItem')
api.add_resource(GetAllItems, '/ListItems')
api.add_resource(GetOneItem, '/Item')
api.add_resource(DeleteItem, '/DeleteItem')
api.add_resource(UpdateItem, '/UpdateItem')

if __name__ == '__main__':
    app.run(debug=True)