from regras import *

""" ----------------------- Função Principal ----------------------- """
if __name__ == "__main__":
    engine = SistemaEspecialista()
    engine.reset()

    print("=== SISTEMA ESPECIALISTA ===")
    tipo = input("Qual luz acendeu? (bateria/oleo/temperatura/freio/cinto): ")

    engine.declare(Luz(tipo=tipo))
    engine.run()
