#!/usr/bin/env python3
"""
Main file for Task 4: replay
"""
from exercise import Cache, replay

# Initialize Cache instance
cache = Cache()

# Store some values
cache.store("foo")
cache.store("bar")
cache.store(42)

# Replay the history of calls to cache.store
replay(cache.store)