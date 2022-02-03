import pymongo
import datetime
 
client = pymongo.MongoClient('localhost')  #caise.geos.ed.ac.uk')
db = client.test_database
posts = db.posts
post = {"author": "Magi",
        "text": "My first blog post!",
        "tags": ["mongodb", "python", "pymongo"],
        "date": datetime.datetime.utcnow()}
post_id = posts.insert(post)
print post_id
print posts.find_one()
