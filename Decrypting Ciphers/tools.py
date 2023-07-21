import re
from probability import ProbabilityCalculator
from genetics import DNA, DNASearcher

class Tools:
    """
    Utility class containing helper methods for text processing and DNA mapping.
    """
    
    @staticmethod
    def read_file(file_name: str) -> str:
        """
        Reads the content of a file and returns it as a string.

        Args:
            file_name (str): The name of the file to read.

        Returns:
            str: The content of the file as a string.
        """
        with open(file_name, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    @staticmethod
    def tokenize(text: str) -> list[str]:
        """
        Tokenizes the input text by splitting it into lowercase alphabetic tokens.

        Args:
            text (str): The input text to be tokenized.

        Returns:
            list[str]: A list of lowercase alphabetic tokens.
        """
        # Compile a regular expression to replace non-alpha characters
        regex = re.compile('[^a-zA-Z]')

        # Replace all non-alpha characters with space
        text = regex.sub(' ', text)

        # Split the text into tokens and lowercase them
        tokens = text.lower().split()

        return tokens
    
    @staticmethod
    def encode_tokens(tokens: list, mapping=None) -> list[str]:
        """
        Encodes a list of tokens using a given mapping or the default DNA mapping.

        Args:
            tokens (list[str]): A list of tokens to be encoded.
            mapping (dict, optional): The mapping to use for encoding. Defaults to None (uses DNA.default_dna).

        Returns:
            list[str]: A list of encoded tokens.
        """
        if mapping is None:
            mapping = DNA.default_dna
        result = ["".join(mapping.get(char, char) for char in token) for token in tokens]
        return result
    
    @staticmethod
    def decode_tokens(tokens: list[str], mapping: dict) -> list[str]:
        """
        Decodes a list of encoded tokens using a given mapping.

        Args:
            tokens (list[str]): A list of encoded tokens to be decoded.
            mapping (dict): The mapping to use for decoding.

        Returns:
            list[str]: A list of decoded tokens.
        """
        result = ["".join(mapping.get(char, char) for char in token) for token in tokens]
        return result

    @staticmethod
    def solve(calculator: ProbabilityCalculator, encoded_tokens: list[str], num_iterations: int = None) -> dict:
        """
        Solves the optimization problem to find the best DNA mapping that maximizes the probability.

        Args:
            calculator (ProbabilityCalculator): The probability calculator used for evaluating token probabilities.
            encoded_tokens (list[str]): A list of encoded tokens to be decoded.
            num_iterations (int, optional): The number of iterations for the optimization algorithm.
                                            Defaults to None (uses 1000 iterations).

        Returns:
            dict: The best DNA mapping represented as a dictionary.
        """
        if num_iterations is None:
            num_iterations = 1000
        best_mapping = DNASearcher.get_best_dna(encoded_tokens, calculator, num_iterations)
        return best_mapping

    @staticmethod
    def str_decoded_tokens(tokens: list[str]) -> str:
        """
        Converts a list of tokens into a string by joining them with spaces.

        Args:
            tokens (list[str]): A list of tokens to be converted to a string.

        Returns:
            str: The string representation of the tokens.
        """
        return " ".join(tokens)
