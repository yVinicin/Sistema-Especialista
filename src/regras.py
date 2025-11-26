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

    # ----------------------- Luz da Bateria ----------------------- #
    @Rule(Luz(tipo="bateria"), NOT(Bateria(cabos=W())))
    def bateria_perguntar_cabos(self):
        resp = input("Os cabos estão soltos, com zinabre ou ok? ")
        self.declare(Bateria(cabos=resp))

    @Rule(Bateria(cabos="soltos"))
    def bateria_soltos(self):
        print("AÇÃO: Aperte os terminais da bateria firmemente. (Alta)")
        self.halt()

    @Rule(Bateria(cabos="zinabre"))
    def bateria_zinabre(self):
        print("AÇÃO: Limpe com bicarbonato + água, WD-40 ou escova. (Alta)")
        self.halt()

    @Rule(Bateria(cabos="ok"),
          NOT(Bateria(fusivel=W())))
    def bateria_fusivel(self):
        resp = input("O fusível do alternador está queimado? (sim/nao) ")
        self.declare(Bateria(fusivel=resp))

    @Rule(Bateria(fusivel="sim"))
    def bateria_fusivel_queimado(self):
        print("AÇÃO: Teste o fusível com multímetro. (Alta)")
        self.halt()

    @Rule(Bateria(fusivel="nao"),
          NOT(Bateria(movimento=W())))
    def bateria_movimento(self):
        resp = input("A luz acendeu com o carro em movimento? (sim/nao) ")
        self.declare(Bateria(movimento=resp))

    @Rule(Bateria(movimento="sim"))
    def bateria_movimento_sim(self):
        print("DIAGNÓSTICO: Falha no alternador. O carro vai parar. (Crítica)")
        print("Verifique a correia ou leve à autoelétrica.")
        self.halt()

    @Rule(Bateria(movimento="nao"))
    def bateria_movimento_nao(self):
        print("DIAGNÓSTICO: Bateria velha/estragada. Substituir. (Média)")
        self.halt()


    # ----------------------- Luz do Óleo ----------------------- #
    @Rule(Luz(tipo="oleo"))
    def oleo_parar(self):
        print("AÇÃO IMEDIATA: Pare o carro e NÃO ligue o motor. (Crítica)")
        resp = input("O nível de óleo está baixo? (sim/nao) ")
        if resp == "sim":
            print("AÇÃO: Complete o óleo até o nível. (Alta)")
        else:
            print("DIAGNÓSTICO: Bomba de óleo ou sensor com falha. (Crítica)")
            print("Chame um guincho.")
        self.halt()


    # ----------------------- Luz da Temperatura ----------------------- #
    @Rule(Luz(tipo="temperatura"))
    def temp_nivel(self):
        resp = input("O reservatório está vazio? (sim/nao) ")
        if resp == "sim":
            print("AÇÃO: Complete com água (motor frio). (Alta)")
            print("Verifique vazamentos.")
        else:
            print("DIAGNÓSTICO: Falha na ventoinha, válvula ou bomba d'água. (Alta)")
        self.halt()


    # ----------------------- Luz de Freio ----------------------- #
    @Rule(Luz(tipo="freio"))
    def freio_inicio(self):
        resp = input("O freio de mão está puxado? (sim/nao) ")
        if resp == "sim":
            print("AÇÃO: Abaixe o freio de mão. (Baixa)")
            self.halt()
        else:
            self.declare(Freio(mao="ok"))

    @Rule(Freio(mao="ok"),
          NOT(Freio(fofo=W())))
    def freio_pedal(self):
        resp = input("O pedal está 'fofo'? (sim/nao) ")
        self.declare(Freio(fofo=resp))

    @Rule(Freio(fofo="sim"))
    def freio_fofo(self):
        print("PERIGO: Vazamento no sistema hidráulico. SEM freios. (Crítica)")
        print("Chame um guincho.")
        self.halt()

    @Rule(Freio(fofo="nao"),
          NOT(Freio(fluido=W())))
    def freio_fluido(self):
        resp = input("O nível de fluido está baixo? (sim/nao) ")
        self.declare(Freio(fluido=resp))

    @Rule(Freio(fluido="sim"))
    def freio_fluido_baixo(self):
        print("AÇÃO: Complete com fluido DOT correto. (Alta)")
        self.halt()

    @Rule(Freio(fluido="nao"),
          NOT(Freio(pastilha=W())))
    def freio_pastilhas(self):
        resp = input("As pastilhas/lonas estão gastas? (sim/nao) ")
        self.declare(Freio(pastilha=resp))

    @Rule(Freio(pastilha="sim"))
    def freio_pastilha_gasta(self):
        print("AÇÃO: Trocar pastilhas/lonas. (Alta)")
        self.halt()

    @Rule(Freio(pastilha="nao"))
    def freio_sem_diag(self):
        print("DIAGNÓSTICO: Falha no sistema de freios. Leve ao mecânico. (Média)")
        self.halt()


    # ----------------------- Luz do Cinto ----------------------- #
    @Rule(Luz(tipo="cinto"))
    def cinto_inicio(self):
        resp = input("Todos os ocupantes estão de cinto? (sim/nao) ")
        if resp == "nao":
            print("AÇÃO: Afivele os cintos. (Baixa)")
            self.halt()
        else:
            self.declare(Cinto(cintos="ok"))

    @Rule(Cinto(cintos="ok"))
    def cinto_objetos(self):
        resp = input("Há mochila/objeto no banco do passageiro? (sim/nao) ")
        if resp == "sim":
            print("AÇÃO: Tire a mochila ou afivele o cinto do passageiro. (Baixa)")
        else:
            print("DIAGNÓSTICO: Sensor de cinto com defeito. (Média)")
        self.halt()
