import string
import sys

from util import *
from copy import deepcopy, copy


class Node:
    def __init__(self, _id: str = "", px: int = 0, py: int = 0, insects: int = 0, max_weight: int = 0):
        """
        id: str(Id nod)
        px: int(Poziția x)
        py: int(Poziția y)
        insects: int(Numărul de insecte de pe frunză)
        max_weight: int(Greutatea totală permisă)
        """
        self.id = _id
        self.pos = (px, py)
        self.insects = insects
        self.max_weight = max_weight

    def parse(self, data: str):
        """
        data: str(input)
        returneaza Nod
        """
        data = data.split(" ")
        if len(data) != 5:
            raise Exception("Date frunza invalide")
        self.id = data[0]
        self.pos = (int(data[1]), int(data[2]))
        self.insects = int(data[3])
        self.max_weight = int(data[4])
        return self


class State:
    def __init__(self, name: string ,node: Node,  weight: int, eaten_insects:int):
        """
        name: string(nume)
        node: Node(Frunza)
        weight: int(Greutatea curentă)
        eaten_insects: int(Numărul de insecte mâncate de pe frunză)
        """
        self.name = name
        self.node = node
        self.pos = node.pos
        self.weight = weight
        self.eaten_insects = eaten_insects


class WalkingNode:
    def __init__(self, id: int, info: State, parent, cost=0, h=0):
        """
        id: int(Id nod)
        info: State(Starea curentă)
        parent: WalkingNode(Nodul părinte)
        cost: int(Costul din nodul start)
        h: int(Costul estimat până într-un nod scop)
        """

        self.id = id
        self.info = info
        self.parent = parent  # parintele din arborele de parcurgere
        self.g = cost
        self.h = h
        self.f = self.g + self.h

    def get_road(self):
        """
        Funcția parcurge nodurile părinte până în rădăcină
        """
        road = [self.info]
        node = self
        while node.parent is not None:
            road.insert(0, node.parent.info)
            node = node.parent
        return road

    def show_road(self):
        """
        Afișare drum parcurs din rădăcină
        """
        print(self)

    def get_eaten_insects(self, on_node: Node):
        """
        Calculare insecte mâncate de pe o frunză, se parcurge arborele de tați
        """
        insects = 0
        current = self
        while current is not None:
            if current.info.pos == on_node.pos:
                insects += current.info.eaten_insects
            current = current.parent
        return insects

    def __repr__(self):
        """
        Reprezentare Nod
        """
        road = self.get_road()
        result = f'0) {road[0].name} se află pe frunza inițială: {road[0].node.id}({road[0].pos[0]},{road[0].pos[1]}).'
        result += f'\nGreutate {road[0].name}:{road[0].weight}'
        for i in range(len(road) - 1):
            result += f'\n{road[0].name} a mâncat {road[i + 1].eaten_insects} insecte. '
            result += f'\n{i + 1}) {road[0].name} a sărit de la {road[i].node.id}({road[i].pos[0]}, {road[i].pos[1]}) la '
            result += f'{road[i + 1].node.id}({road[i + 1].pos[0]}, {road[i + 1].pos[1]}).'
            result += f'Greutate {road[0].name}: {road[i + 1].weight}'
        result += f'\n{len(road)}) {road[0].name} a ajuns la mal în {len(road)} sărituri.'
        return result


# Graful problemei
class Graph:
    def __init__(self, file_path: str, heuristic: str = "admisibila_1"):
        """
        file_path: str(Fișier de input)
        heuristic: str(Tipul euristicii - banala | admisibila_1 | neadmisibila)
        """
        self.heuristic = heuristic
        with open(file_path, "r") as r:
            self.radius = int(r.readline())
            total_distance = calculate_distance((self.radius, 0))
            name = r.readline().replace('\n', '')
            initial_weight = int(r.readline())
            start_node = r.readline().replace('\n', '')
            line = r.readline()
            self.nodes = []
            self.start = None
            while line:
                node = Node().parse(line)
                line = r.readline()
                # Frunza curentă este în afara lacului!
                if calculate_distance(node.pos) >= total_distance:
                    continue
                self.nodes.append(node)
                if node.id == start_node:
                    self.start = State(name , node, initial_weight, 0)
            if self.start is None:
                raise Exception("Nod de start inexistent")
            if self.test_scope(self.start):
                raise Exception("Nodul de start este nod scop")
            if not self.can_continue(self.start):
                raise Exception("Starea inițială nu are soluții")

    def test_scope(self, node_info: State):
        """
        Funcția ce testează dacă nodul dat este scop
        node_info: State(starea curenta)
        """
        dist_required = calculate_distance((self.radius, 0))
        dist = dist_required - calculate_distance(node_info.pos)
        if dist > 0 and node_info.weight - 1 <= 0:
            return False
        return dist <= (node_info.weight / 3)

    def generate_successors(self, parent_node: WalkingNode, ignore_h=True):
        """
        Funcția de generare a succesorilor sub forma de noduri in arborele de parcurgere
        parent_node: WalkingNode(nodul părinte, ce urmează a fi expandat)
        ignore_h: bool(Calculăm h'?)
        """
        successors_list = []
        initial_state = parent_node.info

        if not self.can_continue(initial_state):
            return []

        for node in deepcopy(self.nodes):
            node.insects -= parent_node.get_eaten_insects(node)

            if node.pos != parent_node.info.pos:
                dist = calculate_distance(node.pos, parent_node.info.pos)

                current_state = State(initial_state.name,  node, initial_state.weight, 0)

                if dist > current_state.weight / 3:
                    continue
                if (current_state.weight - 1) > node.max_weight:
                    continue

                max_add = max(0, min(node.insects, node.max_weight - (current_state.weight - 1)))

                for eat in range(max_add + 1):
                    current_state.weight = initial_state.weight + eat - 1
                    current_state.eaten_insects = eat
                    h = 0
                    if not ignore_h:
                        h = self.calculate_h(current_state)
                    #calculam costul saltului
                    cost = calculate_distance(current_state.pos, parent_node.info.pos)
                    new_state = WalkingNode(-1, deepcopy(current_state), parent_node, parent_node.g + cost, h)
                    successors_list.append(new_state)

        return successors_list

    def can_continue(self, node_info: State):
        """
        Verificăm dacă din starea curentă se mai poate ajunge într-o stare finală
        """
        if self.test_scope(node_info):
            return True
        if node_info.weight - 1 <= 0:
            return False
        furthest_node = self.nodes[0]
        for node in self.nodes:
            if calculate_distance(node.pos) > calculate_distance(furthest_node.pos):
                furthest_node = node
        remaining_distance = calculate_distance((self.radius, 0)) - calculate_distance(furthest_node.pos)
        max_valid_gain = max([node.max_weight for node in self.nodes])
        total_gain = sum([node.insects for node in self.nodes]) + node_info.weight
        max_gain = min(max_valid_gain, total_gain)
        return remaining_distance < max_gain / 3

    def calculate_h(self, node_info: State):
        """
        Funcția de calculare h, implementată prin 4 tipuri de euristici
        node_info: State(starea curentă)
        returnam int(h' = numărul de noduri estimate până la destinație)
        """
        remaining_distance = calculate_distance((self.radius, 0)) - calculate_distance(node_info.pos)
        if self.heuristic == "banala":
            # Euristică Banala
            return remaining_distance
        elif self.heuristic == "admisibila_1":
            # Euristică admisibilă 1
            total_add_weight = sum([node.insects for node in self.nodes])
            max_valid_weight = max([node.max_weight for node in self.nodes])
            max_weight = min(max_valid_weight, total_add_weight)

            def get_next_nodes(start_node: Node, max_jump: float):
                current_dist = calculate_distance(start_node.pos)
                next_nodes = []
                for node in self.nodes:
                    dist = calculate_distance(node.pos)
                    dist_diff = calculate_distance(node.pos, start_node.pos)
                    if dist_diff <= max_jump and dist > current_dist:
                        next_nodes.append((node, dist_diff))
                return next_nodes

            def bfs(start_node: Node, max_weight: float):
                nodes_list = [(start_node, 0)]

                while len(nodes_list) > 0:
                    current_node = nodes_list.pop(0)
                    if self.test_scope(State("Broscovina", current_node[0], max_weight, 0)):
                        return current_node[1]
                    next_nodes = get_next_nodes(current_node[0], max_weight / 3)
                    for node in next_nodes:
                        if node not in nodes_list:
                            nodes_list.append((node[0], node[1] + current_node[1]))
                return sys.maxsize

            return bfs(node_info.node, max_weight)
        elif self.heuristic == "neadmisibila":
            # Euristică neadmisibilă
            h = calculate_distance(self.start.pos, self.nodes[0].pos)
            for i in range(1, len(self.nodes)):
                if self.nodes[i].id != self.start.node.id and remaining_distance < calculate_distance(
                        (self.radius, 0)) - calculate_distance(self.nodes[i].pos):
                    h += calculate_distance(self.nodes[i - 1].pos, self.nodes[i].pos)
            return h

    def __repr__(self):
        """
        Funcția de reprezentare a grafului
        """
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir