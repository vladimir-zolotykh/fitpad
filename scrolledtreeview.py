#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk


class ScrolledTreeview(ttk.Treeview):
    def __init__(self, parent, **kw):
        def expand(w):
            w.columnconfigure(0, weight=1)
            w.rowconfigure(0, weight=1)

        box = tk.Frame(parent)
        expand(box)
        box.grid(column=0, row=0, sticky=tk.NSEW)
        hbar = tk.Scrollbar(box, orient=tk.HORIZONTAL, command=self.xview)
        hbar.grid(column=0, row=1, sticky=tk.EW)
        vbar = tk.Scrollbar(box, orient=tk.VERTICAL, command=self.yview)
        vbar.grid(column=1, row=0, sticky=tk.NS)
        kw.update({'xscrollcommand': hbar.set, 'yscrollcommand': vbar.set})
        super().__init__(box, **kw)
        self.grid(column=0, row=0, sticky=tk.NSEW)
        # for meth in ('grid', 'grid_forget', 'grid_configure'):
        for meth in (meth for meth in dir(box) if meth.startswith('grid_')):
            setattr(self, meth, getattr(box, meth))
