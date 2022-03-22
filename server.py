import json

from flask import Flask, Response,request
import pymongo

app = Flask(__name__)
#####################

# connect to db
try:
    mongo = pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
    )
    db = mongo.company
    mongo.server_info()  # trigger exception if connect to db
except:
    print = ("ERROR - Cannot connect to db")

##############
@app.route('/')
def index ():
   return ''' 
   <form method="POST" action="/create" enctype="multipart/form-data">
   <input type="text" name="username">
   <input type="file" name="profile_image">
   <input type="submit" >
   </form>
   '''

@app.route('/create',methods=['POST'])
def create():
    if 'profile_image' in request.files :
        profile_image = request.files['profile_image']
        db.save_file(profile_image.filename,profile_image)
        db.users.insert({'username': request.form.get('username'),'profile_image_name' :profile_image.filename})
    return 'Done!'

##############


@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = {"name":request.form["name"], "lastName":request.form["lastname"]}
        dbResponse = db.users.insert_one(user)
        # for attr in dir(dbResponse):
        # print(attr)
        return Response(
            response=json.dumps({"message": "user created ", "id": f"{dbResponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        print("********")
        print(ex)
        print("******")


##############
# run the application
if __name__ == "__main__":
    app.run(port=80, debug=True)
