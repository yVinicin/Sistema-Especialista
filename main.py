from rules import Diagnostico, LuzesPainel
from experta import Fact

def executar_diagnostico(luzes_acesas):
    """
    Executa o diagnóstico baseado na luz da bateria acesa.
    luzes_acesas: dicionário com chave 'bateria' booleana (ex.: {'bateria': True})
    Retorna uma lista de dicionários com ações, prioridades e explicações.
    """
    engine = Diagnostico()
    engine.reset()

    # Declarar fatos baseados nas luzes acesas
    engine.declare(LuzesPainel(**luzes_acesas))



    # Executar inferência
    engine.run()

    # Coletar ações dos fatos declarados, organizando por prioridade
    diagnosticos = []
    for fact in engine.facts.values():
        if 'acao' in fact:
            diagnostico = {
                'acao': fact['acao'],
                'prioridade': fact.get('prioridade', 'baixa'),
                'explicacao': fact.get('explicacao', 'Diagnóstico baseado em regras especializadas.'),
                'passos': fact.get('passos', [])
            }
            diagnosticos.append(diagnostico)

    # Ordenar por prioridade (critica > alta > media > baixa)
    prioridade_ordem = {'critica': 4, 'alta': 3, 'media': 2, 'baixa': 1}
    diagnosticos.sort(key=lambda x: prioridade_ordem.get(x['prioridade'], 0), reverse=True)

    return diagnosticos

def formatar_diagnostico_para_usuario(diagnosticos):
    """
    Formata os diagnósticos para exibição amigável ao usuário, incluindo passos interativos.
    """
    if not diagnosticos:
        return "Nenhuma luz acesa detectada. Verifique se o painel está funcionando corretamente."

    resultado = ""
    for diag in diagnosticos:
        prioridade_emoji = {
            'critica': 'EMERGÊNCIA',
            'alta': 'URGENTE',
            'media': 'ATENÇÃO',
            'baixa': 'INFORMATIVO'
        }.get(diag['prioridade'], 'ℹ️')

        resultado += f"**{prioridade_emoji}**\n"
        resultado += f"**Ação Recomendada:** {diag['acao']}\n"
        if 'passos' in diag and diag['passos']:
            resultado += "**Passos para diagnóstico:**\n"
            for passo in diag['passos']:
                resultado += f"  - {passo}\n"
        resultado += f"**Por que isso acontece:** {diag['explicacao']}\n\n"

    return resultado.strip()

if __name__ == "__main__":
    # Exemplo de uso direto (para testes)
    luzes_exemplo = {'bateria': True}
    diagnosticos = executar_diagnostico(luzes_exemplo)
    print("Diagnósticos recomendados:")
    print(formatar_diagnostico_para_usuario(diagnosticos))
