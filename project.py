#!/usr/bin/python
from flask import (Flask, render_template, request, redirect,
                   jsonify, url_for, flash)
from sqlalchemy import create_engine, asc, and_, exc
from sqlalchemy.orm import sessionmaker
from database_create import Base, Genre, Game, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"


# Connect to Database and create database session
engine = create_engine('sqlite:///gameCatalog.db?check_same_thread=False')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
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
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already '
                                 'connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: \
               150px;-webkit-border-radius: 150px;-moz-border-radius: \
               150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session[
                                         'email']).one_or_none()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one_or_none()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one_or_none()
        return user.id
    except (exc.StatementError):
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for '
                                 'given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Genre Information
@app.route('/genre/<genre_name>/game/JSON')
def genreGamesJSON(genre_name):
    genre = session.query(Genre).filter_by(name=genre_name).one_or_none()
    games = session.query(Game).filter_by(
        genre_id=genre.id).all()
    return jsonify(Games=[ga.serialize for ga in games])


@app.route('/genre/<genre_name>/game/<game_name>/JSON')
def gameJSON(genre_name, game_name):
    genre = session.query(Genre).filter_by(name=genre_name).one_or_none()
    Game_Item = session.query(Game).filter_by(name=game_name).filter_by(
                genre_id=genre.id).one_or_none()
    return jsonify(Game=Game_Item.serialize)


@app.route('/genre/JSON')
def genresJSON():
    genre = session.query(Genre).all()
    return jsonify(genres=[g.serialize for g in genre])


# Show all genres
@app.route('/')
@app.route('/genre/')
def showGenres():
    genres = session.query(Genre).order_by(asc(Genre.name))
    if 'username' not in login_session:
        return render_template('publicGenres.html', genres=genres)
    else:
        return render_template('genres.html', genres=genres)


# Create a new Genre
@app.route('/genre/new/', methods=['GET', 'POST'])
def newGenre():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        genreName = request.form['name']
        if genreName == '':
            flash('New Genre name can not be blank')
        else:
            newGenre = Genre(
                             name=request.form['name'],
                             user_id=login_session['user_id'])
            session.add(newGenre)
            flash('New Genre %s Successfully Created' % newGenre.name)
            session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('newGenre.html')


# Edit a genre
@app.route('/genre/<genre_name>/edit/', methods=['GET', 'POST'])
def editGenre(genre_name):
    editedGenre = session.query(
        Genre).filter_by(name=genre_name).one_or_none()
    if 'username' not in login_session:
        return redirect('/login')
    if editedGenre.user_id != login_session['user_id']:
        flash('you are not authorized to edit this genre. Please create your '
              'own genre in order to edit.')
        return redirect(url_for('showGenres'))
    if request.method == 'POST':
        if request.form['name']:
            editedGenre.name = request.form['name']
            flash('Genre Successfully Edited %s' % editedGenre.name)
            return redirect(url_for('showGenres'))
    else:
        return render_template('editGenre.html', genre=editedGenre)


# Show a game
@app.route('/genre/<genre_name>/')
@app.route('/genre/<genre_name>/game/')
def showGame(genre_name):
    genre = session.query(Genre).filter_by(name=genre_name).one_or_none()
    creator = getUserInfo(genre.user_id)
    games = session.query(Game).filter_by(
        genre_id=genre.id).all()
    if 'username' not in login_session or \
       creator.id != login_session['user_id']:
        return render_template('publicGame.html', games=games, genre=genre,
                               creator=creator)
    else:
        return render_template('game.html', games=games, genre=genre,
                               creator=creator)


# Delete a genre
@app.route('/genre/<genre_name>/delete/', methods=['GET', 'POST'])
def deleteGenre(genre_name):
    genreToDelete = session.query(
        Genre).filter_by(name=genre_name).one_or_none()
    if 'username' not in login_session:
        return redirect('/login')
    if genreToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized \
                to delete this genre. Please create your own genre in order \
                to delete.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        games = session.query(Game).filter_by(name=genre_name)
        for game in games:
            session.delete(game)
        session.delete(genreToDelete)
        flash('%s Successfully Deleted' % genreToDelete.name)
        session.commit()
        return redirect(url_for('showGenres', genere_name=genre_name))
    else:
        return render_template('deleteGenre.html', genre=genreToDelete)


# Create a new game item
@app.route('/genre/<genre_name>/game/new/', methods=['GET', 'POST'])
def newGame(genre_name):
    if 'username' not in login_session:
        return redirect('/login')
    genre = session.query(Genre).filter_by(name=genre_name).one_or_none()
    if login_session['user_id'] != genre.user_id:
        return "<script>function myFunction() {alert('You are not authorized \
                to add game items to this genre. Please create your own \
                genre in order to add items.');}</script><body \
                onload='myFunction()'>"
    if request.method == 'POST':
        newItem = Game(name=request.form['name'],
                       developer=request.form['developer'],
                       description=request.form['description'],
                       genre_id=genre.id, user_id=genre.user_id)
        session.add(newItem)
        session.commit()
        flash('New Game %s Item Successfully Created' % (newItem.name))
        return redirect(url_for('showGame', genre_name=genre_name))
    else:
        return render_template('newGameItem.html', genre_name=genre_name)


# Edit a game item
@app.route('/genre/<genre_name>/game/<game_name>/edit',
           methods=['GET', 'POST'])
def editGame(genre_name, game_name):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Game).filter_by(name=game_name).one_or_none()
    genre = session.query(Genre).filter_by(name=genre_name).one_or_none()
    if login_session['user_id'] != genre.user_id:
        return "<script>function myFunction() {alert('You are not authorized \
                to edit game items to this genre. Please create your own \
                genre in order to edit items.');}</script><body \
                onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['developer']:
            editedItem.developer = request.form['developer']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Game Item Successfully Edited')
        return redirect(url_for('showGame', genre_name=genre_name))
    else:
        return render_template('editGameItem.html', genre_name=genre_name,
                               game_name=game_name, item=editedItem)


# Delete a game item
@app.route('/genre/<genre_name>/game/<game_name>/delete',
           methods=['GET', 'POST'])
def deleteGame(genre_name, game_name):
    if 'username' not in login_session:
        return redirect('/login')
    genre = session.query(Genre).filter_by(name=genre_name).one_or_none()
    itemToDelete = session.query(Game).filter_by(name=game_name).one_or_none()
    if login_session['user_id'] != genre.user_id:
        return "<script>function myFunction() {alert('You are not authorized \
                to delete game items to this genre. Please create your own \
                genre in order to delete items.');}</script><body \
                onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Game Item Successfully Deleted')
        return redirect(url_for('showGame', genre_name=genre.name))
    else:
        return render_template('deleteGameItem.html', item=itemToDelete)


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showGenres'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showGenres'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
