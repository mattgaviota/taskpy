#! /usr/bin/env python
# -*- coding: utf-8 -*-
""" Printing pretty json tables """
from prettytable import PrettyTable
import datetime


class PrettyJson(object):
    """ A class for printing pretty json table """
    def __init__(self, json_list):
        self.table = PrettyTable()
        self.columns = json_list[0].keys()
        self.table.field_names = self.columns
        for item in json_list:
            self.table.add_row(self.make_custom_row(item))

    def make_custom_row(self, item):
        """ Make a row for printing it with pretty table
            Columns must match json attributes
        """
        row = []
        for col in self.columns:
            try:
                item_value = item[col.lower()]
                # prettytable has not incorporated datetime format
                if isinstance(item[col.lower()], datetime.datetime):
                    item_value = item[col.lower()].strftime("%x %X")
                row.append(item_value)
            except KeyError:
                print "Column %s do not match any json attribute", col
        return row

    def show(self):
        """ Show pretty tasks """
        print self.table


def main():
    """ Main program for pretty json tables """
    pass

if __name__ == '__main__':
    main()
