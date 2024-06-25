#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Dict, Any
from functools import partial
import tkinter as tk


class ExerBox(tk.Frame):
    def __init__(self, parent, exer_name, exer_row):
        super(ExerBox, self).__init__(parent)
        self.grid(column=0, row=0, sticky=tk.EW)
        tk.Label(self, text=exer_name).grid(column=0, row=0, columnspan=2)
        tk.Entry(self, width=5).grid(column=0, row=1)
        tk.Entry(self, width=5).grid(column=1, row=1)
        tk.Button(self, text='Add set', command=None).grid(
            column=0, row=2, columnspan=2)


class Workout(tk.Tk):
    def __init__(self, *args, **kwargs):
        super(Workout, self).__init__(*args, **kwargs)
        self.title('Workout')
        self.geometry('500x200+400+300')
        menubar = tk.Menu(self, tearoff=0)
        self['menu'] = menubar
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='Quit', command=self.quit)
        menubar.add_cascade(label='File', menu=file_menu)
        add_exer_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='Add exercise', menu=add_exer_menu)
        self.exer_dir: Dict[str, Any] = {
            'squat': None, 'bench press': Any, 'deadlift': Any
        }
        exer_box = tk.Frame(self)
        exer_box.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        for exer_name in self.exer_dir:
            _add_exer = partial(self.add_exer, exer_box, exer_name, 0)
            add_exer_menu.add_command(label=exer_name, command=_add_exer)

    def add_exer(self, exer_box, exer_name, exer_row):
        ExerBox(exer_box, exer_name, exer_row)


if __name__ == '__main__':
    Workout().mainloop()
