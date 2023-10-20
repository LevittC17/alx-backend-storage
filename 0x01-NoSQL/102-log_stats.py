#!/usr/bin/env python3
"""
This script provides statistics on an nginx
log collection in a MongoDB database.
"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Total number of logs
    total_logs = collection.count_documents({})

    # Count the occurrence of each HTTP method
    methods = collection.aggregate([
        {"$group": {"_id": "$method", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ])
    method_stats = {method['_id']: method['count'] for method in methods}

    # Count the status check occurrences
    status_check = collection.count_documents({"path": "/status"})

    # Count the top 10 most present IPs
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    ip_stats = {ip['_id']: ip['count'] for ip in top_ips}

    print(f"{total_logs} logs")
    print("Methods:")
    for method, count in method_stats.items():
        print(f"    method {method}: {count}")
    print(f"{status_check} status check")
    print("IPs:")
    for ip, count in ip_stats.items():
        print(f"    {ip}: {count}")
