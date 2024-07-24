#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Optional
from datetime import datetime
from models import Exercise, Workout
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
# $ rm fitpad.db
# $ python make_exercise_table.py
# $ python read_exercise_tables.py
# $ python python make_workout.py
# $ $ sqlite3 fitpad.db
# SQLite version 3.34.1 2021-01-20 14:10:07
# Enter ".help" for usage hints.
# sqlite> select * from workout;
# 1|2024-07-24 17:56:43|5|50.0
# 2|2024-07-24 17:56:43|5|60.0

if __name__ == '__main__':
    engine = create_engine('sqlite:///fitpad.db', echo=True)
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with Session(engine) as session:
        def get_exer(name: str) -> Optional[Exercise]:
            return session.scalar(
                select(Exercise).where(Exercise.name == name))

        session.add_all([Workout(exercise=get_exer('front squat'),
                                 when=now, reps=5, weight=50.0),
                         Workout(exercise=get_exer('squat'),
                                 when=now, reps=5, weight=60.0)])
        session.commit()
