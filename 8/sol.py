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
        """Construct a program from a list of instructions."""
        self.lines = [Instruction('nop', 0) for _ in range(len(instructions))]
        self.forward_arcs = {}
        self.reverse_arcs = defaultdict(set)
        self._reverse_reach_data = {}
        self._reach_data = {}
        for line_num, instruction_string in enumerate(instructions):
            self.process_instruction(instruction_string, line_num)

    @staticmethod
    def parse_from_strings(instruction_strings):
        """Parse a list of instruction strings one by one."""
        instructions = [ProgramDigraph.parse_instruction(string) for string in instruction_strings]
        return ProgramDigraph(instructions) 

    @staticmethod
    def parse_instruction(instruction_string):
        """Parse a single instruction string."""
        func, arg = instruction_string.split()
        return Instruction(func, int(arg))

    def process_instruction(self, instruction, line_num):
        """Process a single instruction and modify program datastructures."""
        self.lines[line_num] = instruction
        next_line, _ = self.transition(instruction, line_num, 0)
        self.forward_arcs[line_num] = next_line
        self.reverse_arcs[next_line].add(line_num)
            
    @staticmethod
    def transition(instruction, line_num, acc):
        """Return a new line number and accumulator computed via the given
        instruction."""
        return transition_map[instruction.func](instruction.arg, line_num, acc)

    def stopping_criteria_met(self, evaluated_lines, current_line):
        """Check if the evaluation of a program should halt."""
        if current_line in evaluated_lines:
            return True
        if current_line >= len(self.lines):
            return True
        return False

    def evaluate(self):
        """Evaluate a program.

        Halts if EOF reached or infinite loop detected."""
        acc = 0
        current_line = 0
        evaluated_lines = set()
        while not self.stopping_criteria_met(evaluated_lines, current_line):
            evaluated_lines.add(current_line)
            instruction = self.lines[current_line]
            current_line, acc = self.transition(instruction, current_line, acc)
        return acc

    def lines_reaching(self, line_num):
        """Compute the set of lines which, if reached, will result in the
        given line being evaluated."""
        if line_num in self._reverse_reach_data:
            return self._reverse_reach_data[line_num]
        self._reverse_reach_data[line_num] = set()
        for previous_line in self.reverse_arcs[line_num]:
            self._reverse_reach_data[line_num].add(previous_line)
            self._reverse_reach_data[line_num].update(self.lines_reaching(previous_line))
        return self._reverse_reach_data[line_num]

    def lines_reached(self, line_num):
        """Compute the set of lines which may be reached from a given line."""
        return self._lines_reached(line_num, [])

    def _lines_reached(self, line_num, visited):
        """Recursively compute the set of lines which may be reached from a
        given line."""
        if line_num in self._reach_data:
            return self._reach_data[line_num]
        self._reach_data[line_num] = set()
        visited.append(line_num)
        next_line = self.forward_arcs[line_num]
        self._reach_data[line_num].add(next_line)
        if next_line in visited:
            cycle_start = visited.index(next_line)
            self._reach_data[line_num].update(visited[cycle_start:])
        else:
            self._reach_data[line_num].update(
                self._lines_reached(next_line, visited))
        return self._reach_data[line_num]

    def repair_instructions(self):
        """Repair a set of instructions by flipping one 'nop' to a 'jmp' (or
        vice versa) so that the program does not enter an infinite loop when
        executing from line 0."""
        eof = len(self.lines)
        for line_num in self.lines_reached(0):
            instruction = self.lines[line_num]
            swap_pairs = [('jmp', 'nop'), ('nop', 'jmp')]
            for current_func, new_func in swap_pairs:
                if instruction.func == current_func:
                    new_instruction = Instruction(new_func, instruction.arg)
                    new_next_line, _ = self.transition(new_instruction, line_num, 0)
                    if new_next_line in self.lines_reaching(eof):
                        new_lines = self.lines.copy()
                        new_lines[line_num] = new_instruction
                        new_program = ProgramDigraph(new_lines)
                        if 0 in new_program.lines_reaching(eof):
                            return new_program
        raise ValueError('This program can not be repaired.')


def main():
    # Part 1.
    program = ProgramDigraph.parse_from_strings(read_input_lines())
    print('Part 1:', program.evaluate())
    # Part 2.
    repaired_program = program.repair_instructions()
    print('Part 2:', repaired_program.evaluate())


if __name__ == '__main__':
    main()
