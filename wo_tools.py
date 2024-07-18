#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from typing import Dict, List, Optional
from prettytable import PrettyTable
from entry_var import EntryVar


def grid_column(widget: tk.Widget) -> int:
    """Return the column of widget"""

    return int(widget.grid_info()['column'])


def row_column(row: List[tk.Widget], column: int = 0) -> Optional[tk.Widget]:
    w: Optional[tk.Widget] = None
    for w in row:
        if grid_column(w) == column:
            return w
    return None


def row_set(row: List[tk.Widget]) -> int:
    """Return the set number

    Each set [of exercise] has a set number, the 1st Entry widget of a
    grid row"""

    w: Optional[tk.Widget] = row_column(row, 0)
    if isinstance(w, EntryVar):
        var: tk.StringVar = w.configure('textvariable')
        return int(var.get())
    else:
        raise TypeError(f'Expected Entry widget, got {type(w)}')


def grid_info(container: tk.Frame) -> str:
    num_cols, num_rows = container.grid_size()
    table = PrettyTable()
    # table.align = 'l'
    table.field_names = ['row', 'num columns']
    for num_row in range(num_rows):
        table.add_row([num_row, len(container.grid_slaves(row=num_row))])
    return str(table)


def rows_info(rows: Dict[int, List[tk.Widget]]) -> str:
    table = PrettyTable()
    table.field_names = ['row', 'num columns']
    for row in range(len(rows)):
        try:
            table.add_row([row, len(rows[row + 1])])
        except KeyError:
            pass
    return str(table)
