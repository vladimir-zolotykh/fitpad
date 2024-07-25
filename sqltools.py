#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import Optional
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from models import Base, Exercise, Workout


# make_exercise_table
if __name__ == '__main__':
    engine = create_engine('sqlite:///fitpad.db', echo=True)
    Base.metadata.create_all(engine)
    front_squat = Exercise(name='front squat')
    squat = Exercise(name='squat')
    bench_press = Exercise(name='bench press')
    deadlift = Exercise(name='deadlift')
    with Session(engine) as session:
        session.add_all([front_squat, squat, bench_press, deadlift])
        session.commit()


# read_exercise_table
if __name__ == '__main__':
    engine = create_engine('sqlite:///fitpad.db', echo=True)
    session = Session(engine)
    stmt = select(Exercise).where(True)
    for exercise in session.scalars(stmt):
        print(exercise)

# make_workout
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


# read_workout_table
if __name__ == '__main__':
    engine = create_engine('sqlite:///fitpad.db', echo=True)
    session = Session(engine)
    stmt = select(Workout).where(True)
    for workout in session.scalars(stmt):
        print(workout)
