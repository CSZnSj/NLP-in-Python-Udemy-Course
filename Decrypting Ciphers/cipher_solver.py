from text_tools import TextTools
from transformer import TextTransformer

class CipherSolver:
    
    def get_instance(file_name):
        text = TextTools.get_text(file_name)
        tt = TextTools.get_instance(text)
        solver = CipherSolver(tt)
        return solver
    
    def __init__(self, text_tools: TextTools, num_iterations: int = 1000):
        self.tt = text_tools
        self.num_iterations = num_iterations
    
    def solve(self, encoded_tokens: list[str], num_iterations: int = None) -> list[str]:
        """Solves the substitution cipher for the given encoded tokens by finding the best mapping using the `evolve_best_dna` method of the `DNAPoolEvolver` class and then decoding the tokens using the best mapping."""
        if num_iterations is None:
            num_iterations = self.num_iterations
        best_mapping = self.tt.evolver.evolve_best_dna(encoded_tokens, self.tt.calc, num_iterations)
        result = TextTransformer.decode_tokens(encoded_tokens, best_mapping)
        return result