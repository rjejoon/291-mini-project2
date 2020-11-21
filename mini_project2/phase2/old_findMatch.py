    # cursor = posts.aggregate([
            # {"$match": {"PostTypeId":"1"}},
            # {"$project": {
                            # "Id": 1,
                            # "AcceptedAnswerId": 1,
                            # "Title": 1,
                            # "CreationDate": 1,
                            # "Score": 1,
                            # "AnswerCount": 1,
                            # "terms": {"$cond": {        # changing 'terms' array may cause failure in index searching 
                                        # "if": {"$not": "$Tags"}, "then": "$terms",
                                        # "else": {  
                                                # "$concatArrays": 
                                                        # [
                                                            # "$terms",
                                                            # {"$split": [{"$substr": [{"$toLower": "$Tags"}, 1, {"$subtract": [{"$strLenCP": "$Tags"}, 2]}]},"><"]} 

                                                        # ]
                                                # }}
                                    # }
                        # }
            # },
            # {"$match": {"terms": {"$in": kwList}}},
            # {"$unwind": "$terms"},  # overhead
            # {"$match": {"terms": {"$in": kwList}}},
            # {"$group": {"_id": "$Id",
                        # "Title": {"$first": "$Title"},
                        # "AcceptedAnswerId": {"$first": "$AcceptedAnswerId"},
                        # "CreationDate": {"$first": "$CreationDate"},
                        # "Score": {"$first": "$Score"},
                        # "AnswerCount": {"$first": "$AnswerCount"},
                        # "match": {"$sum": 1}}},
            # {"$sort": {"match": -1}}
        # ])

