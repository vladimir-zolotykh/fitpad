#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
import argparse
import argcomplete
from typing import Optional
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.engine.base import Engine
from models import Base, Exercise, Workout
_functions = []


def register(func):
    _functions.append(func)
    return func


@register
def make_exercise_table(engine: Engine, verbose: bool = False) -> None:
    if 0 < verbose:
        print('make_exercise_table is called')
    engine = create_engine('sqlite:///fitpad.db', echo=True)
    Base.metadata.create_all(engine)
    front_squat = Exercise(name='front squat')
    squat = Exercise(name='squat')
    bench_press = Exercise(name='bench press')
    deadlift = Exercise(name='deadlift')
    with Session(engine) as session:
        session.add_all([front_squat, squat, bench_press, deadlift])
        session.commit()


@register
def read_exercise_table(engine: Engine, verbose: bool = False) -> None:
    if 0 < verbose:
        print('read_exercise_table is called')
    engine = create_engine('sqlite:///fitpad.db', echo=True)
    session = Session(engine)
    stmt = select(Exercise).where(True)
    for exercise in session.scalars(stmt):
        print(exercise)


@register
def make_workout_table(engine: Engine, verbose: bool = False) -> None:
    if 0 < verbose:
        print('make_workout_table is called')
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


@register
def read_workout_table(engine: Engine, verbose: bool = False) -> None:
    if 0 < verbose:
        print('read_workout_table is called')
    engine = create_engine('sqlite:///fitpad.db', echo=True)
    session = Session(engine)
    stmt = select(Workout).where(True)
    for workout in session.scalars(stmt):
        print(workout)


parser = argparse.ArgumentParser(
    prog='sqltools.py',
    description='Make/read fitpad.db table',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('function_name', nargs='+',
                    choices=[f.__name__ for f in _functions])
parser.add_argument(
    '--echo', action='store_true', help='Print emitted SQL commands')
parser.add_argument('--db', default='fitpad.db', help='Database file (.db)')
parser.add_argument(
    '--verbose', '-v', action='count', default=0, help='Provide some feedback')

if __name__ == '__main__':
    argcomplete.autocomplete(parser)
    args = parser.parse_args()
    engine = create_engine(f'sqlite:///{args.db}', echo=args.echo)
    for fn in args.function_name:
        func = globals()[fn]
        func(engine, verbose=args.verbose)
