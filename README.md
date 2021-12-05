# Gymscape

Gamify your grinding in the gym. Hit level 40 to unlock Rune dumbbells.

## Installation

Currently only requires pandas. requirements.txt will be created at a later time.

## How it works

Each type of exercise (eg. bench, curls, running, pullups) are their own skill - experience is gained for each separately.

Each exercise can either be:

* Weight-based - The exercise requires a weight, like benching.
* Rep-based - The exercise does not require a weight, like pullups. Note that there is currently no system for later adding weight to a rep-based exercise
* Volume-based - The exercise is more about completing something, like running

Start off by defining the skills you want to have tracked in a file called `levels.csv`. An example can be found in `example_levels.csv`.

* exercise - The name of the exercise
* type - Whether it is `weight`, `rep`, or `volume`
* start - The starting point for expected weights/reps/volume
  * For weight-based - A value of 50 (kg or lbs not important) means you would be aiming to start lifting 50 kg or lbs at level 1
  * For rep-based - A value of 5 means you would be aiming to complete sets of 5 reps at level 1
  * For volume-based - A value of 1 (km or mi not important) means you would be aiming to complete runs (or whatever) of 1 km or mi at level 1
* increment - The target weight/rep/volume increase per level
  * Calculate this based on where you would want to be at level 10 or 20 **Due to the exponential increase in experience required to reach the next level it is suggested to consider level 20 as close to end-game**. Example: You can bench 50 kg easily (level 1) and would ideally like to bench 200 kg one day, it is suggested to set the increment to (200-50)/20 = 7.5

Experience is still gained for completing sets at a lower weight/rep/volume than what the level calls for, but there is an experience penalty. If doing more there is an experience bonus. How much exactly depends on the type of exercise and how much higher the weight/rep/volume done was over the expected amount.

When completing workouts, add details of every set in a file called `workouts.csv`. An example can be found in `example_workouts.csv`.

* date - Just the date in format 'YYYY-MM-DD' (not currently used for anything but will be used for analytics later)
* exercise - The name of the exercise completed. **This must match the name given in `levels.csv`**
* weight - The weight, if it is a weight-based exercise. If it is not just leave it empty
* quantity - The reps or volume completed (in the set)

Then run `main.py` - For each skill the level, experience, experience for next level, and expected weight/reps/volume are printed out based off of what you've completed in `workouts.csv`.

### Editing the experience

Depending on how you want to approach it, you may find that the leveling becomes too slow too fast. You don't want to make it from level 1 to level 10 with a few 5 km runs and then have to run 20 marathons to go from level 14 to 15. Right now exponents for experience required at each level are hard-coded in the `next_level_experience` function in `leveling.py` play around with that to get something that works for you.

You can also play with the way the experience gets calculated for completing a set - there are global variable coefficients for that in various functions in `leveling.py`.
