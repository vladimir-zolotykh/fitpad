#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from models import Base, Exercise
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


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
