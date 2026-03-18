import time
import sys

def soma_serial(arquivo):
    inicio = time.perf_counter()

    soma  = 0
    count = 0
    with open(arquivo, "r") as f:
        for linha in f:
            linha = linha.strip()
            if linha:
                soma  += int(linha)
                count += 1

    fim   = time.perf_counter()
    tempo = fim - inicio

    print("=== SOMA SERIAL (Python) ===")
    print(f"Arquivo     : {arquivo}")
    print(f"Linhas lidas: {count}")
    print(f"Soma total  : {soma}")
    print(f"Tempo (s)   : {tempo:.4f}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python soma_serial.py <arquivo>")
        sys.exit(1)
    soma_serial(sys.argv[1])
