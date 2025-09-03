#!/usr/bin/python
# -*- coding: utf-8 -*-





class SmartlingDirective:
    """ Smartling directive which is used for file upload """
    SL_PREFIX = "smartling."

    def __init__(self, name, value):
        if not name:
            raise Exception("name cannot be empty!")
        self.name = self.__unPrefix(name.lower())

        if value is None:
            self.value = ""
        else:
            self.value = value

    def __unPrefix(self, name):
        if name.startswith(self.SL_PREFIX):
            return name[len(self.SL_PREFIX):]
        return name
