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

import doctest
import tkinter as tk


class Frame2D(tk.Frame):
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

    def sort(self, key=None, from_=None, to=None):
        """Sort rows from `from_' to `to' inclusive

        Rows are .grid_forget (-ed), sorted, then .grid (-ed) again in
        the new order. Before forgetting the widget, save its options
        (how it was packed), re -pack the widget how it was orignally
        packed (apply the saved options)

        The default `key' function assumes that the 1st column of a
        row has the EntryVar widget. The function returns the
        EntryVar's associated variable value converted to an integer
        """
        pass


if __name__ == '__main__':
    root = tk.Tk()
    frame = Frame2D(root, name='workout')
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
