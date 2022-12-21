# Day 21: Monkey Math

import operator
import re


def parse_file(fd):
    input_template = r"([a-z]{4}): ((([a-z]{4}) (\+|\-|\*|\/) ([a-z]{4}))|(\d+))"
    re_pattern = re.compile(input_template)
    yells = dict()
    for re_match in re_pattern.finditer(fd.read()):
        yells[re_match[1]] = (
            int(re_match[2])
            if not re_match[3]
            else [re_match[5], re_match[4], re_match[6]]
        )
    return (yells,)


def root_yell(yells):
    oper_map = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.floordiv,
    }

    def yell_number(monk):
        yell = yells[monk]
        if isinstance(yell, int):
            return yell
        return oper_map[yell[0]](yell_number(yell[1]), yell_number(yell[2]))

    return yell_number("root")


def equality_test(yells):
    oper_map = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.floordiv,
    }
    oper_inv_1 = {
        "+": lambda f, s: operator.sub(s, f),
        "-": operator.sub,
        "*": lambda f, s: operator.floordiv(s, f),
        "/": operator.floordiv,
        "=": lambda f, _: f,
    }
    oper_inv_2 = {
        "+": operator.sub,
        "-": operator.add,
        "*": operator.floordiv,
        "/": operator.mul,
        "=": lambda _, s: s,
    }

    yells["humn"] = None
    yells["root"] = ["=", yells["root"][1], yells["root"][2]]

    def upsert_yells(monk):
        yell = yells[monk]
        if not yell:
            return None
        if isinstance(yell, int):
            return yell
        yell_number_1 = upsert_yells(yell[1])
        yell_number_2 = upsert_yells(yell[2])
        if yell_number_1 and yell_number_2:
            yells[monk] = oper_map[yell[0]](yell_number_1, yell_number_2)
            return yells[monk]
        elif yell_number_1:
            yells[monk][1] = yell_number_1
        elif yell_number_2:
            yells[monk][2] = yell_number_2
        else:
            raise NotImplementedError()
        return None

    upsert_yells("root")

    def calc_humn(monk, number):
        yell = yells[monk]
        if not yell:
            return number
        if isinstance(yell[1], int):
            return calc_humn(yell[2], oper_inv_1[yell[0]](yell[1], number))
        if isinstance(yell[2], int):
            return calc_humn(yell[1], oper_inv_2[yell[0]](number, yell[2]))
        raise NotImplementedError()

    return calc_humn("root", 0)


solution_function_01 = root_yell
solution_function_02 = equality_test
