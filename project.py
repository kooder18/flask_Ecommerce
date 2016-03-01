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
@app.route('/catalog/')
def showCategories():
    categories = session.query(Category).all()
    items = session.query(Item).all()
    return render_template('categories.html', categories = categories, items = items)

@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name = request.form['categoryName'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        categories = session.query(Category).all()
        return render_template('newCategory.html', categories = categories)

'''
Displays the category along with all of the items that are listed in
that category. Can edit or delete items.

'''
@app.route('/catalog/<string:name>/edit/')
def editCategory(name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name = name).one()
    id = category.id
    items = session.query(Item).filter_by(category_id = category.id)
    return render_template('categoryDisplay.html', category=category, categories = categories, items = items)




@app.route('/catalog/item/new/', methods=['GET', 'POST'])
def createItem():
    categories = session.query(Category).all()
    return render_template('itemAdd.html', categories = categories)

@app.route('/catalog/<string:name>/<string:item_name>/edit/', methods=['GET', 'POST'])
def editCategoryItem(name, item_name):
    editedItem = session.query(Item).filter_by(item_name = name).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showCategories', name = name, ))


@app.route('/catalog/<string:name>/<string:item_name>/delete/')
def deleteCategoryItem(name, item_name):
    return "This is where items are deleted"


if __name__ =='__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
