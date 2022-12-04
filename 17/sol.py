"""Day 17 solution."""

from collections import defaultdict
from itertools import product


class NDimCubeSim:
    """Simulates an n-Dimensional Conway Cube."""

    def __init__(self, initial_state, dims=3):
        self._active_nodes = initial_state
        self._dims = dims
        self._has_active_neighbors_this_cycle = defaultdict(int)

    @staticmethod
    def parse_from_string(input_string, dims=3):
        """Parse a Conway Cube simulator from an input string."""
        x = 0
        y = 0
        active_indices = set()
        for line in input_string.split("\n"):
            for character in line:
                if character == "#":
                    active_indices.add((x,y) + tuple(0 for _ in range(dims-2)))
                y += 1
            x += 1
            y = 0
        return NDimCubeSim(active_indices, dims=dims)

    def simulate_cycle(self):
        """Simulate a single cycle of the Conway Cube."""
        for node in self._active_nodes:
            for delta in product((-1, 0, 1), repeat=self._dims):
                if all(delta_i == 0 for delta_i in delta):
                    continue
                neighbor_coordinates = tuple(
                    node_i + delta_i for (node_i, delta_i) in zip(node, delta))
                self._has_active_neighbors_this_cycle[neighbor_coordinates] += 1
        next_active_nodes = set()
        for node, active_neighbor_count in self._has_active_neighbors_this_cycle.items():
            if node in self._active_nodes and active_neighbor_count in (2,3):
                next_active_nodes.add(node)
            elif active_neighbor_count == 3:
                next_active_nodes.add(node)
        self._active_nodes = next_active_nodes
        self._has_active_neighbors_this_cycle.clear()

    def simulate_n_cycles(self, n):
        """Simulate the given number of cycles."""
        for _ in range(n):
            self.simulate_cycle()

    def count_active(self):
        """Count the number of currently active nodes in the cube."""
        return len(self._active_nodes)


with open("input", encoding="utf-8") as f:
    input_string = f.read()
    cube_sim3D = NDimCubeSim.parse_from_string(input_string, dims=3)
    cube_sim3D.simulate_n_cycles(n=6)
    print(cube_sim3D.count_active())
    cube_sim4D = NDimCubeSim.parse_from_string(input_string, dims=4)
    cube_sim4D.simulate_n_cycles(n=6)
    print(cube_sim4D.count_active())
