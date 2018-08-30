import xml.etree.ElementTree as XmlTree
import os
from user import User


class UserPreserver:

    __filename__ = ''

    def __init__(self, filename=''):
        if filename == '':
            self.__filename__ = 'users.xml'

    def load(self):
        usr_list = []
        if os.path.exists(self.__filename__):
            tree = XmlTree.parse(self.__filename__)
            users_node = tree.getroot()
            user_nodes = users_node.findall('./user')
            for user_node in user_nodes:
                username = user_node.find('username').text
                password = user_node.find('password').text
                email = user_node.find('email').text
                usr = User()
                usr.username = username
                usr.password = password
                usr.email = email
                usr_list.append(usr)
        return usr_list

    def save(self, usr_list):
        users_node = XmlTree.Element('users')
        for usr in usr_list:
            if type(usr) is User:
                user_node = XmlTree.SubElement(users_node, 'user')
                XmlTree.SubElement(user_node, 'username').text = usr.username
                XmlTree.SubElement(user_node, 'password').text = usr.password
                XmlTree.SubElement(user_node, 'email').text = usr.email
        tree = XmlTree.ElementTree(users_node)
        tree.write(self.__filename__)

