# Day 05: Supply Stacks

import pandas as pd


def parse_file(fd):

    # 1st part of file
    state_data = [[line[i] for i in range(1, len(line), 4)] for _ in range(8) if (line := next(fd))]
    state_df = pd.DataFrame(state_data)
    stacks = [[e for e in stack if e != ' '] for stack in state_df.iloc[::-1].transpose().values]

    # 2 empty lines
    next(fd)
    next(fd)

    # 2nd part of file
    action_df = pd.DataFrame(fd)[0].str.extract(
        '^move (\d+) from (\d+) to (\d+)$', expand=True).astype('int').set_axis(
            ['count', 'from', 'to'], axis=1)
    action_df['from'] = action_df['from'] - 1
    action_df['to'] = action_df['to'] - 1

    return stacks, action_df

def tops_of_stacks_after_rearrangement_9000(stacks, action_df):

    for _, (count, from_, to) in action_df.iterrows():
        for _ in range(count):
            stacks[to].append(stacks[from_].pop())

    tops_of_stacks = ''.join(stack[-1] for stack in stacks)

    return tops_of_stacks

def tops_of_stacks_after_rearrangement_9001(stacks, action_df):

    for _, (count, from_, to) in action_df.iterrows():
        stacks[to].extend(stacks[from_][-count:])
        del stacks[from_][-count:]

    tops_of_stacks = ''.join(stack[-1] for stack in stacks)

    return tops_of_stacks

solution_function_01 = tops_of_stacks_after_rearrangement_9000
solution_function_02 = tops_of_stacks_after_rearrangement_9001
