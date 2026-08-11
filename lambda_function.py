# from dotenv import load_dotenv

import json

import os

from pymongo import MongoClient

from wordle_game import Wordle


from traceback import format_exc


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

daily_solution_collection = db["daily_solution"]


# this is a folder in the cabinet. holds documents in the folder


def lambda_handler(event, context):  # event and context are automatically passed in every time function runs
    # event: python dictionary containing data of what triggered function(the inputs)
    request_method = event.get('httpMethod') #check rest api first
    if not request_method and 'requestContext' in event:
       if 'http' in event['requestContext']:
           request_method = event['requestContext']['http'].get('method')
       else:
           request_method = event['requestContext'].get('httpMethod')
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
        print("Incoming event:", event) #cant concatenate string and dictionary. instead pass two arguments to print()
        #prints both separated by a space
        body = event.get('body') or "{}" #python or operator checks first value - if "truthy", use firs
        #if "falsy" (ie. none or "") uses second
        body_data = json.loads(body)

        user_input = body_data.get("user_input", "")
        # if body:
        #     if event.get('isBase64Encoded', False):
        #         #api payload with json data usually encoded in utf-8
        #         #api gateway uses base64 to transmit binary data ie images
        #         #import base 64 to decode it back to binary, then to utf 8
        #         import base64
        #         body = base64.b64decode(body).decode('utf-8')
        #
        #     if isinstance(body, str): #isinstance checks if body is currently str
        #         body_data = json.loads(body) #if it is, parse the string into dictionary
        #     else:
        #         body_data = body #if not str, then api gateway already converted it to dict
        #     user_input = event.get("user_input", "") #"" safety net - give empty string if no "user_input"
        # elif "user_input" in event:
        #     user_input = event.get("user_input", "")
        # else:
        #     user_input = ""

        if not user_input:
            return {
                'statusCode': 200,
                'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps({
                    "success": False,
                    "message": f"Debug information: Body was parsed as: {body_data}"

                })
            }
        # this assumes frontend sends something that looks like: {"user_input": "bacon"}

        # context: python object aws creates that holds "behind-the-scenes runtime information" ?

        game = Wordle()

        # queries dictionary for document containing "apple"; returns dictionary containing ... "solution": "apple"
        # db_record = collection.find_one({"solution": "apple"})
        # daily_solution = db_record["solution"] if db_record else "apple" #hardcoded for now

        #mongodb randomly samples one document
        # random_solution = collection.aggregate([{"$sample": {"size":1}}
        # ])
        # random_solution = next(random_solution, None)
        #
        # if random_solution:
        #     daily_solution = random_solution["solution"]
        # else:
        #     daily_solution = "apple"

        daily_solution_dict = daily_solution_collection.find_one(sort=[("_id", -1)], projection={"solution": 1})
        daily_solution = daily_solution_dict["solution"]

        return {
            'statusCode': 200,
            'headers': {#headers - CORS; Cross-Origin Resource Sharing
                # #backend explicitly returns headers to allow front end
                #to "talk" to it
                'Access-Control-Allow-Origin': '*', # * allows any website/origin to request
                'Access-Control-Allow-Headers': 'Content-Type', #says front end is allowed to include whatever
                #content-Type is - which is "application/json"
                'Access-Control-Allow-Methods': 'OPTIONS,POST' #http actions OPTIONS and POST are permitted
            },
            'body': json.dumps({
                "colors": game.check_input(user_input, daily_solution)})
        }  # when lambda_handler runs, it hands this dictionary back to aws
    except Exception as e:
        print(f"Error: {format_exc()}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({"Error": str(e)})
        }
# json.dumps: "JSON dump string". takes python data from wordle and translates it into json text string
# value of body is a string that looks like a list. ex [0,2,1,1,0]
