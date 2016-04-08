# TASKpy

A simple ToDo cli app using python and MongoDB.

[![Code Health](https://landscape.io/github/mattgaviota/taskpy/master/landscape.svg?style=flat)](https://landscape.io/github/mattgaviota/taskpy/master)
[![Code Climate](https://codeclimate.com/github/mattgaviota/taskpy/badges/gpa.svg)](https://codeclimate.com/github/mattgaviota/taskpy)

## Requisites

* pymongo

## Usage

```bash
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
```

## Features

* Create task with description and an optional project
* Complete a task
* List all task or filter by description or project
* Show a task

## Incoming Features

* Support for tags
* Support for due date
* Subtasks
* Batch insert from a file
