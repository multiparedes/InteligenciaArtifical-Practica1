import sys
sys.path.append('C:\\Users\\Silvia\\Documents\\Escola\\3rCarrera\\IA\\ia')
sys.path.append('C:\\Users\\marti\\Documents\\UIB\\IA\\InteligenciaArtificial-main')

from practica1 import agent, joc, agent_amplada, agent_aestrella, agent_minimax, agent_genetic

def main():
    #rana = agent_amplada.Rana("Miquel")
    rana = agent_aestrella.Rana("Miquel")
    #rana = agent_genetic.Rana("Miquel")
    lab = joc.Laberint([rana], parets=True)
    #rana1 = agent_minimax.Rana("Marti")
    #rana2 = agent_minimax.Rana("Silvia")
    #lab = joc.Laberint([rana1, rana2], parets=True)
    lab.comencar()


if __name__ == "__main__":
    main()
