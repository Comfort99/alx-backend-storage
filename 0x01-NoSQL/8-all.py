#!/usr/bin/env python3
"""
List all the documments in collection
"""


def list_all(mongo_collection):
    """
    Iterate over the collection
    """
    return [doc for doc in mongo_collection.find()]