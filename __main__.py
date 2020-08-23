
import gd
import keyboard
import win32gui
import win32api
import win32con
import random
import time
import math

mem = gd.memory.get_memory()
win = win32gui.FindWindow(None, 'Geometry Dash')

def click():
    win32api.SendMessage(win, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))

def unclick():
    win32api.SendMessage(win, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(10, 10))


class Brain():
    def __init__(self, framesperround):
        self.directions = []
        self.inputs = framesperround
        self.randomize()
        self.fitness = 0
        self.previousFitness = 0
        self.percent = 0

    def randomize(self):
        for i in range(self.inputs):
            self.directions.append(random.uniform(0, 1) > 0.95)

    def run(self):
        mem.set_x_pos(0)
        while True:
            clicks = 0
            cx = mem.get_x_pos()
            if mem.is_dead():
                break
            if self.directions[math.floor(cx)]:
                click()
                clicks += 1
            else:
                unclick()
        unclick()
        self.fitness = max(0,math.pow(math.ceil(cx),2))
        self.previousFitness = math.floor(cx)
        self.percent = mem.percent

    def clone(self):
        clone = Brain(self.inputs)
        clone.directions = []
        for i in self.directions:
            clone.directions.append(i)
        
        clone.fitness = self.fitness
        clone.previousFitness = self.previousFitness

        return clone

    def mutate(self):
        mutationRate = 0.5
        for i in range(max(self.previousFitness-300,0), min(self.previousFitness+100, math.floor(mem.get_level_length() + 100))):
            rand = random.uniform(0, 1)
            if rand < mutationRate:
                self.directions[i] = random.uniform(0,1) > 0.95
        
class Population:
    def __init__(self, amount, framesperround):
        self.pop = []
        for i in range(amount+1):
            self.pop.append(Brain(framesperround))

        self.gen = 0
        self.sumFitness = 0

    def run(self):
        self.gen += 1
        print(f'GEN {self.gen}')
        mem.player_kill()
        
        if self.gen == 1:
            length = range(len(self.pop))
        else:
            length = range(1, len(self.pop))

        for i in length:
            while mem.is_dead():
                pass
            self.pop[i].run()
            print(f'FINISHED {i}/{len(self.pop)-1}: {self.pop[i].fitness} ({self.pop[i].percent}%)')
            mem.player_kill()
            
        self.naturalSelection()
        self.run()

    def naturalSelection(self):
        newPop = []

        bestDot = 0
        hiFit = 0
        for i in range(len(self.pop)):
            if self.pop[i].fitness > hiFit:
                hiFit = self.pop[i].fitness
                bestDot = i

        newPop.append(self.pop[bestDot].clone())
        for i in range(1, len(self.pop)):
            newPop.append(self.selectParent().clone())
        self.pop = newPop
        self.mutate()
    

    def getSumFitness(self):
        self.sumFitness = 0
        for brain in self.pop:
            self.sumFitness += brain.fitness

    def selectParent(self):
        runningSum = 0
        rand = random.uniform(0, self.sumFitness)

        for i in range(len(self.pop)):
            runningSum += self.pop[i].fitness
            if runningSum > rand:
                return self.pop[i]

    def mutate(self):
        for i in range(1, len(self.pop)):
            self.pop[i].mutate()

print(mem.get_level_length())
pop = Population(1, math.floor(mem.get_level_length() + 100))
pop.run()