# -*- coding: utf-8 -*-
""" Printing pretty json tables """


def clean_tags(tags):
    """Change all tags to lowercase and remove duplicated."""
    new_tags = []
    for tag in tags:
        new_tags.append(tag.lower())
    return list(set(new_tags))


def format_field(name, value):
    """Format a Field of a task"""
    if name == 'status':
        if value == 'complete':
            value = '--{}--'.format(value)
    elif name in ['date', 'due_date', 'complete_date']:
        value = value.strftime("%d/%m/%Y %H:%M")
    return '{}: {}\r\n'.format(name, value)


def prioritize(priority):
    """
    Check if the parameter is a proper priority.
    H for High priority.
    L for Low priority. This is the default.
    """
    if priority and priority in 'hH':
        return 'H'
    else:
        return 'L'


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
