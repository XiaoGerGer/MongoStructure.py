#!/usr/bin/python
#
#       Scan MongoDB Collection Structure
#

__created__ = '2018/6/8'
__author__ = 'Yang Xiao'
__version__ = 'v2.0'

from pymongo import MongoClient
from tqdm import tqdm
import sys
import json
import argparse

parser = argparse.ArgumentParser(description='Scan MongoDB Collection Structure')
parser.add_argument('-v', '--version', action='version', version=' '.join((__version__, __author__, __created__)))
parser.add_argument('host', default='127.0.0.1', help='mongoDB Server host')
parser.add_argument('-p', '--port', default='27017', type=int, help='mongoDB Server host')
parser.add_argument('database', help='mongoDB Database name')
parser.add_argument('collection', help='mongoDB Collection name')
parser.add_argument('-o', '--out_type', default='tree', choices=['tree', 'path'], help='default is value: tree')


def __list_structure(node: list, structure: dict):
    for item in node:
        if isinstance(item, list):
            array_index_name = '@array-' + str(len(set(filter(lambda x: x.startswith('@array'), structure.keys()))))
            structure[array_index_name] = {
                'type': {'list', },
                'children': {}
            }
            __list_structure(item, structure[array_index_name]['children'])
        elif isinstance(item, dict):
            __node_structure(item, structure)
        else:
            pass


def __node_structure(node: dict, structure: dict):
    for node_name, node_value in node.items():

        node_type = str(type(node_value)).split("'")[-2]

        if node_name not in structure:
            structure[node_name] = {
                'type': {node_type, },
                'children': {}
            }
        else:
            structure[node_name]['type'].add(node_type)

        if isinstance(node_value, list):
            __list_structure(node_value, structure[node_name]['children'])
        elif isinstance(node_value, dict):
            __node_structure(node_value, structure[node_name]['children'])
        else:
            pass


def __print_structure_tree(structure, levels):
    for node in sorted(structure.keys()):
        print('|\t' * levels + '|____', node, ':', ', '.join(sorted(list(structure[node]['type']))))
        if len(structure[node]['children']) == 0:
            continue
        __print_structure_tree(structure[node]['children'], levels + 1)


def __print_structure_path(structure, current_path=''):
    for node in sorted(structure.keys()):
        print(current_path + '.' + node) if len(current_path) else print(node)
        if len(structure[node]['children']) == 0:
            continue
        if len(current_path):
            __print_structure_path(structure[node]['children'], current_path + '.' + node)
        else:
            __print_structure_path(structure[node]['children'], node)


def create_structure(host, port, database, collection, out_type):
    client = MongoClient(host, port)

    try:
        table = client[database][collection]
        total = table.count()

        collection_structure = {}

        for it in tqdm(table.find(no_cursor_timeout=True), total=total, desc="Collection Structure"):
            __node_structure(it, collection_structure)
        print('Done!')
        print('=' * 10, database + '.' + collection, '=' * 10)
        if out_type == 'tree':
            __print_structure_tree(collection_structure, 0)
        elif out_type == 'path':
            __print_structure_path(collection_structure, '')
        else:
            raise ValueError(out_type)
        print('=' * 10, database + '.' + collection, '=' * 10)
    finally:
        client.close()


if __name__ == '__main__':
    args = parser.parse_args()
    create_structure(args.host, args.port, args.database, args.collection, args.out_type)
