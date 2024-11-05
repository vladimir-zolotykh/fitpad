#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
import tkinter.simpledialog as simpledialog


class _QueryString(simpledialog._QueryString):
    def __init__(self, *args, **kw):
        self.default = None
        if 'default' in kw:
            self.default = kw['default']
            del kw['default']
        super().__init__(*args, **kw)

    def body(self, master):
        entry = super().body(master)
        var = tk.StringVar()
        var.set(self.default)
        entry.configure(textvariable=var)
        return entry


def askstring(title, prompt, **kw):
    '''get a string from the user

    Arguments:

        title   -- the dialog title
        prompt  -- the label text
        default -- default string value
        **kw    -- see SimpleDialog class

    Return value is a string
    '''
    d = _QueryString(title, prompt, **kw)
    return d.result
