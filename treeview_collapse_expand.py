#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import tkinter as tk
from tkinter import ttk

data = [
    {"date": "2024-09-01", "exercise": "Squat", "weight": 100, "reps": 5},
    {"date": "2024-09-02", "exercise": "Bench Press", "weight": 80, "reps": 8},
    {"date": "2024-09-03", "exercise": "Deadlift", "weight": 120, "reps": 4}
]
root = tk.Tk()
root.title("Exercise Log")
tree = ttk.Treeview(root, columns=("exercise", "weight", "reps"))
tree.heading("#0", text="Date")
tree.heading("exercise", text="exercise")
tree.heading("weight", text="Weight (kg)")
tree.heading("reps", text="Reps")
tree.column("#0", width=100)
tree.column("exercise", width=150)
tree.column("weight", width=100)
tree.column("reps", width=100)
for i, entry in enumerate(data):
    parent = tree.insert("", "end", text=entry["date"],
                         values=(entry["exercise"], "", ""))
    tree.insert(parent, "end", text="",
                values=("", entry["weight"], entry["reps"]))
tree.pack(fill="both", expand=True)
root.mainloop()
