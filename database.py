import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["matcha"]
collection = db["users"]

# Global


def find_user(username):
    user = collection.find_one({'UserName': username})
    return user


def online_status(username):
    query = {"UserName": username}
    update = {"$set": {"LastSeen": 'Online'}}
    collection.update_one(query, update)


def general_update(username, column, value):
    query = {"UserName": username}
    update = {"$set": {column: value}}
    collection.update_one(query, update)


# Registration
def registration_insert(username, firstname, surname, email, password):
    document = {"UserName": username,
                "FirstName": firstname,
                "SurName": surname,
                "Email": email,
                "Password": password,
                "Age": "",
                "Gender": "",
                "SexualPreference": "",
                "Biography": "",
                "AccountVerification": "0",
                "ProfileCompletion": "0",
                "ChatMessage": "",
                "LastSeen": "Offline"}
                
    collection.insert_one(document)


def verify_insert(username):
    general_update(username, "AccountVerification", "1")


# Forgot Password
def find_user_by_email(email):
    user = collection.find_one({'Email': email})
    return user


# Change Password
def password_change(email, password):
    query = {"Email": email}
    update = {"$set": {"Password": password}}
    collection.update_one(query, update)