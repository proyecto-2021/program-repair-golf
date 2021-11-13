from . import users
from .userdao import add_user, get_user_by_name, get_all_users, get_user_by_id, remove_user_by_id
from flask.views import MethodView
from flask import jsonify, request, make_response
from flask_jwt import jwt_required, current_identity


class UserAPI(MethodView):

    def post(self):
        username = request.json['username']
        # TODO: Should check that password is a valid password
        password = request.json['password']
        try:
            add_user(username, password)
            stored_user = get_user_by_name(username)
            return make_response(jsonify({'id': stored_user.id, 'username': stored_user.username}), 200)
        except ValueError:
            return make_response(jsonify({'error': 'user creation error'}), 400)

    @jwt_required()
    def get(self):
        res = []
        print(f'Id of user making the request: {current_identity}')
        for user in get_all_users():
            res.append({'id': user.id, 'username': user.username})
        return make_response(jsonify(res), 200)

    @jwt_required()
    def delete(self, user_id):
        user = get_user_by_id(user_id)
        if user is not None:
            remove_user_by_id(user_id)
            return make_response(jsonify(user.to_dict()), 200)

        return make_response(jsonify({'error': f'no user with id {user_id}'}), 400)


user_view = UserAPI.as_view('user_api')
users.add_url_rule('/users', view_func=user_view, methods=['POST', 'GET'])
users.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['DELETE'])
