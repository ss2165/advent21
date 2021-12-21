from dataclasses import dataclass
import itertools
import operator
from functools import reduce
from typing import Iterable, Iterator

def hex_to_binary( hex_code_str: str ) -> str:
    hex_code = int(hex_code_str, 16)
    bin_code = bin( hex_code )[2:]
    padding = (4-len(bin_code)%4)%4
    return '0'*padding + bin_code

def get_n_bits(s: Iterable[str], n:int) -> str:
    return "".join(itertools.islice(s, n))

@dataclass
class Packet:
    version: int
    type_id: int
    def eval(self) -> int:
        return 0

@dataclass
class LiteralPacket(Packet):
    value: int
    def eval(self) -> int:
        return self.value

@dataclass
class OperatorPacket(Packet):
    length_type: bool
    packets: list[Packet]
    def eval(self) -> int:
        match (self.type_id, self.packets):
            case (_, [p]):
                return p.eval()
            case (0, ps):
                return reduce(operator.add, (p.eval() for p in ps))
            case (1, ps):
                return reduce(operator.mul, (p.eval() for p in ps))
            case (2, ps):
                return min(p.eval() for p in ps)
            case (3, ps):
                return max(p.eval() for p in ps)
            case (5, [p0, p1]):
                return int(p0.eval()>p1.eval())
            case (6, [p0, p1]):
                return int(p0.eval()<p1.eval())
            case (7, [p0, p1]):
                return int(p0.eval()==p1.eval())

        return 0

def decode_literal(literal_s: Iterable[str]) -> int:
    num_bits = ""
    while True:
        next_bits: str = get_n_bits(literal_s, 5)
        num_bits += next_bits[1:]
        if next_bits[0] == "0":
            break
    return int(num_bits, 2)

def decode_total_len_packets(packets_s: Iterator[str], leng: int) -> list[Packet]:
    ps = iter(get_n_bits(packets_s, leng))

    out_packets = []

    while True:
        try:
            out_packets.append(decode_packet(ps))
        except Exception as e:
            break
    return out_packets

def decode_total_num_packets(packets_s: Iterator[str], num: int) -> list[Packet]:

    return [decode_packet(packets_s) for _ in range(num)]

def decode_operator(operator_s: Iterator[str]) -> tuple[bool, list[Packet]]:
    length_type = next(operator_s)
    match length_type:
        case "0":
            leng = int(get_n_bits(operator_s, 15), 2)
            packets = decode_total_len_packets(operator_s, leng)
            return False, packets
        case _:
            num = int(get_n_bits(operator_s, 11), 2)
            packets = decode_total_num_packets(operator_s, num)
            return True, packets

def decode_packet(binstr: Iterator[str]) -> Packet:
    # try:

    version = int(get_n_bits(binstr, 3), 2)
    # except 
    
    type_id = int(get_n_bits(binstr, 3), 2)
    
    match type_id:
        case 4:
            literal = decode_literal(binstr)
            return LiteralPacket(version, type_id, literal)
        case _:
            op_len_type, subpackets = decode_operator(binstr)
            return OperatorPacket(version, type_id, op_len_type, subpackets)



def decode(source: str):
    return decode_packet(iter(hex_to_binary(source)))

def count_versions(pack: Packet) -> int:
    match pack:
        case OperatorPacket(version=v, packets=ps):
            return v + sum(count_versions(p) for p in ps)
        case Packet(version=v):
            return v
    return 0

with open("../inputs/day16_trial.txt") as f:
    src = f.read()

vers_sum = 0

# print(count_versions(decode(src)))
print(decode(src).eval())