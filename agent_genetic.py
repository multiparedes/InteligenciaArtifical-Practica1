from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import AccionsRana, ClauPercepcio, Direccio
from practica1.agent import Rana
from itertools import product
import random
import time

class Rana(joc.Rana):

    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        # Conjunt d'accions.
        self.__accions = None
        self.__MAX_LONG = 5
        self.__NUM_INV = 20
        self.__SEL_ELITE = 10
        self.__llista_individus = []
        self.__primer = True
        self.__PROB_MUT = 10

    UTILITATS = {
        Direccio.BAIX: (0, 1),
        Direccio.DRETA: (1, 0),
        Direccio.DALT: (0, -1),
        Direccio.ESQUERRE: (-1, 0),
    }

    def pinta(self, display):
        pass

    def actua(self, percep: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        tinici = time.time()

        # Feim la cerca de manera recursiva fins obtenir un fill valid
        if self.__accions is None:
            self._cerca(percep[ClauPercepcio.POSICIO][self.nom], percep[ClauPercepcio.OLOR], percep)
            self.__accions.append(tuple([AccionsRana.ESPERAR]))
            self.__accions = self.__accions[::-1]
            print("--- %s seconds ---" % (time.time() - tinici))

        # Retornam les accions tenint en compte els bots
        while len(self.__accions) > 0:
            accio = self.__accions.pop()

            if accio[0] == AccionsRana.BOTAR:
                espera = tuple([AccionsRana.ESPERAR])
                self.__accions.append(espera)
                self.__accions.append(espera)
            return accio

        # Quan no queden accions tancam el programa
        exit()

    def _cerca(self, cord_inicial: tuple[int, int], cord_meta: tuple[int, int], percep, offspring = None):
            # Cream X individus a la vegada
            for n_individu in range(self.__NUM_INV):
                # Llista d'accions associada a cada individud
                cords = cord_inicial

                if self.__primer:
                    ll_accions = list()
                    num_accions = random.randint(1, self.__MAX_LONG)
                    # Producte de les accions possibles amb la seva direccio
                    accions = self.__accions_possibles()

                    # Generam les Y accions de manera aleatoria
                    for _ in range(num_accions):
                        ll_accions.append(accions[random.randrange(len(accions))])
                else:
                    # Si ja tenim individus d'altres generacions reasignam la llista d'accions
                    ll_accions = offspring[n_individu]

                # Calculam les possicions i miram si son camins valids
                ll_accions, cords, esMeta = self.__corregir_cami(ll_accions, cords, percep[ClauPercepcio.PARETS], percep[ClauPercepcio.MIDA_TAULELL], cord_meta)

                # Si conte com a minim una accio l'afegim a la llista per a crear nous individus
                if len(ll_accions) > 0:
                    self.__llista_individus.append((self.__calc_fitness(cords, cord_meta, ll_accions), ll_accions, esMeta))

            # Ordenam de menor a major per la puntuacio de fitness
            self.__llista_individus = sorted(self.__llista_individus, key=lambda x: x[0])

            # Si abans de fer els creuaments tenim una solucio sortim
            for invi in range(len(self.__llista_individus)):
                # Cercam la primea solucio
                if self.__llista_individus[invi][2]:
                    self.__accions = self.__llista_individus[invi][1]
                    # SORTIM DEL METODE
                    return None

            # Selccionam els K millors
            self.__llista_individus = self.__llista_individus[:self.__SEL_ELITE]

            # Feim els creuaments
            offspring = self.__creuaments(self.__llista_individus)
            self.__NUM_INV = len(offspring)
            # Repetim el proces de manera recrusiva
            self._cerca(cord_inicial, cord_meta, percep, offspring)

    def __creuaments(self, ll_individus) -> list:
        offspring = list()
        mitat = int(len(ll_individus) / 2)
        for i in range(mitat):
            xap = random.randint(1, self.__mes_curt(ll_individus[i][1],ll_individus[mitat + i][1]))
            # Realitzam els xaps als individus
            part11 = ll_individus[i][1][:xap]
            part12 = ll_individus[i][1][xap:]
            part21 = ll_individus[mitat + i][1][:xap]
            part22 = ll_individus[mitat + i][1][xap:]

            # Cream els nous fills (Nomes accions)
            fill1 = part11 + part21
            fill2 = part12 + part22

            # Quan mutam canviam una accio aleatoria del fill 1
            accions = self.__accions_possibles()
            if random.randrange(self.__PROB_MUT) == 0:
                fill1[random.randrange(len(fill1))] = accions[random.randrange(len(accions))]

            # Afegim els fills dins la llista d'offsprings
            offspring.append(fill1)
            offspring.append(fill2)
        if self.__primer:
            self.__primer = False
        return offspring

    # Metode que donat un conjut d'accions i una posicio inicial et retorna quina part del cami es valid
    def __corregir_cami(self, ll_accions, cords, parets, mida_taulell, meta):
        esMeta = False
        for idx in range(len(ll_accions)):
            possible_accio = ll_accions[idx]
            # Guardam la posicio previa per si l'accio actual es invalida
            cords_anteriors = cords
            # Calculam la nova posicio
            if possible_accio[0] == AccionsRana.BOTAR:
                cords = tuple(map(sum, zip(self.UTILITATS.get(possible_accio[1]), self.UTILITATS.get(possible_accio[1]), cords)))
            else:
                cords = tuple(map(sum, zip(self.UTILITATS.get(possible_accio[1]), cords)))
            # Miram si la nova posicio es valida
            if not self.__es_valid(cords, parets, mida_taulell):
                # Eliminam la resta d'accions
                ll_accions = ll_accions[:idx]
                # Actualitzam les coordenades
                cords = cords_anteriors
                break
            # Si es troba damunt la pizza marcam el fill com valid
            if self.__es_meta(cords, meta):
                # Eliminam la resta d'accions
                ll_accions = ll_accions[:idx+1]
                esMeta = True
                break
        # Retornam tant la llista modificada com la nova posicio final
        return ll_accions, cords, esMeta

    # Funcio de fitness. dist. manhattan o dist. manhattan + pes al num d'accions
    def __calc_fitness(self, cords: tuple[int, int], meta: tuple[int, int], ll_accions):
        fit = round(abs(cords[0] - meta[0]) + abs(cords[1] - meta[1])*0.8 + len(ll_accions)*0.2, 1)
        return fit

    def __es_valid(self, cords, parets, mida_taulell) -> bool:
        # Checkeam cordenada X, Y i si no es troba damunt una paret.
        if cords not in parets:
            if 0 <= cords[0] < mida_taulell[0]:
                if 0 <= cords[1] < mida_taulell[1]:
                    return True
        return False

    # Metode que retorna si una poscio es la meta
    def __es_meta(self, cords, meta):
        return cords == meta

    # Producte de totes les acions possibles amb la seva direcció corresponent
    def __accions_possibles(self) -> list:
        l_accions = [AccionsRana.MOURE, AccionsRana.BOTAR]
        l_direccions = [Direccio.BAIX, Direccio.DALT, Direccio.DRETA, Direccio.ESQUERRE]
        accions = list(product(l_accions, l_direccions))
        return accions

    # Trona la llargaria de la llista mes curta
    def __mes_curt(self, ind1: list, ind2: list) -> int:
        if len(ind1) > len(ind2):
            return len(ind2)
        else:
            return len(ind1)