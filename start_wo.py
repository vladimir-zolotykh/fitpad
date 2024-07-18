#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import sys
from typing import Dict, Any, List
from functools import partial
from contextlib import contextmanager
import tkinter as tk
from wo_tools import grid_column, row_set
from wo_tools import rows_info


class EntryVar(tk.Entry):
    def __init__(self, parent, cnf=None, **kw):
        super(EntryVar, self).__init__(parent, cnf, **kw)
        if isinstance(cnf, dict):
            kw.update(cnf)
        if 'textvariable' in kw:
            self._var = kw.get('textvariable')

    def configure(self, cnf=None, **kw):
        if cnf is None and not kw:
            return super().configure()
        elif isinstance(cnf, str):
            if cnf == 'textvariable':
                return self._var
            else:
                return self._get_config(cnf)
        elif isinstance(cnf, dict):
            kw.update(cnf)
            return self._set_config(kw)

    def _get_config(self, option=None):
        if option:
            return super().configure(option)
        else:
            return super().configure()

    def _set_config(self, **options):
        if 'textvariable' in options:
            self._var = options.get('textvariable')
        return super().configure(**options)


class ExerTk(tk.Frame):
    """Make tk widgets representing an exercise"""

    NUM_COLUMNS = 3
    COL_WIDTH = {'set_no': 2, 'weight': 10, 'reps': 3}

    def __init__(self, parent, name: str, row: int):
        super(ExerTk, self).__init__(parent)
        self.grid(column=0, row=row, sticky=tk.EW)
        self.name = name
        self.last_set: int = 1
        self.set_no: Dict[int, tk.StringVar] = {}
        self.config(bd=2, relief=tk.RIDGE)
        self.columnconfigure(0, weight=1)
        for c in range(self.NUM_COLUMNS):
            self.columnconfigure(c, weight=1)
        tk.Label(self, text=name).grid(
            column=0, row=0, columnspan=self.NUM_COLUMNS)
        # self.add_set0()
        self.add_set()
        mb = tk.Menubutton(self, relief=tk.RAISED, text='Edit')
        mb.grid(column=0, row=2, columnspan=self.NUM_COLUMNS)
        mb_menu = tk.Menu(mb, tearoff=0)
        mb['menu'] = mb_menu
        # mb_menu.add_command(label='Add set', command=self.add_set2)
        mb_menu.add_command(label='Add set', command=self.add_set)
        mb_menu.add_command(label='Move up')
        mb_menu.add_command(label='Move down')
        mb_menu.add_command(label='Remove')
        mb_menu.add_command(label='Edit sets', command=self.edit_sets)

    @contextmanager
    def num_rows_printed(self, label='***'):
        n1 = self.grid_size()[1]
        yield
        n2 = self.grid_size()[1]
        print(f'{label} num_rows = {n1}/{n2}')
        sys.stdout.flush()

    def edit_sets(self):
        _, num_rows = self.grid_size()
        mb_row = self.grid_slaves(row=num_rows - 1)

        # print(grid_info(self))
        sets_sorted = sorted(
            [self.grid_slaves(row=row) for row in range(1, num_rows - 1)],
            key=row_set)
        rows_sorted: Dict[int, List[tk.Widget]] = {}

        num_row: int = 1
        for row in sets_sorted:
            if row_set(row) == 0:
                for w in row:
                    w.destroy()
            else:
                rows_sorted[num_row] = sorted(row, key=grid_column)
                num_row += 1
                for w in row:
                    w.grid_forget()
            self.last_set -= 1
        mb_row[0].grid_forget()
        self.last_set = 1
        num_row = 0
        for num_row, row in rows_sorted.items():
            for col, w in enumerate(row):
                w.grid(column=col, row=num_row)
            self.last_set += 1
        print(rows_info(rows_sorted))
        mb_row[0].grid(column=0, row=num_row + 1, columnspan=self.NUM_COLUMNS)

    def renumber_existing_sets(self):
        pass

    def grid_the_set(self, num_row: int):
        """Grid a set's widgets

        Exercises have sets. A set has tk widgets organized in a
        row. This method adds widgets for one set.
        """
        var = tk.StringVar()
        var.set(str(num_row))
        self.set_no[num_row] = var
        for c, w in enumerate(self.COL_WIDTH.values()):
            e = EntryVar(self, width=w)
            e.grid(column=c, row=num_row)
            if c == 0:
                e.config(textvariable=var)
        self.last_set += 1

    def add_set(self):
        num_rows: int = self.grid_size()[1]
        if 2 <= num_rows:
            mb = self.grid_slaves(row=num_rows - 1)[0]  # menu button
            last: int = num_rows - 1
            self.grid_the_set(last)
            mb.grid(column=0, row=last + 1, columnspan=self.NUM_COLUMNS)
        elif num_rows == 1:
            self.grid_the_set(self.last_set)
        else:
            raise TypeError(f'{num_rows = }: must be 1 or >= 2')


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
        frame.columnconfigure(0, weight=1)
        dir = ExerDir(frame)
        for name in self.exer_dir:
            _add_exer = partial(dir.add_exer, name)
            add_exer_menu.add_command(label=name, command=_add_exer)


if __name__ == '__main__':
    Workout().mainloop()
