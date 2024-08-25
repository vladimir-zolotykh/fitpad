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
from frame2d_exer import Frame2DExer

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
