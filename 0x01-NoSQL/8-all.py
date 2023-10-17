#!/usr/bin/env python3

'''
:param mongo collection: A pymongo collection object
:return: A list of documents
'''


def list_all(mongo_collection):
    '''Lists all documents in the given MongoDB
    collection'''
    documents = list(mongo_collection.find({}))
    return documents
