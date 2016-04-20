# -*- coding: utf-8 -*-
"""Models to set crud operation into the tasks collection"""
from datetime import datetime
from pymongo import MongoClient
from utils import clean_tags, format_field, prioritize, extract_date


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
        print("Task created with id {}".format(doc['id']))

    def create_task(self, args):
        """Create a document with de args provided"""
        doc = {}
        doc['id'] = self.get_free_id()
        try:
            doc['description'] = ' '.join(args['description'])
        except TypeError:
            doc['description'] = ' '.join(args['parameter'])
        if args['project']:
            doc['project'] = args['project']
        else:
            doc['project'] = 'default'
        doc['status'] = "incomplete"
        doc['date'] = datetime.now()
        doc['priority'] = prioritize(args['priority'])
        try:
            doc['tags'] = clean_tags(args['tags'])
        except TypeError:
            pass
        try:
            actual_date = extract_date(args['due_date'])
            if actual_date:
                doc['due_date'] = actual_date
        except TypeError:
            pass
        try:
            parent_id = self.get_id(int(args['parent']))
            doc['parent'] = parent_id
            doc['ancestors'] = self.get_ancestors(parent_id)
        except TypeError:
            doc['parent'] = None
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
                    'completed_date': datetime.now()
                },
                '$unset': {'id': ""}
            }
        )
        print("Task {} completed".format(clean_id))

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
        task = self.tasks.find_one({'id': clean_id}, {'id': 1})
        if task:
            return task['id']
        else:
            return None

    def get_ancestors(self, clean_id):
        """Return an array of ancestors for the given id"""
        ancestors = [clean_id]
        ancestor = self.tasks.find_one({'id': clean_id}, {'parent': 1})
        while ancestor['parent']:
            ancestors.append(ancestor['parent'])
            ancestor = self.tasks.find_one(
                {'id': ancestor['parent']},
                {'parent': 1}
            )
        return sorted(ancestors)

    def show_task(self, clean_id, doc=None):
        """Show a task given the id(not the _id)"""
        if doc:
            for key, val in sorted(doc.items()):
                print(format_field(key, val), end="")
        else:
            doc = self.tasks.find_one({'id': clean_id}, {'_id': 0})
            if doc:
                for key, val in sorted(doc.items()):
                    print(format_field(key, val), end="")
                childrens = self.tasks.find(
                    {
                        '$and': [
                            {'ancestors': doc['id']},
                            {'status': 'incomplete'}
                        ]
                    },
                    {'_id': 0}
                )
                if childrens.count() > 0:
                    print("+--------+\r\n|Subtasks|\r\n+--------+")
                    for child in childrens:
                        print("----" * 10 + "\r\n", end="")
                        self.show_task(child['id'], child)
            else:
                print("The task doesn't exist or was completed.")

    def show_all_task(self, txtfilter):
        """Show all task, optionaly filter the result"""
        if txtfilter == 'all':
            cursor = self.tasks.find({}, {'_id': 0}).sort('priority', 1)
            if cursor.count() < 1:
                print("----" * 10 + "\r\n", end="")
                print("Nothing added yet. Use '-a' option to create a task")
            else:
                for task in cursor:
                    print("----" * 10 + "\r\n", end="")
                    self.show_task(None, task)
        else:
            cursor = self.tasks.find(
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
                        },
                        {
                            'tags': {
                                '$regex': txtfilter,
                                '$options': 'i'
                            }
                        }
                    ],
                    'status': 'incomplete'
                },
                {'_id': 0}
            ).sort('priority', 1)
            if cursor.count() < 1:
                print("----" * 10 + "\r\n", end="")
                print(
                    "Nothing added with the filter: '{0}'.\r\n"
                    "Use '-a' option to create a task".format(txtfilter)
                )
            else:
                for task in cursor:
                    print("----" * 10 + "\r\n", end="")
                    self.show_task(None, task)
