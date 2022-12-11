# Day 11: Monkey in the Middle

from dataclasses import dataclass
import heapq
import math
import operator
import re
from typing import Callable


@dataclass
class Monkey:
    id: int
    items: list
    amp_op: Callable
    div_val: int
    div_op: Callable
    pass_id_true: int
    pass_id_false: int


def create_monkey(monkey_dict):
    if monkey_dict["amp_op"] == "+":
        amp_op = operator.add
    elif monkey_dict["amp_op"] == "*":
        amp_op = operator.mul
    else:
        raise NotImplementedError(f"Unknown amp_op={monkey_dict['amp_op']}")

    if monkey_dict["amp_val"] == "old":
        iden_op = lambda v: v
    elif monkey_dict["amp_val"].isnumeric():
        iden_op = lambda _: int(monkey_dict["amp_val"])
    else:
        raise NotImplementedError(f"Unknown amp_val={monkey_dict['amp_val']}")

    return Monkey(
        id=int(monkey_dict["monkey_id"]),
        items=[int(it) for it in monkey_dict["items"].split(", ")],
        amp_op=lambda v: amp_op(v, iden_op(v)),
        div_val=int(monkey_dict["div_val"]),
        div_op=lambda v: v % int(monkey_dict["div_val"]) == 0,
        pass_id_true=int(monkey_dict["pass_id_true"]),
        pass_id_false=int(monkey_dict["pass_id_false"]),
    )


def parse_file(fd):
    input_template = (
        r"Monkey (?P<monkey_id>\d+):\n"
        r"  Starting items: (?P<items>(\d+,\s)*\d+)\n"
        r"  Operation: new = old (?P<amp_op>\+|\*) (?P<amp_val>\d+|old)\n"
        r"  Test: divisible by (?P<div_val>\d+)\n"
        r"    If true: throw to monkey (?P<pass_id_true>\d+)\n"
        r"    If false: throw to monkey (?P<pass_id_false>\d+)"
    )
    re_pattern = re.compile(input_template, re.MULTILINE)
    monkeys = [
        create_monkey(re_match.groupdict())
        for re_match in re_pattern.finditer(fd.read())
    ]
    return (monkeys,)


def _count_monkey_business(monkeys, rounds=20, with_division_by_3=False):
    inspection = [0] * len(monkeys)
    invariant = math.prod(m.div_val for m in monkeys)
    for _ in range(rounds):
        for m in monkeys:
            inspection[m.id] += len(m.items)
            for it in m.items:
                new_item = m.amp_op(it) % invariant
                if with_division_by_3:
                    new_item //= 3
                m_pass_id = m.pass_id_true if m.div_op(new_item) else m.pass_id_false
                monkeys[m_pass_id].items.append(new_item)
            m.items = []

    return math.prod(heapq.nlargest(2, inspection))


def count_monkey_business_after_20(monkeys):
    return _count_monkey_business(monkeys, rounds=20, with_division_by_3=True)


def count_monkey_business_after_10000(monkeys):
    return _count_monkey_business(monkeys, rounds=10000)


solution_function_01 = count_monkey_business_after_20
solution_function_02 = count_monkey_business_after_10000
