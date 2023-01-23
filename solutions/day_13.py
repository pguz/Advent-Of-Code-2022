# Day 13: Distress Signal

from functools import cmp_to_key
import math
import re


def parse_line(line):
    mark = ord("A")
    d = {}
    lists = []
    while "[" in line:
        list_found = re.search(r"\[((\d+|[a-zA-Z]),)*(\d+|[a-zA-Z])?\]", line)
        d[chr(mark)] = list_found[0][1:-1].split(",")
        line = line.replace(list_found[0], chr(mark))
        lists.append(list_found[0][1:-1].split(","))
        if mark == ord("Z"):
            mark = ord("a")
        else:
            mark += 1

    def handle_list(l):
        return (
            [handle_list(d[e]) if not e.isdigit() else int(e) for e in l]
            if not (len(l) == 1 and l[0] == "")
            else []
        )

    return handle_list(lists.pop())


def parse_file(fd):
    packets = []
    while (first_line := fd.readline()) and (second_line := fd.readline()):
        fd.readline()
        packets.append(parse_line(first_line))
        packets.append(parse_line(second_line))
    return (packets,)


def _list_comp(l1, l2):
    for v1, v2 in zip(l1, l2):
        if type(v1) == int and type(v2) == int:
            if v1 < v2:
                return True
            if v1 > v2:
                return False
            continue
        if type(v1) == int:
            v1 = [v1]
        if type(v2) == int:
            v2 = [v2]
        v_comp = _list_comp(v1, v2)
        if v_comp is not None:
            return v_comp
    if len(l1) < len(l2):
        return True
    if len(l1) > len(l2):
        return False
    return None


def _packet_gt(l1, l2):
    result = _list_comp(l1, l2)
    if result is False:
        return 1
    return -1


def sum_the_right_order(packets):
    paired_packets = [packets[i : i + 2] for i in range(0, len(packets), 2)]
    return sum(
        i
        for i, (p1, p2) in enumerate(paired_packets, start=1)
        if _list_comp(p1, p2) is not False
    )


def calc_decoder_key(packets):
    div_pckts = [[[2]], [[6]]]
    sorted_packets = sorted(packets + div_pckts, key=cmp_to_key(_packet_gt))
    return math.prod(sorted_packets.index(p) + 1 for p in div_pckts)


solution_function_01 = sum_the_right_order
solution_function_02 = calc_decoder_key
