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
        try:
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
        except Exception as e:
            print(f"Erro na inicialização do SistemaEspecialista: {e}")
            raise

    def _perguntar_seguro(self, pergunta, opcoes):
        """Método auxiliar para perguntar com tratamento de erros."""
        try:
            resp = self.gui.perguntar(pergunta, opcoes)
            if resp not in opcoes:
                print(f"Resposta inválida: {resp}. Usando padrão: {opcoes[0]}")
                return opcoes[0]
            return resp
        except Exception as e:
            print(f"Erro ao perguntar: {e}. Usando padrão: {opcoes[0]}")
            return opcoes[0]

    def _mostrar_seguro(self, mensagem):
        """Método auxiliar para mostrar com tratamento de erros."""
        try:
            self.gui.mostrar(mensagem)
        except Exception as e:
            print(f"Erro ao mostrar mensagem: {e}")

    # ===========================================================================
    # 1. LUZ DA BATERIA
    # ===========================================================================

    @Rule(Luz(tipo="bateria"), NOT(Bateria(cabos=W())))
    def bateria_cabos_iniciais(self):
        """Pergunta inicial sobre o estado dos cabos da bateria."""
        resp = self._perguntar_seguro(
            "Abra o capô. Os cabos da bateria estão soltos ou com 'zinabre' (crosta de corrosão)?",
            ["soltos", "zinabre", "ok"]
        )
        self.declare(Bateria(cabos=resp))

    @Rule(Bateria(cabos="soltos"))
    def bateria_cabos_soltos(self):
        """Instrução para cabos soltos."""
        self._mostrar_seguro("Ação: Aperte os terminais da bateria firmemente.")
        self.halt()

    @Rule(Bateria(cabos="zinabre"))
    def bateria_cabos_zinabre(self):
        """Instrução para cabos com zinabre/corrosão."""
        self._mostrar_seguro("Ação: Utilize produtos como bicarbonato de sódio com água, desengripantes (WD-40) ou removedores específicos. Use uma escova de aço ou lixa para limpar os polos.")
        self.halt()

    @Rule(Bateria(cabos="ok"), NOT(Bateria(fusivel=W())))
    def bateria_fusivel(self):
        """Pergunta sobre o fusível do alternador/bateria."""
        resp = self._perguntar_seguro(
            "Verifique se o fusível do alternador/bateria está danificado/queimado.",
            ["nao_sabe", "ok"]
        )
        self.declare(Bateria(fusivel=resp))

    @Rule(Bateria(fusivel="nao_sabe"))
    def bateria_fusivel_nao_sabe(self):
        """Instrução para testar o fusível."""
        self._mostrar_seguro("Instrução: Teste o fusível indicado pelo manual do veículo usando uma chave de teste ou multímetro.")
        self.halt()

    @Rule(Bateria(fusivel="ok"), NOT(Bateria(movimento=W())))
    def bateria_luz_em_movimento(self):
        """Pergunta se a luz acendeu com o carro em movimento."""
        resp = self._perguntar_seguro(
            "A luz acendeu com o carro em movimento?",
            ["sim", "nao"]
        )
        self.declare(Bateria(movimento=resp))

    @Rule(Bateria(movimento="sim"))
    def bateria_falha_alternador(self):
        """Diagnóstico crítico: Falha no alternador ou esquema elétrico."""
        self._mostrar_seguro("Diagnóstico (Crítico): Falha no Alternador ou Esquema Elétrico. O carro vai parar em breve.")
        self._mostrar_seguro("Instruções Adicionais:")
        self._mostrar_seguro("1. Localize o alternador conforme o manual.")
        self._mostrar_seguro("2. Verifique se a correia está frouxa ou quebrada. Se sim, substitua.")
        self._mostrar_seguro("3. Se a correia estiver normal, é falha interna do alternador. Procure uma autoelétrica especializada.")
        self.halt()

    @Rule(Bateria(movimento="nao"))
    def bateria_estragada(self):
        """Diagnóstico: Bateria estragada/velha."""
        self._mostrar_seguro("Diagnóstico: Bateria estragada/velha. Substitua a bateria.")
        self.halt()

    # ===========================================================================
    # 2. LUZ DO ÓLEO
    # ===========================================================================

    @Rule(Luz(tipo="oleo"), NOT(Oleo(nivel=W())))
    def oleo_nivel_inicial(self):
        """Ação imediata e pergunta sobre o nível de óleo."""
        self._mostrar_seguro("Ação Imediata: Pare o carro imediatamente em um local seguro e NÃO ligue o motor.")
        
        resp = self._perguntar_seguro(
            "O nível de óleo na vareta está baixo?",
            ["sim", "nao"]
        )
        self.declare(Oleo(nivel=resp))

    @Rule(Oleo(nivel="sim"))
    def oleo_completar(self):
        """Instrução para completar o óleo."""
        self._mostrar_seguro("Ação: Complete com óleo do tipo correto indicado pelo fabricante até o nível.")
        self.halt()

    @Rule(Oleo(nivel="nao"))
    def oleo_falha_bomba_sensor(self):
        """Diagnóstico: Falha na bomba de óleo ou sensor de pressão."""
        self._mostrar_seguro("Diagnóstico: Falha na bomba de óleo ou sensor de pressão. Não ligue o motor.")
        self._mostrar_seguro("Instrução: Chame um guincho e leve a uma mecânica especializada para a substituição da peça indicada.")
        self.halt()

    # ===========================================================================
    # 3. LUZ DE TEMPERATURA
    # ===========================================================================

    @Rule(Luz(tipo="temperatura"), NOT(Temperatura(nivel=W())))
    def temperatura_nivel_agua(self):
        """Pergunta sobre o nível do reservatório de água."""
        resp = self._perguntar_seguro(
            "O reservatório de água está vazio?",
            ["sim", "nao"]
        )
        self.declare(Temperatura(nivel=resp))

    @Rule(Temperatura(nivel="sim"))
    def temperatura_completar_vazamento(self):
        """Instrução para completar a água e procurar vazamentos."""
        self._mostrar_seguro("Ação: Complete com água ou fluído de arrefecimento (com motor frio e com o veículo funcionando) conforme indicado pelo fabricante e procure vazamentos.")
        self._mostrar_seguro("Instrução Adicional: Se tiver vazamentos, deverá levar para uma mecânica para analisar a situação (mangueiras, juntas, vedadores).")
        self.halt()

    @Rule(Temperatura(nivel="nao"))
    def temperatura_falha_eletrica(self):
        """Diagnóstico: Provável falha elétrica na ventoinha, válvula termostática ou bomba d’água."""
        self._mostrar_seguro("Diagnóstico: Provável falha elétrica na ventoinha, válvula termostática ou bomba d’água.")
        self._mostrar_seguro("Instrução: Leve para uma mecânica especializada para substituir as peças indicadas.")
        self.halt()

    # ===========================================================================
    # 4. LUZ DE FREIO 
    # ===========================================================================

    @Rule(Luz(tipo="freio"), NOT(Freio(mao=W())))
    def freio_mao_puxado(self):
        """Pergunta se o freio de mão está puxado."""
        resp = self._perguntar_seguro(
            "O freio de mão está puxado?",
            ["puxado", "solto"]
        )
        self.declare(Freio(mao=resp))

    @Rule(Freio(mao="puxado"))
    def freio_mao_abaixar(self):
        """Instrução para abaixar o freio de mão."""
        self._mostrar_seguro("Ação: Abaixe o freio de mão.")
        self.halt()

    @Rule(Freio(mao="solto"), NOT(Freio(pedal=W())))
    def freio_pedal_fofo(self):
        """Pergunta se o pedal do freio está 'fofo'."""
        resp = self._perguntar_seguro(
            "O pedal do freio está 'fofo'?",
            ["fofo", "normal"]
        )
        self.declare(Freio(pedal=resp))

    @Rule(Freio(pedal="fofo"))
    def freio_perigo_guincho(self):
        """Diagnóstico: Perigo de falta/vazamento de fluido."""
        self._mostrar_seguro("PERIGO: Falta/Vazamento de fluido. Você está Sem freios. Chame um guincho.")
        self.halt()

    @Rule(Freio(pedal="normal"), NOT(Freio(fluido=W())))
    def freio_nivel_fluido(self):
        """Pergunta sobre o nível do fluido de freio."""
        resp = self._perguntar_seguro(
            "Verifique o nível no reservatório de fluido de freio. Ele está baixo?",
            ["sim", "nao"]
        )
        self.declare(Freio(fluido=resp))

    @Rule(Freio(fluido="sim"))
    def freio_completar_fluido(self):
        """Instrução para completar o fluido de freio."""
        self._mostrar_seguro("Ação: Complete com fluido de freio do tipo correto indicado pelo fabricante até o nível máximo.")
        self.halt()

    @Rule(Freio(fluido="nao"), NOT(Freio(pastilha=W())))
    def freio_pastilhas(self):
        """Pergunta sobre o desgaste das pastilhas e lonas."""
        resp = self._perguntar_seguro(
            "Verifique visualmente as pastilhas e lonas. Elas estão desgastadas?",
            ["sim", "nao"]
        )
        self.declare(Freio(pastilha=resp))

    @Rule(Freio(pastilha="sim"))
    def freio_substituir_pastilhas(self):
        """Instrução para substituir pastilhas/lonas."""
        self._mostrar_seguro("Ação: Leve para uma mecânica ou auto center especializada para fazer a substituição das pastilhas/lonas.")
        self.halt()
    
    # Se o fluido não está baixo e as pastilhas não estão gastas, o problema é no sensor.
    @Rule(Freio(fluido="nao"), Freio(pastilha="nao"))
    def freio_falha_sensor(self):
        """Diagnóstico: Falha no sensor de freio."""
        self._mostrar_seguro("Diagnóstico: Falha no sensor de freio. Leve a uma oficina para diagnóstico e reparo.")
        self.halt()

    # ===========================================================================
    # 5. LUZ DO CINTO DE SEGURANÇA
    # ===========================================================================

    @Rule(Luz(tipo="cinto"), NOT(Cinto(ocupantes=W())))
    def cinto_ocupantes(self):
        """Pergunta se todos os ocupantes estão com cinto."""
        resp = self._perguntar_seguro(
            "Todos os ocupantes estão com cinto?",
            ["sim", "nao"]
        )
        self.declare(Cinto(ocupantes=resp))

    @Rule(Cinto(ocupantes="nao"))
    def cinto_afivelar(self):
        """Instrução para afivelar os cintos."""
        self._mostrar_seguro("Ação: Afivele os cintos.")
        self.halt()

    @Rule(Cinto(ocupantes="sim"), NOT(Cinto(objetos=W())))
    def cinto_objetos(self):
        """Pergunta sobre objetos/peso no banco do passageiro."""
        resp = self._perguntar_seguro(
            "Há mochilas ou peso no banco do passageiro?",
            ["sim", "nao"]
        )
        self.declare(Cinto(objetos=resp))

    @Rule(Cinto(objetos="sim"))
    def cinto_remover_objeto(self):
        """Instrução para remover o objeto ou afivelar o cinto do passageiro."""
        self._mostrar_seguro("Ação: Remova o objeto ou afivele o cinto do passageiro (para travar o sensor).")
        self.halt()

    @Rule(Cinto(objetos="nao"))
    def cinto_falha_sensor(self):
        """Diagnóstico: Falha no sensor ou no próprio cinto."""
        self._mostrar_seguro("Diagnóstico: Falha no sensor do banco ou no próprio cinto. Leve a um especialista para substituição.")
        self.halt()

    # ===========================================================================
    # 6. LUZ DE COMBUSTÍVEL BAIXO 
    # ===========================================================================

    @Rule(Luz(tipo="combustivel-baixo"), NOT(CombustivelBaixo(verificacao=W())))
    def combustivel_verificacao_inicial(self):
        """Instrução inicial e pergunta sobre o nível real de combustível."""
        self._mostrar_seguro("Ação: Verifique imediatamente (pelo medidor ou visualmente) se o nível de combustível está realmente baixo.")

        resp = self._perguntar_seguro(
            "A verificação confirmou que o nível de combustível está baixo?",
            ["sim", "nao"]
        )
        self.declare(CombustivelBaixo(verificacao=resp))

    @Rule(CombustivelBaixo(verificacao="sim"))
    def combustivel_reabastecer(self):
        """Instrução para reabastecer e aviso de risco técnico."""
        self._mostrar_seguro("Ação: Reabasteça o veículo imediatamente.")
        self._mostrar_seguro("Instrução: Evite rodar com o tanque na reserva.")
        self._mostrar_seguro("Risco Técnico: A bomba de combustível pode superaquecer e queimar, pois sua refrigeração depende do combustível no tanque.")
        self.halt()

    @Rule(CombustivelBaixo(verificacao="nao"))
    def combustivel_falha_sensor(self):
        """Diagnóstico: Falha no sensor de nível de combustível."""
        self._mostrar_seguro("Diagnóstico: Há indício de falha no sensor de nível de combustível.")
        self._mostrar_seguro("Instrução: Leve o veículo a uma oficina especializada para diagnóstico e reparo do sistema de medição.")
        self.halt()

    # ===========================================================================
    # 7. LUZ DE INJEÇÃO (COMPLETA)
    # ===========================================================================

    @Rule(Luz(tipo="flex"), NOT(Flex(mistura=W())))
    def flex_mistura(self):
        """Pergunta se houve mistura recente de combustíveis."""
        resp = self._perguntar_seguro(
            "Você misturou combustíveis recentemente (álcool e gasolina)?",
            ["sim", "nao"]
        )
        self.declare(Flex(mistura=resp))

    # Caso 1 — MISTURA DE COMBUSTÍVEL
    @Rule(Flex(mistura="sim"))
    def flex_recalibracao(self):
        """Diagnóstico: Central em recalibração."""
        self._mostrar_seguro("Diagnóstico: A central está recalibrando a mistura do combustível.")
        self._mostrar_seguro("Instrução: Rode por alguns quilômetros para o módulo ajustar automaticamente.")
        self.halt()

    # CASO 2 — NÃO HOUVE MISTURA: INVESTIGAÇÃO COMPLETA
    @Rule(Flex(mistura="nao"))
    def flex_investigar(self):
        """Pergunta sobre sintomas adicionais."""
        resp = self._perguntar_seguro(
            "O carro está falhando, engasgando ou com marcha lenta irregular?",
            ["sim", "nao"]
        )
        self.declare(Fact(falhando=resp))

    # Falhando → investigar ignição
    @Rule(Fact(falhando="sim"))
    def flex_falhando(self):
        """Pergunta sobre sintomas de falha de ignição."""
        resp = self._perguntar_seguro(
            "A falha ocorre mais forte ao acelerar?",
            ["sim", "nao"]
        )
        self.declare(Fact(falha_acelerar=resp))

    @Rule(Fact(falhando="sim"), Fact(falha_acelerar="sim"))
    def flex_bobina_vela(self):
        """Diagnóstico: Bobina ou velas."""
        self._mostrar_seguro("Diagnóstico: Possível falha na bobina de ignição ou velas de ignição.")
        self._mostrar_seguro("Instrução: Leve a uma mecânica para verificar faísca, cabos, velas e bobina.")
        self.halt()

    # Falhando, mas não apenas acelerando → sensor MAP/MAF ou corpo de borboleta
    @Rule(Fact(falhando="sim"), Fact(falha_acelerar="nao"))
    def flex_marcha_lenta_irregular(self):
        """Pergunta sobre corpo de borboleta."""
        resp = self._perguntar_seguro(
            "A marcha lenta sobe e desce sozinha?",
            ["sim", "nao"]
        )
        self.declare(Fact(oscilando=resp))

    @Rule(Fact(oscilando="sim"))
    def flex_corpo_borboleta(self):
        """Diagnóstico: Corpo de borboleta ou IAC."""
        self._mostrar_seguro("Diagnóstico: Corpo de borboleta sujo ou atuador de marcha lenta (IAC) com defeito.")
        self._mostrar_seguro("Instrução: Leve a uma mecânica para realizar uma limpeza do corpo de borboleta e adaptação no scanner.")
        self.halt()

    @Rule(Fact(oscilando="nao"))
    def flex_sensor_map(self):
        """Diagnóstico: Sensor MAP/MAF."""
        self._mostrar_seguro("Diagnóstico: Possível falha no sensor MAP/MAF.")
        self._mostrar_seguro("Instrução: Leve a uma oficina para teste de pressão e leitura do sensor com scanner.")
        self.halt()

    # Se NÃO está falhando → investigar combustível e bomba
    @Rule(Fact(falhando="nao"))
    def flex_sem_falha(self):
        """Pergunta sobre combustível suspeito."""
        resp = self._perguntar_seguro(
            "Você abasteceu em um posto DUVIDOSO recentemente?",
            ["sim", "nao"]
        )
        self.declare(Fact(comb_suspeito=resp))

    @Rule(Fact(comb_suspeito="sim"))
    def flex_combustivel_ruim(self):
        """Diagnóstico: Combustível adulterado."""
        self._mostrar_seguro("Diagnóstico: Combustível adulterado ou com excesso de etanol/água.")
        self._mostrar_seguro("Instrução: Rode até quase esvaziar e reabasteça com combustível de boa procedência.")
        self._mostrar_seguro("Se não melhorar: drene o tanque e limpe os bicos injetores.")
        self.halt()

    @Rule(Fact(comb_suspeito="nao"))
    def flex_verificar_bomba(self):
        """Pergunta sobre perda de força."""
        resp = self._perguntar_seguro(
            "O carro perde força em subidas ou acima de 80 km/h?",
            ["sim", "nao"]
        )
        self.declare(Fact(perdendo_forca=resp))

    @Rule(Fact(perdendo_forca="sim"))
    def flex_bomba_fraca(self):
        """Diagnóstico: Bomba fraca ou filtro obstruído."""
        self._mostrar_seguro("Diagnóstico: Bomba de combustível fraca ou filtro de combustível obstruído.")
        self._mostrar_seguro("Instrução: Leve a uma mecânica para medir a pressão da linha no scanner/manômetro e substituir filtro se necessário.")
        self.halt()

    # Se nada disso → sensores de forma geral
    @Rule(Fact(perdendo_forca="nao"))
    def flex_sonda_lambda(self):
        """Pergunta sobre consumo alto."""
        resp = self._perguntar_seguro(
            "O consumo aumentou significativamente?",
            ["sim", "nao"]
        )
        self.declare(Fact(consumo_alto=resp))

    @Rule(Fact(consumo_alto="sim"))
    def flex_sonda_lambda_falha(self):
        """Diagnóstico: Sonda lambda."""
        self._mostrar_seguro("Diagnóstico: Sonda lambda com falha (mistura rica/pobre).")
        self._mostrar_seguro("Instrução: Teste e substitua se necessário. Caso não saiba como testar leve a uma mecânicapara realiza-los.")
        self.halt()

    @Rule(Fact(consumo_alto="nao"))
    def flex_sensor_temperatura(self):
        """Diagnóstico: Sensor de temperatura do motor."""
        self._mostrar_seguro("Diagnóstico: Sensor de temperatura do motor (CTS) defeituoso.")
        self._mostrar_seguro("Instrução: Leve a uma mecânica para passsar um scanner para verificar e substituir se necessário.")
        self.halt()


    # ===========================================================================
    # 8. LUZ DO AIRBAG
    # ===========================================================================

    @Rule(Luz(tipo="airbag"), NOT(Airbag(colisao=W())))
    def airbag_colisao(self):
        """Pergunta se o carro sofreu colisão leve recentemente."""
        resp = self._perguntar_seguro(
            "O carro já sofreu alguma colisão leve recentemente?",
            ["sim", "nao"]
        )
        self.declare(Airbag(colisao=resp))

    @Rule(Airbag(colisao="sim"))
    def airbag_modulo_travado(self):
        """Diagnóstico: Módulo do airbag travado após impacto."""
        self._mostrar_seguro("Diagnóstico: O módulo do airbag está travado após o impacto.")
        self._mostrar_seguro("Instrução: Leve a uma mecânica ou auto center, pois o reparo exige um scanner profissional para resetar o módulo.")
        self.halt()

    @Rule(Airbag(colisao="nao"))
    def airbag_falha_sensor_fiacao(self):
        """Diagnóstico: Falha no sensor do banco ou na fiação."""
        self._mostrar_seguro("Diagnóstico: Falha no sensor do banco ou na fiação do airbag.")
        self._mostrar_seguro("Instrução: Leve a uma oficina especializada em airbag.")
        self.halt()

    # ===========================================================================
    # 9. LUZ DO FAROL ALTO
    # ===========================================================================

    @Rule(Luz(tipo="farol-alto"), NOT(FarolAlto(estado=W())))
    def farol_alto_estado(self):
        """Pergunta se o farol alto está realmente ligado."""
        resp = self._perguntar_seguro(
            "O farol alto está realmente ligado?",
            ["sim", "nao"]
        )
        self.declare(FarolAlto(estado=resp))

    @Rule(FarolAlto(estado="sim"))
    def farol_alto_ativado(self):
        """Informação: Farol alto ativado."""
        self._mostrar_seguro("Informação: O farol alto está ativado.")
        self.halt()

    @Rule(FarolAlto(estado="nao"))
    def farol_alto_mau_contato(self):
        """Diagnóstico: Sensor/comutador do farol com mau contato."""
        self._mostrar_seguro("Diagnóstico: Sensor/comutador do farol está com mau contato.")
        self._mostrar_seguro("Instrução: Leve a uma autoelétrica para fazer uma revisão da chave de seta.")
        self.halt()

    # ===========================================================================
    # 10. LUZ DA SETA/PISCA
    # ===========================================================================

    @Rule(Luz(tipo="seta"), NOT(Seta(lanternas=W())))
    def seta_lanternas(self):
        """Pergunta se todas as lanternas (setas) estão piscando normalmente."""
        resp = self._perguntar_seguro(
            "Todas as lanternas (setas) estão piscando normalmente?",
            ["sim", "nao"]
        )
        self.declare(Seta(lanternas=resp))

    @Rule(Seta(lanternas="sim"))
    def seta_lampada_queimada(self):
        """Diagnóstico: Lâmpada da seta queimada."""
        self._mostrar_seguro("Diagnóstico: Lâmpada da seta queimada.")
        self._mostrar_seguro("Instrução: Substitua a lâmpada queimada da lanterna correspondente.")
        self.halt()

    @Rule(Seta(lanternas="nao"))
    def seta_falha_rele_modulo(self):
        """Diagnóstico: Possível falha no relê, interruptor ou módulo de controle."""
        self._mostrar_seguro("Diagnóstico: Possível falha no relê (pisca-pisca), interruptor ou módulo de controle.")
        self._mostrar_seguro("Instrução: Leve a uma oficina autoelétrica para o diagnóstico preciso.")
        self.halt()

    # ===========================================================================
    # 11. LUZ DE PORTA ABERTA
    # ===========================================================================

    @Rule(Luz(tipo="porta"), NOT(Porta(fechamento=W())))
    def porta_fechamento(self):
        """Pergunta se todas as portas e o portamalas estão totalmente fechados."""
        resp = self._perguntar_seguro(
            "Todas as portas e o portamalas estão totalmente fechados?",
            ["sim", "nao"]
        )
        self.declare(Porta(fechamento=resp))

    @Rule(Porta(fechamento="nao"))
    def porta_fechar(self):
        """Instrução para fechar firmemente os compartimentos."""
        self._mostrar_seguro("Ação: Feche firmemente todos os compartimentos.")
        self.halt()

    @Rule(Porta(fechamento="sim"), NOT(Porta(persistencia=W())))
    def porta_persistencia(self):
        """Pergunta se o aviso permanece aceso com tudo fechado."""
        resp = self._perguntar_seguro(
            "O aviso permanece aceso com tudo fechado?",
            ["sim", "nao"]
        )
        self.declare(Porta(persistencia=resp))

    @Rule(Porta(persistencia="sim"))
    def porta_falha_sensor_trava(self):
        """Diagnóstico: Provável falha no sensor ou na trava elétrica de uma porta."""
        self._mostrar_seguro("Diagnóstico: Provável falha no sensor ou na trava elétrica de uma porta.")
        self._mostrar_seguro("Instrução: Leve o veículo a uma oficina para diagnóstico e reparo do sistema.")
        self.halt()
        
    @Rule(Porta(fechamento="sim"), Porta(persistencia="nao"))
    def porta_normal(self):
        """Caso o aviso não persista, o sistema está normal."""
        self._mostrar_seguro("O aviso apagou com tudo fechado. Sistema funcionando normalmente.")
        self.halt()

    # ===========================================================================
    # 12. LUZ DO FREIO DE MÃO 
    # ===========================================================================

    @Rule(Luz(tipo="freio-mao"), NOT(FreioMao(acionado=W())))
    def freio_mao_acionado(self):
        """Pergunta se o freio de mão está acionado."""
        resp = self._perguntar_seguro(
            "O freio de mão está acionado?",
            ["sim", "nao"]
        )
        self.declare(FreioMao(acionado=resp))

    @Rule(FreioMao(acionado="sim"))
    def freio_mao_liberar(self):
        """Instrução para liberar o freio de mão."""
        self._mostrar_seguro("Ação: Libere completamente o freio de mão.")
        self.halt()

    @Rule(FreioMao(acionado="nao"))
    def freio_mao_falha_sensor(self):
        """Diagnóstico: Provável falha no sensor ou no próprio freio de mão."""
        self._mostrar_seguro("Diagnóstico: Provável falha no sensor ou no próprio freio de mão.")
        self._mostrar_seguro("Instrução: Leve o veículo a uma oficina para diagnóstico e reparo do sistema.")
        self.halt()
