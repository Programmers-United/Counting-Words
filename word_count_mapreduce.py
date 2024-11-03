import threading
import os
import glob

# Função Map que gera arquivos temporários
def map_function(file_part, output_dir):
    word_count = {}
    
    # Abrir a parte do arquivo e contar as palavras
    with open(file_part, 'r') as f:
        for line in f:
            words = line.split()
            for word in words:
                if word not in word_count:
                    word_count[word] = 1
                else:
                    word_count[word] += 1

    # Gravar o resultado em um arquivo temporário
    with open(os.path.join(output_dir, f"map_{os.path.basename(file_part)}.txt"), 'w') as f_out:
        for word, count in word_count.items():
            f_out.write(f"{word}: {count}\n")

# Função Reduce que lê os arquivos temporários e consolida as contagens
def reduce_function(output_dir):
    word_count = {}

    # Lê todos os arquivos temporários gerados pela função Map
    for temp_file in glob.glob(os.path.join(output_dir, "map_*.txt")):
        with open(temp_file, 'r') as f:
            for line in f:
                word, count = line.strip().split(": ")
                if word in word_count:
                    word_count[word] += int(count)
                else:
                    word_count[word] = int(count)

    # Imprimir os resultados finais
    for word, count in word_count.items():
        print(f"Reduce({word}) -> {count}")

# Controlador que gerencia as threads de Map e Reduce
def controller(input_files, output_dir):
    map_threads = []

    # Criar diretório para arquivos temporários, se não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Executa a função Map em threads separadas
    for file_part in input_files:
        t = threading.Thread(target=map_function, args=(file_part, output_dir))
        map_threads.append(t)
        t.start()

    # Espera todas as threads Map terminarem
    for t in map_threads:
        t.join()

    # Executa a função Reduce em uma thread
    reduce_thread = threading.Thread(target=reduce_function, args=(output_dir,))
    reduce_thread.start()
    reduce_thread.join()

    # Limpar arquivos temporários
    for temp_file in glob.glob(os.path.join(output_dir, "map_*.txt")):
        os.remove(temp_file)

# Exemplo de uso
if __name__ == "__main__":
    # Diretório onde os arquivos de teste estão localizados
    test_files_dir = 'test_files'
    output_dir = 'temp_dir'

    # Obter os arquivos gerados pelo FileGenerator
    input_files = [os.path.join(test_files_dir, f) for f in os.listdir(test_files_dir) if f.endswith('.txt')]

    # Executar o controlador MapReduce com os arquivos gerados
    controller(input_files, output_dir)
