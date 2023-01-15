# Day 16: Proboscidea Volcanium

from collections import defaultdict
import re


def parse_file(fd):
    input_template = r"Valve ([A-Z][A-Z]) has flow rate=(\d+); tunnel(s)? lead(s)? to valve(s)? (?P<child>[A-Z][A-Z](, ([A-Z][A-Z]))*)"
    re_pattern = re.compile(input_template)
    valves_map = {}
    valves_flow = {}
    for re_match in re_pattern.finditer(fd.read()):
        valves_map[re_match[1]] = re_match['child'].split(', ')
        if flow := int(re_match[2]):
            valves_flow[re_match[1]] = flow

    valid_valves = set(valves_flow.keys())
    valid_valves_with_AA = valid_valves | {'AA'}

    valid_valves_map = defaultdict(list)
    for v in valid_valves_with_AA:
        queue = [(n, 1) for n in valves_map[v]]
        visited = set(valves_map[v]) | {v}
        while queue:
            n, d = queue.pop()
            if n in valid_valves_with_AA:
                valid_valves_map[v].append((n, d))
                continue
            for c in valves_map[n]:
                if c not in visited:
                    visited.add(c)
                    queue.append((c, d + 1))

    return (valid_valves_map, valves_flow)


def most_pressure(valves_map, valves_flow):
    valid_valves = set(valves_flow.keys())

    def possible_moves(room, open_valve, rate, opened, state):
        if open_valve:
            new_opened = opened.copy()
            new_opened.add(room)
            new_rate = rate + valves_flow[room]
            new_state = state.copy()
            new_state[room] = new_rate
            return [(room, False, 1, new_rate, new_opened, new_state)]
        
        moves = []
        for next_room, next_move_dur in valves_map[room]:
            if next_room in state and state[next_room] == rate:
                continue
            new_state = state.copy()
            new_state[next_room] = rate
            moves.append((next_room, False, next_move_dur, rate, opened, new_state))

            if next_room in valid_valves and next_room not in opened:
                moves.append((next_room, True, next_move_dur, rate, opened, new_state))

        return moves

    perf = dict()
    def dfs(time, room, open_valve, move_dur, released, rate, opened, state):
        if time <= 0:
            return released

        if time - move_dur <= 0:
            return released + rate * time

        if len(opened) == len(valid_valves):
            return released + rate * time

        time = time - move_dur
        released = released + (rate * move_dur)

        moves = []
        for next_room, open_next_valve, next_move_dur, new_rate, new_opened, new_state in possible_moves(room, open_valve, rate, opened, state):
            if (next_room, open_next_valve, time) in perf:
                acc_released, acc_rate = perf[(next_room, open_next_valve, time)]
                if acc_released > released and acc_rate > new_rate:
                    continue
                if released >= acc_released and new_rate >= acc_rate:
                    perf[(next_room, open_next_valve, time)] = (released, new_rate)
            else:
                perf[(next_room, open_next_valve, time)] = (released, new_rate)

            moves.append(dfs(time, next_room, open_next_valve, next_move_dur, released, new_rate, new_opened, new_state))

        return max(moves, default=0)

    return dfs(30, 'AA', None, 1, 0, 0, set(), {})


def most_pressure_with_elephant(valves_map, valves_flow):
    valves = set(valves_flow.keys())

    glob_state_2 = dict()
    
    def possible_moves(room, open_valve, rate, opened, state):
        if open_valve:
            if room in opened:
                return [(room, -1, 1, rate, opened, state)]
            new_opened = opened.copy()
            new_opened.add(room)
            new_rate = rate + valves_flow[room]
            new_state = state.copy()
            new_state[room] = new_rate
            return [(room, False, 1, new_rate, new_opened, new_state)]
        
        moves = []
        for next_room, next_move_dur in valves_map[room]:
            if next_room in state and state[next_room] == rate:
                continue
            new_state = state.copy()
            new_state[next_room] = rate
            moves.append((next_room, False, next_move_dur, rate, opened, new_state))

            if next_room in valves and next_room not in opened:
                moves.append((next_room, True, next_move_dur, rate, opened, new_state))

        return moves

    def check_state(room_1, room_2, open_valve_1, open_valve_2, time, released, rate):
        if (room_1, room_2, open_valve_1, open_valve_2, time) in glob_state_2:
            re, ra = glob_state_2[(room_1, room_2, open_valve_1, open_valve_2, time)]
            if re > released and ra > rate:
                return False
            if (released > re and rate > ra):
                glob_state_2[(room_1, room_2, open_valve_1, open_valve_2, time)] = (released, rate)
                glob_state_2[(room_2, room_1, open_valve_2, open_valve_1, time)] = (released, rate)
        elif released and rate:
            glob_state_2[(room_1, room_2, open_valve_1, open_valve_2, time + 1)] = (released, rate)
            glob_state_2[(room_2, room_1, open_valve_2, open_valve_1, time + 1)] = (released, rate)

        return True

    def check_state_2(room_1, room_2, open_valve_1, open_valve_2, time, released, rate):
        if (room_1, room_2, open_valve_1, open_valve_2, time) in glob_state_2:
            re, ra = glob_state_2[(room_1, room_2, open_valve_1, open_valve_2, time)]
            if re > released and ra > rate:
                return False
            if (released > re and rate > ra):
                glob_state_2[(room_1, room_2, open_valve_1, open_valve_2, time)] = (released, rate)
                glob_state_2[(room_2, room_1, open_valve_2, open_valve_1, time)] = (released, rate)
        elif released and  rate:
            glob_state_2[(room_1, room_2, open_valve_1, open_valve_2, time)] = (released, rate)
            glob_state_2[(room_2, room_1, open_valve_2, open_valve_1, time)] = (released, rate)

        return True


    def dfs(room_1, room_2, time, released, rate, opened, state_1, open_1, open_2, move_1, move_2, history):
        if move_1 == -1 or move_2 == -1:
            return 0
        if time <= 0:
            return released
        
        first_player = move_1 <= move_2
        move = min(move_1, move_2)
        
        if time - move <= 0:
            return released + rate * time
    
        if len(opened) == len(valves):
            return released + rate * time

        time = time - move
        released = released + (rate * move)

        if first_player:
            result = []
            for c, open, d, rate, opened, state in possible_moves(room_1, open_1, rate, opened, state_1):
                if not check_state(room_1, c, open, open_2, time, released, rate):
                    continue
                new_history = history.copy()
                new_history.append((time, c, room_2, open, open_2, move_1, move_2))
                result.append(dfs(c, room_2, time, released, rate, opened, state, open, open_2, d, move_2 - move_1, new_history))
            return max(result, default=0)

        else:
            result = []
            for c, open, d, rate, opened, state in possible_moves(room_2, open_2, rate, opened, state_1):
                if not check_state_2(c, room_2, open_1, open, time, released, rate):
                    continue
                new_history = history.copy()
                new_history.append((time, room_1, c, open_1, open, move_1, move_2))
                result.append(dfs(room_1, c, time, released, rate, opened, state, open_1, open, move_1 - move_2, d, new_history))
            return max(result, default=0)

    return dfs('AA', 'AA', 26, 0, 0, set(), {}, None, None, 1, 1, [])

solution_function_01 = most_pressure
solution_function_02 = most_pressure_with_elephant
