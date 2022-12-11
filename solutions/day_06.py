# Day 06: Tuning Trouble


def parse_file(fd):
    return (fd.read(),)


def _find_marker(cs_signal, marker_length):
    chain = list(cs_signal[: marker_length - 1])
    for i, c in enumerate(cs_signal[marker_length - 1:], marker_length):
        chain.append(c)
        if len(set(chain)) == marker_length:
            return i
        chain.pop(0)
    return None


def find_start_of_packet_marker(cs_signal):
    return _find_marker(cs_signal, 4)


def find_start_of_message_marker(cs_signal):
    return _find_marker(cs_signal, 14)


solution_function_01 = find_start_of_packet_marker
solution_function_02 = find_start_of_message_marker
