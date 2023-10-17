#!/usr/bin/env python3

'''
:param mongo_collection: A pymongo collection object
:param name: The name of the school to update
:param topics: The list of topics to set for the school
'''


mongo_collection.update_many(
    {"name": name},
    {"$set": {"topics": topics}}
)
