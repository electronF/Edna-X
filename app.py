#built-in module
import os
import json
from datetime import datetime

# 3rd party moudles
from flask import (
    jsonify, 
    request,
    make_response
)

# Local modules
import configs
import constants

from webapi.modelsDTO.query import QueryDTO
from webapi.controllers.query import QueryController

from webapi.services.textgenerator import TextGenerator


# Get the application instance
connex_app = configs.connexion_app
connex_app.app_context().push()

text_generator = TextGenerator()


@connex_app.before_first_request
def init():
    from webapi.models.query import Query
    configs.database.create_all()


# Create a URL route in our application for "/api/document/"
@connex_app.route("/api/query/", methods=['GET'])
def get_all_queries():
    """
    This function just responds to the URL
    localhost:5000/api/query/ to get the list of queries
    
    Args:
    Returns:
        (JSON): A list of dict as list of queries
    """
    try:
        response = QueryController.read_all()
        code = response.pop('code')
        return make_response(jsonify(response), code)
    except Exception as error:
        connex_app.logger('app', error)
        return make_response (
            jsonify({
                'success': False,
                'message': 'something happen wrong on server'
            }),
            500
        )


# Create a URL route in our application for "/api/bot/"
@connex_app.route("/api/bot/", methods=['POST'])
def get_one_query():
    """
        This function just responds to the URL
        localhost:5000/api/bot/<str:query>
        Args:
            query(str): the query to get answer for.
        Returns:
            (str): The response of the query.
    """
    try:
        query = request.form
        if(not (None in [
                query.get('query', None), 
                query.get('username', None),
                query.get('user_id', None)
                ])
            ):
            
            #Remove the Z included by iso 8601 
            sended_at = query.get('sended_at', None)
            if sended_at != None:
                pos = sended_at.find('Z')
                if pos > 0:
                    list_sended_at = list(sended_at)
                    list_sended_at.remove('Z')
                    sended_at = "".join(list_sended_at)
                    
            query_dto = QueryDTO(
                username = query.get('username'),
                query = query.get('query'),
                email = query.get('email', None),
                user_id = query.get('user_id'),
                sended_at = (datetime.fromisoformat(sended_at) if sended_at != None else None)
            )
            
            first_response = QueryController.create(query_dto)
            code = first_response.pop('code')
            success = first_response.pop('success', False)
            if success == True:
                #Get generated response 
                bot_response = text_generator.query(query.get('query'))
                if bot_response['success'] == True:
                    first_response = {
                        **first_response,
                        'query_response':bot_response, 
                        'replyed_at': datetime.utcnow().isoformat()
                    }
                    second_response = QueryController.update(first_response['id'], first_response)
                    code = second_response.pop('code')
                    return make_response(jsonify(second_response), code)
                else:
                    return make_response(jsonify({'success':False, 'message':bot_response['message']}), bot_response['code'])
            return make_response(jsonify({**first_response, 'success':success}), code)
    except Exception as error:
        connex_app.logger('info', error)
        return make_response (
            jsonify({
                'success': False,
                'message': 'something happen wrong on server'
            }),
            500
        )
    
# Create a URL route in our application for "/api/query/"
@connex_app.route("/api/query/<int:query_id>", methods=['GET'])
def get_one(query_id:int):
    """
    This function just responds to the URL
    localhost:5000/query/<int:query_id>
    
    Args:
        query_id(str): The id of the query to get info
    Returns:
        (JSON): An object containing the response
    """
    response = QueryController.read_one(query_id)
    code = response.pop('code')
    return make_response(jsonify(response), code)

    
# Create a URL route in our application for "/api/bot/"
@connex_app.route("/api/query/<int:query_id>", methods=['DELETE'])
def delete(query_id:int):
    """
    This function just responds to the URL
    localhost:5000/query/<int:query_id>
    
    Args:
        query_id(str): The id of the query to delete
    Returns:
        (JSON): An object containing the success of message, success state
    """
    response = QueryController.delete(query_id)
    code = response.pop('code')
    return make_response(jsonify(response), code)


# Create a URL route in our application for "/api/bot/"
@connex_app.route("/api/query/<int:query_id>", methods=['PUT'])
def update(query_id:int):
    """
    This function just responds to the URL
    localhost:5000/query/<int:query_id>
    
    Args:
        query_id(str): The id of the query to update
    Returns:
        (JSON): An object containing the success of message, success state
    """
    if(len(request.form) > 0):
        response =QueryController.update(query_id, request.form)
        code = response.pop('code')
        return make_response(jsonify(response), code)
    else:
        return make_response(
            jsonify({
                'success': False,
                'message': 'Missing some information in the request'
            }),
            400
        )

# Create a URL route in our application for "/api/bot/"
@connex_app.route("/api/user/<int:query_id>", methods=['DELETE'])
def get_user_queries(user_id:int):
    """
    This function just responds to the URL
    localhost:5000/bot/<int:user_id>
    
    Args:
        user_id(str): The id of the user to get all his performed queries
    Returns:
        (JSON): An object containing the response
    """
    try:
        response = QueryController.user_queries()
        code = response.pop('code')
        return make_response(jsonify(response), code)
    except Exception as error:
        connex_app.logger('info', error)
        return make_response (
            jsonify({
                'success': False,
                'message': 'something happen wrong on server'
            }),
            500
        )



if __name__ == "__main__":
    connex_app.run(host="0.0.0.0", port=5000, debug=True)