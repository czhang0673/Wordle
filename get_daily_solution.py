#

import os


from pymongo import MongoClient


import random


from wordfreq import iter_wordlist



uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client["my_database"]
collection = db["previous_solutions"]
daily_solution = db["daily_solution"]

#pymongo takes the dictionaries and turns them into bson. and then will turn them back to dictionaries with find operations

#other operations: find/find_one, update_one/update_many, delete_one/delete_many

all_words = [word for word in iter_wordlist('en') if len(word) == 5 and word.isalpha()]


def get_solution_pool(pool_size=2000, word_length=5):
    """Get most common {word_length}-letter words to use as a full answer pool."""
    pool = []
    for word in iter_wordlist('en'):
        if len(word) == word_length and word.isalpha():
            pool.append(word)
        if len(pool) == pool_size:
            break
    return pool

def lambda_handler(event, context):
    solutions = get_solution_pool()

    #empty dictionary tells mongoDB to find every document in the collection
    #projection: {"solution":1} tells mongoDB to send back the "solution" field + default id
    used_documents = collection.find({}, {"solution": 1})
    #set comprehension. take only the string value doc["solution"]
    used_words = {doc["solution"] for doc in used_documents if "solution" in doc}

    #turn solutions list into set. set subtraction: removes all overlapping words from the two sets
    available_words = list(set(solutions) - used_words)

    if not available_words:
        print("No solutions available.")
        #consider implementation to expand words to more obscure things
        random_solution = None
    else:
        random_solution = random.choice(available_words)

    if random_solution is not None:
        prev_result = collection.insert_one({"solution": random_solution}) if random_solution is not None else None
        print(f"Inserted solution #{prev_result.inserted_id} into previous solution database.")

        daily_result = daily_solution.insert_one({"solution": random_solution}) if random_solution is not None else None
        print(f"Inserted solution #{daily_result.inserted_id} into daily solution database.")

        return {
            'statusCode': 200,
            'body': f"Randomly chose and inserted: {random_solution}",
        }
    else:
        return {
            'statusCode': 400,
            'body': "No solutions to insert."
        }


