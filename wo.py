#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Dict, Any
from functools import partial
import tkinter as tk


class ExerTk(tk.Frame):
    """Make tk widgets representing an exercise"""

    def __init__(self, parent, name: str, row: int):
        super(ExerTk, self).__init__(parent)
        self.config(bd=2, relief=tk.RIDGE)
        self.columnconfigure(0, weight=1)
        self.grid(column=0, row=row, sticky=tk.EW)
        NCOL = 3
        for c in range(NCOL):
            self.columnconfigure(c, weight=1)
        tk.Label(self, text=name).grid(column=0, row=0, columnspan=NCOL)
        for c, w in enumerate((2, 10, 2)):
            tk.Entry(self, width=w).grid(column=c, row=1)
        tk.Button(self, text='Add set', command=None).grid(
            column=0, row=2, columnspan=NCOL)


class ExerDir(Dict[str, ExerTk]):
    """A dict of Workout exercises

    Dict[str, ExerTk]
    """

    def __init__(self, frame: tk.Frame):
        super().__init__()
        self.frame: tk.Frame = frame
        self.row: int = 0

    def add_exer(self, name: str):
        self[name] = ExerTk(self.frame, name, self.row)
        self.row += 1

    def del_exer(self, name: str):
        exertk = self[name]
        exertk.destroy()
        self.row -= 1


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
        frame = tk.Frame(self)
        frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        dir = ExerDir(frame)
        frame.columnconfigure(0, weight=1)
        for name in self.exer_dir:
            _add_exer = partial(dir.add_exer, name)
            add_exer_menu.add_command(label=name, command=_add_exer)


if __name__ == '__main__':
    Workout().mainloop()
