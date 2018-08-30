from user import User


class UserRepository:

    __users_list__ = [User]

    def __init__(self):
        self.__users_list__.clear()

    def add(self, usr):
        if not UserRepository.__user_valid__(usr):
            return
        self.__users_list__.append(usr)

    def remove(self, usr):
        if not UserRepository.__user_valid__(usr):
            return

        target = self.__get_exist__(usr.username)

        if target is not None:
            self.__users_list__.remove(target)

    def update(self, usr):
        if not UserRepository.__user_valid__(usr):
            return
        target = self.__get_exist__(usr.username)
        if target is not None:
            target.username = usr.username
            target.password = usr.password
            target.email = usr.email

    def get_user(self, username):
        target: User = None
        for item in self.__users_list__:
            if item.username == username:
                target = item
        return target

    def get_users(self):
        return self.__users_list__

    def __get_exist__(self, username):
        target = None
        for item in self.__users_list__:
            if item.username == username:
                target = item
        return target

    @staticmethod
    def __user_valid__(usr):
        return usr is not None and type(usr) is User
