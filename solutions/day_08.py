# Day 08: Treetop Tree House

import pandas as pd


def parse_file(fd):
    input_map = pd.read_csv(fd, header=None, dtype=str).squeeze("columns")
    return pd.DataFrame(list(input_map.map(list))).astype(int),

def count_visibility(tree_map):
    def find_visibility(row):
        return row.cummax().diff() != 0
 
    first_conf_visibility = tree_map.pipe(find_visibility)
    second_conf_visibility = tree_map[::-1].pipe(find_visibility)[::-1]
    third_conf_visibility = tree_map.transpose().pipe(find_visibility).transpose()
    fourth_conf_visibility = tree_map.transpose()[::-1].pipe(find_visibility)[::-1].transpose()
    visibility = first_conf_visibility | second_conf_visibility | third_conf_visibility | fourth_conf_visibility
    return visibility.to_numpy().sum()

def find_highest_scenic_score(tree_map):
    def calc_scenic_scores(row):
        scores = []
        s = [0] * 10
        for h in row:
            scores.append(s[h])
            thresh = h + 1
            for k in range(len(s)):
                if k < thresh:
                    s[k] = 1
                else:
                    s[k] += 1
        return scores
        
    first_conf_scores = tree_map.apply(calc_scenic_scores)
    second_conf_scores = tree_map[::-1].apply(calc_scenic_scores)[::-1]
    third_conf_scores = tree_map.transpose().apply(calc_scenic_scores).transpose()
    fourth_conf_scores = tree_map.transpose()[::-1].apply(calc_scenic_scores)[::-1].transpose()
    scenic_scores = first_conf_scores * second_conf_scores * third_conf_scores * fourth_conf_scores   
    return scenic_scores.to_numpy().max()

solution_function_01 = count_visibility
solution_function_02 = find_highest_scenic_score
