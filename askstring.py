#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from tkinter import simpledialog
from tkinter import _get_default_root  # noqa


class QueryString(simpledialog._QueryString):
    def __init__(self, *args, **kw):
        self.message = kw.pop('message') if 'message' in kw else None
        self.width = kw.pop('width') if 'width' in kw else 50
        super().__init__(*args, **kw)

    def body(self, master):
        entry = super().body(master)
        assert entry is self.entry
        if self.message:
            entry.insert(0, self.message)
        if isinstance(self.width, int):
            entry.configure(width=self.width)
        return entry


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
