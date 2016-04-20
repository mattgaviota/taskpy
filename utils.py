# -*- coding: utf-8 -*-
""" Printing pretty json tables """
from datetime import datetime
import re
from dateutil.relativedelta import relativedelta


PERIODS = {
    'h': 'hours',
    'd': 'days',
    'w': 'weeks',
    'm': 'months',
    'y': 'years'
}


def clean_tags(tags):
    """Change all tags to lowercase and remove duplicated."""
    return sorted(list(set([tag.lower() for tag in tags])))


def format_field(name, value):
    """Format a Field of a task"""
    if value:
        if name == 'status':
            value = '--{}--'.format(value)
        elif name in ['date', 'due_date', 'complete_date']:
            value = value.strftime("%d/%m/%Y %H:%M")
        elif name == 'ancestors':
            value = ', '.join(['Task {}'.format(id) for id in value])
        elif name == 'parent':
            value = 'Task {}'.format(value)
        return '{}: {}\r\n'.format(name, value)
    else:
        return ''


def prioritize(priority):
    """
    Check if the parameter is a proper priority.
    H for High priority.
    L for Low priority. This is the default.
    """
    if priority and priority in 'hH':
        return 'High'
    else:
        return 'Low'


def extract_date(due_date):
    r"""
    Check the due date parameter to extract a date.
    Accepted Format:
        [((^\+){1}(\d+)([d|D|h|H|w|W|m|M|y|Y]))|(dd/mm/YYYY)]
    """
    # find delta
    delta_regx = re.compile(r'(^\+){1}(\d+)([d|D|h|H|w|W|m|M|y|Y])')
    search = delta_regx.search(due_date)
    if search:
        number, quantifier = search.groups()[1:]
        number = int(number)
        quantifier = quantifier.lower()
        date = datetime.now()
        if quantifier:
            date = date + relativedelta(**{PERIODS[quantifier]: number})
            return date
        else:
            return None
    else:
        # find datetime
        date_regx = re.compile(r'(\d\d)[-/](\d\d)[/|-](\d\d)')
        search = date_regx.search(due_date)
        if search:
            day, month, year = search.groups()
            str_date = "{0}/{1}/{2}".format(day, month, year)
            try:
                date = datetime.strptime(str_date, '%d/%m/%y')
            except ValueError:
                return None
            return date


# class PrettyJson(object):
#     """ A class for printing pretty json table """
#     def __init__(self, json_list):
#         self.table = PrettyTable()
#         self.columns = json_list[0].keys()
#         self.table.field_names = self.columns
#         for item in json_list:
#             self.table.add_row(self.make_custom_row(item))
#
#     def make_custom_row(self, item):
#         """ Make a row for printing it with pretty table
#             Columns must match json attributes
#         """
#         row = []
#         for col in self.columns:
#             try:
#                 item_value = item[col.lower()]
#                 # prettytable has not incorporated datetime format
#                 if isinstance(item[col.lower()], datetime.datetime):
#                     item_value = item[col.lower()].strftime("%x %X")
#                 row.append(item_value)
#             except KeyError:
#                 print(
#                    "Column {0} do not match any json attribute".format(col)
#                 )
#         return row
#
#     def show(self):
#         """ Show pretty tasks """
#         print(self.table)
