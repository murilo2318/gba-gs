"""
Roda todos os exportadores do painel GBA em sequencia, gerando/atualizando
todos os arquivos de dados_integrados/*.json.

Uso:
    python3.13 painel_gba/exportadores/exportar_todos.py
"""
import exportar_orbital_rpa
import exportar_astroguard
import exportar_neurospace_alert
import exportar_quantica_mythos
import exportar_wildfire_vc
import exportar_agrosentinel
import exportar_rag_espacial
import exportar_rag_net_zero

EXPORTADORES = [
    exportar_orbital_rpa,
    exportar_astroguard,
    exportar_neurospace_alert,
    exportar_quantica_mythos,
    exportar_wildfire_vc,
    exportar_agrosentinel,
    exportar_rag_espacial,
    exportar_rag_net_zero,
]


def main():
    print("Exportando dados de todos os modulos para dados_integrados/...\n")
    for modulo in EXPORTADORES:
        try:
            modulo.main()
        except Exception as erro:
            print(f"[erro] {modulo.__name__}: {erro}")
    print("\nConcluido.")


if __name__ == "__main__":
    main()
