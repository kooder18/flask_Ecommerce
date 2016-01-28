#This file will contain the routes, to perform CRUD operations on
#All of the items in the catalog

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item
import login_auth

#Connect to Database and create Database session
APPLICATION_NAME = "Item Catalogue"

engine = create_engine('sqlite:///catalogue.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

'''
This block is the routes for the main page and
categories
'''
@app.route('/')
@app.route('/category/')
def showCategories():
    category = session.query(Category).first()
    items = session.query(Item).filter_by(category_id = category.id)
    return render_template('index.html', category = category, items=items)

@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    return "This where new categories are added"

@app.route('/category/<string:name>/edit/')
def editCategory(name):
    category = session.query(Category).filter_by(name = name).one()
    id = category.id
    items = session.query(Item).filter_by(category_id = category.id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.description
        output += '</br>'
    return output

@app.route('/category/<string:name>/delete/')
def deleteCategory(name):
    category = session.query(Category).filter_by(name = name).one()
    id = category.id
    items = session.query(Item).filter_by(category_id = category.id)
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.description
        output += '</br>'
    return output

@app.route('/category/<string:name>/new/', methods=['GET', 'POST'])
def newCategoryItem(name):
    if request.method == 'POST':
        newItem = Item(name = request.form['name'])
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategories'))

    else:
        return render_template('newCategoryItem.html', name = name)
    return "page to create a new item Task 1 complete"

@app.route('/category/category_id/item/new')
def createItem():
    return "This is where items are created"

@app.route('/category/<string:name>/<string:item_name>/edit/')
def editCategoryItem(name, item_name):
    return "This is where items are edited"

@app.route('/category/<string:name>/<string:item_name>/delete/')
def deleteCategoryItem(name, item_name):
    return "This is where items are deleted"


if __name__ =='__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
