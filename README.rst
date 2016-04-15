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
    priority: H
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
    priority: H
    project: Shopping
    status: --complete--
    ----------------------------------------
    date: 15/04/2016 10:43
    description: buy 2kg of bread
    id: 2
    priority: L
    project: Shopping
    status: incomplete
    tags: ['shopp', 'reminder']


Features

* Create task with description
* Complete a task
* List all task or filter for:
    * description
    * project
    * tags

* Show a task
* Support for project
* Support for priority
* Support for tags

Incoming Features
-----------------

* Improve global look and feel
* Support for due date
* Subtasks
* Batch insert from a file
* Support for projection settings in "PrettyJson"

Usage
-----

.. code-block:: bash

    usage: task.py [-h] [-a DESCRIPTION [DESCRIPTION ...] | -c TASK ID | -l
                   [FILTER] | -s TASK ID] [-p PROJECT]
                   [PARAMETER [PARAMETER ...]]

    Task Manager app

    positional arguments:
      PARAMETER

    optional arguments:
      -h, --help            show this help message and exit
      -a DESCRIPTION [DESCRIPTION ...], --add DESCRIPTION [DESCRIPTION ...]
                            Add a task
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
