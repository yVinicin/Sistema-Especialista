from experta import *

""" ----------------------- Definição dos Fatos ----------------------- """

# Fato inicial que dispara o sistema, indicando qual luz acendeu.
class Luz(Fact):
    """Representa a luz de advertência acesa. Ex: Luz(tipo='bateria')"""
    tipo = Field(str, mandatory=True)

# Fatos específicos para cada diagnóstico.
class Bateria(Fact):
    """Fatos relacionados ao diagnóstico da luz da Bateria."""
    cabos = Field(str) # 'soltos', 'zinabre', 'ok'
    fusivel = Field(str) # 'nao_sabe', 'ok'
    movimento = Field(str) # 'sim', 'nao'

class Oleo(Fact):
    """Fatos relacionados ao diagnóstico da luz do Óleo."""
    nivel = Field(str) # 'sim', 'nao'

class Temperatura(Fact):
    """Fatos relacionados ao diagnóstico da luz da Temperatura."""
    nivel = Field(str) # 'sim', 'nao'

class Freio(Fact):
    """Fatos relacionados ao diagnóstico da luz do Freio."""
    mao = Field(str) # 'puxado', 'solto'
    pedal = Field(str) # 'fofo', 'normal'
    fluido = Field(str) # 'sim', 'nao'
    pastilha = Field(str) # 'sim', 'nao'

class Cinto(Fact):
    """Fatos relacionados ao diagnóstico da luz do Cinto de Segurança."""
    ocupantes = Field(str) # 'sim', 'nao'
    objetos = Field(str) # 'sim', 'nao'

class CombustivelBaixo(Fact):
    """Fatos relacionados ao diagnóstico da luz de Combustível Baixo."""
    verificacao = Field(str) # 'sim', 'nao'

class Flex(Fact):
    """Fatos relacionados ao diagnóstico da luz Flex."""
    mistura = Field(str) # 'sim', 'nao'

class Airbag(Fact):
    """Fatos relacionados ao diagnóstico da luz do Airbag."""
    colisao = Field(str) # 'sim', 'nao'

class FarolAlto(Fact):
    """Fatos relacionados ao diagnóstico da luz do Farol Alto."""
    estado = Field(str) # 'sim', 'nao'

class Seta(Fact):
    """Fatos relacionados ao diagnóstico da luz da Seta/Pisca."""
    lanternas = Field(str) # 'sim', 'nao'

class Porta(Fact):
    """Fatos relacionados ao diagnóstico da luz de Porta Aberta."""
    fechamento = Field(str) # 'sim', 'nao'
    persistencia = Field(str) # 'sim', 'nao'

class FreioMao(Fact):
    """Fatos relacionados ao diagnóstico da luz do Freio de Mão."""
    acionado = Field(str) # 'sim', 'nao'

""" ----------------------- Sistema Especialista ----------------------- """

class SistemaEspecialista(KnowledgeEngine):
    """
    Motor de Conhecimento para o diagnóstico de luzes de advertência de veículos populares btrasileiros flex.
    Utiliza um objeto 'gui' (interface gráfica/usuário) para interação.
    """
    
    def __init__(self, gui=None):
        """Inicializa o motor de conhecimento e injeta a interface de usuário."""
        super().__init__()
        self.gui = gui
        if self.gui is None:
            # Adiciona um fallback simples para testes sem GUI
            class MockGUI:
                def perguntar(self, pergunta, opcoes):
                    print(f"PERGUNTA: {pergunta} Opções: {opcoes}")
                    # Retorna a primeira opção por padrão para não travar
                    return opcoes[0] 
                def mostrar(self, mensagem):
                    print(f"MENSAGEM: {mensagem}")
            self.gui = MockGUI()

    # ===========================================================================
    # 1. LUZ DA BATERIA
    # ===========================================================================

    @Rule(Luz(tipo="bateria"), NOT(Bateria(cabos=W())))
    def bateria_cabos_iniciais(self):
        """Pergunta inicial sobre o estado dos cabos da bateria."""
        resp = self.gui.perguntar(
            "Abra o capô. Os cabos da bateria estão soltos ou com 'zinabre' (crosta de corrosão)?",
            ["soltos", "zinabre", "ok"]
        )
        self.declare(Bateria(cabos=resp))

    @Rule(Bateria(cabos="soltos"))
    def bateria_cabos_soltos(self):
        """Instrução para cabos soltos."""
        self.gui.mostrar("Ação: Aperte os terminais da bateria firmemente.")
        self.halt()

    @Rule(Bateria(cabos="zinabre"))
    def bateria_cabos_zinabre(self):
        """Instrução para cabos com zinabre/corrosão."""
        self.gui.mostrar("Ação: Utilize produtos como bicarbonato de sódio com água, desengripantes (WD-40) ou removedores específicos. Use uma escova de aço ou lixa para limpar os polos.")
        self.halt()

    @Rule(Bateria(cabos="ok"), NOT(Bateria(fusivel=W())))
    def bateria_fusivel(self):
        """Pergunta sobre o fusível do alternador/bateria."""
        resp = self.gui.perguntar(
            "Verifique se o fusível do alternador/bateria está danificado/queimado.",
            ["nao_sabe", "ok"]
        )
        self.declare(Bateria(fusivel=resp))

    @Rule(Bateria(fusivel="nao_sabe"))
    def bateria_fusivel_nao_sabe(self):
        """Instrução para testar o fusível."""
        self.gui.mostrar("Instrução: Teste o fusível indicado pelo manual do veículo usando uma chave de teste ou multímetro.")
        self.halt()

    @Rule(Bateria(fusivel="ok"), NOT(Bateria(movimento=W())))
    def bateria_luz_em_movimento(self):
        """Pergunta se a luz acendeu com o carro em movimento."""
        resp = self.gui.perguntar(
            "A luz acendeu com o carro em movimento?",
            ["sim", "nao"]
        )
        self.declare(Bateria(movimento=resp))

    @Rule(Bateria(movimento="sim"))
    def bateria_falha_alternador(self):
        """Diagnóstico crítico: Falha no alternador ou esquema elétrico."""
        self.gui.mostrar("Diagnóstico (Crítico): Falha no Alternador ou Esquema Elétrico. O carro vai parar em breve.")
        self.gui.mostrar("Instruções Adicionais:")
        self.gui.mostrar("1. Localize o alternador conforme o manual.")
        self.gui.mostrar("2. Verifique se a correia está frouxa ou quebrada. Se sim, substitua.")
        self.gui.mostrar("3. Se a correia estiver normal, é falha interna do alternador. Procure uma autoelétrica especializada.")
        self.halt()

    @Rule(Bateria(movimento="nao"))
    def bateria_estragada(self):
        """Diagnóstico: Bateria estragada/velha."""
        self.gui.mostrar("Diagnóstico: Bateria estragada/velha. Substitua a bateria.")
        self.halt()

    # ===========================================================================
    # 2. LUZ DO ÓLEO
    # ===========================================================================

    @Rule(Luz(tipo="oleo"), NOT(Oleo(nivel=W())))
    def oleo_nivel_inicial(self):
        """Ação imediata e pergunta sobre o nível de óleo."""
        self.gui.mostrar("Ação Imediata: Pare o carro imediatamente em um local seguro e NÃO ligue o motor.")
        
        resp = self.gui.perguntar(
            "O nível de óleo na vareta está baixo?",
            ["sim", "nao"]
        )
        self.declare(Oleo(nivel=resp))

    @Rule(Oleo(nivel="sim"))
    def oleo_completar(self):
        """Instrução para completar o óleo."""
        self.gui.mostrar("Ação: Complete com óleo do tipo correto indicado pelo fabricante até o nível.")
        self.halt()

    @Rule(Oleo(nivel="nao"))
    def oleo_falha_bomba_sensor(self):
        """Diagnóstico: Falha na bomba de óleo ou sensor de pressão."""
        self.gui.mostrar("Diagnóstico: Falha na bomba de óleo ou sensor de pressão. Não ligue o motor.")
        self.gui.mostrar("Instrução: Chame um guincho e leve a uma mecânica especializada para a substituição da peça indicada.")
        self.halt()

    # ===========================================================================
    # 3. LUZ DE TEMPERATURA
    # ===========================================================================

    @Rule(Luz(tipo="temperatura"), NOT(Temperatura(nivel=W())))
    def temperatura_nivel_agua(self):
        """Pergunta sobre o nível do reservatório de água."""
        resp = self.gui.perguntar(
            "O reservatório de água está vazio?",
            ["sim", "nao"]
        )
        self.declare(Temperatura(nivel=resp))

    @Rule(Temperatura(nivel="sim"))
    def temperatura_completar_vazamento(self):
        """Instrução para completar a água e procurar vazamentos."""
        self.gui.mostrar("Ação: Complete com água (com motor frio e com o veículo funcionando) e procure vazamentos.")
        self.gui.mostrar("Instrução Adicional: Se tiver vazamentos, deverá levar para uma mecânica para analisar a situação (mangueiras, juntas, vedadores).")
        self.halt()

    @Rule(Temperatura(nivel="nao"))
    def temperatura_falha_eletrica(self):
        """Diagnóstico: Provável falha elétrica na ventoinha, válvula termostática ou bomba d’água."""
        self.gui.mostrar("Diagnóstico: Provável falha elétrica na ventoinha, válvula termostática ou bomba d’água.")
        self.gui.mostrar("Instrução: Leve para uma mecânica especializada para substituir as peças indicadas.")
        self.halt()

    # ===========================================================================
    # 4. LUZ DE FREIO 
    # ===========================================================================

    @Rule(Luz(tipo="freio"), NOT(Freio(mao=W())))
    def freio_mao_puxado(self):
        """Pergunta se o freio de mão está puxado."""
        resp = self.gui.perguntar(
            "O freio de mão está puxado?",
            ["puxado", "solto"]
        )
        self.declare(Freio(mao=resp))

    @Rule(Freio(mao="puxado"))
    def freio_mao_abaixar(self):
        """Instrução para abaixar o freio de mão."""
        self.gui.mostrar("Ação: Abaixe o freio de mão.")
        self.halt()

    @Rule(Freio(mao="solto"), NOT(Freio(pedal=W())))
    def freio_pedal_fofo(self):
        """Pergunta se o pedal do freio está 'fofo'."""
        resp = self.gui.perguntar(
            "O pedal do freio está 'fofo'?",
            ["fofo", "normal"]
        )
        self.declare(Freio(pedal=resp))

    @Rule(Freio(pedal="fofo"))
    def freio_perigo_guincho(self):
        """Diagnóstico: Perigo de falta/vazamento de fluido."""
        self.gui.mostrar("PERIGO: Falta/Vazamento de fluido. Você está Sem freios. Chame um guincho.")
        self.halt()

    @Rule(Freio(pedal="normal"), NOT(Freio(fluido=W())))
    def freio_nivel_fluido(self):
        """Pergunta sobre o nível do fluido de freio."""
        resp = self.gui.perguntar(
            "Verifique o nível no reservatório de fluido de freio. Ele está baixo?",
            ["sim", "nao"]
        )
        self.declare(Freio(fluido=resp))

    @Rule(Freio(fluido="sim"))
    def freio_completar_fluido(self):
        """Instrução para completar o fluido de freio."""
        self.gui.mostrar("Ação: Complete com fluido de freio do tipo correto indicado pelo fabricante até o nível máximo.")
        self.halt()

    @Rule(Freio(fluido="nao"), NOT(Freio(pastilha=W())))
    def freio_pastilhas(self):
        """Pergunta sobre o desgaste das pastilhas e lonas."""
        resp = self.gui.perguntar(
            "Verifique visualmente as pastilhas e lonas. Elas estão desgastadas?",
            ["sim", "nao"]
        )
        self.declare(Freio(pastilha=resp))

    @Rule(Freio(pastilha="sim"))
    def freio_substituir_pastilhas(self):
        """Instrução para substituir pastilhas/lonas."""
        self.gui.mostrar("Ação: Leve para uma mecânica ou auto center especializada para fazer a substituição das pastilhas/lonas.")
        self.halt()
    
    # Se o fluido não está baixo e as pastilhas não estão gastas, o problema é no sensor.
    @Rule(Freio(fluido="nao"), Freio(pastilha="nao"))
    def freio_falha_sensor(self):
        """Diagnóstico: Falha no sensor de freio."""
        self.gui.mostrar("Diagnóstico: Falha no sensor de freio. Leve a uma oficina para diagnóstico e reparo.")
        self.halt()

    # ===========================================================================
    # 5. LUZ DO CINTO DE SEGURANÇA
    # ===========================================================================

    @Rule(Luz(tipo="cinto"), NOT(Cinto(ocupantes=W())))
    def cinto_ocupantes(self):
        """Pergunta se todos os ocupantes estão com cinto."""
        resp = self.gui.perguntar(
            "Todos os ocupantes estão com cinto?",
            ["sim", "nao"]
        )
        self.declare(Cinto(ocupantes=resp))

    @Rule(Cinto(ocupantes="nao"))
    def cinto_afivelar(self):
        """Instrução para afivelar os cintos."""
        self.gui.mostrar("Ação: Afivele os cintos.")
        self.halt()

    @Rule(Cinto(ocupantes="sim"), NOT(Cinto(objetos=W())))
    def cinto_objetos(self):
        """Pergunta sobre objetos/peso no banco do passageiro."""
        resp = self.gui.perguntar(
            "Há mochilas ou peso no banco do passageiro?",
            ["sim", "nao"]
        )
        self.declare(Cinto(objetos=resp))

    @Rule(Cinto(objetos="sim"))
    def cinto_remover_objeto(self):
        """Instrução para remover o objeto ou afivelar o cinto do passageiro."""
        self.gui.mostrar("Ação: Remova o objeto ou afivele o cinto do passageiro (para travar o sensor).")
        self.halt()

    @Rule(Cinto(objetos="nao"))
    def cinto_falha_sensor(self):
        """Diagnóstico: Falha no sensor ou no próprio cinto."""
        self.gui.mostrar("Diagnóstico: Falha no sensor do banco ou no próprio cinto. Leve a um especialista para substituição.")
        self.halt()

    # ===========================================================================
    # 6. LUZ DE COMBUSTÍVEL BAIXO 
    # ===========================================================================

    @Rule(Luz(tipo="combustivel-baixo"), NOT(CombustivelBaixo(verificacao=W())))
    def combustivel_verificacao_inicial(self):
        """Instrução inicial e pergunta sobre o nível real de combustível."""
        self.gui.mostrar("Ação: Verifique imediatamente (pelo medidor ou visualmente) se o nível de combustível está realmente baixo.")
        
        resp = self.gui.perguntar(
            "A verificação confirmou que o nível de combustível está baixo?",
            ["sim", "nao"]
        )
        self.declare(CombustivelBaixo(verificacao=resp))

    @Rule(CombustivelBaixo(verificacao="sim"))
    def combustivel_reabastecer(self):
        """Instrução para reabastecer e aviso de risco técnico."""
        self.gui.mostrar("Ação: Reabasteça o veículo imediatamente.")
        self.gui.mostrar("Instrução: Evite rodar com o tanque na reserva.")
        self.gui.mostrar("Risco Técnico: A bomba de combustível pode superaquecer e queimar, pois sua refrigeração depende do combustível no tanque.")
        self.halt()

    @Rule(CombustivelBaixo(verificacao="nao"))
    def combustivel_falha_sensor(self):
        """Diagnóstico: Falha no sensor de nível de combustível."""
        self.gui.mostrar("Diagnóstico: Há indício de falha no sensor de nível de combustível.")
        self.gui.mostrar("Instrução: Leve o veículo a uma oficina especializada para diagnóstico e reparo do sistema de medição.")
        self.halt()

    # ===========================================================================
    # 7. LUZ FLEX
    # ===========================================================================

    @Rule(Luz(tipo="flex"), NOT(Flex(mistura=W())))
    def flex_mistura(self):
        """Pergunta se houve mistura recente de combustíveis."""
        resp = self.gui.perguntar(
            "Você misturou combustíveis recentemente (álcool e gasolina)?",
            ["sim", "nao"]
        )
        self.declare(Flex(mistura=resp))

    @Rule(Flex(mistura="sim"))
    def flex_recalibracao(self):
        """Diagnóstico: Central em recalibração."""
        self.gui.mostrar("Diagnóstico: A central ainda está recalibrando a mistura do combustível.")
        self.gui.mostrar("Instrução: Rode por alguns quilômetros para o módulo ajustar automaticamente.")
        self.halt()

    @Rule(Flex(mistura="nao"))
    def flex_falha_sensor(self):
        """Diagnóstico: Sensor de etanol (ESensor) com falha."""
        self.gui.mostrar("Diagnóstico: Sensor de etanol (ESensor) com falha.")
        self.gui.mostrar("Instrução: Levar a uma mecânica para verificar o sensor ou atualizações da ECU.")
        self.halt()

    # ===========================================================================
    # 8. LUZ DO AIRBAG
    # ===========================================================================

    @Rule(Luz(tipo="airbag"), NOT(Airbag(colisao=W())))
    def airbag_colisao(self):
        """Pergunta se o carro sofreu colisão leve recentemente."""
        resp = self.gui.perguntar(
            "O carro já sofreu alguma colisão leve recentemente?",
            ["sim", "nao"]
        )
        self.declare(Airbag(colisao=resp))

    @Rule(Airbag(colisao="sim"))
    def airbag_modulo_travado(self):
        """Diagnóstico: Módulo do airbag travado após impacto."""
        self.gui.mostrar("Diagnóstico: O módulo do airbag está travado após o impacto.")
        self.gui.mostrar("Instrução: Leve a uma mecânica ou auto center, pois o reparo exige um scanner profissional para resetar o módulo.")
        self.halt()

    @Rule(Airbag(colisao="nao"))
    def airbag_falha_sensor_fiacao(self):
        """Diagnóstico: Falha no sensor do banco ou na fiação."""
        self.gui.mostrar("Diagnóstico: Falha no sensor do banco ou na fiação do airbag.")
        self.gui.mostrar("Instrução: Leve a uma oficina especializada em airbag.")
        self.halt()

    # ===========================================================================
    # 9. LUZ DO FAROL ALTO
    # ===========================================================================

    @Rule(Luz(tipo="farol-alto"), NOT(FarolAlto(estado=W())))
    def farol_alto_estado(self):
        """Pergunta se o farol alto está realmente ligado."""
        resp = self.gui.perguntar(
            "O farol alto está realmente ligado?",
            ["sim", "nao"]
        )
        self.declare(FarolAlto(estado=resp))

    @Rule(FarolAlto(estado="sim"))
    def farol_alto_ativado(self):
        """Informação: Farol alto ativado."""
        self.gui.mostrar("Informação: O farol alto está ativado.")
        self.halt()

    @Rule(FarolAlto(estado="nao"))
    def farol_alto_mau_contato(self):
        """Diagnóstico: Sensor/comutador do farol com mau contato."""
        self.gui.mostrar("Diagnóstico: Sensor/comutador do farol está com mau contato.")
        self.gui.mostrar("Instrução: Leve a uma autoelétrica para fazer uma revisão da chave de seta.")
        self.halt()

    # ===========================================================================
    # 10. LUZ DA SETA/PISCA
    # ===========================================================================

    @Rule(Luz(tipo="seta"), NOT(Seta(lanternas=W())))
    def seta_lanternas(self):
        """Pergunta se todas as lanternas (setas) estão piscando normalmente."""
        resp = self.gui.perguntar(
            "Todas as lanternas (setas) estão piscando normalmente?",
            ["sim", "nao"]
        )
        self.declare(Seta(lanternas=resp))

    @Rule(Seta(lanternas="sim"))
    def seta_lampada_queimada(self):
        """Diagnóstico: Lâmpada da seta queimada."""
        self.gui.mostrar("Diagnóstico: Lâmpada da seta queimada.")
        self.gui.mostrar("Instrução: Substitua a lâmpada queimada da lanterna correspondente.")
        self.halt()

    @Rule(Seta(lanternas="nao"))
    def seta_falha_rele_modulo(self):
        """Diagnóstico: Possível falha no relê, interruptor ou módulo de controle."""
        self.gui.mostrar("Diagnóstico: Possível falha no relê (pisca-pisca), interruptor ou módulo de controle.")
        self.gui.mostrar("Instrução: Leve a uma oficina autoelétrica para o diagnóstico preciso.")
        self.halt()

    # ===========================================================================
    # 11. LUZ DE PORTA ABERTA
    # ===========================================================================

    @Rule(Luz(tipo="porta"), NOT(Porta(fechamento=W())))
    def porta_fechamento(self):
        """Pergunta se todas as portas e o portamalas estão totalmente fechados."""
        resp = self.gui.perguntar(
            "Todas as portas e o portamalas estão totalmente fechados?",
            ["sim", "nao"]
        )
        self.declare(Porta(fechamento=resp))

    @Rule(Porta(fechamento="nao"))
    def porta_fechar(self):
        """Instrução para fechar firmemente os compartimentos."""
        self.gui.mostrar("Ação: Feche firmemente todos os compartimentos.")
        self.halt()

    @Rule(Porta(fechamento="sim"), NOT(Porta(persistencia=W())))
    def porta_persistencia(self):
        """Pergunta se o aviso permanece aceso com tudo fechado."""
        resp = self.gui.perguntar(
            "O aviso permanece aceso com tudo fechado?",
            ["sim", "nao"]
        )
        self.declare(Porta(persistencia=resp))

    @Rule(Porta(persistencia="sim"))
    def porta_falha_sensor_trava(self):
        """Diagnóstico: Provável falha no sensor ou na trava elétrica de uma porta."""
        self.gui.mostrar("Diagnóstico: Provável falha no sensor ou na trava elétrica de uma porta.")
        self.gui.mostrar("Instrução: Leve o veículo a uma oficina para diagnóstico e reparo do sistema.")
        self.halt()

    # ===========================================================================
    # 12. LUZ DO FREIO DE MÃO 
    # ===========================================================================

    @Rule(Luz(tipo="freio-mao"), NOT(FreioMao(acionado=W())))
    def freio_mao_acionado(self):
        """Pergunta se o freio de mão está acionado."""
        resp = self.gui.perguntar(
            "O freio de mão está acionado?",
            ["sim", "nao"]
        )
        self.declare(FreioMao(acionado=resp))

    @Rule(FreioMao(acionado="sim"))
    def freio_mao_liberar(self):
        """Instrução para liberar o freio de mão."""
        self.gui.mostrar("Ação: Libere completamente o freio de mão.")
        self.halt()

    @Rule(FreioMao(acionado="nao"))
    def freio_mao_falha_sensor(self):
        """Diagnóstico: Provável falha no sensor ou no próprio freio de mão."""
        self.gui.mostrar("Diagnóstico: Provável falha no sensor ou no próprio freio de mão.")
        self.gui.mostrar("Instrução: Leve o veículo a uma oficina para diagnóstico e reparo do sistema.")
        self.halt()
