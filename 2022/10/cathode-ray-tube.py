with open('input.txt') as f:
    opcodes = [i.split() for i in f.readlines()]

instr_latency = {
    "noop": 1,
    "addx": 2,
}

class ELF6502:

    def __init__(self):
        self._reg_x = 1
        self.program = list()
        self.cycles = 0

    def load_program(self, program: dict) -> None:
        for code in program:
            opcode = {
                "instr": code[0],
                "data": code[1:],
                "cycles": instr_latency[code[0]] - 1
            }
            self.program.append(opcode)
        self.program.reverse()

    def tick(self) -> bool:
        if self.program[-1]["cycles"] == 0:
            i = self.program.pop()
            getattr(self, i["instr"])(*i["data"])
        else:
            self.program[-1]["cycles"] -= 1
        self.cycles += 1
        return bool(len(self.program))

    def addx(self, value: str) -> None:
        self._reg_x += int(value)

    def noop(self) -> None:
        pass

    @property
    def reg_x(self) -> int:
        return self._reg_x

    
# Part One
cpu = ELF6502()
cpu.load_program(opcodes)
power_level = 0
while cpu.tick():
    cycles = cpu.cycles + 1
    if not (cycles - 20) % 40:
        power_level += cycles * cpu.reg_x

print(power_level)

# Part Two
cpu = ELF6502()
cpu.load_program(opcodes)
v_pos = 0
while cpu.program:
    scanline = list()
    for h_pos in range(40):
        sprite_location = range(cpu.reg_x - 1, cpu.reg_x + 2)
        if cpu.cycles - (40 * v_pos) in sprite_location:
            scanline.append('#')
        else:
            scanline.append(' ')
        cpu.tick()
    print(''.join(scanline))
    v_pos += 1
