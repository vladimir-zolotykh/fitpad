#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from datetime import datetime
from models import Exercise, Workout
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session


if __name__ == '__main__':
    engine = create_engine('sqlite:///fitpad.db', echo=True)
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')
    with Session(engine) as session:
        stmt = select(Exercise).where(Exercise.name == 'front squat')
        front_squat = session.scalar(stmt)
        stmt = select(Exercise).where(Exercise.name == 'squat')
        squat = session.scalar(stmt)
        workout1 = Workout(exercise=front_squat, when=now, reps=5, weight=50.0)
        session.add(workout1)
        workout2 = Workout(exercise=squat, when=now, reps=5, weight=60.0)
        session.add(workout2)
        session.commit()
