from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from UserRepository import UserRepository
from preserver import UserPreserver
from user import User
import json

app = Flask(__name__)
api = Api(app)


class UsersApiController(Resource):

    __user_repository__: UserRepository = None
    __user_preserver__: UserPreserver = None

    def __init__(self, repository: UserRepository, preserver: UserPreserver):
        self.__user_repository__ = repository
        self.__user_preserver__ = preserver

    def put(self):
        # this is for from data
        # parser = reqparse.RequestParser()
        # parser.add_argument('username', type=str)
        # parser.add_argument('password', type=str)
        # parser.add_argument('email', type=str)
        # args = parser.parse_args()

        # this is for raw.
        args = request.get_json(force=True)
        username = args['username']
        password = args['password']
        email = args['email']

        usr = User()
        usr.username = username
        usr.password = password
        usr.email = email

        result = Result()
        if usr is None or usr.username == '':
            result.Success = False
            result.Message = 'Invalid user'
            result.Code = 201
        elif self.__contains_usr__(usr.username):
            result.Success = False
            result.Message = '{arg1} has existed.'.format(arg1=usr.username)
            result.Code = 200
        else:
            self.__user_repository__.add(usr)
            result.Success = True
            result.Message = '{arg1} has been added.'.format(arg1=usr.username)
            result.Code = 200
            self.__user_preserver__.save(self.__user_repository__.get_users())
            j_obj = json.dumps(result.__dict__)
        return j_obj, result.Code

    def post(self):
        # this is for from data
        # parser = reqparse.RequestParser()
        # parser.add_argument('username', type=str)
        # parser.add_argument('password', type=str)
        # parser.add_argument('email', type=str)
        # args = parser.parse_args()

        # this is for raw.
        args = request.get_json(force=True)
        username = args['username']
        password = args['password']
        email = args['email']

        usr = User()
        usr.username = username
        usr.password = password
        usr.email = email

        result = Result()

        if usr is None or usr.username == '':
            result.Success = False
            result.Message = 'Invalid user'
            result.Code = 201
        elif self.__contains_usr__(usr.username):
            self.__user_repository__.update(usr)
            self.__user_preserver__.save(self.__user_repository__.get_users())
            result.Success = True
            result.Message = '{arg1} has been updated'.format(arg1=usr.username)
            result.Code = 200
        else:
            self.__user_repository__.add(usr)
            self.__user_preserver__.save(self.__user_repository__.get_users())
            result.Success = True
            result.Message = '{arg1} has been added'.format(arg1=usr.username)
            result.Code = 200

        j_obj = json.dumps(result.__dict__)
        return j_obj , result.Code

    def get(self):
        users = self.__user_repository__.get_users()
        array = []
        for usr in users:
            if type(usr) is User:
                usr_json = json.dumps(usr.__dict__)
                array.append(usr_json)

        return array, 200

    def __contains_usr__(self, username):
        contains: bool = False
        for usr in self.__user_repository__.get_users():
            if usr.username == username:
                contains = True
                break
        return contains


class UserApiController(Resource):

    __user_repository__: UserRepository = None

    def __init__(self, repository: UserRepository):
        self.__user_repository__ = repository

    def get(self, username: str):
        result = Result()
        if username == '':
            result.Success = False
            result.Code = 201
            result.Message = 'Invalid username'
            j_obj = json.dumps(result.__dict__)
            return j_obj, result.Code
        elif self.__contains_usr__(username):
            usr = self.__user_repository__.get_user(username)
            j_obj = json.dumps(usr.__dict__)
            return j_obj, 200
        else:
            result.Success = False
            result.Message = '{arg1} is not in repository'.format(arg1=username)
            result.Code = 200
            j_obj = json.dumps(result.__dict__)
            return j_obj, result.Code

    def __contains_usr__(self, username):
        contains: bool = False
        for usr in self.__user_repository__.get_users():
            if usr.username == username:
                contains = True
                break
        return contains


class Result(object):
    Success: bool = False
    Message: str = ''
    Code: int = 201


if __name__ == '__main__':
    user_repository = UserRepository()
    user_preserver = UserPreserver()
    users = user_preserver.load()
    for usr in users:
        user_repository.add(usr)
    users_controller_args = {'repository': user_repository, 'preserver': user_preserver}
    api.add_resource(UsersApiController, '/users', resource_class_kwargs=users_controller_args)

    user_controller_args = {'repository': user_repository}
    api.add_resource(UserApiController, '/user/<username>', resource_class_kwargs=user_controller_args)
    app.run('localhost', 9981, debug=True)
