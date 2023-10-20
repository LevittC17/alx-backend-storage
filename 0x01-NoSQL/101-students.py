#!/usr/bin/env python3
"""
This module provides a function to return top students sorted by average score.
"""

from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Return a list of top students sorted by their average scores.
    """
    pipeline = [
        {
            "$unwind": "$topics"
        },
        {
            "$group": {
                "_id": "$_id",
                "name": {"$first": "$name"},
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            "$sort": {"averageScore": -1}
        }
    ]

    top_students = list(mongo_collection.aggregate(pipeline))
    return top_students


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

    # Example usage:
    top_students_list = top_students(students_collection)
    for student in top_students_list:
        print("[{}] {} => {}".format(student.get('_id'),
                                     student.get('name'),
                                     student.get('averageScore')))
