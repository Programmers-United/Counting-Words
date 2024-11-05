import os
import random

class FileGenerator:
    def __init__(self, split, n, alphabet, min_size, max_size):
        self.split = split
        self.n = n
        self.alphabet = alphabet
        self.min_size = min_size
        self.max_size = max_size

    def generate_files(self, output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Gera palavras aleatórias e as divide em arquivos
        words = self._generate_random_words()
        chunk_size = len(words) // self.split

        for i in range(self.split):
            part_words = words[i*chunk_size: (i+1)*chunk_size]
            with open(os.path.join(output_dir, f'file_part{i+1}.txt'), 'w') as f:
                f.write(' '.join(part_words))

    def _generate_random_words(self):
        words = []
        for _ in range(self.n):
            word_length = random.randint(self.min_size, self.max_size)
            word = ''.join(random.choice(self.alphabet) for _ in range(word_length))
            words.append(word)
        return words

# Exemplo de uso do FileGenerator
if __name__ == "__main__":
    file_generator = FileGenerator(
        split=3,              # Dividir o texto em 3 arquivos
        n=100,                # Gerar 100 palavras
        alphabet=['a', 'b', 'c', 'd', 'e'],  # Definir as letras permitidas
        min_size=3,           # Tamanho mínimo de palavras: 3 letras
        max_size=6            # Tamanho máximo de palavras: 6 letras
    )

    # Diretório onde os arquivos serão gerados
    test_files_dir = 'test_files'
    file_generator.generate_files(test_files_dir)
