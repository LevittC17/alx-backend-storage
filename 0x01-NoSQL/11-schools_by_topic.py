#!/usr/bin/env python3

'''
:param mongo_collection: A pymongo collection object
:param topic: The topic to search for
:return: A list of schools matching the specified topic
'''


def schools_by_topic(mongo_collection, topic):
    '''returns a list of schools having a specific topic'''
    matching_sch = []

    for school in mongo_collection.find():
        if 'topics' in school and topic in school['topics']:
            matching_sch.append(school)

    return matching_sch
