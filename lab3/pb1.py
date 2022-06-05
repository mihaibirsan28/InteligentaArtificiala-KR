from copy import deepcopy

INF = 1 << 31


class Nod:
    def __init__(self, info, h=INF):
        self.info = info
        self.h = h

    def __repr__(self):
        return str(self.info)

    def calculeaza_h(self):  # calculeaza h pentru un nod
        nc = self.info
        ns = nod_scop.info
        h = 0
        for stiva in range(n):
            for i in range(len(nc[stiva])):
                if i >= len(ns[stiva]) or ns[stiva][i] != nc[stiva][i]:
                    h += 1
        self.h = h

    def mutare(self, s1, s2): #realizeaza o mutare; muta elem din vf stivei s1 in vf stivei s2
        m = deepcopy(self.info)
        e = m[s1].pop()
        m[s2].append(e)
        return m

    def succesor(self):  # returneaza lista succesorilor unui nod
        l_succ = []
        for stiva1 in range(n):
            for stiva2 in range(n):
                if stiva1 != stiva2 and len(self.info[stiva1]) != 0:
                    x = Nod(self.mutare(stiva1, stiva2))
                    x.calculeaza_h()
                    l_succ.append(x)
        return l_succ


class NodParcurgere:
    def __init__(self, nod, parinte, g, f):
        self.nod = nod
        self.parinte = parinte
        self.g = g
        self.f = f

    def __repr__(self):
        return f'{self.nod}'

    def ciclu(self, elem):  # verifica daca alegant elem, se formeaza cicluri
        x = self.parinte
        while x is not None:
            if x.nod == elem.nod:
                return True
            x = x.parinte
        return False

    def expandeaza(self, l_open, l_closed):  # expandeaza un nod
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

    def drum(self):  # reconstruieste drumul de la starea final la cea initiala
        x = self
        D = []
        while x is not None:
            D.append(x)
            x = x.parinte
        return D[::-1], self.f

    def test_scop(self):  # verifica daca configuratia curenta este finala
        nc = self.nod.info
        ns = nod_scop.info
        for i in range(n):
            for j in range(len(nc[i])):
                if len(nc[i]) != len(ns[i]):
                    return False
                if nc[i][j] != ns[i][j]:
                    return False
        return True


def cmp(o):  # cmp pentru lista open
    return o.f, -o.g


def in_lista(l, elem):  # verifica daca elem este in lista l si il returneaza in caz afirmativ
    for x in l:
        if x.nod == elem.nod:
            return x
    return -1


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
            print(*D, sep='\n')
            break
        (l_open, l_closed) = nod_curent.expandeaza(l_open, l_closed)


if __name__ == '__main__':
    with open("date1.in") as f:
        date = f.read().splitlines()
        (n, m) = date[0].split()
        n = int(n)
        m = int(m)
        s = [[] for _ in range(n)]
        for i in range(1, n + 1):
            stiva = date[i].split()
            for cub in stiva:
                s[i - 1].append(cub)
        nod_start = Nod(s)
        s = [[] for _ in range(n)]
        for i in range(n + 1, 2 * n + 1):
            stiva = date[i].split()
            for cub in stiva:
                s[i - n - 1].append(cub)
        nod_scop = Nod(s)
        nod_start.calculeaza_h()
        rezolva(nod_start)
