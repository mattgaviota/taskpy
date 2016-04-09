#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple todo manager app"""
from argparse import ArgumentParser
from datetime import datetime
from pymongo import MongoClient
from prettyjson import PrettyJson


class Client(object):
    """Controller of the mongoDB"""
    def __init__(
            self,
            dbname="taskpy",
            collection="tasks",
            host="localhost",
            port="27017"
    ):
        self.client = MongoClient("mongodb://{}:{}/".format(host, port))
        self.mongodb = self.client[dbname]
        if not self.mongodb[collection]:
            self.tasks = self.mongodb.create_collection(collection)
        else:
            self.tasks = self.mongodb[collection]
        if not self.mongodb['free_ids']:
            self.free_ids = self.mongodb.create_collection('free_ids')
            self.free_ids.insert_one({'internal_id': 1})
        else:
            self.free_ids = self.mongodb['free_ids']
            if self.free_ids.count() < 1:
                self.free_ids.insert_one({'internal_id': 1})

    def get_collection(self, name="tasks"):
        """Return the collection passed by name"""
        return self.mongodb[name]

    def set_collection(self, name="tasks"):
        """Create the collection passed by name"""
        self.mongodb.create_collection(name)

    def insert_task(self, doc):
        """Insert a task into tasks collection"""
        self.tasks.insert_one(doc)
        print "task created with id {}".format(doc['id'])

    def create_task(self, **args):
        """Create a document with de args provided"""
        doc = {}
        doc['id'] = self.get_free_id()
        doc['description'] = args['description']
        try:
            doc['project'] = args['project']
        except KeyError:
            doc['project'] = 'default'
        doc['status'] = "incomplete"
        doc['date'] = datetime.now()
        try:
            doc['priority'] = args['priority']
        except KeyError:
            pass
        try:
            doc['tags'] = args['tags']
        except KeyError:
            pass
        try:
            doc['due_date'] = args['due_date']
        except KeyError:
            pass
        try:
            doc['parent'] = self.get_id(args['parent'])
        except KeyError:
            pass
        return doc

    def complete_task(self, clean_id):
        """Mark a task as complete"""
        saved_id = self.tasks.find_one({'id': clean_id})
        self.free_ids.insert_one({'internal_id': saved_id['id']})
        self.tasks.update_one(
            {'id': clean_id},
            {
                '$set': {
                    'status': 'complete',
                    'id': None,
                    'complete_date': datetime.now()
                }
            }
        )
        print "Task {} completed".format(clean_id)

    def get_free_id(self):
        """Return the next free internal id."""
        free_id = self.free_ids.find(
            {},
            {'internal_id': 1},
        ).sort('internal_id', 1)
        free_id = list(free_id)
        next_id = free_id[0]['internal_id']
        if len(free_id) > 1:
            self.free_ids.delete_one({'internal_id': next_id})
        else:
            self.free_ids.update_one(
                {'internal_id': next_id},
                {'$inc': {'internal_id': 1}}
            )
        return next_id

    def get_id(self, clean_id):
        """Return the mongodb _id from a task given the id field"""
        task = self.tasks.find_one({'id': clean_id}, {'_id': 1})
        return task['_id']

    def show_task(self, clean_id):
        """Show a task given the id(not the _id)"""
        print self.tasks.find_one({'id': clean_id}, {'_id': 0})

    def show_all_task(self, txtfilter):
        """Show all task, optionaly filter the result"""
        if txtfilter == 'all':
            json_list = list(self.tasks.find({}, {'_id': 0}))
            table_json = PrettyJson(json_list)
            table_json.show()
        else:
            for task in self.tasks.find(
                    {
                        '$or': [
                            {
                                'description': {
                                    '$regex': txtfilter,
                                    '$options': 'i'
                                }
                            },
                            {
                                'project': {
                                    '$regex': txtfilter,
                                    '$options': 'i'
                                }
                            }
                        ]
                    },
                    {'_id': 0}
            ):
                print task


class Taskparser(object):
    """Parser to manage de options and arguments"""
    def __init__(self):
        self.args = []
        self.parser = ArgumentParser(description="Simple todo app")
        self.create_argument_parser()
        self.dbclient = Client()

    def create_argument_parser(self):
        """Create the argument group and other arguments."""
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument("-a", "--add", nargs="+", help="Add a task")
        group.add_argument(
            "-c",
            "--complete",
            type=int,
            help="Check a task as complete"
        )
        group.add_argument(
            "-l",
            "--list",
            nargs='?',
            const='all',
            help="List all task"
        )
        group.add_argument("-s", "--show", type=int, help="Show a task")
        self.parser.add_argument("-p", "--project", help="Project of a task")
        self.parser.add_argument("parametro", nargs="*")

    def process_args(self):
        """Procesa los argumentos y devuelve un resultado afín"""
        args = self.parser.parse_args()
        if args.list:
            self.dbclient.show_all_task(args.list)
        elif args.show:
            self.dbclient.show_task(args.list)
        elif args.add:
            if args.project:
                new_doc = self.dbclient.create_task(
                    description=' '.join(args.add),
                    project=args.project
                )
                self.dbclient.insert_task(new_doc)
            else:
                new_doc = self.dbclient.create_task(
                    description=' '.join(args.add)
                )
                self.dbclient.insert_task(new_doc)
        elif args.complete:
            self.dbclient.complete_task(args.complete)
        elif args.parametro:
            if args.project:
                new_doc = self.dbclient.create_task(
                    description=' '.join(args.parametro),
                    project=args.project
                )
                self.dbclient.insert_task(new_doc)
            else:
                new_doc = self.dbclient.create_task(
                    description=' '.join(args.parametro)
                )
                self.dbclient.insert_task(new_doc)


def main():
    """Main function"""
    task = Taskparser()
    task.process_args()


if __name__ == '__main__':
    main()
