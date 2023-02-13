import copy
from itertools import product

from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)

    def pinta(self, display):
        pass

    def actua(
            self, percep: entorn.Percepcio
    ) -> entorn.Accio | tuple[entorn.Accio, object]:
        pass


class Estat:
    def __init__(self, info: dict, nomMax, percep, nomMin=None, pes=0, pare=None):
        self.__info = info
        self.__pes = pes
        self.__pare = pare
        self.__nomMax = nomMax
        self.__nomMin = nomMin
        self.__cordMax = percep[ClauPercepcio.POSICIO][nomMax]
        if nomMin is not None:
            self.__cordMin = percep[ClauPercepcio.POSICIO][nomMin]

    # Diccionari emprat per a calcular posicions i pesos
    UTILITATS = {
        Direccio.BAIX: (0, 1),
        Direccio.DRETA: (1, 0),
        Direccio.DALT: (0, -1),
        Direccio.ESQUERRE: (-1, 0),
        AccionsRana.BOTAR: 6,
        AccionsRana.MOURE: 1
    }

    # Sobreescribim funcions defaults
    def __hash__(self):
        return hash(self.__pare)

    def __getitem__(self, key):
        return self.__info[key]

    def __setitem__(self, key, value):
        self.__info[key] = value

    def __eq__(self, other):
        return self.__cordMax == other.__cordMax

    def __lt__(self, other):
        return True

    # La granota esta damunt la pizza
    def es_meta(self) -> bool:
        return self[ClauPercepcio.OLOR] == self.__cordMax

    # La posició pasada per parametre no es una paret, no esta damunt una altre granota i esta dins el tauler.
    def es_possible(self, torn_max=True) -> bool:
        # Si estam a estrella o minimax no se poden trepitjar, sempre estarà a fals
        cords = self.__cordMax
        if not torn_max:
            cords = self.__cordMin
        setrepitjen = False
        # Si no hi ha min nomes tenim un jugador, per lo tant no se trepitjen
        if self.__nomMin is not None:
            if self.__cordMax == self.__cordMin:
                setrepitjen = True
        if not setrepitjen:
            # Miram els altres casos
            if cords not in self[ClauPercepcio.PARETS]:
                if 0 <= cords[0] < self[ClauPercepcio.MIDA_TAULELL][0]:
                    if 0 <= cords[1] < self[ClauPercepcio.MIDA_TAULELL][1]:
                        return True
        return False

    # Genera tots els possibles filles a partir del nostre estat actual.
    def generar_fills(self, torn_max=True) -> list:
        l_accions = [AccionsRana.MOURE, AccionsRana.BOTAR]
        l_direccions = [Direccio.BAIX, Direccio.DALT, Direccio.DRETA, Direccio.ESQUERRE]
        # Llista de fills a retornar
        fills = list()
        # Feim el producte cartesia de les accions
        for accio in product(l_accions, l_direccions):
            possible_fill = copy.deepcopy(self)
            possible_fill.__pare = (self, accio)
            # Suposam que som MAX
            cords = possible_fill.__cordMax
            # Si som min actualitzam les cords
            if not torn_max:
                cords = possible_fill.__cordMin
            # Obtenim les noves coordenades
            if accio[0] == AccionsRana.BOTAR:
                cords = tuple(map(sum, zip(self.UTILITATS.get(accio[1]), self.UTILITATS.get(accio[1]), cords)))
                self.__pes = self.__pes + 6;
            else:
                cords = tuple(map(sum, zip(self.UTILITATS.get(accio[1]), cords)))
                self.__pes = self.__pes + 2;
            # Assignam al nou fill les coordenades actualitzades.
            if torn_max:
                possible_fill.__cordMax = cords
            else:
                possible_fill.__cordMin = cords
            # Si es un fill valid l'afegim, sino el descartam
            if possible_fill.es_possible(torn_max):
                fills.append(possible_fill)
        return fills

    # Per l'heurística emprarem la distància de Manhattan.
    def calc_heuristica(self) -> int:
        heur = (abs(self.__cordMax[0] - self[ClauPercepcio.OLOR][0]) + abs(
            self.__cordMax[1] - self[ClauPercepcio.OLOR][1])) + self.__pes
        return heur

    # Funcio d'avaluacio de les branques filles
    def evaluar(self, MAX_DEPTH) -> int:
        # Calculam les distancies dels dos jugadors a la pizza
        distanciaMax = abs(self.__cordMax[0] - self[ClauPercepcio.OLOR][0]) + abs(
            self.__cordMax[1] - self[ClauPercepcio.OLOR][1])
        distanciaMin = abs(self.__cordMin[0] - self[ClauPercepcio.OLOR][0]) + abs(
            self.__cordMin[1] - self[ClauPercepcio.OLOR][1])

        # Treim la primera acció que ens ha fet arribar fins aquest estat fill
        if self.es_meta() or MAX_DEPTH == 0:
            iterador = self
            accio = tuple([AccionsRana.ESPERAR])
            while iterador.pare is not None:
                pare, accio = iterador.pare
                iterador = pare
            return (distanciaMin - distanciaMax, accio)

    # Definim getter i setter de pare
    @property
    def pare(self):
        return self.__pare

    @pare.setter
    def pare(self, value):
        self.__pare = value