#This file will contain the routes, to perform CRUD operations on
#All of the items in the catalog

from flask import Flask, Blueprint, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Item

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

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



#Adds a new item
@app.route('/catalog/item/new/', methods=['GET', 'POST'])
def createItem():
    if request.method == 'POST':
        category = request.form['category']
        #Get category object from db that is equal to name selected from form
        category1 = session.query(Category).filter_by(name = category).one()
        newItem = Item(name = request.form['itemName'], description =
        request.form['itemdescript'], category = category1)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        categories = session.query(Category).all()
        return render_template('itemAdd.html', categories = categories)

#Displays item information has links to edit delete item
@app.route('/catalog/<string:name>/<string:item_name>/')
def showItem(name, item_name):
    item = session.query(Item).filter_by(name = item_name).one()
    return render_template('itemDisplay.html', item = item)

#Allows user to edit item
@app.route('/catalog/<string:name>/<string:item_name>/edit/', methods=['GET', 'POST'])
def editCategoryItem(name, item_name):
    item = session.query(Item).filter_by(name = item_name).one()
    category = session.query(Category).filter_by(name = name).one()
    #Query all categories to populate drop down list in template
    categories = session.query(Category).all()
    if request.method == 'POST':
        if request.form['itemName']:
            item.name = request.form['itemName']
        if request.form['itemdescript']:
            item.description = request.form['itemdescript']
        if request.form['category']:
            category = request.form['category']
            #Search database to get category object
            category1 = session.query(Category).filter_by(name = category).one()
            item.category = category1
        session.add(item)
        session.commit()
        return redirect(url_for('editCategory', name = item.category.name))
    else:
        return render_template('itemEdit.html', item =item, categories = categories)


#This route deletes items

@app.route('/catalog/<string:name>/<string:item_name>/delete/', methods =['GET', 'POST'])
def deleteCategoryItem(name, item_name):
    category = session.query(Category).filter_by(name = name).one()
    itemdelete = session.query(Item).filter_by(name = item_name).one()
    if request.method == 'POST':
        session.delete(itemdelete)
        session.commit()
        return redirect(url_for('editCategory', name = category.name))
    else:
        return render_template('deleteItem.html', name = item_name)


#Routes for API endpoints
@app.route('/catalog/categories/JSON')
def catalogJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[i.serialize for i in categories])

@app.route('/catalog/<string:name>/JSON')
def categoryItemsJSON(name):
    category = session.query(Category).filter_by(name = name).one()
    items = session.query(Item).filter_by(category_id = category.id)
    return jsonify(Category= category.name, items = [i.serialize for i in items])

#The following are routes for basic error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ =='__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
