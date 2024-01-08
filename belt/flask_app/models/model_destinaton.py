from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db = 'belt_exam'

class Destination:
    def __init__(self, data):
        self.id = data['id']
        self.destination = data['destination']
        self.end_date = data['end_date']
        self.start_date = data['start_date']
        self.plan = data['plan']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @classmethod
    def create(cls,data):
        query = """
        INSERT INTO destination (destination, start_date, end_date, plan, user_id)
        VALUES (%(destination)s, %(start_date)s, %(end_date)s, %(plan)s, %(user_id)s);
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM destination WHERE id = %(id)s;'
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM destination;"
        results = connectToMySQL(db).query_db(query)
        plan = []
        for destination in results:
            plan.append(cls(destination))
        return plan

    @classmethod
    def update(cls,data,id):
        query =f"UPDATE destination SET destination=%(destination)s,start_date=%(start_date)s,end_date=%(end_date)s, plan = %(plan)s WHERE id = {id}"
        return connectToMySQL(db).query_db(query,data)


    @classmethod
    def delete(cls,id):
        query = "DELETE FROM destination WHERE id =%(id)s;"
        data = {'id': id}
        return connectToMySQL(db).query_db(query, data)


    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['destination']) < 3 :
            flash("Destination is required",'trip')
            is_valid= False
        if len(data['start_date']) == 0:
            flash("start date is needed",'trip')
            is_valid= False
        if len(data['end_date']) == 0:
            flash("end date is needed", 'trip')
            is_valid= False
        if len(data['plan']) < 3 :
            flash("plan  description is mandatory", 'trip')
            is_valid= False
        return is_valid

