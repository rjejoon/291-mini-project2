

// this query currently ignores tags
db.posts.aggregate([            
            {"$match": {"$and": [{"terms": {"$in": kwList}},
                                {"PostTypeId":"1"}]}},
            {}
            {"$project": {
                "Id" : 1,
                "Title": 1,
                "Body": 1,
                "match": {
                            "$reduce": {
                                "input": kwList,
                                "initialValue": 0,
                                "in": { "$add" : ["$$value", 
                                                    { "$divide": [
                                                            {"$subtract": [
                                                                            { "$strLenCP": { "$toLower": "$Title" } },
                                                                            { "$strLenCP": { "$replaceAll": { "input": { "$toLower": "$Title" },
                                                                                                              "find": "$$this",
                                                                                                              "replacement": "" }
                                                                                        }
                                                                            }
                                                                        ]},
                                                            { "$strLenCP": "$$this" }
                                                        ] 
                                                    }
                                                ]
                                                

                            }
                        }
                    }
                }
            }
                        
])


// find done with index searching
db.posts.find({"$and": [{"terms": {"$in": kwList}},
                                {"PostTypeId":"1"}]}).explain()


// js anoynymous function for getting matches
function(s, terms) {

    let match = 0
    terms.forEach(term => {
        let replaced_s =  s.replace(term, '')
        match += Math.trunc((s.length - replaced_s.length) / term.length)
    })
    return match
}


                    
