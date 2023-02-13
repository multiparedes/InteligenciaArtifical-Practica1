from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import AccionsRana, ClauPercepcio
from practica1.agent import Rana, Estat

from queue import PriorityQueue
import time

class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        self.__oberts = None
        self.__tancats = None
        self.__accions = None

    def pinta(self, display):
        pass

    def actua(self, percep: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Guardam l'estat inicial
        estat = Estat(info=percep.to_dict(), nomMax = self.nom, percep = percep, pes=0)


        # Cridam a cerca nomes per a la primera iteracio
        if self.__accions is None:
            self._cerca(estat=estat)

        # Retornam les accions en ordre
        while len(self.__accions) > 0:
            accio = self.__accions.pop()
            # Si ens retorna un bot esperam dos torns
            if accio[0] == AccionsRana.BOTAR:
                espera = tuple([AccionsRana.ESPERAR])
                self.__accions.append(espera)
                self.__accions.append(espera)
            return accio
        # Quan no quedin mes accions tancam el joc
        exit(0)

    def _cerca(self, estat: Estat):
        self.__oberts = PriorityQueue()
        self.__tancats = set()

        self.__oberts.put((estat.calc_heuristica(), estat))
        actual = None
        while not self.__oberts.empty():
            actual = self.__oberts.get()[1]

            if actual in self.__tancats:
                continue

            if actual.es_meta():
                break

            estats_fills = actual.generar_fills()

            for eFill in estats_fills:
                self.__oberts.put((eFill.calc_heuristica(), eFill))

            self.__tancats.add(actual)

        if actual.es_meta():
            accions = []
            iterador = actual
            # Afegim un espera extra per veure que arriba a la pizza
            accions.append(tuple([AccionsRana.ESPERAR]))
            # Recorrem la llista d'accions i les guardam
            while iterador.pare is not None:
                pare, accio = iterador.pare
                accions.append(accio)
                iterador = pare
            # Assignam les accions a la clase
            self.__accions = accions