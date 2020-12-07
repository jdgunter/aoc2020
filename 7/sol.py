"""Solution to Advent of Code Day 7."""


def read_input_lines():
    with open('input') as f:
        return f.readlines()


class BagDAG:
    """A Directed Acyclic Graph representation of bag content constraints."""

    def __init__(self, bag_rules):
        """Create a graph from a sequence of bag rule strings."""
        self.vertices = set()
        self.arcs = {}
        self.reverse_arcs = {}
        self.bags_containing = {}
        for bag_rule in bag_rules:
            self.process_bag_rule(bag_rule)

    def process_bag_rule(self, bag_rule):
        """Process a bag rule string.
        
        This adds all forward arcs for a bag's vertex, along with the 
        corresponding reverse arcs, and also adds the bag to the list of 
        vertices if it has not been seen previously.
        """
        bag, contents = bag_rule.split(' bags contain ')
        if bag not in self.vertices:
            self.add_new_vertex(bag)
        if contents[:2] == 'no':
            return
        for content in contents.split(','):
            words = content.split()
            count = int(words[0])
            inner_bag = words[1] + ' ' + words[2]
            if inner_bag not in self.vertices:
                self.add_new_vertex(inner_bag)
            self.arcs[bag][inner_bag] = count
            self.reverse_arcs[inner_bag][bag] = count
    
    def add_new_vertex(self, vertex):
        """Add a new vertex to the graph."""
        self.vertices.add(vertex)
        self.arcs[vertex] = {}
        self.reverse_arcs[vertex] = {}

    def compute_bags_containing(self, bag):
        """Recursively compute the set of bags containing a bag.
        
        Stores the results in a dictionary mapping bags to a 
        a map of containing bags to number of copies of the first bag stored.
        """
        if bag in self.bags_containing:
            return self.bags_containing[bag]

        self.bags_containing[bag] = set()
        for outer_bag in self.reverse_arcs[bag]:
            self.bags_containing[bag].add(outer_bag)
            if outer_bag not in self.bags_containing:
                self.bags_containing[outer_bag] = self.compute_bags_containing(outer_bag)
            self.bags_containing[bag].update(self.bags_containing[outer_bag])
        return self.bags_containing[bag]

    def count_bags_inside(self, bag):
        """Recursively compute the set of bags contained inside of a bag."""
        total_bags = 0
        for inner_bag in self.arcs[bag]:
            num_inner_bags = self.arcs[bag][inner_bag]
            total_bags += num_inner_bags * (1 + self.count_bags_inside(inner_bag))
        return total_bags


def main():
    dag = BagDAG(read_input_lines())
    print('Part 1:', len(dag.compute_bags_containing('shiny gold')))
    print('Part 2:', dag.count_bags_inside('shiny gold'))


if __name__=='__main__':
    main()