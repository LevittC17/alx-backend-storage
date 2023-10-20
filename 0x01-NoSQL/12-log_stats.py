#!/usr/bin/env python3

'''
script that provides some stats about Nginx
logs storen in MongoDB
'''


from pymongo import MongoClient


def print_nginx_stats(nginx_collection):
    '''stats about nginx logs in stored in MongoDB'''
    logs_count = nginx_collection.count_documents({})
    print(f"{logs_count} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status_check_count = nginx_collection.count_documents({"method": "GET",
                                                           "path": "/status"})
    print(f"{status_check_count} status check")


def main():
    '''Main function'''
    client = MongoClient("mongodb://127.0.0.1:27017")
    nginx_collection = client.logs.nginx
    print_nginx_stats(nginx_collection)


if __name__ == "__main__":
    main()
