#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

### AUTHENTICATION HANDLING ###

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        
        # Retrieve user by username
        user = User.query.filter_by(name=username).first()
        
        if user:
            session['user_id'] = user.id
            return jsonify(user.to_dict()), 200
        else:
            return {'error': 'Unauthorized'}, 401

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {}, 204

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            user = User.query.get(user_id)
            if user:
                return jsonify(user.to_dict()), 200
        return {'error': 'Unauthorized'}, 401

### ARTICLE & SESSION HANDLING ###

class ClearSession(Resource):
    def delete(self):
        session['page_views'] = 0
        session['user_id'] = None
        return {}, 204

class IndexArticle(Resource):
    def get(self):
        articles = [article.to_dict() for article in Article.query.all()]
        return articles, 200

class ShowArticle(Resource):
    def get(self, id):
        # Set initial page views using a ternary operator
        session['page_views'] = session.get('page_views', 0)
        session['page_views'] += 1

        if session['page_views'] <= 3:
            # Fetch the article by id
            article = Article.query.get(id)
            if article:
                return jsonify(article.to_dict()), 200
            return {'message': 'Article not found'}, 404
        else:
            return {'message': 'Maximum pageview limit reached'}, 401

### ROUTES ###

api.add_resource(Login, '/login')
api.add_resource(Logout, '/logout')
api.add_resource(CheckSession, '/check_session')
api.add_resource(ClearSession, '/clear')
api.add_resource(IndexArticle, '/articles')
api.add_resource(ShowArticle, '/articles/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
