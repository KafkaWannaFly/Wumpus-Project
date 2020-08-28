import numpy as np
import itertools
import sys
from heapq import heappush, heappop
from pysat.solvers import Glucose3

class Map:
    def __init__(self):
        map, agen_pos = readFile()
        self.map = map
        self.a_p = agen_pos
        self.width = len(map)
        self.height = len(map[0])
        self.cave = self.a_p

    def getSize(self):
        return tuple(self.width, self.height)

    def getMap(self):
        return self.map

    def getAgentPos(self):
        return self.a_p

    def updateMap(self, pos, status):
        self.map[pos[0]][pos[1]] = status

def readFile():
    path = "map1.txt"
    file = open(path, "r")
    size = int(file.readline())
    map = []
    agent_pos: tuple
    for i in file:
        temp = []
        for j in i:
            if j != '.' and j != '\n':
                temp.append(j)
            if j == 'A':
                agent_pos = (i, j)
        map.append(temp)
    return map, agent_pos

def add_adjacent(matrix, width, height):
    dict = {}
    k = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for i in range(height):
        for j in range(width):
            temp = []
            for x in k:
                tnp_pos = (i + x[0], j + x[1])
                if validCell(tmp_pos[0], tmp_pos[1], (width, height)):
                    temp.append(matrix[tmp_pos[0]][tmp_pos[1]])
            dict[(i, j)] = temp
    return dict

def manhattan_distance(current_pos, food):
    return sum(map(lambda x, y: abs(x - y), current_pos, food))

def backtracking(current, parent_list):
    path = []
    tracer = current

    while True:
        path.append(tracer)
        tracer = parent_list[tracer]
        if tracer is None:
            break

    return path

def A_star(maze, cur_pos, des_pos):
    frontier = []
    explored = []
    parent_nodes = {}
    cost = 0
    adjacent_nodes = add_adjacent(maze, len(maze), len(mae[0]))

    start_node = (cost + manhattan_distance(cur_pos, des_pos), cur_pos)
    parent_nodes[cur_pos] = None

    heappush(frontier, start_node)

    while True:
        if not frontier:
            return None
        else:
            tmp_tuple = heappop(frontier)  
            current_node = tmp_tuple[1]
            cost = tmp_tuple[0] - manhattan_distance(current_node, des_pos)

            is_explored = False
            for explored_node in explored:
                if(current_node == explored_node):
                    is_explored = True
                    break

            if is_explored:
                continue

            explored.append(current_node)

            if current_node == des_pos:
                final_path = backtracking(current_node, parent_nodes)
                return final_path[::-1]

            for adjacent in adjacent_nodes[current_node]:
                heappush(frontier, ((cost + 1) + manhattan_distance(adjacent, des_pos), adjacent))
                if adjacent not in explored:
                    parent_nodes[adjacent] = current_node


def validCell(i, j, shape):
    return 0 <= i and i < shape[0] and 0 <= j and j < shape[1]

class Knowlegdesbase:
    def __init__(self, maps_size):
        self.DangerFormula = []
        self.wumpus = Glucose3()
        self.pit = Glucose3()
        self.size = maps_size

    def is_wumpus(self, pos):
        return self.wumpus.solve([self.pos_to_num(pos, 0, 1)])

    def is_pit(self, pos):
        return self.pit.solve([self.pos_to_num(pos, 0, 1)])

    def makeFormula(self):
        k = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        map = getsize()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                cur = self.pos_to_num((i, j), 0, -1)
                for x in k:
                    temp = (i + x[0], j + x[1])
                    if validCell(temp[0], temp[1], self.size):
                        temp2 = pos_to_num((temp[0], temp[1]), 1, 1)
                        self.DangerFormula.append([cur, temp2])
        self.wumpus.append_formula(self.DangerFormula)
        self.pit.append_formula(self.DangerFormula)

    def newKB(self, pos, breeze, stench):
        temp = 0
        if (stench):
            temp = self.pos_to_num(pos, 1, 1)
        else:
            temp = self.pos_to_num(pos, 1, -1)
        self.DangerFormula.append([temp])
        self.wumpus.add_clause([temp])

        if (breeze):
            temp = self.pos_to_num(pos, 1, 1)
        else:
            temp = self.pos_to_num(pos, 1, -1)
        self.pit.add_clause([temp])

    def showKB(self):
        return self.DangerFormula

    def Remove(self):
        #Dùng cho bắn, chưa bắn nên chưa biết làm
        pass

    def pos_to_num(self, pos, is_stench, s):
        return int(s * (pos[1] * self.size[0] + pos[0] + 1 + is_stench * pos[0] * pos[1]))

class Agent:
    def _init_(self):
        self.map = Map.getMap()
        self.temp_map = Map
        self.moveset = [1, 2, 3, 4] #1 move, 2 shoot, 3 pick, 4 climb out
        self.AKB = Knowlegdesbase((len(self.map), len(self.map[0])))
        self.AKB.makeFormula()
        self.visited = []
        self.doing = []
        self.where_e_w = []
        self.climb_out = False
        self.point = 0
        self.agent_pos = self.temp_map.getAgentPos()
        self.spawn = self.temp_map.getAgentPos()

    def Solving(self, pos):
        cur = self.agent_pos
        self.visited.append(cur)
        do, safe_pos = getAgentAction(cur)
        if do != 0:
            if do == 3:
                self.Pick_gold(cur, self.map[cur[0]][cur[1]])
                return (do, cur)
            elif do == 1:
                for x in safe_pos:
                    if x not in self.doing:
                        self.doing.append(x)

        next_step = None
        try:
            next_step = self.doing.pop()
        except:
            if self.climb_out == False:
                next_step = self.spawn
                self.climb_out = True

        if next_step == None:
            return 0, None

        path = Move(cur, next_step)
        if path != next_step:
            self.doing.append(next_step)
        return (self.moveset[0], path)

    def getAgentAction(self, pos):
        cur = self.map[pos[0]][pos[1]]
        if cur == 'G' or cur == 'GB' or cur == 'BG' or cur == 'GS' or cur == 'SG' or cur == 'GBS' or cur == 'GSB' or cur == 'BGS' or cur == 'BSG' or cur == 'SGB' or cur == 'SBG':
            return (self.moveset[2], None)
        
        self.Checksafe(pos)
        safe_pos = []
        k = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for i in k:
            temp = (pos[0] + i[0], pos[1] + i[1])
            if temp in self.visited or not validCell(temp[0], temp[1], (len(self.map), len(self.map[0]))):
                continue
            if self.AKB.is_pit(temp):
                continue
            elif self.AKB.is_wumpus(temp):
                self.where_e_w.append(temp)
                continue
            safe_pos.append(temp)

        if len(safe_pos) > 0:
            return (self.moveset[0], safe_pos)
        return 0, None

    def Checksafe(self, pos):
        cur = []
        B = False
        S = False
        if self.map[cur[0]][cur[1]] == 'B' or self.map[cur[0]][cur[1]] == 'SB' or self.map[cur[0]][cur[1]] == 'BS' or self.map[cur[0]][cur[1]] == 'GB' or self.map[cur[0]][cur[1]] == 'BG' or self.map[cur[0]][cur[1]] == 'GBS' or self.map[cur[0]][cur[1]] == 'GSB' or self.map[cur[0]][cur[1]] == 'SGB' or self.map[cur[0]][cur[1]] == 'SBG' or self.map[cur[0]][cur[1]] == 'BGS'  or self.map[cur[0]][cur[1]] == 'BSG':
            B = True
        if self.map[cur[0]][cur[1]] == 'S' or self.map[cur[0]][cur[1]] == 'SB' or self.map[cur[0]][cur[1]] == 'BS' or self.map[cur[0]][cur[1]] == 'GS' or self.map[cur[0]][cur[1]] == 'SG' or self.map[cur[0]][cur[1]] == 'GBS' or self.map[cur[0]][cur[1]] == 'GSB' or self.map[cur[0]][cur[1]] == 'SGB' or self.map[cur[0]][cur[1]] == 'SBG' or self.map[cur[0]][cur[1]] == 'BGS'  or self.map[cur[0]][cur[1]] == 'BSG':
            S = True
        self.AKB.newKB(cur, B, S)

    def Move(self, cur, next):
        temp = self.map.getMap()
        path = A_star(temp, cur, next)
        if len(path) >= 0:
            self.agent_pos = path[0]
            return path[0]
        return None

    def Shoot(self):
        #Chưa biết làm
        pass

    def Pick_gold(self, pos, state):
        if state == 'G':
            self.map.updateMap(pos, '-')
        elif state == 'GB' or state == 'BG':
            self.map.updateMap(pos, 'B')
        elif state == 'GS' or state == 'SG':
            self.map.updateMap(pos, 'S')
        else:
            self.map.updateMap(pos, 'GS')

    def calPoint(self):
        move, next_step = self.Solving()
        if move == 0:
            return None, None
        elif move == 1:
            self.point -= 10
        elif move == 3:
            self.point += 100
        elif move == 2:
            self.point -= 100

        return (move, next_step), self.point
