#! /usr/bin/env python3
# coding=utf-8

"""Simple todo manager app"""
from argparse import ArgumentParser, FileType, RawTextHelpFormatter
from model import Client


OPTIONALS = ['parameter', 'tags', 'project', 'priority']


class Taskparser(object):
    """Parser to manage de options and arguments"""
    def __init__(self):
        self.args = []
        self.parser = ArgumentParser(
            description="Task Manager app",
            formatter_class=RawTextHelpFormatter
        )
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
            "-f",
            "--file",
            dest="file",
            type=FileType('r', encoding=None),
            help="Add batch of tasks in a file",
            metavar="INPUT FILE"
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
            "parameter",
            nargs="*",
            metavar="Description"
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
            "-q",
            "--queue-priority",
            dest="priority",
            help="Priority ([H]igh, [L]ow)",
            metavar="PRIORITY"
        )
        help_due = r"""Due date as a date(dd/mm/YYYY) or a period in the format
(^\+){1}(\d+)([d|D|h|H|w|W|m|M|y|Y])
h -> hours
d -> days
w -> weeks
m -> months
y -> years"""
        self.parser.add_argument(
            "-d",
            "--due-date",
            dest="due_date",
            help=help_due,
            metavar="DUE DATE"
        )
        self.parser.add_argument(
            "-b",
            "--bairn",
            dest="parent",
            help="Id of the parent task",
            metavar="PARENT ID"
        )

    def parse_args(self, args=None):
        """Parse arguments"""
        if args:
            return self.parser.parse_args(args)
        else:
            return self.parser.parse_args()

    def process_args(self, args):
        """Process arguments to execute the right for each one."""
        if args.parameter:
            if [
                    key for key, val in vars(args).items()
                    if val and key not in OPTIONALS
            ]:
                self.parser.print_help()
            else:
                new_doc = self.dbclient.create_task(vars(args))
                self.dbclient.insert_task(new_doc)
        elif args.list:
            self.dbclient.show_all_task(args.list)
        elif args.show:
            self.dbclient.show_task(args.show)
        elif args.description:
            new_doc = self.dbclient.create_task(vars(args))
            self.dbclient.insert_task(new_doc)
        elif args.complete:
            self.dbclient.complete_task(args.complete)
        elif args.file:
            for line in args.file:
                args = self.parse_args(line.rstrip('\r\n').split())
                self.process_args(args)
        else:
            self.parser.print_usage()


def main():
    """Main function"""
    task = Taskparser()
    args = task.parse_args()
    task.process_args(args)


if __name__ == '__main__':
    main()
