import random
from deap import base 
from deap import creator
from deap import tools

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness = creator.FitnessMin)

toolbox = base.Toolbox()

toolbox.register("attribute_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute_bool, 100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMin(individual):
    return sum(individual),

toolbox.register("evaluate", evalOneMin)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.5)
toolbox.register("select", tools.selTournament, tournsize = 3)

def main():
    random.seed(300)
    population = toolbox.population(n=300)
    
    CROSSOVER_PROBABILITY, MUTATION_PROBABILITY = 0.5, 0.2

    print("Start of evolution")

    fitnesses = list(map(toolbox.evaluate, population))

    for individual, fit in zip(population, fitnesses):
        individual.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(population))

    fits = [individual.fitness.values[0] for individual in population]

    generation = 0

    while max(fits) < 100 and generation < 1000:
        generation += 1

        print("-- Generation %i --" % generation)

        offspring = toolbox.select(population, len(population))
        offspring = list(map(toolbox.clone, offspring))

        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CROSSOVER_PROBABILITY:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child1.fitness.values

        for mutant in offspring:
            if random.random() < MUTATION_PROBABILITY:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        invalid_individuals = [individual for individual in offspring if not individual.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_individuals)

        for individual, fit in zip(invalid_individuals, fitnesses):
            individual.fitness.values = fit

        population[:] = offspring
        fits = [individual.fitness.values[0] for individual in population]

        length = len(population)
        mean = sum(fits) / length
        square_sum = sum(x*x for x in fits)
        standard_deviation = abs(square_sum / length - mean**2)**0.5

        print("  Minimun %s" % min(fits))
        print("  Maximun %s" % max(fits))
        print("  Average %s" % mean)
        print("  Standard deviation %s" % standard_deviation)
    
    print("-- End of successful evolution --")

    best_individual = tools.selBest(population, 1)[0]

    print("Best individual is %s, %s" % (best_individual, best_individual.fitness.values))

if __name__ == "__main__":
    main()