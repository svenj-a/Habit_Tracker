# Habit_Tracker

This habit tracking app helps you to implement new habits efficiently and supports you in reaching your goals faster. It
motivates you to stick to your good resolutions and rewards you with completion streaks for your successfully completed
daily, weekly, or monthly tasks and thus pursuing your long-term goals. You can track and analyze your progress, so that
you can always check how you're doing and how close you already are to having established your new routines.

## Functionality
The program offers the possibility to create and completed habits, analyze the progress on stored habits and delete
those which you don't want to keep any longer.

### Creating habits
For creating a habit, first of all you must provide a unique name. Optionally a short description can be added (this one
can be skipped by hitting enter). Select a periodicity from the selection menu (either daily, weekly or monthly) and set
a realistic final goal for your habit. This specifies how often you must complete the habit before it is considered
established.

### Completing habits
Completing a habit is fairly easy: Select the habit you want to check off from the selection menu. Complete a habit
several times within the specified time period to build a streak and keep it going! If you fail to complete the habit in
time, you break the habit and your current streak is reset to 1. The longest streak you ever reached is saved as
"high score". Be honest to yourself! Only check off tasks that you have already fulfilled. Moreover, you can complete a
habit only once per period (once a day, once a week, once a month), so don't attempt to cheat!
The very first completion of a habit has no time restrictions, so you can create habits in advance.

### Analyzing habits
To track your progress, the analysis menu offers the options to get an overview of all stored habits, filter them by
periodicity or view the detailed record of a single habit. You can also check the habits with the longest streaks and
those with the closest goal, both stratified by periodicity and a summary of all established habits.

### Delete habits
If you created a task that you don't want to pursue anymore or misconfigured the habit you just created, you can simply
delete it by choosing the habit name from the selection menu. Use this option with great caution! Deleted habits cannot
be restored...

## Installation
Before you start, run the following command in your terminal to install all required packages and modules.
```shell
pip install -r requirements.txt
```
The program was developed under python 3.11. Older versions might not be supported.

## Testing
Run the following command in your terminal to start the test suite of the program.
```shell
pytest .
```

## Usage
To start the program execute
```shell
python main.py
```
and follow the instructions in your console.

**_Enjoy!_**
