#!/usr/bin/env python3

'''
:param mongo_collection: A pymongo collection object
:param topic: The topic to search for
:return: A list of schools matching the specified topic
'''


def schools_by_topic(mongo_collection, topic):
    '''returns a list of schools having a specific topic'''
    schools = list(mongo_collection.find({"topic": topic}))
    return schools
