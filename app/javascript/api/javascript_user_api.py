from app.javascript.models.models_user import db, JavascriptUser
from flask import jsonify, make_response,request
from .. import javascript



class JavascriptUserAPI(MethodView):
    #No requiere JWT ya que puedo no estar logeado
    def post(self): 
        username = request.json['username']
        password = request.json['password']

        user_new = JavascriptUser(username = username,
                                  password = password)

        #Debo verificar que el user no exista
        db.session.add(username,password)
        db.session.commit()

        return make_response(jsonify({'username': username, 'password': password}), 200)



javascript_user_view = JavascriptUserAPI.as_view('javascript_user_api')

javascript.add_url_rule('users', view_func=javascript_user_view, methods=['POST',])