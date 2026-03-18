import time, sys, os, multiprocessing as mp

def encontrar_inicio_linha(arquivo, offset):
    """Retorna o offset do início da próxima linha completa a partir de offset."""
    if offset == 0:
        return 0
    with open(arquivo, "rb") as f:
        f.seek(offset)
        f.readline()          # descarta linha parcial
        return f.tell()       # agora estamos no início de uma linha completa

def somar_trecho(arquivo, byte_ini, byte_fim, fila):
    soma  = 0
    BLOCO = 8 * 1024 * 1024

    with open(arquivo, "rb") as f:
        f.seek(byte_ini)
        resto = b""

        while f.tell() < byte_fim:
            a_ler = min(BLOCO, byte_fim - f.tell())
            chunk = f.read(a_ler)
            if not chunk:
                break
            partes = (resto + chunk).split(b"\n")
            resto  = partes[-1]
            for p in partes[:-1]:
                s = p.strip()
                if s:
                    soma += int(s)

        if resto.strip():
            soma += int(resto.strip())

    fila.put(soma)

def soma_gigante(arquivo, num_proc):
    tamanho = os.path.getsize(arquivo)

    # Calcula offsets exatos no início de linhas completas
    chunk    = tamanho // num_proc
    offsets  = []
    for i in range(num_proc):
        ini = encontrar_inicio_linha(arquivo, i * chunk)
        fim = encontrar_inicio_linha(arquivo, (i+1) * chunk) if i < num_proc-1 else tamanho
        offsets.append((ini, fim))

    print("=== SOMA GIGANTE (Python multiprocessing) ===")
    print(f"Arquivo    : {arquivo}")
    print(f"Processos  : {num_proc}")

    inicio    = time.perf_counter()
    fila      = mp.Queue()
    processos = []

    for ini, fim in offsets:
        p = mp.Process(target=somar_trecho, args=(arquivo, ini, fim, fila))
        processos.append(p)
        p.start()

    for p in processos:
        p.join()

    soma_total = sum(fila.get() for _ in range(num_proc))
    tempo      = time.perf_counter() - inicio

    print(f"Soma total : {soma_total}")
    print(f"Tempo (s)  : {tempo:.2f}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python soma_gigante.py <arquivo> <num_processos>")
        sys.exit(1)
    soma_gigante(sys.argv[1], int(sys.argv[2]))
