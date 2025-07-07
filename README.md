# Foxhole War Data Analysis

This repository contains a Python script and data for analyzing war statistics from the game Foxhole. The project focuses on calculating and visualizing war duration and win rates for the two factions: Colonials and Wardens.

## Data

The `foxhole_war_data.csv` file contains historical data for each war, including:

*   **War:** The war number.
*   **Start (UTC):** The start date of the war.
*   **Days:** The duration of the war in days.
*   **Casualties:** The total number of casualties.
*   **Winner:** The winning faction.

## Analysis

The `Calculate_Avg_WarTime.py` script performs the following analysis:

*   Calculates the average war duration for each faction across all wars.
*   Calculates the average war duration for each faction for wars after War 100.
*   Counts the number of wins for each faction for wars lasting more than 20 days.
*   Counts the number of wins for each faction for wars lasting more than 25 days and after War 108.
*   Generates a scatter plot of war duration vs. war number, with points colored by the winning faction.

## REquirements

*   Python
*   pandas
*   matplotlib