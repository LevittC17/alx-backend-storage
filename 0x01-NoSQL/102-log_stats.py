#!/usr/bin/env python3
"""
This script provides statistics on an nginx
log collection in a MongoDB database.
"""


from pymongo import MongoClient


def get_nginx_request_logs_stats(nginx_collection):
    '''Get stats about Nginx request logs.
    '''
    stats = {}

    # Count total logs
    stats['Total Logs'] = nginx_collection.count_documents({})

    # Count HTTP methods
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    method_stats = {}
    for method in methods:
        req_count = nginx_collection.count_documents({'method': method})
        method_stats[f'Method {method}'] = req_count
    stats['Methods'] = method_stats

    # Count status checks
    status_checks_count = nginx_collection.count_documents({'method': 'GET',
                                                            'path': '/status'})
    stats['Status Checks'] = status_checks_count

    return stats


def get_top_ips_stats(server_collection):
    '''Get statistics about the top 10 HTTP IPs in a collection.
    '''
    stats = {}
    stats['Top IPs'] = []

    request_logs = server_collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for request_log in request_logs:
        ip = request_log['_id']
        ip_requests_count = request_log['totalRequests']
        stats['Top IPs'].append({'IP': ip, 'Request Count': ip_requests_count})

    return stats


def run():
    '''Provides some stats about Nginx logs stored in MongoDB.
    '''
    client = MongoClient('mongodb://127.0.0.1:27017')

    nginx_collection = client.logs.nginx
    nginx_stats = get_nginx_request_logs_stats(nginx_collection)

    server_collection = client.logs.nginx
    top_ips_stats = get_top_ips_stats(server_collection)

    print(f"{nginx_stats['Total Logs']} logs")
    print("Methods:")
    for method, count in nginx_stats['Methods'].items():
        print(f"\t{method}: {count}")
    print(f"{nginx_stats['Status Checks']} status check")

    print("IPs:")
    for ip_stat in top_ips_stats['Top IPs']:
        print(f"\t{ip_stat['IP']}: {ip_stat['Request Count']}")


if __name__ == '__main__':
    run()
