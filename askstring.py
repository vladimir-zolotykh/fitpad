#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from tkinter import simpledialog
from tkinter import _get_default_root  # noqa


class QueryString(simpledialog._QueryDialog):
    def __init__(self, *args, **kw):
        if "show" in kw:
            self.__show = kw["show"]
            del kw["show"]
        else:
            self.__show = None
        self.message = None
        if 'message' in kw:
            self.message = kw.pop('message')
        simpledialog._QueryDialog.__init__(self, *args, **kw)

    def body(self, master):
        entry = simpledialog._QueryDialog.body(self, master)
        if self.message:
            self.entry.insert(0, self.message)
        if self.__show is not None:
            entry.configure(show=self.__show)
        return entry

    def getresult(self):
        return self.entry.get()


def askstring(title, prompt, message=None, **kw):
    '''get a string from the user

    Arguments:

        title -- the dialog title
        prompt -- the label text
        **kw -- see SimpleDialog class

    Return value is a string
    '''
    d = QueryString(title, prompt, message=message, **kw)
    return d.result
