#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import sys
from contextlib import contextmanager
from typing import Dict
from typing import Generator, List
import tkinter as tk
from entry_var import EntryVar
from frame2d import Frame2D
from wo_tools import NumberedSet, sets_info


class ExerTk(Frame2D):
    """Make tk widgets representing an exercise"""

    NUM_COLUMNS = 3
    COL_WIDTH = {'set_no': 2, 'weight': 10, 'reps': 3}

    def __init__(self, parent, name: str, row: int):
        super(ExerTk, self).__init__(parent)
        self.grid(column=0, row=row, sticky=tk.EW)
        self.name = name
        self.last_set: int = 1
        self.set_no: Dict[int, tk.StringVar] = {}
        pady: int = 2
        self.config(bd=pady, relief=tk.RIDGE)
        self.columnconfigure(0, weight=1)
        for c in range(self.NUM_COLUMNS):
            self.columnconfigure(c, weight=1)
        label = tk.Label(self, text=name)
        label.grid(column=0, row=0, columnspan=self.NUM_COLUMNS)
        self.add_set()
        mb = tk.Menubutton(self, relief=tk.RAISED, text='Edit')
        mb.grid(column=0, row=2, columnspan=self.NUM_COLUMNS)
        mb_menu = tk.Menu(mb, tearoff=0)
        mb['menu'] = mb_menu
        mb_menu.add_command(label='Add set', command=self.add_set)
        mb_menu.add_command(label='Edit sets', command=self.edit_sets)
        label.configure(pady=pady + (mb.winfo_reqheight() -
                                     label.winfo_reqheight()) // 2)

    @contextmanager
    def num_rows_printed(self, label='***'):
        n1 = self.grid_size()[1]
        yield
        n2 = self.grid_size()[1]
        print(f'{label} num_rows = {n1}/{n2}')
        sys.stdout.flush()

    # def yield_sets(self) -> Generator[Tuple[str, str, str], None, None]:
    def yield_sets(self) -> Generator[List[str], None, None]:
        num_columns, num_rows = self.grid_size()
        sets_sorted = sorted(
            [NumberedSet.from_grid(self, row=row)
             for row in range(1, num_rows - 1)],
            key=NumberedSet.set_no)
        for row in sets_sorted:
            values = []
            for w in row:
                if isinstance(w, EntryVar):
                    values.append(w.get())
                else:
                    raise TypeError(f'Expected EntryVar widget, got {type(w)}')
            yield values

    def edit_sets(self):
        _, num_rows = self.grid_size()
        mb_row = self.grid_slaves(row=num_rows - 1)

        # print(grid_info(self))
        sets_sorted = sorted(
            [NumberedSet.from_grid(self, row=row)
             for row in range(1, num_rows - 1)],
            key=NumberedSet.set_no)
        # rows_sorted: Dict[int, List[tk.Widget]] = {}
        rows_sorted: Dict[int, NumberedSet] = {}

        num_row: int = 1
        for row in sets_sorted:
            if row.set_no() == 0:
                for w in row:
                    w.destroy()
            else:
                rows_sorted[num_row] = NumberedSet.from_list(row)
                num_row += 1
                for w in row:
                    w.grid_forget()
            self.last_set -= 1
        mb_row[0].grid_forget()
        self.last_set = 1
        num_row = 0
        self.renumber_existing_rows(rows_sorted)
        for num_row, row in rows_sorted.items():
            for col, w in enumerate(row):
                w.grid(column=col, row=num_row)
            self.last_set += 1
        # self.renumber_existing_sets()
        print(sets_info(rows_sorted))
        mb_row[0].grid(column=0, row=num_row + 1, columnspan=self.NUM_COLUMNS)

    def renumber_existing_rows(self, rows: Dict[int, NumberedSet]):
        set_no: int = 1
        for row in rows.values():
            e = row[0]
            v = e.configure('textvariable')
            v.set(set_no)
            set_no += 1

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
                e.configure(textvariable=var)
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
