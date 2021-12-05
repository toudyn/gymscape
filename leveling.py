# -*- coding: utf-8 -*-
"""
Created on Sat Dec  4 19:04:39 2021

@author: jerem
"""

import pandas as pd

MAX_LEVEL = 100 # The max level I'm considering
WEIGHT_COEFF = 2 # Coefficient of base experience per rep x weight
REP_COEFF = 50 # Coefficient of base experience per rep
REP_PENALTY_COEFF = 0.5 # Coefficient of experience penalty for every rep under expected reps
REP_BONUS_COEFF = 1 # Coefficient of bonus experience for every rep over expected reps
VOLUME_COEFF = 1000 # Coefficient of base experience per unit of volume (km for running)
VOLUME_BONUS = 0.2 # Extra experience for meeting expected volume

class Exercise():
    """
    Stores everything related to an exercise like current level, required
    experience, etc.
    """
    def __init__(self, name, exercise_type, start, increment):
        self.name = name
        self.exercise_type = exercise_type
        self.start = start
        self.increment = increment
        self.expected_quantity = None
        self.level = 1
        self.experience = 0
        self.experience_levels = self.calculate_experience_levels()
        self.update_level()
    
    @staticmethod
    def get_level(total_experience, experience_df):
        """
        Returns the level that the total_experience .
        """
        achieved_levels = experience_df[experience_df['total_experience'] <= total_experience]
        level = max(achieved_levels['level'])
        expected_qty = max(achieved_levels['quantity'])
        return level, expected_qty

    def update_level(self):
        level, expected_qty = self.get_level(self.experience, self.experience_levels)
        if self.level != level:
            # print(f'Exercise: {self.name} is now level {level}!')
            self.level = level
        self.expected_quantity = expected_qty
    
    def calculate_experience_levels(self):
        """
        Calculates the experience required per level and the expected weight
        per level.
        """
        experiences = []
        tot_exp = 0
        for lvl in range(1, MAX_LEVEL + 1):
            if lvl == 1:
                exp = 0
                qty = self.start
            else:
                exp = self.next_level_experience(lvl)
                qty = self.start + (lvl - 1) * self.increment
            tot_exp += exp
            experiences.append({'level': lvl,
                                'quantity': qty,
                                'experience':exp,
                                'total_experience': tot_exp})
        
        return pd.DataFrame(experiences)
    
    def add_set(self, weight, quantity, date):
        exp = self.calculate_set_experience(weight, quantity)
        # print(f'{date}: Completed set for {self.name}. Got {exp} experience')
        self.experience += exp
        self.update_level()
    
    def calculate_set_experience(self, weight, quantity):
        """
        Returns the experience obtained for a single set.
        """
        if self.exercise_type == 'weight':
            return self.calculate_set_experience_weight(weight, quantity, self.expected_quantity)
        elif self.exercise_type == 'reps':
            return self.calculate_set_experience_reps(quantity, self.expected_quantity)
        elif self.exercise_type == 'volume':
            return self.calculate_set_experience_volume(quantity, self.expected_quantity)
    
    @staticmethod
    def calculate_set_experience_reps(reps, expected_reps):
        """
        Returns the experience obtained for a single set for rep-type
        exercises. Small penalty for not meeting expected reps.
        """
        base_exp = reps * REP_COEFF
        if reps < expected_reps:
            exp = base_exp - (base_exp * (reps/expected_reps) * REP_PENALTY_COEFF)
        else:
            exp = base_exp + (base_exp * (reps/expected_reps) * REP_BONUS_COEFF)
        
        return round(exp)
    
    @staticmethod
    def calculate_set_experience_weight(weight, reps, expected_weight):
        """
        Returns the experience obtained for a single set for weight-type
        exercises.
        """
        base_exp = reps * weight * WEIGHT_COEFF
        expected_weight_coeff = weight/expected_weight
        return round(base_exp * expected_weight_coeff)
    
    @staticmethod
    def calculate_set_experience_volume(volume, expected_volume):
        """
        Returns the experience obtained for a single set for volume-type
        exercises. No penalty for doing less than the expected quantity (running).
        """
        exp = VOLUME_COEFF * volume
        if volume >= expected_volume:
            exp *= (1 + VOLUME_BONUS * volume/expected_volume)
        return round(exp)
    
    @staticmethod
    def next_level_experience(level):
        """
        Returns the experience required to reach the next level.
        """
        return round(0.02 * (level ** 3) + 0.2 * (level ** 2) + 2 * level) * 500
    
    def get_level_info(self, level):
        level_info = self.experience_levels[self.experience_levels['level'] == level]
        return level_info.iloc[0]

class Character():
    """
    Combines the info from several exercises together.
    """
    
    def __init__(self, levels_df):
        self.levels_df = levels_df
        self.exercises = dict()
        self.load_exercises()
    
    def load_exercises(self):
        for _, row in self.levels_df.iterrows():
            exercise = row['exercise']
            exercise_type = row['type']
            start = row['start']
            increment = row['increment']
            
            self.exercises[exercise] = Exercise(exercise, exercise_type, start, increment)
    
    def add_set(self, exercise, weight, quantity, date):
        self.exercises[exercise].add_set(weight, quantity, date)
    
    def batch_run(self, workout_df):
        for _, row in workout_df.iterrows():
            exc = row['exercise']
            dt = row['date']
            qty = row['quantity']
            weight = row['weight']
            self.exercises[exc].add_set(weight, qty, dt)
    
    def get_exercise_levels(self):
        info = []
        for _, exc in self.exercises.items():
            name = exc.name
            lvl = exc.level
            exp = exc.experience
            exp_req = exc.get_level_info(lvl + 1)['total_experience'] - exc.experience
            qty_req = exc.expected_quantity
            info.append({'exercise': name,
                         'lvl': lvl,
                         'difficulty': qty_req,
                         'xp': exp,
                         'xp for next lvl': exp_req})
        
        return pd.DataFrame(info)
            
            
