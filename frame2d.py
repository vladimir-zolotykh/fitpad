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
            raise IndexError()


# if __name__ == '__main__':
root = tk.Tk()
frame = Frame2D(root, name='workout')
frame.grid(column=0, row=0, sticky=tk.NSEW)
label = tk.Label(frame, text='Deadlift', name='exercise_name')
label.grid(column=0, row=0, columnspan=3)
set_no = tk.Entry(frame, width=2, name='set_no')
set_no.grid(column=0, row=1)
weight = tk.Entry(frame, width=8, name='weight')
weight.grid(column=1, row=1)
reps = tk.Entry(frame, width=4, name='reps')
reps.grid(column=2, row=1)
btn = tk.Button(frame, text='Edit', name='edit')
btn.grid(column=0, row=2, columnspan=3)
# root.mainloop()
if __name__ == '__main__':
    doctest.testmod()