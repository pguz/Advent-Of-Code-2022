# Day 09: Rope Bridge


def parse_file(fd):
    return fd.readlines(),

def handle_head(d, hp):
    if d == 'R':
        return (hp[0] + 1, hp[1])
    if d == 'U':
        return (hp[0], hp[1] + 1)
    if d == 'L':
        return (hp[0] - 1, hp[1])
    if d == 'D':
        return (hp[0], hp[1] - 1)
    raise NotImplementedError()

def handle_tail(d, hp, tp):
    if d == 'R':
        return (tp[0] + 1, hp[1])
    if d == 'U':
        return (hp[0], tp[1] + 1)
    if d == 'L':
        return (tp[0] - 1, hp[1])
    if d == 'D':
        return (hp[0], tp[1] - 1)
    raise NotImplementedError()

def handle_tail_extended(hp, tp):
    dx = hp[0] - tp[0]
    dy = hp[1] - tp[1]
    def check_sign(v):
        if v > 0:
            return 1
        elif v == 0:
            return 0
        else:
            return -1
    return (tp[0] + check_sign(dx), tp[1] + check_sign(dy))

def check_if_positions_is_stable(hp, tp):
    if abs(hp[0] - tp[0]) <= 1 and abs(hp[1] - tp[1]) <= 1:
        return True
    return False

def tail_rope_positions(commands):
    hp = (0, 0)
    tp = (0, 0)
    tps = {(0, 0)}
    for c in commands:
        d, v = c.split()
        for _ in range(int(v)):
            hp = handle_head(d, hp)
            if check_if_positions_is_stable(hp, tp):
                continue
            tp = handle_tail(d, hp, tp)
            tps.add(tp)

    return len(tps)

def tail_long_rope_positions(commands):
    rope_size = 10
    rps = [(0, 0)] * rope_size
    tps = {(0, 0)}
    for c in commands:
        d, v = c.split()
        for _ in range(int(v)):
            rps[0] = handle_head(d, rps[0])
            for i in range(1, rope_size):
                if check_if_positions_is_stable(hp=rps[i - 1], tp=rps[i]):
                    break
                rps[i] = handle_tail_extended(rps[i - 1], rps[i])
                if i == rope_size - 1:
                    tps.add(rps[i])
    return len(tps)

solution_function_01 = tail_rope_positions
solution_function_02 = tail_long_rope_positions
