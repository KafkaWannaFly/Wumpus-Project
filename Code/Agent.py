import numpy as np
import itertools
import sys
from heapq import heappush, heappop
from pysat.solvers import Glucose3

from Code.AppData import MapData


class Map:
    def __init__(self):
        map, agent_pos = readFile()
        self.map = map
        self.a_p = agent_pos
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
    file = open(MapData.path, "r")
    size = file.readline()
    size = int(size.split()[0])

    map = []
    for i in range(size):
        line = file.readline().replace('\n', '')
        map.append(line.split('.'))

    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 'A':
                agent_pos = (i, j)
                break

    return map, agent_pos


def add_adjacent(matrix, width, height):
    dict = {}
    k = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    for i in range(height):
        for j in range(width):
            temp = []
            for x in k:
                tmp_pos = (i + x[0], j + x[1])
                if validCell(tmp_pos[0], tmp_pos[1], (width, height)):
                    temp.append(tmp_pos)
            dict[(i, j)] = temp
    return dict


def common_adj(pos_1, pos_2, width, height, visited):
    k = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    temp1 = []
    for x in k:
        tmp_pos = (pos_1[0] + x[0], pos_1[1] + x[1])
        if validCell(tmp_pos[0], tmp_pos[1], (width, height)):
            temp1.append(tmp_pos)
    temp2 = []
    for x in k:
        tmp_pos = (pos_2[0] + x[0], pos_2[1] + x[1])
        if validCell(tmp_pos[0], tmp_pos[1], (width, height)):
            temp2.append(tmp_pos)

    for i in temp1:
        for j in temp2:
            if i == j and i not in visited:
                return True, i

    return False, None


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


def A_star(maze, cur_pos, des_pos, danger_pos):
    frontier = []
    explored = []
    parent_nodes = {}
    cost = 0
    adjacent_nodes = add_adjacent(maze, len(maze), len(maze[0]))

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
                if (current_node == explored_node):
                    is_explored = True
                    break

            if danger_pos != None:
                if current_node in danger_pos:
                    continue

            if is_explored:
                continue

            explored.append(current_node)

            if current_node == des_pos:
                final_path = backtracking(current_node, parent_nodes)
                final_path.pop()
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

    def is_pit(self, pos, list_wumpus):
        if pos in list_wumpus:
            return False
        else:
            return self.pit.solve([self.pos_to_num(pos, 0, 1)])

    def makeFormula(self):
        k = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                cur = self.pos_to_num((i, j), 0, -1)
                for x in k:
                    temp = (i + x[0], j + x[1])
                    if validCell(temp[0], temp[1], self.size):
                        temp2 = self.pos_to_num((temp[0], temp[1]), 1, 1)
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

    def Remove(self, list):
        wumpus = list.pop()
        self.DangerFormula.append([self.pos_to_num(wumpus, 0, -1)])

        for i in list:
            stench = self.pos_to_num(i, 1, 1)
            if stench in self.DangerFormula:
                self.DangerFormula.remove([stench])
            self.DangerFormula.append(-1 * stench)

        self.wumpus.delete()
        self.wumpus.append_formula(self.DangerFormula)

    def pos_to_num(self, pos, is_stench, s):
        return int(s * (pos[1] * self.size[0] + pos[0] + 1 + is_stench * self.size[0] * self.size[1]))


class Agent:
    def __init__(self):
        self.temp_map = Map()
        self.map = self.temp_map.getMap()
        self.moveset = [1, 2, 3, 4]  # 1 move, 2 shoot, 3 pick, 4 climb out
        self.AKB = Knowlegdesbase((len(self.map), len(self.map[0])))
        self.AKB.makeFormula()
        self.visited = []
        self.doing = []
        self.list_stench = []
        self.wumpus_pos = []
        self.climb_out = False
        self.point = 0
        self.agent_pos = self.temp_map.getAgentPos()
        self.spawn = self.temp_map.getAgentPos()

    def Solving(self):
        cur = self.agent_pos
        self.visited.append(cur)
        do, safe_pos, danger_pos = self.getAgentAction(cur)
        if do != 0:
            if do == 3:
                self.Pick_gold(cur, self.map[cur[0]][cur[1]])
                return (do, cur)
            elif do == 1:
                for x in safe_pos:
                    if x not in self.doing:
                        self.doing.append(x)
            elif do == 2:
                wumpus = safe_pos.pop()
                self.wumpus_pos.append(wumpus)
                self.Shoot(wumpus, self.map[wumpus[0]][wumpus[1]])
                self.AKB.Remove(danger_pos)
                print(self.AKB.is_pit(wumpus, self.wumpus_pos))
                return (do, wumpus)

        next_step = None
        try:
            next_step = self.doing.pop()
        except:
            if self.climb_out == False:
                next_step = self.spawn
                self.climb_out = True

        if next_step == None:
            return 0, None

        path = self.Move(cur, next_step, danger_pos)
        if path != next_step:
            self.doing.append(next_step)
        return (self.moveset[0], path)

    def getAgentAction(self, pos):
        cur = self.map[pos[0]][pos[1]]
        if cur == 'G' or cur == 'GB' or cur == 'BG' or cur == 'GS' or cur == 'SG' or cur == 'GBS' or cur == 'GSB' or cur == 'BGS' or cur == 'BSG' or cur == 'SGB' or cur == 'SBG':
            return (self.moveset[2], None, None)

        self.Checksafe(pos)

        if cur == 'S' or cur == 'SB' or cur == 'BS' or cur == 'GS' or cur == 'SG' or cur == 'GBS' or cur == 'GSB' or cur == 'BGS' or cur == 'BSG' or cur == 'SGB' or cur == 'SBG':
            if len(self.list_stench) > 1:
                for w in self.list_stench:
                    check, wumpus_pos = common_adj(pos, w, len(self.map[0]), len(self.map), self.visited)
                    if check == True:
                        list_need_to_del = [wumpus_pos, pos, w]
                        return (self.moveset[1], [wumpus_pos], list_need_to_del)

        safe_pos = []
        danger_pos = []
        k = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for i in k:
            temp = (pos[0] + i[0], pos[1] + i[1])
            if temp in self.visited or not validCell(temp[0], temp[1], (len(self.map), len(self.map[0]))):
                continue
            if self.AKB.is_pit(temp, self.wumpus_pos):
                danger_pos.append(temp)
                continue
            elif self.AKB.is_wumpus(temp):
                danger_pos.append(temp)
                continue
            safe_pos.append(temp)

        if len(safe_pos) > 0 and len(danger_pos) > 0:
            return (self.moveset[0], safe_pos, danger_pos)
        elif len(safe_pos) > 0:
            return (self.moveset[0], safe_pos, None)
        elif len(danger_pos) > 0:
            return (0, None, danger_pos)
        else:
            return 0, None, None

    def createAgent(self):
        return self.agent_pos, self.point

    def Checksafe(self, pos):
        cur = pos
        B = False
        S = False
        if self.map[cur[0]][cur[1]] == 'B' or self.map[cur[0]][cur[1]] == 'SB' or self.map[cur[0]][cur[1]] == 'BS' or \
                self.map[cur[0]][cur[1]] == 'GB' or self.map[cur[0]][cur[1]] == 'BG' or self.map[cur[0]][
            cur[1]] == 'GBS' or self.map[cur[0]][cur[1]] == 'GSB' or self.map[cur[0]][cur[1]] == 'SGB' or \
                self.map[cur[0]][cur[1]] == 'SBG' or self.map[cur[0]][cur[1]] == 'BGS' or self.map[cur[0]][
            cur[1]] == 'BSG':
            B = True
        if self.map[cur[0]][cur[1]] == 'S' or self.map[cur[0]][cur[1]] == 'SB' or self.map[cur[0]][cur[1]] == 'BS' or \
                self.map[cur[0]][cur[1]] == 'GS' or self.map[cur[0]][cur[1]] == 'SG' or self.map[cur[0]][
            cur[1]] == 'GBS' or self.map[cur[0]][cur[1]] == 'GSB' or self.map[cur[0]][cur[1]] == 'SGB' or \
                self.map[cur[0]][cur[1]] == 'SBG' or self.map[cur[0]][cur[1]] == 'BGS' or self.map[cur[0]][
            cur[1]] == 'BSG':
            S = True
            if cur not in self.list_stench:
                self.list_stench.append(cur)

        self.AKB.newKB(cur, B, S)

    def Move(self, cur, next, danger_pos):
        temp = self.map
        path = A_star(temp, cur, next, danger_pos)
        if len(path) >= 0:
            self.agent_pos = path[0]
            return path[0]
        return None

    def Shoot(self, pos, state):
        x = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        if state == 'W':
            self.temp_map.updateMap(pos, '-')
            for k in x:
                if validCell(pos[0] + k[0], pos[1] + k[1], (len(self.map), len(self.map[0]))):
                    if self.map[pos[0] + k[0]][pos[1] + k[1]] == 'S':
                        self.temp_map.updateMap((pos[0] + k[0], pos[1] + k[1]), '-')
                    elif self.map[pos[0] + k[0]][pos[1] + k[1]] == 'BS' or self.map[pos[0] + k[0]][
                        pos[1] + k[1]] == 'SB':
                        self.temp_map.updateMap((pos[0] + k[0], pos[1] + k[1]), 'B')
                    elif self.map[pos[0] + k[0]][pos[1] + k[1]] == 'GS' or self.map[pos[0] + k[0]][
                        pos[1] + k[1]] == 'SG':
                        self.temp_map.updateMap((pos[0] + k[0], pos[1] + k[1]), 'G')
                    else:
                        self.temp_map.updateMap((pos[0] + k[0], pos[1] + k[1]), 'GB')
                    if (pos[0] + k[0], pos[1] + k[1]) in self.list_stench:
                        self.list_stench.remove((pos[0] + k[0], pos[1] + k[1]))
                else:
                    continue
        else:
            pass

    def Pick_gold(self, pos, state):
        if state == 'G':
            self.temp_map.updateMap(pos, '-')
        elif state == 'GB' or state == 'BG':
            self.temp_map.updateMap(pos, 'B')
        elif state == 'GS' or state == 'SG':
            self.temp_map.updateMap(pos, 'S')
        else:
            self.temp_map.updateMap(pos, 'BS')

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
