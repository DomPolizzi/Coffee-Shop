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


DRINKS_PER_PAGE = 5

# Paginiation of drinks

def paginate_drinks(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * DRINKS_PER_PAGE
    end = start + DRINKS_PER_PAGE

    drinks = [drink.format() for drinks in selection]
    current_drinks = drinks[start:end]

    return current_drinks

app = Flask(__name__)
setup_db(app)
CORS(app)


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ===================
## ROUTES
# ===================

@app.route('/drinks')
def retrieve_drinks():
    
    drinks = Drink.query.all()
    
    try:
        return jsonify({
            'success': True,
            'drinks' : [drink.short() for drink in drinks]
        }), 200
    except:
        abort(404)


@app.route('/drinks-detail')
def drinks_detail():
    
    drinks = Drink.query.all()
    
    try:
        return jsonify({
            'sucess': True,
            'drinks': [drink.long() for drink in drinks]
        }), 200

    except:
        abort(404)


@app.route('/drinks', methods=['POST'])
def create_drink():
    body =request.get_json()
    new_drink = body.get('title', None)
    new_recipe = body.get('recipe', None)

    try:
        drink = Drink(drink=new_drink, recipe=new_recipe)
        drink.insert()

        #selection = Drink.query.order_by(Drink.id).all()
        #current_drinks = paginate_drinks(request, selection)
        #created_id = drink.id

        #total_drinks = len(Drink.query.all())

        return jsonify({
            "success": True,
            "drinks": drink.long()
            #"created": created_id,
            #"drink_created": drink.drink,
            #"drinks": current_drinks,
            #"total_questions": total_drinks
        })

    except:
        abort(422)
        

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(404)
def unreachable(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Not Found"
                    }), 404
'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
