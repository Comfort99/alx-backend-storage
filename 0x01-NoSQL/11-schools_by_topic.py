#!/usr/bin/env python3
"""
Filter Model
"""


def schools_by_topic(mongo_collection, topic):
    """
    Function that returns a filtered lists of collections
    containing a specific topic
    """
    topic_filter = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            }
        }
    }

    return [doc for doc in mongo_collection.find(topic_filter)]
