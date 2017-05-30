import numpy as np

# In each cell
BASE_MUTATION_RATE = 10**5
TELOMER_LENGTH = 50

# Global
DEATH_PROBABILITY = 10
FACTOR_INCREASE_BASE_RATE_MUTATION = 10**2
KILL_NEIGHBOR_PROBABILITY = 30
RANDOM_CELL_DEATH = 10**3

# Growth factor
PREDEFINED_SPATIAL_BOUNDARY = 0.95 #TODO: Check this value. Other posibility is 0.858.

# Random parameters for generating future mitotic event
MIN_FUTURE_MITOTIC_EVENT = 5
MAX_FUTURE_MITOTIC_EVENT = 10

class SimulationGlobals:

    def __init__(self, base_mutation_rate, telomer_length, death_probability, factor_increase_base_rate_mutation, kill_neighbor, random_death, predefined_spatial_boundary, min_future_mitotic_event, max_future_mitotic_event):
        self.m = base_mutation_rate
        self.tl = telomer_length
        self.e = death_probability
        self.i = factor_increase_base_rate_mutation
        self.g = kill_neighbor
        self.a = random_death
        self.predefined_spatial_boundary = predefined_spatial_boundary
        self.min_future_mitotic_event = min_future_mitotic_event
        self.max_future_mitotic_event = max_future_mitotic_event

class Tests:

    def __init__(self, simulationGlobals):
        self. simulationGlobals = simulationGlobals

    """ 
        Test 1: muerte aleatoria de la célula, con probabilidad 1/a.
    """
    def random_death_test(self):
        if np.random.random() < 1/self.simulationGlobals.a:
            return True
        return False

    """
        Test 2: muerte por mutaciones, con n mutaciones sufridas tiene probabilidad de muerte n/e.
    """
    def genetic_damage_test(self, n, ea):
        if ea == 0 and np.random.randint(0,n) < n/self.simulationGlobals.e:
            return True
        return False

    """
        Test 3: factor de crecimiento dentro de umbral 
    """
    def growth_factor_cheking(self, sg, spatial_boundary):
        if spatial_boundary > self.predefined_spatial_boundary and sg == 0:
            return False
        return True

    """
        Test 4: matar a un vecino, si el vecindario está completo, probabilidad de matar a un vecino 1/g.
    """
    def ignore_growth_inhibit_checking(self, is_neighborhood_full, igi):
        if is_neighborhood_full and igi == 1 and np.random.random() < 1/self.simulationGlobals.g:
            return True
        return False

    """
        Test 5: muerte por acortamiento de telomero. 
    """
    def limitless_replicative_potencial_checking(self, tl, ei):
        if tl == 0 and ei == 0:
            return True
        return False

    def mitosis_test(self, checking_results):
        if checking_results == (True, False, False):
            return True
        return False


class Genome:
    
    def __init__(self, sg, igi, ea, ei, gi):
        self.sg = sg
        self.igi = igi
        self.ea = ea
        self.ei = ei
        self.gi = gi

    def mutations(self):
        return sum(vars(self).values())

    def __str__(self):
        return str(self.sg) + str(self.igi) + str(self.ea) + str(self.ei) + str(self.gi)

class Cell:

    def __init__(self, position, sg, igi, ea, ei, gi, tl, m):
        self.position = position
        self.tl = tl
        self.m = m
        self.genome = Genome(sg, igi, ea, ei, gi)

    def decrease_telomer(self):
        self.tl -= 1

    def increment_base_muration_rate(self, i):
        if self.gi == 1:
            self.m *= i

    def mutations(self):
        return self.genome.mutations()

    def add_mutations(self): #TODO: Make this method
        pass

    def perform_mitosis(self, position, i):
        self.decrease_telomer()
        self.increment_base_muration_rate(i)
        self.add_mutations()
        return Cell(position, self.sg, self.igi, self.ea, self.ei, self.gi, self.tl, self.m)

    def __str__(self):
        return str(self.genome)

class Grid:

    def __init__(self, height, width, depth, first_cell):
        self.height = height
        self.width = width
        self.depth = depth
        self.grid = self.build()
        self.initialization(first_cell)

    def build(self):
        grid = np.empty((self.height,self.width,self.depth))
        grid = grid.astype(np.str_)
        grid.fill('')
        return grid

    def initialization(self, first_cell):
        self.grid[self.__middle__(self.height)][self.__middle__(self.width)][self.__middle__(self.depth)] = first_cell

    def __middle__(self, value):
        return int(value/2)

class Automata:
    
    def __init__(self, dimension, iterations, simulationGlobals):
        self.dimension = dimension
        self.iterations = iterations
        self.simulationGlobals = simulationGlobals
        self.tests = Tests(simulationGlobals)
        self.cells = {}
        self.mitotic_agenda = {}
        self.grid = self.build()
        

    def build(self):
        position = (self.dimension/2,self.dimension/2,self.dimension/2)
        first_cell = Cell(position, 0, 0, 0, 0, 0, self.simulationGlobals.tl, self.simulationGlobals.m)
        self.cells[position] = first_cell
        grid = Grid(self.dimension,self.dimension,self.dimension, first_cell)
        self.mitotic_agenda[self.future_mitotic_event()] = position
        return grid

    def push_event(self):
        pass

    def future_mitotic_event(self):
        return np.random.randint(self.simulationGlobals.min_future_mitotic_event, self.simulationGlobals.max_future_mitotic_event+1)

    def run(self):
        pass


if __name__ == "__main__":

    simulationGlobals = SimulationGlobals(BASE_MUTATION_RATE, TELOMER_LENGTH, DEATH_PROBABILITY, FACTOR_INCREASE_BASE_RATE_MUTATION, KILL_NEIGHBOR_PROBABILITY, RANDOM_CELL_DEATH, PREDEFINED_SPATIAL_BOUNDARY, MIN_FUTURE_MITOTIC_EVENT, MAX_FUTURE_MITOTIC_EVENT)

    automata = Automata(3, 10, simulationGlobals)

    print(automata.grid.grid)

    #first_cell = Genome(0, 0, 0, 0, 0, 0, 50)

    #grid = Grid(3,3,3)

    """height = 10
    width = 10
    depth = 10

    grid = np.empty((height,width,depth))

    grid = grid.astype(np.str_)

    grid.fill(0)

    print(grid)"""

    """grid = Grid(10,10,10, None)
    print(grid.grid)"""


