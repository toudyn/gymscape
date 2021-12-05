# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 19:22:39 2021

@author: jerem
"""

from leveling import *
import pandas as pd

levels_df = pd.read_csv('levels.csv')
workout_df = pd.read_csv('workouts.csv')

me = Character(levels_df)

me.batch_run(workout_df)
xp = me.get_exercise_levels()
print(xp)
xp.to_clipboard() # Copies the current experience per skill to the clipboard

