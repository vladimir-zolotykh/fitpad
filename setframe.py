#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import sys
from contextlib import contextmanager
from typing import Dict
from typing import Generator, List, cast
import tkinter as tk
from entry_var import EntryVar
import frame2d_set as f2s
# from wo_tools import NumberedSet, sets_info


class SetFrame(f2s.Frame2DSet):
    """Make tk widgets representing an exercise"""

    NUM_COLUMNS = 3
    COL_WIDTH = {'set_no': 2, 'weight': 10, 'reps': 3}

    def __init__(self, parent, name: str, row: int):
        super().__init__(parent)
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

    def yield_sets(self) -> Generator[List[str], None, None]:
        num_columns, num_rows = self.grid_size()
        for i in range(1, num_rows - 1):
            values = []
            for j in range(num_columns):
                w: tk.Widget = self[i, j]
                if isinstance(w, EntryVar):
                    e: EntryVar = cast(EntryVar, w)
                    values.append(e.get())
                else:
                    raise TypeError(f'Expected EntryVar widget, got {type(w)}')
            yield values

    # @Frame2D.print_size
    def edit_sets(self):
        self.arrange()

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
