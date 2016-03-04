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

import random, string
from flask import make_response
from flask import session as login_session
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


#Connect to Database and create Database session
APPLICATION_NAME = "Item Catalogue"

engine = create_engine('sqlite:///catalogue.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

'''
get and set functions

'''

#Function displays all categories
def getCategories():
    categories = session.query(Category).all()
    return categories

#Returns a single category based on name
def getCategory(name):
    category = session.query(Category).filter_by(name = name).one()
    return category

#Returns all items
def getAllItems():
    items = session.query(Item).all()
    return items

#Returns all items in a given category
def getItems(id):
    items = session.query(Item).filter_by(category_id = id)
    return items

#Gets the top 15 items sorted by time added
def getItems_time():
    items = session.query(Item).order_by(Item.myTime.desc()).limit(15)
    return items

#Creates a random 32 digit token
def tokenMaker():
    token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    return token

'''
This block is the routes for the main page and
categories
'''
@app.route('/')
@app.route('/catalog/')
def showCategories():
    categories = getCategories()
    items = getItems_time()
    return render_template('categories.html', categories = categories, items = items)

@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name = request.form['categoryName'])
        session.add(newCategory)
        session.commit()
        return redirect(url_for('showCategories'))
    else:
        categories = getCategories()
        return render_template('newCategory.html', categories = categories)

'''
Displays the category along with all of the items that are listed in
that category. Can edit or delete items.

'''
@app.route('/catalog/<string:name>/edit/')
def editCategory(name):
    categories = session.query(Category).all()
    category = getCategory(name)
    id = category.id
    items = getItems(id)
    return render_template('categoryDisplay.html', category=category, categories = categories, items = items)



#Adds a new item
@app.route('/catalog/item/new/', methods=['GET', 'POST'])
def createItem():
    if request.method == 'POST':
        category = request.form['category']
        #Get category object from db that is equal to name selected from form
        category1 = getCategory(category)
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
    category = getCategory(name)
    #Query all categories to populate drop down list in template
    categories = getCategories()
    if request.method == 'POST':
        if request.form['itemName']:
            item.name = request.form['itemName']
        if request.form['itemdescript']:
            item.description = request.form['itemdescript']
        if request.form['category']:
            category = request.form['category']
            #Search database to get category object
            category1 = getCategory(name)
            item.category = category1
        session.add(item)
        session.commit()
        return redirect(url_for('editCategory', name = item.category.name))
    else:
        return render_template('itemEdit.html', item =item, categories = categories)


#This route deletes items

@app.route('/catalog/<string:name>/<string:item_name>/delete/', methods =['GET', 'POST'])
def deleteCategoryItem(name, item_name):
    category = getCategory(name)
    itemdelete = session.query(Item).filter_by(name = item_name).one()
    if request.method == 'POST':
        session.delete(itemdelete)
        session.commit()
        return redirect(url_for('editCategory', name = category.name))
    else:
        return render_template('deleteItem.html', name = item_name)


#Routes for API endpoints
@app.route('/catalog/categories/JSON')
# JSON endpoint for all categories
def catalogJSON():
    categories = getCategories()
    return jsonify(categories=[i.serialize for i in categories])

@app.route('/catalog/<string:name>/JSON')
# JSON endpoint for all items in a category
def categoryItemsJSON(name):
    category = getCategory(name)
    items = getItems(category.id)
    return jsonify(Category= category.name, items = [i.serialize for i in items])



#The following routes pertain to user authentication and login
@app.route('/login')
def showLogin():
    state = tokenMaker()
    login_session['state'] = state
    return render_template('login.html')



@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        print("Error1")
        return response
    code = request.data
    try:
    # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        print("Error2")
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
            % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)

        response.headers['Content-Type'] = 'application/json'
        #Verify that the access code is used for the intended user
        gplus_id = credentials.id_token['sub']
        if result['user_id'] != gplus_id:
            response = make_response(
                json.dumps("Token's user ID doesn't match given user ID."),
            401)
        response.headers['Content-Type'] = 'application/json'
        print("Error3")
        return response
    #Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's!"),
        401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response
    #Check to see if the user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected'),
        200)
        response.headers['Content-Type'] = 'application/json'
    #Store the access token in the session for later use.
    login_session['credentials'] = credentials
    login_session['gplus_id'] = gplus_id

    #Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt':'json'}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' "style = width: 300px; height: 300px; border-radius: 150px; -webkit-border-radius: 150px; -moz-border-radius: 150px;">'
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

#The following are routes for basic error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ =='__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
