import threading
import os

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
    with open(os.path.join(output_dir, 'arq.tmp'), 'a') as f_out:
        for word, count in word_count.items():
            f_out.write(f"{word} {count}\n")
            
# Função Reduce que lê os arquivos temporários e consolida as contagens
def reduce_function(key, value):
    arq_final = open('arqfinal', 'a')
    arq_final.write(f"{key} {sum(value)}\n")
    arq_final.close()

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

    # Agrupar os resultados do arquivo temporário
    agrupamento = {}
    tmp = open(os.path.join(output_dir, 'arq.tmp'), 'r')
    for line in tmp:
        key, value = line.split()
        if key in agrupamento:
            agrupamento[key].append(int(value))
        else:
            agrupamento[key] = [int(value)]
    
    tmp.close()

    # Executar a função Reduce em threads separadas para cada chave
    reduce_threads = []
    for key in agrupamento.keys():
        t = threading.Thread(target=reduce_function, args=(key, agrupamento[key]))
        reduce_threads.append(t)
        t.start()

    # Espera todas as threads Reduce terminarem
    for t in reduce_threads:
        t.join()

# Exemplo de uso
if __name__ == "__main__":
    # Diretório onde os arquivos de teste estão localizados
    test_files_dir = 'test_files'
    output_dir = 'temp_dir'

    # Obter os arquivos gerados pelo FileGenerator
    input_files = [os.path.join(test_files_dir, f) for f in os.listdir(test_files_dir) if f.endswith('.txt')]
    print(input_files)

    # Executar o controlador MapReduce com os arquivos gerados
    controller(input_files, output_dir)
