from experta import *

""" ----------------------- Definição dos fatos ----------------------- """
class Luz(Fact):
    """Tipo de luz acesa"""
    pass

class Bateria(Fact):
    pass

class Oleo(Fact):
    pass

class Temperatura(Fact):
    pass

class Freio(Fact):
    pass

class Cinto(Fact):
    pass

""" ----------------------- Sistema Especialista ----------------------- """
class SistemaEspecialista(KnowledgeEngine):
    gui = None

    # ----------------------- Luz da Bateria ----------------------- #
    @Rule(Luz(tipo="bateria"), NOT(Bateria(cabos=W())))
    def bateria_perguntar_cabos(self):
        resp = self.gui.perguntar(
            "Os cabos estão soltos, com zinabre ou ok?",
            ["soltos", "zinabre", "ok"]
        )
        self.declare(Bateria(cabos=resp))

    @Rule(Bateria(cabos="soltos"))
    def bateria_soltos(self):
        self.gui.mostrar("AÇÃO: Aperte os terminais da bateria firmemente. (Alta)")
        self.halt()

    @Rule(Bateria(cabos="zinabre"))
    def bateria_zinabre(self):
        self.gui.mostrar("AÇÃO: Limpe com bicarbonato + água, WD-40 ou escova. (Alta)")
        self.halt()

    @Rule(Bateria(cabos="ok"),
          NOT(Bateria(fusivel=W())))
    def bateria_fusivel(self):
        resp = self.gui.perguntar(
            "O fusível do alternador está queimado?",
            ["sim", "nao"]
        )
        self.declare(Bateria(fusivel=resp))

    @Rule(Bateria(fusivel="sim"))
    def bateria_fusivel_queimado(self):
        self.gui.mostrar("AÇÃO: Teste o fusível com multímetro. (Alta)")
        self.halt()

    @Rule(Bateria(fusivel="nao"),
          NOT(Bateria(movimento=W())))
    def bateria_movimento(self):
        resp = self.gui.perguntar(
            "A luz acendeu com o carro em movimento?",
            ["sim", "nao"]
        )
        self.declare(Bateria(movimento=resp))

    @Rule(Bateria(movimento="sim"))
    def bateria_movimento_sim(self):
        self.gui.mostrar("DIAGNÓSTICO: Falha no alternador. O carro vai parar. (Crítica)")
        self.gui.mostrar("Verifique a correia ou leve à autoelétrica.")
        self.halt()

    @Rule(Bateria(movimento="nao"))
    def bateria_movimento_nao(self):
        self.gui.mostrar("DIAGNÓSTICO: Bateria velha/estragada. Substituir. (Média)")
        self.halt()


    # ----------------------- Luz do Óleo ----------------------- #
    @Rule(Luz(tipo="oleo"))
    def oleo_parar(self):
        self.gui.mostrar("AÇÃO IMEDIATA: Pare o carro e NÃO ligue o motor. (Crítica)")
        resp = self.gui.perguntar(
            "O nível de óleo está baixo?)",
            ["sim", "nao"]
        )
        if resp == "sim":
            self.gui.mostrar("AÇÃO: Complete o óleo até o nível. (Alta)")
        else:
            self.gui.mostrar("DIAGNÓSTICO: Bomba de óleo ou sensor com falha. (Crítica)")
            self.gui.mostrar("Chame um guincho.")
        self.halt()


    # ----------------------- Luz da Temperatura ----------------------- #
    @Rule(Luz(tipo="temperatura"))
    def temp_nivel(self):
        resp = self.gui.perguntar(
            "O reservatório está vazio?",
            ["sim", "nao"]
        )
        if resp == "sim":
            self.gui.mostrar("AÇÃO: Complete com água (motor frio). (Alta)")
            self.gui.mostrar("Verifique vazamentos.")
        else:
            self.gui.mostrar("DIAGNÓSTICO: Falha na ventoinha, válvula ou bomba d'água. (Alta)")
        self.halt()


    # ----------------------- Luz de Freio ----------------------- #
    @Rule(Luz(tipo="freio"))
    def freio_inicio(self):
        resp = self.gui.perguntar(
            "O freio de mão está puxado?",
            ["sim", "nao"]
        )
        if resp == "sim":
            self.gui.mostrar("AÇÃO: Abaixe o freio de mão. (Baixa)")
            self.halt()
        else:
            self.declare(Freio(mao="ok"))

    @Rule(Freio(mao="ok"),
          NOT(Freio(fofo=W())))
    def freio_pedal(self):
        resp = self.gui.perguntar(
            "O pedal está 'fofo'?",
            ["sim", "nao"]
        )
        self.declare(Freio(fofo=resp))

    @Rule(Freio(fofo="sim"))
    def freio_fofo(self):
        self.gui.mostrar("PERIGO: Vazamento no sistema hidráulico. SEM freios. (Crítica)")
        self.gui.mostrar("Chame um guincho.")
        self.halt()

    @Rule(Freio(fofo="nao"),
          NOT(Freio(fluido=W())))
    def freio_fluido(self):
        resp = self.gui.perguntar(
            "O nível de fluido está baixo?",
            ["sim", "nao"]
        )
        self.declare(Freio(fluido=resp))

    @Rule(Freio(fluido="sim"))
    def freio_fluido_baixo(self):
        self.gui.mostrar("AÇÃO: Complete com fluido DOT correto. (Alta)")
        self.halt()

    @Rule(Freio(fluido="nao"),
          NOT(Freio(pastilha=W())))
    def freio_pastilhas(self):
        resp = self.gui.perguntar(
            "As pastilhas/lonas estão gastas?",
            ["sim", "nao"]
        )
        self.declare(Freio(pastilha=resp))

    @Rule(Freio(pastilha="sim"))
    def freio_pastilha_gasta(self):
        self.gui.mostrar("AÇÃO: Trocar pastilhas/lonas. (Alta)")
        self.halt()

    @Rule(Freio(pastilha="nao"))
    def freio_sem_diag(self):
        self.gui.mostrar("DIAGNÓSTICO: Falha no sistema de freios. Leve ao mecânico. (Média)")
        self.halt()


    # ----------------------- Luz do Cinto ----------------------- #
    @Rule(Luz(tipo="cinto"))
    def cinto_inicio(self):
        resp = self.gui.perguntar(
            "Todos os ocupantes estão de cinto?",
            ["sim", "nao"]
        )
        if resp == "nao":
            self.gui.mostrar("AÇÃO: Afivele os cintos. (Baixa)")
            self.halt()
        else:
            self.declare(Cinto(cintos="ok"))

    @Rule(Cinto(cintos="ok"))
    def cinto_objetos(self):
        resp = self.gui.perguntar(
            "Há mochila/objeto no banco do passageiro?",
            ["sim", "nao"]
        )
        if resp == "sim":
            self.gui.mostrar("AÇÃO: Tire a mochila ou afivele o cinto do passageiro. (Baixa)")
        else:
            self.gui.mostrar("DIAGNÓSTICO: Sensor de cinto com defeito. (Média)")
        self.halt()
