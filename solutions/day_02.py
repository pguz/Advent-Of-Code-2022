# Day 02: Rock Paper Scissors

import pandas as pd


def parse_file(fd):
    return pd.read_csv(fd, header=None).squeeze("columns"),

def score_based_on_input(input_df):
    POS_SCORE = {
        ('A X'): 4,
        ('A Y'): 8,
        ('A Z'): 3,
        ('B X'): 1,
        ('B Y'): 5,
        ('B Z'): 9,
        ('C X'): 7,
        ('C Y'): 2,
        ('C Z'): 6,
    }
    return input_df.map(POS_SCORE).sum()

def score_based_on_result(input_df):
    POS_SCORE = {
        ('A X'): 3,
        ('A Y'): 4,
        ('A Z'): 8,
        ('B X'): 1,
        ('B Y'): 5,
        ('B Z'): 9,
        ('C X'): 2,
        ('C Y'): 6,
        ('C Z'): 7,
    }
    return input_df.map(POS_SCORE).sum()

solution_function_01 = score_based_on_input
solution_function_02 = score_based_on_result
