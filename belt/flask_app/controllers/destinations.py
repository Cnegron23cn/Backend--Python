from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.model_destinaton import Destination
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/create_trip') #CREATE  RENDER PAGE
def create_recipe_page():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('/create_trip.html')

@app.route('/add_trip', methods=['POST']) #CREATE TRIP
def add_trip():
    data = {
        'destination': request.form['destination'],
        'start_date': request.form['start_date'],
        'end_date': request.form['end_date'],
        'plan': request.form['plan'],
        'user_id': session['user_id']
    }
    Destination.create(data)
    if Destination.validate(request.form): #VALIDATION FOR CREATE
        return redirect('/dashboard')
    return redirect ('/create_trip')

@app.route('/edit/<int:id>') #EDIT RECIPE PAGFE
def edit_page(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {"id": id}
    plan = Destination.get_one(data)
    return render_template('/edit_trip.html', plan = plan)


@app.route('/edit_trip/<int:id>', methods=['POST']) #EDIT RECIPE BY ID
def edit_trip(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if Destination.validate(request.form):
        Destination.update(request.form, id)
        return redirect ('/dashboard')
    return redirect(f"/edit/{session['user_id']}")

@app.route('/show/<int:id>') # READ PAGE
def show(id):
    data = { 'id': id }
    return render_template('/show_trip_info.html', show = Destination.get_one(data))

@app.route('/delete/<int:id>') #DELETE BY ID
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    Destination.delete(id)
    return redirect('/dashboard')


