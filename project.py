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
    output = ''
    for i in items:
        output += i.name
        output += '</br>'
        output += i.description
        output += '</br>'
    return output

@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    return "This where new categories are added"

@app.route('/category/category_id/edit')
def editCategory():
    return "This is where categories are edited"

@app.route('/category/category_id/delete')
def deleteCategory():
    return "This is where categories are deleted"

@app.route('/category/category_id/item')
def showItems():
    return "This is where the items are displayed"

@app.route('/category/category_id/item/new')
def createItem():
    return "This is where items are created"

@app.route('/category/category_id/item/item_id/edit')
def editItem():
    return "This is where items are edited"

@app.route('/category/category_id/item/item_id/delete')
def deleteItem():
    return "This is where items are deleted"


if __name__ =='__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
