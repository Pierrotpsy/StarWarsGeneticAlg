from ast import While
from asyncore import read
from hashlib import new
import os
import math
import random
from fastnumbers import isfloat
import numpy as np

MUTATE = 0.0000001
MAX_ITER = 10000
POPULATION = None
MUTATE_ODDS = 0.4

def readF(filepath):
    with open(filepath, "r") as rfile:
        dic= {}
        for line in rfile:
            stripped_line = line.strip()
            item = stripped_line.split(';')
            if(isfloat(item[0])):
                dic[float(item[0])] = [float(item[1]), float(item[2])]
        return dic
    
os.chdir('c:\\Users\\33769\\Documents\\Python Scripts\\Star Wars')
global CHECK 
CHECK = readF("position_sample.csv")

class Orbit():
    def __init__(self, _type, params = None):
        self.params = params
        self.fitness = None
        self._type = _type
        
    def getValue_t(self, t):
        return self.params[0]*math.sin(self.params[1]*t+self.params[2])
        
    def setFitness(self):
        ind = None
        f_added = 0
        if(self._type == 'X'):
            ind = 0
        else:
            ind = 1
            
        for i in CHECK.keys():
            f_added += abs(CHECK[i][ind] - self.getValue_t(i))**2
            
        self.fitness = f_added
        
    def __str__(self):
        return f'{self.params[0]} | {self.params[1]} | {self.params[2]}'
    
    def setParams(self, ps):
        self.params = ps
        
    def __eq__(self, other):
        return self.params[0] == other.params[0] and self.params[1] == other.params[1] and self.params[2] == other.params[2]
    
def generateChromosome():
    params = []
    for i in range(3):
        params.append(round(random.uniform(-100, 100), 3))
    return params

def create_pop(t, n = 100):
    pop = [Orbit(_type = t) for i in range(n)]
    for i in range(len(pop)):
        pop[i].setParams(generateChromosome())
        pop[i].setFitness()
    return pop

def stop():
    if MAX_ITER == iteration:
        return True
    return False

def selection(pop):
    newpop = []
    pop.sort(key = lambda x : x.fitness)
    i = 0
    
    newpop = pop[0:len(pop)//2]
    return newpop

def getParents(population):
    parent1 = None
    parent2 = None
    
    sum_fitness = np.sum([x.fitness for x in population])
    for i in population:
        i.survival = i.fitness/(sum_fitness*1.0)
        
    while True:
        randomParentFitness = np.random.rand()
        parent1_random = [x for x in population if x.survival <= randomParentFitness]
        try:
            parent1 = parent1_random[0]
            break
        except:
            pass
    
    while True:
        randomParentFitness = np.random.rand()
        parent2_random = [x for x in population if x.survival <= randomParentFitness]
        try:
            ind = np.random.randint(len(parent2_random))
            parent2 = parent2_random[ind]
            if parent1 != parent2:
                break
            else:
                continue
        except:
            continue
        
    return parent1, parent2

def reproduce(p1, p2):
    k = np.random.randint(3)
    child1, child2 = Orbit(_type = p1._type), Orbit(_type = p1._type)
    child1.params = p1.params[0:k] + p2.params[k:]
    child1.setFitness()
    child2.params = p2.params[0:k] + p1.params[k:]
    child2.setFitness()
    if(child1.fitness > child2.fitness):
        return child2
    else: 
        return child1

def mutateChromosome(chrom, ind):
    k = random.randint(0,10)
    
    rate = np.random.rand()
    c = chrom
    if (k < 4):
        chrom[ind] = min(chrom[ind] + rate*chrom[ind], 100) if chrom[ind] > 0 else max(chrom[ind] + rate*chrom[ind], -100)
    elif(k < 8):
        chrom[ind] = min(chrom[ind] - rate*chrom[ind], -100) if chrom[ind] > 0 else max(chrom[ind] - rate*chrom[ind], 100)
    elif(k < 9):
        chrom[ind] = round(random.uniform(-100, 0), 3)
    else:
        chrom[ind] = round(random.uniform(0, 100), 3)
    return chrom

def mutate(c, odds = MUTATE_ODDS):
    p = c.params.copy()
    for i in range(3):
        k = np.random.rand()
        if c.fitness > MUTATE and k < odds:
            c.setParams(mutateChromosome(c.params, i))
    c.setFitness()
    return c

def geneticAlg(pop):
    newpopulation = []
    for i in range(len(pop)):
        parent1, parent2 = getParents(pop)
        
        child = reproduce(parent1, parent2)
        
        child = mutate(child)
        
        newpopulation.append(child)
        
    newpopulation.sort(key = lambda x : x.fitness)
    return newpopulation

pop_size = 300

populationX = create_pop('X', pop_size)
populationY = create_pop('Y', pop_size)


iteration = 0
while not stop():
    populationX = geneticAlg(populationX)
    populationY = geneticAlg(populationY)
    
    iteration += 1
    if(iteration % 100 == 0):
        print ("X |Iteration number : ", iteration, "   Parameters : ", populationX[0].params, "   Fitness : ", populationX[0].fitness)
        print ("Y |Iteration number : ", iteration, "   Parameters : ", populationY[0].params, "   Fitness : ", populationY[0].fitness)
