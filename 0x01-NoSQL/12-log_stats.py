#!/usr/bin/env python3

'''
script that provides some stats about Nginx
logs storen in MongoDB
'''


from pymongo import MongoClient


def log_stats():
    '''Connect to the MongoDB server'''
    client = pymongo.MongoClient('mongodb://127.0.0.1:27017')

    # Access the logs database and nginx collection
    db = client.logs
    collection = db.nginx

    # Count the total number of logs
    total_logs = collection.count_documents({})

    # Create a dictionary to store method counts
    method_counts = {
        'GET': 0,
        'POST': 0,
        'PUT': 0,
        'PATCH': 0,
        'DELETE': 0
    }

    # Count the number of logs for each method
    for method in method_counts.keys():
        method_counts[method] = collection.count_documents({'method': method})

    # Count the number of logs with method=GET and path=/status
    status_check_count = collection.count_documents({'method': 'GET',
                                                     'path': '/status'})

    # Display the statistics
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"\tmethod {method}: {count}")
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    log_stats()
