# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 13:46:05 2020

Championship Algorithm for knapsack problem

@author: Fadhluddin bin Sahlan (1817445) & Muhammad Hassan bin Ashhuri (1812637)
"""
import random
import csv
import copy
import time


#GROUPING PARAMETER
NUM_OF_SOLUTIONS_GROUP = 32 #choose 2^n value
NUM_OF_GROUP = 32           #choose 2^n value

#GENETIC OPERATOR PARAMETER
MUTATION_NUM = 3
CROSSOVER_NUM = 16  
MUTATION_ITERATION = 10
CROSSOVER_ITERATION = 10
FINAL_ITERATOR = 10

#PUT DATA IN ARRAY FROM CSV
MAX_CAPACITY = 65

dataset = []
power = []
weight = []
filename = "Data.csv"

with open(filename) as csvDataSet:
    csvRead = csv.reader(csvDataSet)
    
    for eachdata in csvRead:
        dataset.append(eachdata)
        
csvDataSet.close()

dataset.pop()

for rec in dataset:
    power.append(int(rec[0]))
    weight.append(int(rec[1]))

#CLASS OF SOLUTION
class Solution:
    binary = []

    def __init__(self):
        zeroArray = [0]*32
        self.binary = zeroArray
        
    def getWeight(self):
        global weight
        totalWeight = 0
        i = 0
        for each in self.binary:
            totalWeight += (self.binary[i] * weight[i])
            i += 1
        return totalWeight
    
    def getPower(self):
        global power
        totalPower = 0
        i = 0
        for each in self.binary:
            totalPower += (self.binary[i] * power[i])
            i += 1
        return totalPower
    
    def randomSolution(self):
        randomArray = list(range(0,32))
        random.shuffle(randomArray)
        j = 0
        while j < len(randomArray):
            if (self.getWeight() + weight[randomArray[j]]) <= MAX_CAPACITY:
                self.binary[randomArray[j]] = 1
            
            else:
                self.binary[randomArray[j]] = 0
            j += 1
    
    def display(self):
        print(self.binary)
        print(self.getPower())

#CLASS OF GROUP
class Group:
    
    def __init__(self):
        self.setOfSolutions = []
        self.createSetOfSolutions()

    def getTotalValue(self):
        totalValue = 0
        for i in self.setOfSolutions:
            totalValue += i.getPower()
        
        return totalValue
    
    def sortSolutions(self):
        self.setOfSolutions.sort(key = lambda x: x.getPower(), reverse = True)
        
    def createSetOfSolutions(self):
        i = 0
        while i < NUM_OF_SOLUTIONS_GROUP:
    
            temp = Solution()
            temp.randomSolution()
    
            self.setOfSolutions.append(temp)
            i += 1
    
    def display(self):
        for i in self.setOfSolutions:
            print(i.binary)
            print(i.getPower())
        print(" ")


#GENETIC ALGORITHM OPERATOR FUNCTIONS
def mutate(item):
    randomArray = list(range(0,32))
    random.shuffle(randomArray)
    count = 0
    temp = copy.deepcopy(item)
    
    while count < MUTATION_NUM:
        
        if temp.binary[randomArray[count]] == 0:
            temp.binary[randomArray[count]] = 1
        else:
            temp.binary[randomArray[count]] = 0
        count += 1
    
    if temp.getPower() > item.getPower() and temp.getWeight() <= MAX_CAPACITY:
        item = temp
        
    return item
            
def crossover(item1, item2):
    randomArray = list(range(0,32))
    random.shuffle(randomArray)
    count = 0
    temp1 = copy.deepcopy(item1)
    temp2 = copy.deepcopy(item2)

    while count < CROSSOVER_NUM:
        temp1.binary[randomArray[count]], temp2.binary[randomArray[count]] = temp2.binary[randomArray[count]], temp1.binary[randomArray[count]]
        
        count += 1
    
    if temp1.getPower() > item1.getPower() and temp1.getWeight() <= MAX_CAPACITY:
        item1 = temp1
        
    if temp2.getPower() > item2.getPower() and temp2.getWeight() <= MAX_CAPACITY:
        item2 = temp2
    
    return item1.binary, item2.binary

def crossover2(item1, item2):
    randomArray = list(range(0,32))
    random.shuffle(randomArray)
    count = 0
    temp1 = copy.deepcopy(item1)
    temp2 = copy.deepcopy(item2)

    while count < CROSSOVER_NUM:
        temp1.binary[randomArray[count]], temp2.binary[randomArray[count]] = temp2.binary[randomArray[count]], temp1.binary[randomArray[count]]
        
        count += 1
    
    if temp1.getPower() > item1.getPower() and temp1.getWeight() <= MAX_CAPACITY:
        item1 = temp1
        
    if temp2.getPower() > item2.getPower() and temp2.getWeight() <= MAX_CAPACITY:
        item2 = temp2
    
    return item1, item2

#GROUP BASED GENETIC OPERATOR
def groupMutate(group):
    
    for x in range(MUTATION_ITERATION):
        for i in group.setOfSolutions:
            i.binary = mutate(i).binary
    group.sortSolutions()
    return group

def groupCrossover(group1, group2):
    group1.sortSolutions()
    group2.sortSolutions()
    for x in range(CROSSOVER_ITERATION):
        for i in range(NUM_OF_SOLUTIONS_GROUP):
            group1.setOfSolutions[i].binary, group2.setOfSolutions[i].binary = crossover(group1.setOfSolutions[i], group2.setOfSolutions[i])
    group1.sortSolutions()
    group2.sortSolutions()
    return group1, group2
       
#GENERATE RANDOM SOLUTION AND PUT IN GROUP
start_time = time.time()

Groups = []
i = 0

while i < NUM_OF_GROUP:
    Groups.append(Group())
    i += 1

#GROUP ELIMINATION ROUND
print("=================")
print("GROUPING ELIMINATION STAGE (TOTAL POWER OF GROUP)")
print("=================")
for i in Groups:
    print(i.getTotalValue())
print("=================")

while (len(Groups) > 1):
    x = 0
    iterator = int(len(Groups)/2)
    while x < iterator:
        Groups.sort(key = lambda x: x.getTotalValue(), reverse = True)

        Groups[x] = groupMutate(Groups[x])
        Groups[x+iterator] = groupMutate(Groups[x+iterator])
        Groups[x], Groups[x+iterator] = groupCrossover(Groups[x], Groups[x+iterator])
        x += 1

    Groups.sort(key = lambda x: x.getTotalValue(), reverse = True)
    i = 1
    while i <= iterator:
        Groups.pop(len(Groups) - i)
        i += 1
    
    for i in Groups:
        print(i.getTotalValue())
    print("=================")
    
    
#IMPROVING FINAL WINNING GROUP
winningGroup = Groups[0].setOfSolutions
print("=================")
print("SOLUTIONS OF WINNING GROUP ELIMINATION (POWER OF SOLUTION)")
print("=================")
for i in winningGroup:
    print(i.getPower())
print("=================")    
while (len(winningGroup) > 1):
    x = 0
    iterator = int(len(winningGroup)/2)
    while x < iterator:
        for i in range(FINAL_ITERATOR):
            winningGroup.sort(key = lambda x: x.getPower(), reverse = True)
            winningGroup[x] = mutate(winningGroup[x])
            winningGroup[x + iterator] = mutate(winningGroup[x + iterator])
            winningGroup[x], winningGroup[x+iterator] = crossover2(winningGroup[x], winningGroup[x+iterator])
        x += 1

    winningGroup.sort(key = lambda x: x.getPower(), reverse = True)
    i = 1
    while i <= iterator:
        winningGroup.pop(len(winningGroup) - i)
        i += 1
    
    for i in winningGroup:
        print(i.getPower())
    print("=================")

optimalSolution = winningGroup[0]

print ("OPTIMAL SOLUTION IS")
optimalSolution.display()

print("Running Time: ")
print((time.time() - start_time))
