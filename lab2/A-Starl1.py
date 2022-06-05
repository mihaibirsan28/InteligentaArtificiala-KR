INF = 1 << 31


class Nod:
    def __init__(self, info, h=INF):
        self.info = info
        self.h = h

    def __repr__(self):
        return f'({self.info}, h={self.h})'


class NodParcurgere:
    def __init__(self, nod, parinte, g, f):
        self.nod = nod
        self.parinte = parinte
        self.g = g
        self.f = f

    def __repr__(self):
        if self.parinte is not None:
            p = self.parinte.nod.info
        else:
            p = None
        return f'({self.nod}, parinte={p}, g={self.g}, f={self.f})'

    def ciclu(self, elem):
        x = self.parinte
        while x is not None:
            if x.nod == elem.nod:
                return True
            x = x.parinte
        return False

    def expandeaza(self, la, l_open, l_closed):
        for muchie in la[self.nod]:  # muchie -> (nod, cost)
            np = NodParcurgere(muchie[0], self, muchie[1] + self.g, muchie[1] + self.g + muchie[0].h)
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

    def drum(self):
        x = self
        D = []
        I = []
        while x is not None:
            D.append(x)
            I.append(x.nod.info)
            x = x.parinte
        return I[::-1], D[::-1], self.f

    def test_scop(self, nod_s):
        for n in nod_s:
            if self.nod == n:
                return True
        return False


def cmp(o):
    return o.f, -o.g


def in_lista(l, elem):
    for x in l:
        if x.nod == elem.nod:
            return x
    return -1


def rezolva(la, start, n_scop):
    l_closed = []
    n1 = NodParcurgere(start, None, 0, INF)
    l_open = [n1]
    while len(l_open) > 0:
        nod_curent = l_open[0]
        l_open.remove(nod_curent)
        l_closed.append(nod_curent)
        if nod_curent.test_scop(n_scop):
            (I, D, c) = nod_curent.drum()
            print(f'Drumul de cost minim: {I}\n{D}\nCostul minim: {c}')
        (l_open, l_closed) = nod_curent.expandeaza(la, l_open, l_closed)


if __name__ == '__main__':
    noduri = {}
    noduri_scop = []
    la = {}  # lista de adiacenta de tip la[n1] = [(n2, cost)]
    with open("lab2_in.in") as f:
        date = f.read().splitlines()
        n = int(date[0])
        for line in date[1: n + 1]:
            (index, val) = line.split()
            nod = Nod(index, int(val))
            la[nod] = []
            noduri[index] = nod
        nod_start = noduri[date[n + 1]]
        for nod in date[n + 2].split():
            noduri_scop.append(noduri[nod])
        m = int(date[n + 3])
        for muchie in date[n + 4: m + n + 4]:
            muchie = muchie.split()
            la[noduri[muchie[0]]].append((noduri[muchie[1]], int(muchie[2])))
    rezolva(la, nod_start, noduri_scop)
