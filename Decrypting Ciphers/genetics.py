from transformer import TextTransformer
import string
import random

class DNA:
    
    def get_instance():
        return DNA()
    
    def __init__(self):
        self.default_dna = self._create_random_dna()
        
    def _create_random_dna(self, random_seed = 13) -> dict:
        letters1 = list(string.ascii_lowercase)
        letters2 = list(string.ascii_lowercase)
        random.seed(random_seed)
        random.shuffle(letters2)
        result = dict(zip(letters1, letters2))
        return result

    def generate_dna_pool(self, number: int = 20) -> list[dict]:
        pool = []
        for _ in range(number):
            random_seed = random.randint(0, 1000)
            dna = self._create_random_dna(random_seed)
            pool.append(dna)
        return pool

    def _evolve_dna(self, dna: dict) -> dict:
        result = dna.copy()
        keys = list(result.keys())
        n = len(keys)
        i, j = random.randrange(n), random.randrange(n)
        key_i, key_j = keys[i], keys[j]
        result[key_i], result[key_j] = result[key_j], result[key_i]
        return result

    def evolve_dna_pool(self, dna_pool: list[dict], num_offspring: int = 4) -> list[dict]:
        pool = []
        for dna in dna_pool:
            for _ in range(num_offspring):
                evolved_dna = self._evolve_dna(dna)
                pool.append(evolved_dna)
        return pool


class DNAPoolEvolver:
    
    def get_instance(DNA):
        return DNAPoolEvolver(DNA)
    
    def __init__(self, DNA: DNA):
        self.DNA = DNA

    def _select_best_dnas(self, scores: list[tuple[dict, float]], n: int = 5) -> list[dict]:
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        best_dnas = [x[0] for x in sorted_scores[:n]]
        return best_dnas

    def _evolve_dna_pool(self, dna_pool: list[dict]) -> list[dict]:
        evolved_pool = []
        for dna in dna_pool:
            offspring = self.DNA.evolve_dna_pool([dna])
            evolved_pool.extend(offspring)
        return evolved_pool

    def evolve_best_dna(self, encoded_tokens: list[str], calc,
                        num_iterations: int) -> dict:
        dna_pool = self.DNA.generate_dna_pool()
        for i in range(num_iterations):
            if i > 0:
                dna_pool = self._evolve_dna_pool(dna_pool)
            scores = []
            for dna in dna_pool:
                decoded_tokens = TextTransformer.decode_tokens(encoded_tokens, dna)
                score = calc.calculate_prob(decoded_tokens)
                scores.append((dna, score))
            dna_pool = self._select_best_dnas(scores, 5)
        return dna_pool[0]

