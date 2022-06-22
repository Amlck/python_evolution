import random


class Individual:
    def __init__(self, name, gene):
        self.gene = gene  # array of genes
        self.name = "Individual " + str(name)
        self.num = name

    alive = False
    score = 0.0

    def info(self):
        print(self.name, self.gene, "Score:", self.score)


# <editor-fold desc="Setup">
next_ind = 1  # next individual number
highest = 0  # current highest score
generation = 0
highest_item = Individual("h", [])  # storage for best specimen
population = []
pop_holder = []
gene_arr = []
genome_failed = False
size = int(input("Enter size of max population: "))
for i in range(size):
    population.append(Individual(i, []))
    next_ind += 1
gene_size = int(input("Enter size of genome: "))
founder = int(input("Enter size of founding population: "))
max_gene_num = int(input("Enter max gene: "))
min_gene_num = int(input("Enter min gene: "))
for ent in range(founder):
    print("Now editing " + str(population[ent].name))
    population[ent].gene = [int(i) for i in input().split()]
    population[ent].alive = True
target = int(input("Enter target score: "))
for j in range(min_gene_num, max_gene_num):
    gene_arr.append(j)


# </editor-fold>

def score_det(indi: Individual):  # returns Individual() with updated score
    sum_score = 0
    for i1 in indi.gene:
        sum_score += int(i1)
    # sum_score = sum_score / indi.gene[0]
    return sum_score


def survival_of_fittest(pop):
    relative_str = []
    weakest = []
    killed = 0
    for ind_sf1 in pop:
        ind_sf1.score = score_det(ind_sf1)
        relative_str.append(ind_sf1.score)
    for ind_sf2 in pop:
        if ind_sf2.score == min(relative_str):
            weakest.append(pop.index(ind_sf2))
    if weakest:
        a = random.choice(weakest)
        pop[a].alive = False
        killed += 1
    if weakest and len(pop) > 7:
        for kil in range(int(len(pop) / 5)):
            b = random.choice(weakest)
            pop[b].alive = False
            killed += 1
    print(killed)
    return pop


def breed(a: Individual, b: Individual):  # returns born Individual()
    child = Individual(next_ind, [])
    for g in range(gene_size):
        child.gene.append(random.choice([a.gene[g], b.gene[g]]))
    child.alive = True
    mut = random.randint(0, gene_size)
    ation = random.randint(0, gene_size)
    if mut == ation:
        done = False
        while not done:
            gene_to_change = random.randint(0, gene_size - 1)
            old_gene = child.gene[gene_to_change]
            child.gene[gene_to_change] = random.choice(gene_arr)
            if old_gene != child.gene[gene_to_change]:
                done = True
    return child


def check_identical(pop):
    identical = True
    checker = pop[0].gene
    for k in pop:
        if k.gene != checker:
            identical = False
    return identical


while highest < target:
    full = True
    list_of_empty_spots = []
    list_of_occupied_spots = []
    for check in population:  # checking for empty spaces
        if not check.alive:
            full = False
            list_of_empty_spots.append(population.index(check))
    list_of_occupied_spots = [x for x in range(size) if x not in list_of_empty_spots]
    if not full:
        for spot in list_of_empty_spots:
            population[spot] = breed(population[random.choice(list_of_occupied_spots)],
                                     population[random.choice(list_of_occupied_spots)])
            next_ind += 1

    # now the population is full
    population = survival_of_fittest(population)
    for item in population:
        if item.score > highest:
            highest = item.score
            highest_item = item

    if check_identical(population):
        genome_failed = True
        break
    pop_holder = population
    generation += 1

    for p in population:
        print(p.gene)
    highest_item.info()
    print()
    # print(list_of_empty_spots)
    # print(list_of_occupied_spots)
if not genome_failed:
    print("Evolution complete!")
    print("Generation:%s" % (int(highest_item.num) - size + 2))
else:
    print("Genome failed due to identical population")
    for p in population:
        print(p.gene)
    print("Highest score: %d" % highest)
