from functools import cmp_to_key, reduce
from itertools import chain
from pathlib import Path
from typing import Union


class PacketFixer:
    def __init__(self, packet_file: Union[str, Path]):
        self.divider_packets = [[[2]], [[6]]]
        self.packet_file = Path(packet_file)
        self.packets = self.parse_packets()
        self.all_packets = list(chain.from_iterable(self.packets))
        self.all_packets.extend(self.divider_packets)

    def parse_packets(self) -> list:
        packets = list()
        raw_data = self.packet_file.open().readlines()
        i = 0
        while i < len(raw_data):
            packets.append([eval(raw_data[i]), eval(raw_data[i + 1])])
            i += 3
        return packets

    def index_sum(self) -> int:
        results = 0
        for i, v in enumerate(self.packets):
            try:
                self.__compare_packet(v[0], v[1])
            except PacketOrderException as e:
                results += (i + 1) * e.is_correct
        return results

    def get_divider_packet_indexes(self) -> list:
        return [self.all_packets.index(i) for i in self.divider_packets]

    def compare_packet(self, p0, p1) -> int:
        try:
            self.__compare_packet(p0, p1)
        except PacketOrderException as e:
            return -1 if e.is_correct else 1

    def __compare_packet(self, p0, p1) -> None:
        t0, t1 = (isinstance(i, int) for i in (p0, p1))
        if t0 & t1:
            if p0 != p1:
                raise PacketOrderException(is_correct=p0 < p1)
            return

        p0, p1 = ([i] if isinstance(i, int) else i for i in (p0, p1))
        if len(p0) == 0 or len(p1) == 0:
            if len(p0) == len(p1):
                return
            raise PacketOrderException(is_correct=len(p0) < len(p1))

        max_len = sorted((len(i) for i in (p0, p1)))[-1]
        for i in range(max_len):
            try:
                self.__compare_packet(p0[i], p1[i])
            except IndexError:
                raise PacketOrderException(is_correct=len(p0) < len(p1))


class PacketOrderException(Exception):
    def __init__(self, is_correct: bool):
        self.is_correct = is_correct


# Part One
p = PacketFixer(packet_file="input.txt")
print(p.index_sum())

# Part Twp
p.all_packets.sort(key=cmp_to_key(p.compare_packet))
results = reduce((lambda x, y: (x + 1) * (y + 1)), p.get_divider_packet_indexes())
print(results)
