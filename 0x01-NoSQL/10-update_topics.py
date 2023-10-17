#!/usr/bin/env python3

'''
:param mongo_collection: A pymongo collection object
:param name: The name of the school to update
:param topics: The list of topics to set for the school
'''


def update_topics(mongo_collection, name, topics):
    '''changes the topics of a school document based on
    the school's name'''
    mongo_collection.update_many(
        {"name": name},
        {"$set": {"topics": topics}}
    )
