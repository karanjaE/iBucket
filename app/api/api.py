from flask import Flask
from flask_restful import Resource

from app import app

class Index(Resource):
    def get(self):
        return "This is index."

class BucketList(Resource):
    """Defines crud methods for all bucketlists"""
    def __init__(self):
        pass

    def post(self):
        """Create a new bucketlist"""
        return "Create a new Bucket"

    def get(self):
        """Get all bucketlists"""
        return "Get bucketlists"


class BucketListSingle(Resource):
    """Defines CRUD for a single bucketlist"""
    def __init__(self):
        pass

    def get(self):
        """Retriev a single bucketlist"""
        return "Get single Bucket"

    def put(self):
        """Update a bucketlist"""
        return "Update a bucket"

    def delete(self):
        """Delete a bucketlist and it's children."""
        return "Delete a bucket and it's kids"


class BucketListSearch(Resource):
    """Defines the search by name"""
    def __init__(self):
        pass

    def get(self):
        """Get bucketlists by name"""
        return "search buckets by name."


class BucketListItem(Resource):
    """Defines CRUD for bucletlist items"""
    def __init__(self):
        pass

    def post(self):
        return "Create an item"

    def get(self):
        return "get all items in a bucket"

    def put(self):
        return "Update an item"

    def delete(self):
        return "Delete an item"
