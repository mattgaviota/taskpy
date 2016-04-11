# TASKpy

A simple ToDo cli app using python and MongoDB.

[![Code Health](https://landscape.io/github/mattgaviota/taskpy/master/landscape.svg?style=flat)](https://landscape.io/github/mattgaviota/taskpy/master)
[![Code Climate](https://codeclimate.com/github/mattgaviota/taskpy/badges/gpa.svg)](https://codeclimate.com/github/mattgaviota/taskpy)

## Requisites

* python 3.X
* pymongo(MongoDB 3.2)

## Examples
```
$ task.py -a buy some milk -p Shopping
Task created with id 1

$ task.py buy 2kg of bread -p Shopping
Task created with id 2

$ task.py -s 1
date: 11/04/2016 16:44
description: buy some milk
id: 2
project: Shopping
status: incomplete

$task.py -c 1
Task 2 completed

$ task.py -l shopping # only show incompleted tasks
----------------------------------------
date: 11/04/2016 16:45
description: buy 2kg of bread
id: 3
project: Shopping
status: incomplete

$ task.py -l # show all tasks
----------------------------------------
complete_date: 11/04/2016 16:46
date: 11/04/2016 16:44
description: buy some milk
project: Shopping
status: --complete--
----------------------------------------
date: 11/04/2016 16:45
description: buy 2kg of bread
id: 3
project: Shopping
status: incomplete

```

## Features

* Create task with description and an optional project
* Complete a task
* List all task or filter by description or project
* Show a task

## Incoming Features

* Improve global look and feel
* Support for tags
* Support for due date
* Subtasks
* Batch insert from a file
* Support for projection settings in "PrettyJson"

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
