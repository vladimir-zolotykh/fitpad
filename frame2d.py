#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from abc import ABC, abstractmethod
import tkinter as tk


class Frame2D(tk.Frame, ABC):
    def __init__(self, parent, **kwargs):
        super(Frame2D, self).__init__(parent, **kwargs)

    def __getitem__(self, rowcol):
        col_max, row_max = self.grid_size()
        row, col = rowcol
        if (0 <= col < col_max) and (0 <= row < row_max):
            slaves = self.grid_slaves(row=row)
            for widget in slaves:
                if widget.grid_info()['column'] == col:
                    return widget
        else:
            raise IndexError(f'Invalid index {rowcol}. '
                             f'Expected ({row_max = }, {col_max = })')

    @abstractmethod
    def arrange(self):
        """Sort rows from `from_' to `to' [from, to(

        Rows are .grid_forget (-ed), sorted, then .grid (-ed) again in
        the new order. Before forgetting the widget, save its options
        (how it was packed), re -pack the widget how it was orignally
        packed (apply the saved options)

        The default `key' function assumes that the 1st column of a
        row has the EntryVar widget. The function returns the
        EntryVar's associated variable value converted to an integer
        """
        # raise NotImplementedError()
        return
