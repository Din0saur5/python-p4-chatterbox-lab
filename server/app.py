from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

class AllMessages(Resource):
    def get(self):
        messages_sort = Message.query.order_by(Message.created_at.asc()).all()
        
        return make_response([m.to_dict() for m in messages_sort], 200)    
        
    def post(self):
        new_msg = Message(
            body=request.json.get('body'),
            username=request.json.get('username')
        )
        db.session.add(new_msg)
        db.session.commit()
        resp_body = new_msg.to_dict()
        return make_response(resp_body, 200)
    
class MessageById(Resource):
    
    def get(self,id):
        msg = Message.query.filter(Message.id == id).first()
        if msg:
            return make_response(msg.to_dict(), 200)
        error_body = {
            "error": "404 Not found",
            "message": " There is no msg at this id"
        }
        return make_response(error_body, 404)
    
    def patch(self, id):
        msg = Message.query.filter(Message.id == id).first()
        for attr in request.json:
            setattr(msg, attr, request.json.get(attr))
        
        db.session.add(msg)
        db.session.commit()
        resp_body = msg.to_dict()
        return make_response(resp_body, 200)
    
    def delete(self, id):
        msg = Message.query.filter(Message.id == id).first()
        db.session.delete(msg)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "messgae" : "Msg deleted"
        }
        return make_response(response_body, 200)
    
api.add_resource(AllMessages, '/messages')         
api.add_resource(MessageById, '/messages/<int:id>')

@app.route('/messages/<int:id>')
def messages_by_id(id):
    return ''

if __name__ == '__main__':
    app.run(port=5001, debug=True)
