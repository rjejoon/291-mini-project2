from mini_project2.phase1.phase1 import loadAllDocumentsFrom
import asyncio, motor.motor_asyncio, sys




port = sys.argv[1]
client = motor.motor_asyncio.AsyncIOMotorClient(port=port)
db = client['291db']
tags = db['tags']
votes = db['votes']

_, voteDocs, tagDocs = loadAllDocumentsFrom('Posts.json', 'Votes.json', 'Tags.json')

tags.insert_many(tagDocs, ordered=False)
votes.insert_many(voteDocs, ordered=False)

