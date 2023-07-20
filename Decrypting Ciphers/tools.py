import re
from genetics import DNA, DNASearcher

class Tools:
    
    @staticmethod
    def read_file(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            text = f.read()
        return text

    @staticmethod
    def tokenize(text: str) -> list[str]:
        
        # Compile a regular expression to replace non-alpha characters
        regex = re.compile('[^a-zA-Z]')

        # Replace all non-alpha characters with space
        text = regex.sub(' ', text)

        # Split the text into tokens and lowercase them
        tokens = text.lower().split()

        return tokens
    
    @staticmethod
    def encode_tokens(tokens: list, mapping = None):
        if mapping is None:
            mapping = DNA.default_dna
        result = ["".join(mapping.get(char, char) for char in token) for token in tokens]
        return result
    
    @staticmethod
    def decode_tokens(tokens: list, mapping: dict):
        result = ["".join(mapping.get(char, char) for char in token) for token in tokens]
        return result

    
    @staticmethod
    def solve(calculator, encoded_tokens: list[str], num_iterations: int = None) -> list[str]:
        if num_iterations is None:
            num_iterations = 1000
        best_mapping = DNASearcher.get_best_dna(encoded_tokens, calculator, num_iterations)
        return best_mapping
    
    @staticmethod
    def str_decoded_tokens(tokens: list[str]):
         return " ".join(tokens)
