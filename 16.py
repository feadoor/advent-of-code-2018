import re

before_re = re.compile('Before: (.*)')
after_re = re.compile('After: (.*)')

class Command:

    def __init__(self, opcode, operands):
        self.opcode = opcode
        self.operands = operands

class Example:

    def __init__(self, before, after, command):
        self.before = before
        self.after = after
        self.command = command

    def matches(self, op_f):
        return op_f(self.before, *self.command.operands) == self.after

class Program:

    def __init__(self, commands):
        self.registers = [0, 0, 0, 0]
        self.commands = commands

    def execute(self, command, opcode_map):
        self.registers = opcode_map[command.opcode](self.registers, *command.operands)

    def run(self, opcode_map):
        for command in self.commands:
            self.execute(command, opcode_map)


def get_examples():
    with open('data/16.txt', 'r') as f:
        lines, examples = f.readlines(), []
        for idx in range((len(lines) + 3) // 4):
            example_lines = lines[4 * idx : 4 * (idx + 1)]
            before = eval(before_re.match(example_lines[0]).group(1))
            after = eval(after_re.match(example_lines[2]).group(1))
            inputs = [int(x) for x in example_lines[1].split()]
            opcode, operands = inputs[0], inputs[1:]
            examples.append(Example(before, after, Command(opcode, operands)))
        return examples

def get_program():
    with open('data/16a.txt', 'r') as f:
        commands = []
        for line in f:
            inputs = [int(x) for x in line.split()]
            commands.append(Command(inputs[0], inputs[1:]))
        return Program(commands)

def addr(registers, a, b, c):
    result = list(registers)
    result[c] = result[a] + result[b]
    return result

def addi(registers, a, b, c):
    result = list(registers)
    result[c] = result[a] + b
    return result

def mulr(registers, a, b, c):
    result = list(registers)
    result[c] = result[a] * result[b]
    return result

def muli(registers, a, b, c):
    result = list(registers)
    result[c] = result[a] * b
    return result

def banr(registers, a, b, c):
    result = list(registers)
    result[c] = result[a] & result[b]
    return result

def bani(registers, a, b, c):
    result = list(registers)
    result[c] = result[a] & b
    return result

def borr(registers, a, b, c):
    result = list(registers)
    result[c] = result[a] | result[b]
    return result

def bori(registers, a, b, c):
    result = list(registers)
    result[c] = result[a] | b
    return result

def setr(registers, a, b, c):
    result = list(registers)
    result[c] = result[a]
    return result

def seti(registers, a, b, c):
    result = list(registers)
    result[c] = a
    return result

def gtir(registers, a, b, c):
    result = list(registers)
    result[c] = 1 if a > result[b] else 0
    return result

def gtri(registers, a, b, c):
    result = list(registers)
    result[c] = 1 if result[a] > b else 0
    return result

def gtrr(registers, a, b, c):
    result = list(registers)
    result[c] = 1 if result[a] > result[b] else 0
    return result

def eqir(registers, a, b, c):
    result = list(registers)
    result[c] = 1 if a == result[b] else 0
    return result

def eqri(registers, a, b, c):
    result = list(registers)
    result[c] = 1 if result[a] == b else 0
    return result

def eqrr(registers, a, b, c):
    result = list(registers)
    result[c] = 1 if result[a] == result[b] else 0
    return result

def matching_opcodes(example):
    OPCODES = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
    return [op for op in OPCODES if example.matches(op)]

def assigned_opcodes(examples):
    OPCODES = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
    possibilities = [set(OPCODES) for _ in range(16)]
    for example in examples:
        possibilities[example.command.opcode] &= set(matching_opcodes(example))

    reverse_possibilities = {op_f: {op for op in range(16) if op_f in possibilities[op]} for op_f in OPCODES}
    assignments = [None] * 16

    def assign(idx, op):
        assignments[idx] = op
        possibilities[idx] = set()
        for poss in possibilities: poss -= {op}
        reverse_possibilities[op] = set()
        for r_poss in reverse_possibilities.values(): r_poss -= {idx}

    while any(ass is None for ass in assignments):
        for idx, ops in enumerate(possibilities):
            if len(ops) == 1:
                assign(idx, next(iter(ops)))
        for op, idxs in reverse_possibilities.items():
            if len(idxs) == 1:
                assign(next(iter(idxs)), op)

    return assignments

def very_ambiguous_opcodes():
    examples = get_examples()
    return sum(1 if len(matching_opcodes(example)) >= 3 else 0 for example in examples)

def register_0():
    examples, program = get_examples(), get_program()
    opcode_map = assigned_opcodes(examples)
    program.run(opcode_map)
    return program.registers[0]

print(very_ambiguous_opcodes())
print(register_0())
