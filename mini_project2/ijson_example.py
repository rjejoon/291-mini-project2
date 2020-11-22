import ijson
import time
import pprint

def main():

    st = time.time()
    with open('../Posts.json', 'r') as f:
        n = 0
        for doc in ijson.items(f, 'posts.row.item'):
            pprint.pprint(doc)
            return
            n += 1
            
    print(n)
    print(time.time() - st)




main()
