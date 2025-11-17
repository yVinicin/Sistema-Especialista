from experta import *

class LuzesPainel(Fact):
    """Fato que representa as luzes acesas no painel do carro."""
    pass

class SintomasAdicionais(Fact):
    """Fato para sintomas adicionais como dificuldade para ligar."""
    pass

class Diagnostico(KnowledgeEngine):
    """Motor de inferência para diagnosticar problemas com base na luz da bateria e sintomas adicionais."""

    @Rule(LuzesPainel(bateria=True), salience=9)
    def luz_bateria(self):
        """Regra para luz de bateria acesa com passos simples para leigos."""
        passos = [
            "Passo 1: Abra o capô e procure a bateria (uma caixa preta grande com dois cabos).",
            "Passo 2: Veja se os cabos estão bem presos nos bornes (as pontas da bateria). Se estiverem frouxos, aperte bem.",
            "Passo 3: Olhe se tem uma crosta branca nos bornes. Se tiver, limpe com uma escova ou pano molhado em água com bicarbonato.",
            "Passo 4: Tente ligar o carro. Se não ligar, a bateria pode estar fraca - leve para trocar em uma loja de auto-peças.",
            "Passo 5: Se ligar mas a luz fica acesa, pode ser o alternador (a peça que carrega a bateria) com problema."
        ]
        self.declare(Fact(acao="A luz da bateria acendeu! Isso significa problema na parte elétrica. Faça assim:", prioridade="media", explicacao="Essa luz avisa quando a bateria ou o sistema de carregamento está com problema. Sem eletricidade, o carro não funciona!", passos=passos))

    @Rule(LuzesPainel(bateria=True), SintomasAdicionais(dificuldade_ligar=True), salience=9)
    def bateria_dificuldade_ligar(self):
        """Bateria com dificuldade para ligar com linguagem simples."""
        self.declare(Fact(acao="Sua bateria está fraca ou descarregada. Tente carregar com um carregador externo ou trocar a bateria. Verifique se o alternador está funcionando.", prioridade="alta", explicacao="Esse sintoma confirma que tem problema na parte elétrica, talvez na bateria ou no sistema que carrega ela."))
