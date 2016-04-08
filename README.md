# TASKpy

A simple ToDo cli app using python and MongoDB.

## Requisites

* pymongo

## Usage

usage: task.py [-h] [-a ADD [ADD ...] | -c COMPLETE | -l [LIST] | -s SHOW]
               [-p PROJECT]
               [parametro [parametro ...]]

Simple todo app

positional arguments:
  parametro

optional arguments:
  -h, --help            show this help message and exit
  -a ADD [ADD ...], --add ADD [ADD ...]
                        Add a task
  -c COMPLETE, --complete COMPLETE
                        Check a task as complete
  -l [LIST], --list [LIST]
                        List all task
  -s SHOW, --show SHOW  Show a task
  -p PROJECT, --project PROJECT
                        Project of a task
