# from dotenv import load_dotenv

import json

import os

from pymongo import MongoClient

from wordle_game import Wordle

# load_dotenv()

uri = os.environ.get("MONGODB_URI")
# os.environ - dictionary-like object that holds environment variables. can use .get() on it to get a key
# uri - uniform resource identifier. like "url". tells pycharm where to find database on the internet
# tells it to use protocol mongodb+srv, and how to log in(provided credentials)
# youre not supposed to hardcode your credentials

client = MongoClient(uri)
# MongoClient class creates new object/class instance
# when it gets uri: 1) looks up the servers. 2) logs in 3) manages an active connection

db = client["my_database"]  # pymongo mimics dictionary behavior?
# this looks for a database named my_database

collection = db["solutions"]


# this is a folder in the cabinet. holds documents in the folder


def lambda_handler(event, context):  # event and context are automatically passed in every time function runs
    # event: python dictionary containing data of what triggered function(the inputs)

    #api gateway passes options request to function and crashes it
    request_method = event.get('httpMethod') or event.get('requestContext', {}).get('httpMethod')
    #httpmethod - the name of the thing, ie. options. first half checks for if the method is at the top level of dict
    #or look for nested dictionary called requestContext that contains httpMethod

    if request_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': ''
        }
    try:
        user_input = event.get("user_input")
        # this assumes frontend sends something that looks like: {"user_input": "bacon"}

        # context: python object aws creates that holds "behind-the-scenes runtime information" ?

        game = Wordle()

        # queries dictionary for document containing "apple"; returns dictionary containing ... "solution": "apple"
        db_record = collection.find_one({"solution": "apple"})

        if db_record:
            daily_solution = db_record["solution"]
        else:
            daily_solution = "apple"  # if query fails or database is empty

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps(game.check_input(user_input, daily_solution))
        }  # when lambda_handler runs, it hands this dictionary back to aws
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': str(e)
        }
# json.dumps: "JSON dump string". takes python data from wordle and translates it into json text string
# value of body is a string that looks like a list. ex [0,2,1,1,0]
