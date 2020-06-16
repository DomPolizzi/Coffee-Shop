import os
from flask import (
    Flask,
    request,
    jsonify,
    abort,
    request,
    Response
)
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth, get_token_auth_header

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()

# ===================
# ROUTES
# ===================

# Get Drinks


@app.route('/drinks')
def retrieve_drinks():

    drinks = Drink.query.all()

    if len(drinks) == 0:
        print("no drinks found")
        abort(401)

    drink_format = [drink.short() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': drink_format
    })

# Get Drink-Detail


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):

    drinks = Drink.query.all()

    if len(drinks) == 0:
        print("no drinks found")
        abort(404)

    drink_format = [drink.long() for drink in drinks]

    return jsonify({
        'sucess': True,
        'drinks': drink_format
    })

# Post Drink


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(payload):

    body = request.json
    new_drink = body['title']
    new_recipe = body['recipe']

    try:
        drink = Drink(title=new_drink, recipe=json.dumps(new_recipe))
        drink.insert()

    except Exception:
        abort(400)

    return jsonify({
        "success": True,
        "drinks": drink.long()
    })


# Patch Drinks

@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink_by_id(*args, **kwargs):

    body = request.get_json()
    id = kwargs['id']
    drink = Drink.query.filter_by(id=id).one_or_none()

    if drink is None:
        abort(404)

    if 'title' in body:
        drink.title = body['title']

    if 'recipe' in body:
        drink.recipe = json.dumps(body['recipe'])

    try:
        drink.insert()

    except Exception:
        abort(400)

    drink = [drink.long()]

    return jsonify({
        'success': True,
        'drinks': drink
    })


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    drink = Drink.query.filter(Drink.id == id).one_or_none()

    if not drink:
        abort(404)

    try:
        drink.delete()
    except:
        abort(400)

    return jsonify({
        'success': True,
        'delete': id
    }), 200


# =================================================================
#  Error Handlers
# =================================================================

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": 'Unathorized'
    }), 401


@app.errorhandler(404)
def unreachable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not Found"
    }), 404


@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "Not Allowed"
    }), 405


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Server Error'
    }), 500


@app.errorhandler(AuthError)
def auth_error(auth):
    a_error = jsonify(auth.error)
    a_error.status_code = auth.status_code
    return a_error
