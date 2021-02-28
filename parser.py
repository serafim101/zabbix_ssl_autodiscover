#!/usr/bin/env python3
import os, sys, string, json
from pyparsing import (
    Literal, White, Word, alphanums, CharsNotIn, Forward, Group, SkipTo,
    Optional, OneOrMore, ZeroOrMore, pythonStyleComment, LineEnd)

# parsing the system argument to get the path folder with nginx configs
if __name__ == "__main__":
        for param in sys.argv:
                location = param


# This part was taken from this project - https://github.com/fatiherikli/nginxparser
# For convenience, the class and function have been placed inside my script, FOR USE PERFORMANCE ONLY!
### The beginning of the copied part ###
class NginxParser(object):
    """
    A class that parses nginx configuration with pyparsing
    """

    # constants
    left_bracket = Literal("{").suppress()
    right_bracket = Literal("}").suppress()
    semicolon = Literal(";").suppress()
    space = White().suppress()
    key = Word(alphanums + "_/")
    value = CharsNotIn("{};")
    value2 = CharsNotIn(";")
    location = CharsNotIn("{};," + string.whitespace)
    ifword = Literal("if")
    setword = Literal("set")
    # modifier for location uri [ = | ~ | ~* | ^~ ]
    modifier = Literal("=") | Literal("~*") | Literal("~") | Literal("^~")

    # rules
    assignment = key + Optional(space + value) + semicolon
    comment = pythonStyleComment + LineEnd()
    setblock = setword + OneOrMore(space + value2) + semicolon
    block = Forward()
    ifblock = Forward()
    subblock = Forward()

    ifblock << (
        Group(ifword + Optional(space) + Optional(value) + SkipTo('{'))
        + left_bracket
        + Group(subblock)
        + right_bracket)

    subblock << ZeroOrMore(
        Group(comment) | Group(assignment) | block | Group(ifblock) | setblock
    )

    block << Group(
        Group(key + Optional(space + modifier) + Optional(space) + Optional(location))
        + left_bracket
        + Group(subblock)
        + right_bracket
    )

    # script = OneOrMore(Group(assignment) | block).ignore(pythonStyleComment)
    script = OneOrMore(Group(comment) | Group(assignment) | block)

    def __init__(self, source):
        self.source = source

    def parse(self):
        """
        Returns the parsed tree.
        """
        return self.script.parseString(self.source)

    def as_list(self):
        """
        Returns the list of tree.
        """
        return self.parse().asList()

def loads(source):
    return NginxParser(source).as_list()

def load(_file):
    return loads(_file.read())

def doubles(lst):
        tmp_list = []
        for item in lst:
                if item not in tmp_list:
                        tmp_list.append(item)
        return(tmp_list)
### End of the copied part of the code ###

# Parsing config directory for getting confil files list
config_list = os.listdir(path=location)

# parse the list of domains from the resulting list of configuration files. We are interested in the server_name option, which will contain a set of dns names
domain_list = []
for nginx_file in config_list:
        nginx_list = load(open(location+nginx_file))
        for list1 in nginx_list:
                for list2 in list1:
                        if len(list2) > 1:
                                for list3 in list2:
                                        if len(list3) > 1:
                                                if list3[0] == 'server_name':
                                                        if list3[1] != '_':
                                                                if len(list3[1].split()) > 1:
                                                                        for name in list3[1].split():
                                                                                domain_list.append(name)
                                                                else:
                                                                        domain_list.append(list3[1])

# This operation eliminates duplicates in the resulting list of domains. It could have been done more gracefully, but it must have been lazy
new_list = doubles(domain_list)
domain_list = []
for domain in new_list:
        domain_list.append({'{#NGINXVHOST}': domain})
domain_dict = {'data': domain_list}

# We display the finished result in json format
print(json.dumps(domain_dict))
