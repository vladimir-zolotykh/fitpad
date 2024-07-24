#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import List
from sqlalchemy import ForeignKey, Column, Table, Integer
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


workout_exercise = Table(
    'workout_exercise',
    Base.metadata,
    Column('workout_id', Integer,
           ForeignKey('workout.id', ondelete='CASCADE')),
    Column('exercise_id', Integer,
           ForeignKey('exercise.id', ondelete='CASCADE')))


class Workout(Base):
    __tablename__ = 'workout'
    id: Mapped[int] = mapped_column(primary_key=True)
    when: Mapped[str]
    reps: Mapped[int]
    weight: Mapped[float]
    exercise: Mapped['Exercise'] = relationship(
        'Exercise', secondary='workout_exercise', back_populates='workouts',
        cascade='all, delete')


class Exercise(Base):
    __tablename__ = 'exercise'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    workouts: Mapped[List['Workout']] = relationship(
        'Workout', secondary='workout_exercise',
        back_populates='exercise', passive_deletes=True)
