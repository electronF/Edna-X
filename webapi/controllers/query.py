# Built-in modules
import os
from typing import Dict, List, Union, Any
import datetime

# External modules
from sqlalchemy import DateTime

from flask import make_response


#Local modules
from configs import database, connexion_app

from webapi.models.query import Query, QuerySchema
from webapi.modelsDTO.query import QueryDTO


class QueryController:
    '''
        This class provide functions to get, edit, update and delete a query on database.
    '''
    
    @classmethod
    def read_all(cls)->(Union[List[Dict[str, Union[str, int, DateTime]]], Dict[str, Union[str, int]]]):
        """
        This get the complete lists of saved queries.
        
        Args:
        Returns:
            (List[Dict[str, Any]]): Object with code 201 and success state and the 
                list of saved queries. Or code 500 
                and success state and error message if failed.
        """
        try:
            # Get the list of queries
            queries = database.session.query(Query).order_by(Query.received_at).all()

            # Serialize response and return it
            return {
                'data': QuerySchema(many=True).dump(queries), 
                'sucess': True,
                'code':200
                }
        except Exception as error:
            connexion_app.logger.error('controllers',str(error))
            return {
                'success':False, 
                'message':f'something happens wrong on server {str(error)}', 
                'code':500
            }
    
    @classmethod
    def user_queries(cls, user_id:str)->(Union[List[Dict[str, Union[str, int, DateTime]]], Dict[str, Union[str, int]]]):
        """
        This function get the lists of queries for a given user_id.
        
        Args:
            user_id(str): The id of the user to ge the queries performed by him.
        Returns:
            (List[Dict[str, Any]] | Dict[str, Any]): Object with code 201 and success state and the 
                list of saved queries. Or code 500 
                and success state and error message if failed.
        """
        # Get the list of queries
        queries = Query.query.filter(Query.user_id == user_id).all()
        
        # Serialize response and return it
        try:
            return {
                **QuerySchema(many=True).dump(queries), 
                'success': True, 
                'code':200
            }
        except Exception as error:
            connexion_app.logger.error(error)
            return {
                'success':False, 
                'message':f'something happens wrong on server {str(error)}', 
                'code':500
            }

    @classmethod
    def read_one(cls, query_id:id)->(Union[Dict[str, Union[str, int, DateTime]], Dict[str, Union[str, int]]]):
        """
        This function return one matching saved query from the list of using query_id.
        
        Args:
            query_id(int): The id of the needed query.
        Returns:
            (Dict[str, Union[str, int, DateTime]] | None): code 201 and success state and the 
                list of saved queries. Or code 404, 
                500 and success state and error message if failed.
        """
        # Build the initial query
        
        query = (
            database.session.query(Query)
            .filter(Query.id == query_id)
            .one_or_none()
        )
        try:
            # Did we find a query?
            if query is not None:
                # Serialize the data for the response
                return {
                    **QuerySchema().dump(query), 
                    'success':True, 
                    'code': 200
                }
            # Otherwise, nope, didn't find that query
            else:
                return {
                    'success': False, 
                    'message':f"Query not found for Id: {query_id}", 
                    'code': 404
                }
        except Exception as error:
            # Otherwise, nope, query ists already
            connexion_app.logger.error(error)
            return {
                'success': False,
                'message': 'Something happens wrong on server', 
                'code': 500
            }
            
    @classmethod
    def create(cls,query:QueryDTO)->(Union[Dict[str, Union[str, int, DateTime]], Dict[str, Union[str, int]]]):
        """
        This function save a new query in the list of queries
        Args:
            query(QueryDTO): The query instance. 
        Returns:
            (Dict[str, Any]] | Dict[str, Any):  Object with code 201 and success message
                and success sate and query schema on success, or 500 and error message if an error occured.
        """
        query_db_model = Query(
            username = query.username,
            email = query.email,
            query = query.query,
            user_id = query.user_id,
            sended_at = query.sended_at
        )
            
        # Does the query could be inserted?
        try:
            # Add the query to the database
            database.session.add(query_db_model)
            database.session.commit()
            
            # Uncomment the two nexts lines of code if the id of insterted data
            # is not automatically add to the instance
            
            # database.session.flush()
            # database.session.refresh(query_db_model)

            # Serialize and return the newly created query in the response
            return {
                **QuerySchema().dump(query_db_model), 
                'success':True, 
                'code': 201
            }
        except Exception as error:
            # Otherwise, nope, query ists already
            connexion_app.logger.error('controller', str(error))
            return {
                'success': False,
                'message': f'Something happens wrong on server {error}', 
                'code': 500
            }

    @classmethod
    def update(cls, query_id:int, query:Dict[str, Union[int, str, DateTime]])->(Union[Dict[str, Union[str, int, DateTime]], Dict[str, Union[str, int]]]):
        """
        This function updates an existing query in the list of query.
        
        Args:
            query_id(int):   The id of the query to update
            query(Dict[str, int | str | DateTime]): 
                The query with the information to update
        Returns:
            (Dict | None): code 201 and the update query object and the success state on success,
                or code 404 or code 500 and the success state and the error message if .
        """
        # Get the query requested
        existing_query = (
            database.session.query(Query)
            .filter(Query.id == query_id)
            .one_or_none()
        )
        
        try:
            # Update the query if it exists?
            if existing_query is not None:
                schema = QuerySchema()
                update = schema.load(query, session=database.session)

                # Set the id to the query to update
                update.id = query['id']

                # merge the new object with the old one and save to the database
                database.session.merge(update)
                database.session.commit()

                return {**schema.dump(update), 'success': True, 'code':200}

            # Otherwise, nope, didn't find that query
            else:
                return {
                    'success':False,
                    'message':f"Query not found for Id: {query_id}", 
                    'code':404
                }
        except Exception as error:
            # Otherwise, nope, query exists already
            connexion_app.logger.error(error)
            return {
                'success': False,
                'message': 'Something happens wrong on server', 
                'code': 500
            }

    @classmethod
    def delete(cls, query_id:int):
        """
            This function deletes a query in the list of queries
            
            Args:
                query_id(int):  The id of the query to delete
            Returns:
                (Dict): Code 201 and success state and success message on successful delete. 
                    Code 404 or 500 and success state and error message .
        """
        # Get the query requested
        query = (
            database.session.query(Query)
            .filter(Query.id == query_id)
            .one_or_none()
        )

        try:
            # Delete the query if its exists
            if query is not None:   
                database.session.delete(query)
                database.session.commit()
                return {
                        'success': True,
                        'message':f"Query with Id {query_id} has been deleted",
                        'code': 200
                    } 
            else:
                return {
                        'success':False, 
                        'message':f"Query not found for Id: {query_id}", 
                        'code': 404
                    }
        except Exception as error:
            # Otherwise, nope, query exists already
            connexion_app.logger.error(error)
            return {
                'success': False,
                'message': 'Something happens wrong on server', 
                'code': 500
            }
