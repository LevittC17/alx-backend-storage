#!/usr/bin/env python3

'''
:param mongo_collection: A pymongo collection object
:param kwargs: Keyword arguments for the new document
:return: The new _id for the inserted document
'''


def insert_school(mongo_collection, **kwargs):
    '''Insert a new document in the given MongoDB collection
    based on keyword arguments'''
    new_document = kwargs
    result = mongo_collection.insert_one(new_document)
    return result.inserted_id
