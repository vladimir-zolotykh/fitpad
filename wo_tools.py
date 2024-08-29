#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from typing import Dict, cast
from prettytable import PrettyTable
from frame2d_exer import Frame2DExer
# from numbered_set import NumberedSet
from numbered_exer import NumberedExer


class Wo(list):
    def __init__(self, frame: Frame2DExer):
        # frame: '.workout_frame'
        num_cols, num_rows = frame.grid_size()  # 1, 1
        super().__init__(
            [NumberedExer(cast(Frame2DExer, frame.grid_slaves(row=row)[0]))
             for row in range(num_rows)])
        self.sort(key=lambda e: e.exer_no())


# def grid_info(container: tk.Frame) -> str:
#     num_cols, num_rows = container.grid_size()
#     table = PrettyTable()
#     # table.align = 'l'
#     table.field_names = ['row', 'num columns']
#     for num_row in range(num_rows):
#         table.add_row([num_row, len(container.grid_slaves(row=num_row))])
#     return str(table)


# def sets_info(rows: Dict[int, NumberedSet]) -> str:
#     table = PrettyTable()
#     table.field_names = ['row', 'num columns']
#     for row in range(len(rows)):
#         try:
#             table.add_row([row, len(rows[row + 1])])
#         except KeyError:
#             pass
#     return str(table)
