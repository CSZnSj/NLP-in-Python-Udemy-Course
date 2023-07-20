import random
import string

class DNA:
    
    @staticmethod
    def _create_random_dna(random_seed: int = 13) -> dict:
        letters1 = list(string.ascii_lowercase)
        letters2 = list(string.ascii_lowercase)
        random.seed(random_seed)
        random.shuffle(letters2)
        result = dict(zip(letters1, letters2))
        return result

    @staticmethod
    def generate_dna_pool(number: int = 20) -> list[dict]:
        pool = []
        for _ in range(number):
            random_seed = random.randint(0, 1000)
            dna = DNA._create_random_dna(random_seed)
            pool.append(dna)
        return pool
    
    @staticmethod
    def _evolve_dna(dna: dict) -> dict:
        result = dna.copy()
        keys = list(result.keys())
        n = len(keys)
        i, j = random.randrange(n), random.randrange(n)
        key_i, key_j = keys[i], keys[j]
        result[key_i], result[key_j] = result[key_j], result[key_i]
        return result

    @staticmethod
    def evolve_dna_pool(dna_pool: list[dict], num_offspring: int = 4) -> list[dict]:
        pool = []
        for dna in dna_pool:
            for _ in range(num_offspring):
                evolved_dna = DNA._evolve_dna(dna)
                pool.append(evolved_dna)
        return pool + dna_pool

    default_dna = _create_random_dna()

class DNASearcher:

    @staticmethod
    def _get_top_dnas(dna_score_list: list[tuple[dict, float]], n: int = 5) -> list[dict]:
        sorted_dna_score_list = sorted(dna_score_list, key=lambda x: x[1], reverse=True)
        top_dnas = [x[0] for x in sorted_dna_score_list[:n]]
        return top_dnas

    @staticmethod
    def get_best_dna(encoded_tokens: list[str], calc, num_iterations: int) -> dict:
        from tools import Tools
        dna_pool = DNA.generate_dna_pool()
        for i in range(num_iterations):
            if i > 0:
                dna_pool = DNA.evolve_dna_pool(dna_pool)
            dna_score_list = []
            for dna in dna_pool:
                decoded_tokens = Tools.decode_tokens(encoded_tokens, dna)
                score = calc.calculate_prob(decoded_tokens)
                dna_score_list.append((dna, score))
            dna_pool = DNASearcher._get_top_dnas(dna_score_list)
        return dna_pool[0]