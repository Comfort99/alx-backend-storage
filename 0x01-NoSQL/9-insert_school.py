#!/usr/bin/env python3
"""
Insertion Method
"""


def insert_school(mongo_collection, **kwargs):
    """
    function that inserts a new document
    in collection based on kwargs
    and allocates a new an _id to the new document
    """
    rec = mongo_collection.insert_one(kwargs)
    return rec.inserted_id
