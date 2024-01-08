from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'belt_exam'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#CRUD +1
    @classmethod
    def get_all(cls):
        query= 'SELECT * FROM user;'
        results = connectToMySQL(db).query_db(query)
        user = []
        for row in results:
            user.append(cls[row])
        return user

    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO user (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM user WHERE id = %(id)s;'
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT *  FROM user WHERE email =%(email)s;'
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:  #USE THIS TO VALIDATE LOGIN
            return False
        return cls(results[0])

    @staticmethod
    def validate_register(data):
        is_valid = True
        query = "SELECT * FROM user WHERE email = %(email)s;" #CHECK IF EMAIL IS ALREADT TAKEN
        results = connectToMySQL(db).query_db(query, data)
        if len(results) != 0:
            flash("Email already taken", 'register')
            is_valid=False
        if not EMAIL_REGEX.match(data['email']): #CHECK IF EMAIL FORMAT IS CORRECT
            flash("Invalid Email", 'register')
            is_valid=False
        if len(data['first_name']) < 3:    #CHECK FOR PROPER FIRST NAME
            flash("First name must be at least 3 characters",'register')
            is_valid= False
        if len(data['last_name']) < 3:     #CHECK FOR PROPER LAST NAME
            flash("Last name must be at least 3 characters",'register')
            is_valid= False
        if len(data['password']) < 8:      # #CHECK FOR PROPER PASSWORD
            flash("Password must be at least 8 characters", 'register')
            is_valid= False
        if data['password'] != data['confirm_password']: #CONFIRM THE PASWORD
            flash("Passwords do not match",'register')
        return is_valid

