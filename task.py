#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple todo manager app"""
from argparse import ArgumentParser
from model import Client


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
            self.dbclient.show_task(args.show)
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
