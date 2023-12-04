from copy import copy

with open('input.txt') as f:
    program = [i.split() for i in f.readlines()]

# instruction: {data_length: cycles}
instr_latency = {
    "noop": {0: 1},
    "addx": {1: 2},
}

class ELF6502:

    def __init__(self):
        self._current_address = 0
        self._current_instr = None
        self._reg_x = 1
        self._start_address = 0
        self.program_length = 0
        self.program = list()
        self._ticks = 0

    def load_program(self, program: list) -> None:
        for code in program:
            instr = code[0]
            data = code[1:]
            latency = instr_latency[instr][len(data)] - 1
            opcode = {
                "instr": instr,
                "data": data,
                "cycles": latency,
            }
            self.program.append(opcode)
        self.program_length = len(self.program)

    def tick(self) -> None:
        if not self._current_instr:
            self._current_instr = copy(self.program[self._current_address])
        if self._current_instr["cycles"] == 0:
            instr = self._current_instr
            getattr(self, f'_instr_{instr["instr"]}')(*instr["data"])
            self._current_address += 1
            if not self.halted: self._current_instr = copy(self.program[self._current_address])
        else:
            self._current_instr["cycles"] -= 1
        self._ticks += 1

    def _instr_addx(self, *data: str) -> None:
        if len(data) == 1:
            self._reg_x += int(data[0])

    def _instr_noop(self) -> None:
        pass

    @property
    def reg_x(self) -> int:
        return self._reg_x

    @property
    def ticks(self) -> int:
        return self._ticks

    @property
    def start_address(self) -> int:
        return self._start_address

    @start_address.setter
    def start_address(self, address: int) -> None:
        self._start_address = address
        self._current_address = address

    @property
    def current_address(self) -> int:
        return self._current_address
    
    @property
    def halted(self) -> bool:
        return not bool(self.program_length - self._current_address)


# Part One
cpu = ELF6502()
cpu.load_program(program)
power_level = 0
while not cpu.halted:
    cycles = cpu.ticks + 1
    if not (cycles - 20) % 40:
        power_level += cycles * cpu.reg_x
    cpu.tick()

print(power_level)

# Part Two
cpu = ELF6502()
cpu.load_program(program)
v_pos = 0
while not cpu.halted:
    scanline = list()
    for h_pos in range(40):
        sprite_location = range(cpu.reg_x - 1, cpu.reg_x + 2)
        if cpu.ticks - (40 * v_pos) in sprite_location:
            scanline.append('#')
        else:
            scanline.append(' ')
        if cpu.halted: break
        cpu.tick()
    print(''.join(scanline))
    v_pos += 1
