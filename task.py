#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple todo manager app"""
from argparse import ArgumentParser
from model import Client


class Taskparser(object):
    """Parser to manage de options and arguments"""
    def __init__(self):
        self.args = []
        self.parser = ArgumentParser(description="Task Manager app")
        self.create_argument_parser()
        self.dbclient = Client()

    def create_argument_parser(self):
        """Create the argument group and other arguments."""
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument(
            "-a",
            "--add",
            nargs="+",
            dest="description",
            help="Add a task",
            metavar="DESCRIPTION"
        )
        group.add_argument(
            "-c",
            "--complete",
            type=int,
            help="Check a task as complete",
            metavar="TASK ID"
        )
        group.add_argument(
            "-l",
            "--list",
            nargs='?',
            const='all',
            help="List all task",
            metavar="FILTER"
        )
        group.add_argument(
            "-s",
            "--show",
            type=int,
            help="Show a task",
            metavar="TASK ID"
        )
        self.parser.add_argument(
            "-p",
            "--project",
            dest="project",
            help="Project of a task",
            metavar="PROJECT"
        )
        self.parser.add_argument(
            "-t",
            "--tags",
            nargs="+",
            dest="tags",
            help="Tags of a task(space between tags)",
            metavar="TAGS"
        )
        self.parser.add_argument(
            "parameter",
            nargs="*",
            metavar="Description"
        )

    def process_args(self):
        """Procesa los argumentos y devuelve un resultado afín"""
        args = self.parser.parse_args()
        if args.list:
            self.dbclient.show_all_task(args.list)
        elif args.show:
            self.dbclient.show_task(args.show)
        elif args.description:
            new_doc = self.dbclient.create_task(vars(args))
            self.dbclient.insert_task(new_doc)
        elif args.complete:
            self.dbclient.complete_task(args.complete)
        elif args.parameter:
            new_doc = self.dbclient.create_task(vars(args))
            self.dbclient.insert_task(new_doc)


def main():
    """Main function"""
    task = Taskparser()
    task.process_args()


if __name__ == '__main__':
    main()
