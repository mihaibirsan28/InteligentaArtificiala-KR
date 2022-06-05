from time import time
from math import sqrt, pow

from os import listdir, mkdir, path
from os.path import isfile, join, exists

# Modul debug - ignorăm timpul limită
DEBUG = False


def extract_file_name(input_file):
    """
    Extragem numele fișierului din locația lui
    input_file: Adresa fișierului
    """
    return input_file.split("/")[-1].split(".")[0]


def get_folder_files(folder):
    """
    Preluăm toate fișierele dintr-un folder specificat
    folder: Adresa folder-ului
    """
    return [f for f in listdir(folder) if isfile(join(folder, f))]


def generate_output_file(input_file, opt="out"):
    """
    Generează fișiere de output din fișierele de input date
    input_file: Locația fișierului de input
    opt: Opțiune
    """
    part = input_file.split(".")
    return part[0] + "_" + opt + "." + part[1]


def check_time_limit(start_time, timeout):
    """
    Verificare limită de timp depășită
    start_time: Timpul de început
    timeout: Limita de timp alocată
    """
    current_time = time()
    return current_time - start_time >= timeout


def calculate_distance(p1, p2=None):
    """
    Calcularea distantei dintre 2 puncte
    p1: Punctul 1 (x1, y1)
    p2: Punctul 2 (x2, y2)
    returnam float(Distanța)
    """
    if p2 is None:
        p2 = (0, 0)
    return sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))


def in_list(list, node):
    """
    Căutăm nodul curent în list dată
    list: list de noduri
    node: nodul curent
    returnam None | WalkingNode
    """
    for s in list:
        if s.info == node.info:
            return s
    return None


def insert_node(node, list):
    idx = 0
    while idx < len(list) and (node.f > list[idx].f or (node.f == list[idx].f and node.g < list[idx].g)):
      idx += 1
    list.insert(idx, node)


class Solution:

    def __init__(self, graph, i=0, solution=None, time=0, ):
        """
        i: int(id soluție)
        solution: WalkingNode(soluția calculată)
        time: int(timp - ms)

        """
        self.graph = graph
        self.i = i
        self.solution = solution
        self.time = time

    def __repr__(self):
        """
        returnam str(reprezentare soluție)
        """

        cost_left = calculate_distance((self.graph.radius, 0)) - calculate_distance(self.solution.info.pos)
        max_h = 0
        sol = self.solution
        while sol is not None:
            max_h = max(max_h, sol.h)
            sol = sol.parent

        result = f"Soluția {self.i}: \n"
        result += f"Lungime drum: {len(self.solution.get_road())}\n"
        result += f"Cost drum: {round(self.solution.g + cost_left, 2)}\n"
        result += f"Cost maxim estimat: {round(max_h, 2)}\n"
        result += f"Timp de găsire: {round(self.time * 1000)} ms\n"
        result += str(self.solution)
        result += "\n\n"
        return result