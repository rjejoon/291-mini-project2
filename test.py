import asyncio, motor.motor_asyncio, sys, os, json


port = int(sys.argv[1])
client = motor.motor_asyncio.AsyncIOMotorClient(port=port)
db = client['291db']
dir_path = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(dir_path, "Votes.json"), 'r') as f:
    db['votes'].insert_many(json.load(f)["votes"]['row'], ordered=False)

with open(os.path.join(dir_path, "Tags.json"), 'r') as f:
    db['tags'].insert_many(json.load(f)["tags"]['row'], ordered=False)





