"""Template."""

from collections import namedtuple, defaultdict

def read_input_lines():
    with open('input') as f:
        return f.readlines()

class Instruction(namedtuple('Instruction', ['func', 'arg'])):
    __slots__ = ()


transition_map = {
    'acc': lambda arg, line_num, acc: (line_num + 1,   acc + arg),
    'jmp': lambda arg, line_num, acc: (line_num + arg, acc),
    'nop': lambda _, line_num, acc:   (line_num + 1,   acc),
}


class ProgramDigraph:

    def __init__(self, instructions):
        self.lines = [None for _ in range(len(instructions))]
        self.forward_arcs = {}
        self.reverse_arcs = defaultdict(set)
        self._reach_data = {}
        for line_num, instruction_string in enumerate(instructions):
            self.process_instruction(instruction_string, line_num)

    @staticmethod
    def parse_from_strings(instruction_strings):
        instructions = [ProgramDigraph.parse_instruction(string) for string in instruction_strings]
        return ProgramDigraph(instructions) 

    @staticmethod
    def parse_instruction(instruction_string):
        func, arg = instruction_string.split()
        return Instruction(func, int(arg))

    def process_instruction(self, instruction, line_num):
        self.lines[line_num] = instruction
        next_line, _ = self.transition(instruction, line_num, 0)
        self.forward_arcs[line_num] = next_line
        self.reverse_arcs[next_line].add(line_num)
            
    @staticmethod
    def transition(instruction, line_num, acc):
        return transition_map[instruction.func](instruction.arg, line_num, acc)
    
    def stopping_criteria_met(self, evaluated_lines, current_line):
        if current_line in evaluated_lines:
            return True
        if current_line >= len(self.lines):
            return True
        return False

    def evaluate(self):
        acc = 0
        current_line = 0
        evaluated_lines = set()
        while not self.stopping_criteria_met(evaluated_lines, current_line):
            evaluated_lines.add(current_line)
            instruction = self.lines[current_line]
            current_line, acc = self.transition(instruction, current_line, acc)
        return acc

    def lines_reaching(self, line_num):
        if line_num in self._reach_data:
            return self._reach_data[line_num]

        self._reach_data[line_num] = set()
        for previous_line in self.reverse_arcs[line_num]:
            self._reach_data[line_num].add(previous_line)
            self._reach_data[line_num].update(self.lines_reaching(previous_line))
        return self._reach_data[line_num]

    def repair_instructions(self):
        eof = len(self.lines)
        for line_num, instruction in enumerate(self.lines):
            if instruction.func == 'jmp':
                new_instruction = Instruction('nop', instruction.arg)
                new_next_line, _ = self.transition(instruction, line_num, 0)
                if new_next_line in self.lines_reaching(eof):
                    new_lines = self.lines.copy()
                    new_lines[line_num] = new_instruction
                    new_program = ProgramDigraph(new_lines)
                    if 0 in new_program.lines_reaching(eof):
                        return new_program
            elif instruction.func == 'nop':
                new_instruction = Instruction('jmp', instruction.arg)
                new_next_line, _ = self.transition(instruction, line_num, 0)
                if new_next_line in self.lines_reaching(eof):
                    new_lines = self.lines.copy()
                    new_lines[line_num] = new_instruction
                    new_program = ProgramDigraph(new_lines)
                    if 0 in new_program.lines_reaching(eof):
                        return new_program

def test():
    test_data = '''nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6'''.split('\n')
    prog = ProgramDigraph(test_data)
    print(prog.lines)
    print(prog.forward_arcs)
    print(prog.reverse_arcs)
    print(prog.lines_reaching(9))
    acc = prog.evaluate()
    new_prog = prog.repair_instructions()
    print(prog.evaluate)



def main():
    test()


if __name__=='__main__':
    main()