#!/usr/bin/env python3

'''
script that provides some stats about Nginx
logs storen in MongoDB
'''


from pymongo import MongoClient


def log_stats():
    '''Connect to the MongoDB server'''
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Calculate the total number of logs
    total_logs = collection.count_documents({})

    # Calculate the number of logs with each HTTP method
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    method_counts = {method: collection.count_documents(
                     {"method": method}) for method in methods}

    # Calculate the number of logs with method=GET and path=/status
    status_check_count = collection.count_documents(
                             {"method": "GET", "path": "/status"})

    # Display the results
    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_counts.items():
        print(f"method {method}: {count}")
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    log_stats()
