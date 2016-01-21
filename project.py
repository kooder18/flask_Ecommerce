#This file will contain the routes, to perform CRUD operations on
#All of the items in the catalog

from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Sub_Category, Item
import login_auth

#Connect to Database and create Database session
APPLICATION_NAME = "Item Catalogue"

engine = create_engine('sqlite:///catalogueitems.db')
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
    return "This is the main page"

@app.route('/category/new/', methods=['GET', 'POST'])
def newCategory():
    return "This where new categories are added"

@app.route('/category/category_id/edit')
def editCategory():
    return "This is where categories are edited"

@app.route('/category/category_id/delete')
def deleteCategory():
    return "This is where categories are deleted"

'''
This block is for the sub_category routes
'''

@app.route('/category/category_id/sub_category/')
def showSubCategories():
    return "This is where the sub categories are displayed"

@app.route('/category/category_id/sub_category/new')
def newSubCategory():
    return "This is where the sub categories are created"

@app.route('/category/category_id/sub_category/sub_category_id/edit')
def editSubCategory():
    return "This is where sub categories are edited"

@app.route('/category/category_id/sub_category/sub_category_id/delete')
def deleteSubCategory():
    return "This is where sub categories are deleted"

@app.route('/category/category_id/sub_category/sub_category_id/item')
def showItems():
    return "This is where the items are displayed"

@app.route('/category/category_id/sub_category/sub_category_id/item/new')
def createItem():
    return "This is where items are created"

@app.route('/category/category_id/sub_category/sub_category_id/item/item_id/edit')
def editItem():
    return "This is where items are edited"

@app.route('/category/category_id/sub_category/sub_category_id/item/item_id/delete')
def deleteItem():
    return "This is where items are deleted"                


if __name__ =='__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
