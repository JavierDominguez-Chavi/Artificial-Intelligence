import random 
#Base para la definicion de tipos y estructuras de datos
from deap import base 
#Crear clases personalizadas para los individuos(individuals) y la aptitud en el algoritmo(fitness)
from deap import creator
#Herramientas y funciones utilies para el algoritmo
from deap import tools

#Crear la clase personalizada "FitnessMax" mediante el uso de 2base.Fitness" y establece el peso(weights) de la aptitud en 1.0
#En esta clase se representa la aptitud(fitness) maxima en el problema de optimizacion
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

#Crear la clase "Individual" utilizando la clase "list" como base
#Se asigna la clase "FitnessMax" como la clase de aptitud(fitness) para los individuos
creator.create("Individual", list, fitness=creator.FitnessMax)

#Crear una instancia de la clase "Toolbox" que se encuntra en el modulo "base"
#La clase instanciada sera el contenedor para registrar y almacenar las herramientas del algoritmo
toolbox = base.Toolbox()

#Registrar la funcion "random.randint" en el toolbox con el nombre "attribute_bool"
#Esta funcion sera utilizada para generar atributos booleanos(0 o 1)
toolbox.register("attribute_bool", random.randint, 0, 1)

#Registrar la funcion "tools.initRepeat" en el toolbox con el nombre "individual"
#Esta funcion sera utilizada para inicializar un individuo con atributos booleanos generados por la funcion "attribute_bool"
#En este caso de establece que cada individuo tendra 100 atributos
toolbox.register("indivual", tools.initRepeat, creator.Individual, toolbox.attribute_bool, 100)

#Registrar la funcion "initRepeat" en el toolbox con el nombre "population"
#Esta funcion sera utilizada para inicializar una poblacion(population) de individuos utilizando la funcion "individual"
#La poblacion(population) sera una lista de individuos
toolbox.register("population", tools.initRepeat, list, toolbox.indivual)

#Definir la funcion "evalOneMax" que toma un individuo como argumento y calcula la suma de sus atributos
#La funcion devuelve una tupla con el resultado de "sum"
#La coma al final de la funcion indica el retorno de una tupla en lugar de un valor unico(aspecto de suma importancia)
def evalOneMax(individual):
    return sum(individual),

#Registrar la funcion "evalOneMax" en el toolbox con el nombre "evaluate"
#La funcion se utiliza para evaluar la aptitud(fitness) de un individuo
toolbox.register("evaluate", evalOneMax)

#Registrar la funcion "cxTwoPoint" en el toolbox con el nombre "mate"
#La funcion "mate" implementa la cruza(crossover) de dos puntos(padres) para realizar la reproduccion en el algoritmo
toolbox.register("mate", tools.cxTwoPoint)

#Registrar la funcion "mutFlipBiten" en el toolbox con el nombre "mutate"
#La funcion implementa la mutacion de bits para variar a los individuos
#El argumento "indpb=0.05"(individual probability) determina la probabilidad de mutacion de cada bit
toolbox.register("mutate", tools.mutFlipBit, indpb = 0.05)

#Registrar la funcion "selTournament" en el toolbox con el nombre "select"
#La funcion implementa la selección de torneos para seleccionar a los individuos
#"tournsize = 3" determina que se realizara un torneo entre 3 individuos para seleccionar uno
toolbox.register("select", tools.selTournament, tournsize = 3)

def main():
    #Semilla para asegurar que la secuencia de numeros aleatorios sea igual en cada ejecucion
    random.seed(300)
    #Inicializar la poblacion(population) utilizando la funcion "population" definida en pasos anteriores de este codigo
    #Crear una poblacion(population) de 300 idividuos(individuals)
    population = toolbox.population(n=300)

    #Establecer la probabilidad de que dos individuos(individuals) se cruzen (CROSSOVER_PROBABILITY)
    #Establecer la probabilidad de que un individuo(individual) mute (MUTATION_PROBABILITY)
    CROSSOVER_PROBABILITY, MUTATION_PROBABILITY = 0.5, 0.2

    print("Start of evolution")

    #Evaluar la aptitud(fitness) de toda la poblacion(population) 
    #Utilizar la funcion "evaluate" definida en pasos anteriores de este codigo
    fitnesses = list(map(toolbox.evaluate, population))

    #Asignar las aptitudes(fitnesses) evaluadas a cada individuo de la poblacion(population)
    for individual, fit in zip(population, fitnesses):
        individual.fitness.values = fit
    
    print("  Evaluated %i individuals" % len(population))

    #Extraer las apitudes(fitness) de los individuos de la poblacion y guardarlos en una lista
    fits = [individual.fitness.values[0] for individual in population]

    #Contador para el numero de generaciones
    generation = 0

    while max(fits) < 100 and generation < 1000:
        generation += 1
        print("-- Generation %i --" % generation)

        #Seleccionar la siguiente generacion de individuos(individuals)
        #Utilizar "select" funcion definida en pasos anteriores de este codigo
        offspring = toolbox.select(population, len(population))

        #Clonar los individuos(individuals) seleccionados para crear una nueva generacion 
        offspring = list(map(toolbox.clone, offspring))

        #Operaciones de cruce(crossover)
        #Iterar sobre pares e inpares de individuos que se asignaran a child1 y child2
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            #Si el numero generado de la funcion "random"(1 o 0) es menor a "CROSSOVER_PROBABILITY" se ejecuta el cruce(mate)
            #Funcion "mate" definida en pasos anteriores de este codigo
            #La funcion combina informacion genetica de dos individuos para generar un nuevo descendiente
            if random.random() < CROSSOVER_PROBABILITY:
                toolbox.mate(child1, child2)
                #Eliminar los valores de aptitud(fitness) del individuo "child1" 
                #Asegurar que se vuelvan a evaluar mas adelante en el bucle principal
                del child1.fitness.values
                del child2.fitness.values
        
        #Operaciones de mutacion(mutate)
        #Iterar sobre los individuos de "offspring"
        for mutant in offspring:
            #Si el numero generado de la funcion "random"(1 o 0) es menor a "MUTATION_PROBABILITY" se ejecuta la mutacion(mutate)
            #Funcion "mutate" definida en pasos anteriores de este codigo
            #La funcion introduce variacion para cada individuo de la poblacion
            if random.random() < MUTATION_PROBABILITY:
                toolbox.mutate(mutant)
                #Eliminar el valor de aptitud(fitness) del individuo "mutant"
                #Asegurar que se vuelva a evaluar mas adelante en el bucle principal.
                del mutant.fitness.values
        
        #Lista "invalid_individual" que contiene los individuos en la descendencia(offspring) cuya aptitud(fitness) no es valida
        invalid_individual = [individual for individual in offspring if not individual.fitness.valid]
        #Evaluar cada individuo de la lista "invalid_individual" y devolver el iterador de las aptitudes(fitness) evaluadas
        fitnesses = map(toolbox.evaluate, invalid_individual)
        #Iterar cada individuo y su aptitud "fit" en el iterador "fitnesses"
        for individual, fit in zip(invalid_individual, fitnesses):
            #Asignar la aptitud calculada "fit" al atributo "fitness.values" de cada individuo 
            #Se actualiza la aptitud del individuo con los nuevos valores calculados
            individual.fitness.values = fit

        #Actualizar la poblacion original(population) asignandole los individuos modificados en la descendencia(offspring)
        #Asegurar que todos los individuos en la población tengan aptitudes validas y actualizadas para la proxima iteracion
        population[:] = offspring

        #Lista que contiene los valores de aptitud(fitness) cada individuo en la poblacion
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

    #Seleccionar al mejor individuo(individual) 
    #"1" especifica seleccionar solo un individuo
    best_individual = tools.selBest(population, 1)[0]

    print("Best individual is %s, %s" % (best_individual, best_individual.fitness.values))

if __name__ == "__main__":
    main()

