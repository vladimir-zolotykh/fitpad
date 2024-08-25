#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
"""
>>> frame[0, 0]
<tkinter.Label object .workout.exercise_name>
>>> frame[1, 0]
<tkinter.Entry object .workout.set_no>
>>> frame[1, 1]
<tkinter.Entry object .workout.weight>
>>> frame[1, 2]
<tkinter.Entry object .workout.reps>
>>> frame[2, 0]
<tkinter.Button object .workout.edit>
"""

from abc import ABC, abstractmethod
from typing import Tuple
import doctest
import tkinter as tk
from entry_var import EntryVar
# from wo_tools import NumberedExer


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

    # @abstractclassmethod
    # def row_range(self) -> Tuple[int, int]:
    #     """Return the number of rows in the frame"""
    #     return (0, 0)

    # def row_sorted(self, row: int) -> List[tk.Widget]:
    #     """Return the row ROW sorted by column number"""

    #     return sorted(self.grid_slaves(row=row),
    #                   key=lambda w: w.grid_info()['column'])

    # def row_forget(self, row: int) -> None:
    #     """.grid_forget all widgets in the row ROW"""

    #     for w in self.grid_slaves(row=row):
    #         w.grid_forget()

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

    @staticmethod
    def print_size(meth):
        """A decorator to print called method's name

        and the Frame's size
        in the form
        NumberedFrame.edit_sets: num_cols = 2, num_rows = 2
        """

        def wrapper(self, *args, **kwargs):
            num_cols, num_rows = self.grid_size()
            cls_name = self.__class__.__name__
            print(f'{cls_name}.{meth.__name__}: {num_cols = }, {num_rows = }')
            return meth(self, *args, **kwargs)
        return wrapper


class Frame2DSet(Frame2D):
    def row_range(self) -> Tuple[int, int]:
        _, num_rows = self.grid_size()
        return (1, num_rows - 1)

    def arrange(self):
        cols, rows = self.grid_size()
        for i in range(1, rows - 1):
            slaves = self.grid_slaves(row=i)
            saved.append(slaves)
            set_no: EntryVar = self[i, 0]
            if int(set_no.get()) == 0:
                pass
            else:
                pass

            print(numbered_set)
        # print(f'Frame2DSet.arrange {cols = }, {rows = }')


if __name__ == '__main__':
    root = tk.Tk()
    frame = Frame2DExer(root, name='workout')
    frame.grid(column=0, row=0, sticky=tk.NSEW)
    label = tk.Label(frame, text='Deadlift', name='exercise_name')
    label.grid(column=0, row=0, columnspan=3)
    for col, (width, name) in enumerate(((2, 'set_no'), (8, 'weight'),
                                         (4, 'reps'))):
        _ = tk.Entry(frame, width=width, name=name)
        _.grid(column=col, row=1)
    btn = tk.Button(frame, text='Edit', name='edit')
    btn.grid(column=0, row=2, columnspan=3)
    # root.mainloop()
    doctest.testmod()
