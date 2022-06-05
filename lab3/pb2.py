from copy import deepcopy
INF = 1 << 31

class Nod:
    def __init__(self, info, h=INF):
        self.info = info
        self.h = h

    def __repr__(self):
        s = ''
        for x in range(3):
            for y in range(3):
                s += str(self.info[x][y])
                s += ' '
            s += '\n'
        return s

    def calculeaza_h(self): #calculeaza h pentru un nod
        h = 0
        for x in range(3):
            for y in range(3):
                if self.info[x][y] != 0:
                    p = pozitie(self.info[x][y])
                    h += abs(p[0] - x) + abs(p[1] - y)
        self.h = h

    def zero(self): # returneaza pozitia lui 0 in matrice
        for x in range(3):
            for y in range(3):
                if self.info[x][y] == 0:
                    return x, y

    def mutare(self, xz, yz, x, y): # o mutare in puzzle
        m = deepcopy(self.info)
        m[xz][yz], m[x][y] = m[x][y], m[xz][yz]
        return m

    def succesor(self): # returneaza lista succesorilor unui nod
        l_succ = []
        (x, y) = self.zero()
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        for k in range(4):
            xx = x + dx[k]
            yy = y + dy[k]
            if nu_iese(xx, yy):
                mat = self.mutare(x, y, xx, yy)
                n = Nod(mat)
                n.calculeaza_h()
                l_succ.append(n)
        return l_succ


class NodParcurgere:
    def __init__(self, nod, parinte, g, f):
        self.nod = nod
        self.parinte = parinte
        self.g = g
        self.f = f

    def __repr__(self):
        return f'{self.nod}'

    def ciclu(self, elem): # verifica daca alegant elem, se formeaza cicluri
        x = self.parinte
        while x is not None:
            if x.nod == elem.nod:
                return True
            x = x.parinte
        return False

    def expandeaza(self, l_open, l_closed): #expandeaza un nod
        succesori = self.nod.succesor()
        for succ in succesori:
            np = NodParcurgere(succ, self, 1 + self.g, 1 + self.g + succ.h)
            if not self.ciclu(np):
                nod_lista_c = in_lista(l_closed, np)
                if nod_lista_c != -1 and (np.f < nod_lista_c.f or (np.f == nod_lista_c.f and np.g > nod_lista_c.g)):
                    l_closed.remove(nod_lista_c)
                    l_open.append(np)
                nod_lista_o = in_lista(l_open, np)
                if nod_lista_o == -1:
                    l_open.append(np)
                elif np.f < nod_lista_o.f or (np.f == nod_lista_o.f and np.g > nod_lista_o.g):
                    l_open.remove(nod_lista_o)
                    l_open.append(np)
        l_open.sort(key=cmp)
        return l_open, l_closed

    def drum(self): #reconstruieste drumul de la starea final la cea initiala
        x = self
        D = []
        while x is not None:
            D.append(x)
            x = x.parinte
        return D[::-1], self.f

    def test_scop(self): #verifica daca configuratia curenta este finala
        i = 1
        for linie in self.nod.info:
            for e in linie:
                if i == 9:
                    return True
                if e != i:
                    return False
                i += 1
        return True


def are_solutie(m): # daca configuratia are un nr par de inversiuni este rezolvabil, astfel nu
    l = []
    for linie in m:
        for elem in linie:
                l.append(elem)
    inv = 0
    for i in range(8):
        for j in range(i + 1, 9):
            if l[i] and l[j] and l[i] > l[j]: # inversiune
                inv += 1
    if inv % 2 == 0:
        return True
    return False

def cmp(o): #cmp pentru lista open
    return o.f, -o.g


def pozitie(x):  # pentru x -> pozitia unde ar trebui sa se afle in starea finala
    return (x - 1) // 3, (x - 1) % 3


def in_lista(l, elem): #verifica daca elem este in lista l si il returneaza in caz afirmativ
    for x in l:
        if x.nod == elem.nod:
            return x
    return -1


def nu_iese(x, y): #verifica daca pozitia (x, y) este in matrice
    if -1 < x < 3 and -1 < y < 3:
        return True
    return False


def rezolva(start):
    l_closed = []
    n1 = NodParcurgere(start, None, 0, INF)
    l_open = [n1]
    while len(l_open) > 0:
        nod_curent = l_open[0]
        l_open.remove(nod_curent)
        l_closed.append(nod_curent)
        if nod_curent.test_scop():
            (D, c) = nod_curent.drum()
            print(f'Numarul minim de mutari: {c}\n')
            print("Pasii rezolvarii jocului: ")
            print(*D, sep='-----\n')
            break
        (l_open, l_closed) = nod_curent.expandeaza(l_open, l_closed)


if __name__ == '__main__':
    with open("date2.in") as f:
        date = f.read().splitlines()
        (a11, a12, a13) = date[0].split()
        (a21, a22, a23) = date[1].split()
        (a31, a32, a33) = date[2].split()
        i = [[int(a11), int(a12), int(a13)], [int(a21), int(a22), int(a23)], [int(a31), int(a32), int(a33)]]
        nod_start = Nod(i)
        nod_start.calculeaza_h()
        if are_solutie(i):
            rezolva(nod_start)
        else:
            print("Puzzle-ul dat nu are solutie.")
