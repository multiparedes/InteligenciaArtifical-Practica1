from ia_2022 import entorn
from practica1 import joc
from practica1.entorn import AccionsRana, ClauPercepcio
from practica1.agent import Rana, Estat


class Rana(joc.Rana):
    def __init__(self, *args, **kwargs):
        super(Rana, self).__init__(*args, **kwargs)
        # Atributs de clase, definim nivell de profunditat i variable d'acabament
        self.__MAX_DEPTH = 3

    def pinta(self, display):
        pass

    def actua(self, percep: entorn.Percepcio) -> entorn.Accio | tuple[entorn.Accio, object]:
        # Obtenim el nostre nom i el del rival
        noms = list(percep[ClauPercepcio.POSICIO].keys())
        noms.remove(self.nom)

        # Si l'altre ha acabat aturam
        if percep[ClauPercepcio.POSICIO][noms[0]] == percep[ClauPercepcio.OLOR]:
            return AccionsRana.ESPERAR

         # Cream un estat i cridam a la funciÃ³ minimax
        estat = Estat(percep.to_dict(), nomMax=self.nom, percep = percep, nomMin =noms[0])
        accio = self.__minimax(estat, True, self.__MAX_DEPTH)
        # Feim l'accio
        return accio[1]

    def __minimax(self, estat, torn_max, MAX_DEPTH):
        # Evaluam si esteim a un node fulla o no.
        score = estat.evaluar(MAX_DEPTH)
        # Si retornam algo es que es una fulla
        if score is not None:
            # Sortim un nivell de recursivitat
            return score
        # Cream fills per evaluar la millor jugada de l'altre torn
        puntuacio_fills = [self.__minimax(estat_fill, not torn_max, MAX_DEPTH-1) for estat_fill in estat.generar_fills(torn_max)]
        # Minimitzam o maximitzam depenent del torn
        if torn_max:
            return self.__maximitzar(puntuacio_fills)
        else:
            return self.__minimitzar(puntuacio_fills)

    # Funcio per ordenar (menor a major) una llista i retornar el darrer
    def __maximitzar(self, puntuacio_fills):
        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[0])
        return puntuacio_fills[len(puntuacio_fills)-1]
    # Funcio per ordenar (menor a major) una llista i retornar el primer
    def __minimitzar(self, puntuacio_fills):
        puntuacio_fills = sorted(puntuacio_fills, key=lambda x: x[0])
        return puntuacio_fills[0]