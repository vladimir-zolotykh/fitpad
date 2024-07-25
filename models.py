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
    weight: Mapped[float]
    reps: Mapped[int]
    exercise: Mapped['Exercise'] = relationship(
        'Exercise', secondary='workout_exercise', back_populates='workouts',
        cascade='all, delete')

    def __repr__(self) -> str:
        return (f'Workout(id={self.id!r}, when={self.when!r}, '
                f'weight={self.weight!r}, reps={self.reps!r})')


class Exercise(Base):
    __tablename__ = 'exercise'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    workouts: Mapped[List['Workout']] = relationship(
        'Workout', secondary='workout_exercise',
        back_populates='exercise', passive_deletes=True)

    def __repr__(self) -> str:
        return (f'Exercise(id={self.id!r}, name={self.name!r})')
