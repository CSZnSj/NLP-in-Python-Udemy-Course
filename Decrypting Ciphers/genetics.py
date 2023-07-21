import string
import random

class DNA:
    """
    Class representing a DNA code, which is a mapping of characters.
    """

    @staticmethod
    def _create_random_dna() -> dict:
        """
        Generates a random DNA code by shuffling the lowercase letters of the alphabet.

        Returns:
            dict: A random DNA code represented as a mapping of characters.
        """
        letters1 = list(string.ascii_lowercase)
        letters2 = list(string.ascii_lowercase)
        random.shuffle(letters2)
        result = dict(zip(letters1, letters2))
        return result

    @staticmethod
    def generate_dna_pool(number: int = 20) -> list[dict]:
        """
        Generates a pool of random DNA codes.

        Args:
            number (int): Number of DNA codes to generate.

        Returns:
            list[dict]: A list of randomly generated DNA codes represented as mappings of characters.
        """
        return [DNA._create_random_dna() for _ in range(number)]

    default_dna = _create_random_dna()  # A default random DNA code


class DNAEvolver:
    """
    Class representing the evolution of DNA codes.
    """

    @staticmethod
    def _evolve_dna(dna: dict) -> dict:
        """
        Performs a single evolution step on a given DNA code.

        Args:
            dna (dict): The DNA code represented as a mapping of characters.

        Returns:
            dict: The evolved DNA code represented as a mapping of characters.
        """
        result = dna.copy()
        keys = random.sample(result.keys(), 2)
        key_i, key_j = keys[0], keys[1]
        result[key_i], result[key_j] = result[key_j], result[key_i]
        return result

    @staticmethod
    def evolve_dna_pool(dna_pool: list[dict], num_offspring: int = 4) -> list[dict]:
        """
        Evolves a pool of DNA codes by applying evolution steps on each code multiple times.

        Args:
            dna_pool (list[dict]): A list of DNA codes represented as mappings of characters.
            num_offspring (int): Number of offspring per DNA code to generate during evolution.

        Returns:
            list[dict]: The evolved pool of DNA codes represented as mappings of characters.
        """
        return [DNAEvolver._evolve_dna(dna) for dna in dna_pool for _ in range(num_offspring)]


class DNASearcher:
    """
    Class responsible for searching and finding the best DNA code for a given problem.
    """

    @staticmethod
    def _get_top_dnas(dna_score_list: list[tuple[dict, float]], n: int = 5) -> list[dict]:
        """
        Extracts the top 'n' DNA codes based on their scores.

        Args:
            dna_score_list (list[tuple[dict, float]]): A list of DNA codes and their corresponding scores.
            n (int): Number of top DNA codes to extract.

        Returns:
            list[dict]: The top 'n' DNA codes represented as mappings of characters.
        """
        sorted_dna_score_list = sorted(dna_score_list, key=lambda x: x[1], reverse=True)
        top_dnas = [x[0] for x in sorted_dna_score_list[:n]]
        return top_dnas

    @staticmethod
    def get_best_dna(encoded_tokens: list[str], calc, num_iterations: int) -> dict:
        """
        Finds the best DNA code that produces the highest score after a certain number of iterations.

        Args:
            encoded_tokens (list[str]): The encoded tokens to decode using the DNA codes.
            calc: The scoring function to evaluate the decoded tokens.
            num_iterations (int): Number of iterations to evolve the DNA codes.

        Returns:
            dict: The best DNA code represented as a mapping of characters.
        """
        from tools import Tools
        dna_pool = DNA.generate_dna_pool()
        for i in range(num_iterations):
            if i > 0:
                dna_pool = DNAEvolver.evolve_dna_pool(dna_pool)
            dna_score_list = []
            for dna in dna_pool:
                decoded_tokens = Tools.decode_tokens(encoded_tokens, dna)
                score = calc.get_prob(decoded_tokens)
                dna_score_list.append((dna, score))
            dna_pool = DNASearcher._get_top_dnas(dna_score_list)

        return dna_pool[0]
