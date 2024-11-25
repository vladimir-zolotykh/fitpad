#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# PYTHON_ARGCOMPLETE_OK
from typing import List
from datetime import datetime
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


workout_schedule = Table(
    'workout_schedule',
    Base.metadata,
    Column('workout_id', Integer,
           ForeignKey('workout.id', ondelete='CASCADE')),
    Column('schedule_id', Integer,
           ForeignKey('schedule.id', ondelete='CASCADE')))


class Workout(Base):
    __tablename__ = 'workout'
    id: Mapped[int] = mapped_column(primary_key=True)
    when: Mapped[str]
    weight: Mapped[float]
    reps: Mapped[int]
    exercise: Mapped['Exercise'] = relationship(
        'Exercise', secondary='workout_exercise', back_populates='workouts',
        cascade='all, delete')
    schedule: Mapped['Schedule'] = relationship(
        'Schedule', secondary='workout_schedule', back_populates='workouts',
        cascade='all, delete')

    def __repr__(self) -> str:
        return (f'Workout(id={self.id!r}, when={self.when!r}, '
                f'weight={self.weight!r}, reps={self.reps!r})')

    def date(self, relative: bool = False) -> str:
        """Date of workout"""
        if relative:
            date: datetime = datetime.strptime(self.when, '%Y-%m-%d %H:%M:%S')
            td = datetime.now() - date
            return f'-{td.days}d <{self.schedule.name}>'
        else:
            return self.when.split()[0]


class Exercise(Base):
    __tablename__ = 'exercise'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    workouts: Mapped[List['Workout']] = relationship(
        'Workout', secondary='workout_exercise',
        back_populates='exercise', passive_deletes=True)

    def __repr__(self) -> str:
        return (f'Exercise(id={self.id!r}, name={self.name!r})')


class Schedule(Base):
    __tablename__ = 'schedule'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    workouts: Mapped[List['Workout']] = relationship(
        'Workout', secondary='workout_schedule',
        back_populates='schedule', passive_deletes=True)

    def __repr__(self) -> str:
        return (f'Schedule(id={self.id!r}, name={self.name!r})')


# col_names = ['id', 'when', 'weight', 'reps']
col_names: list[str] = [col.name for col in Workout.__table__.columns]
# rel_names = ['exercise', 'schedule']
rel_names: list[str] = [rel.key for rel in Workout.__mapper__.relationships]
col_config = (('#0', 100, rel_names[1]), (rel_names[0], 150),
              *(zip(col_names[1:4], (100, 100, 100))))
