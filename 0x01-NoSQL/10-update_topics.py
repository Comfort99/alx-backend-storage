#!/usr/bin/env python3
"""
Update Method
"""


def update_topics(mongo_collection, name, topics):
    """
    Function that updates the documents in the collection
    """
    mongo_collection.update_many(
        {'name': name},
        {'$set': {'topics': topics}}
    )
