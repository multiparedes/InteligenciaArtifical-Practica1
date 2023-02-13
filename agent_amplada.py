from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import AccionsRana, ClauPercepcio
from practica1.agent import Rana, Estat

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
        estat = Estat(info=percep.to_dict(), nomMax = self.nom, percep = percep, pes=0)

        if self.__accions is None:
            self._cerca(estat=estat)

        while len(self.__accions) > 0:
            accio = self.__accions.pop()

            if accio[0] == AccionsRana.BOTAR:
                espera = tuple([AccionsRana.ESPERAR])
                self.__accions.append(espera)
                self.__accions.append(espera)
            return accio
        exit(0)

    def _cerca(self, estat: Estat):
        self.__oberts = []
        self.__tancats = set()

        self.__oberts.append(estat)
        actual = None
        while len(self.__oberts) > 0:
            # Eliminam l'estat actual de oberts
            actual = self.__oberts[0]
            self.__oberts = self.__oberts[1:]

            # Evitam bucels
            if actual in self.__tancats:
                continue

            if actual.es_meta():
                break

            estats_fills = actual.generar_fills()

            # Afegim els es fills a oberts
            for eFill in estats_fills:
                self.__oberts.append(eFill)

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