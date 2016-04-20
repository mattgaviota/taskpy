TASKpy
======

A simple ToDo cli app using python and MongoDB.

.. image:: https://landscape.io/github/mattgaviota/taskpy/master/landscape.svg?style=flat
   :target: https://landscape.io/github/mattgaviota/taskpy/master
   :alt: Code Health

.. image:: https://codeclimate.com/github/mattgaviota/taskpy/badges/gpa.svg
  :target: https://codeclimate.com/github/mattgaviota/taskpy
  :alt: Code Climate

Requisites
----------

* python 3.X
* pymongo(MongoDB 3.2)
* dateutil

Examples
--------

.. code-block:: bash

    $ task.py -a buy some milk -p Shopping -q H
    Task created with id 1

    $ task.py buy 2kg of bread -p Shopping -t shopp reminder
    Task created with id 2

    $ task.py -s 1
    date: 15/04/2016 10:43
    description: buy some milk
    id: 1
    priority: High
    project: Shopping
    status: incomplete


    $task.py -c 1
    Task 1 completed

    $ task.py -l shopping # only show incompleted tasks
    ----------------------------------------
    date: 11/04/2016 16:45
    description: buy 2kg of bread
    id: 2
    project: Shopping
    status: incomplete

    $ task.py -l # show all tasks
    ----------------------------------------
    complete_date: 15/04/2016 10:44
    date: 15/04/2016 10:43
    description: buy some milk
    priority: High
    project: Shopping
    status: --complete--
    ----------------------------------------
    date: 15/04/2016 10:43
    description: buy 2kg of bread
    id: 2
    priority: Low
    project: Shopping
    status: incomplete
    tags: ['shopp', 'reminder']

Batch insert
------------

Every line of the file must be a proper add task syntax

.. code-block::

    tastks.txt

    -a Buy some milk -p Shopping
    buy 2kg of bread -p Shopping -t food shopp
    make some food -q H -t hungry

    $ task.py -f tasks.txt
    Task created with id 1
    Task created with id 2
    Task created with id 3

Due Date
--------

In order to define a due date you have two options:

1. Date in the format 'dd/mm/yyyy' or 'dd-mm-yyyy'
2. Adding a period of time to the current date with the format
   (^\+){1}(\d+)([h|d|w|m|y])

..code-block::

    Assuming the current date is 19/04/2016

    $ task.py -a refactor the tests -d 04/05/2016 -p ImportantProject
    Task created with id 1

    $ task.py -a rewrite module credits -d +1w -p ImportantProject -q H
    Task created with id 2

    $ task.py -l
    ----------------------------------------
    date: 19/04/2016 23:52
    description: rewrite module credits
    due_date: 26/04/2016 23:52
    id: 2
    priority: High
    project: ImportantProject
    status: incomplete
    ----------------------------------------
    date: 19/04/2016 23:51
    description: refactor the tests
    due_date: 04/05/2016 00:00
    id: 1
    priority: Low
    project: ImportantProject
    status: incomplete


Features
--------

* Create task with description
* Complete a task
* List all task or filter for
    * description
    * project
    * tags
* Show a task
* Support for project(Case sensitive)
* Support for priority
* Support for tags
* Support for due date
* Batch insert from a file

Incoming Features
-----------------

* Improve global look and feel
* Subtasks
* Support for projection settings in "PrettyJson"

Usage
-----

.. code-block:: bash

    usage: task.py [-h] [-a DESCRIPTION [DESCRIPTION ...] | -f INPUT FILE | -c
           TASK ID | -l [FILTER] | -s TASK ID] [-p PROJECT]
           [-t TAGS [TAGS ...]] [-q PRIORITY] [-d DUE DATE]
           [Description [Description ...]]

    Task Manager app

    positional arguments:
    Description

    optional arguments:
    -h, --help            show this help message and exit
    -a DESCRIPTION [DESCRIPTION ...], --add DESCRIPTION [DESCRIPTION ...]
                    Add a task
    -f INPUT FILE, --file INPUT FILE
                    Add batch of tasks in a file
    -c TASK ID, --complete TASK ID
                    Check a task as complete
    -l [FILTER], --list [FILTER]
                    List all task
    -s TASK ID, --show TASK ID
                    Show a task
    -p PROJECT, --project PROJECT
                    Project of a task
    -t TAGS [TAGS ...], --tags TAGS [TAGS ...]
                    Tags of a task(space between tags)
    -q PRIORITY, --queue-priority PRIORITY
                    Priority ([H]igh, [L]ow)
    -d DUE DATE, --due-date DUE DATE
                    Due date as a date(dd/mm/YYYY) or a period in the format
                    (^\+){1}(\d+)([d|D|h|H|w|W|m|M|y|Y])
                    h -> hours
                    d -> days
                    w -> weeks
                    m -> months
                    y -> years
