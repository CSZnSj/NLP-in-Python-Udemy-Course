from file_processing import read_file, tokenize
from probability import TextCounter, ProbabilityCalculator
from transformer import TextTransformer
from genetics import DNA, DNAPoolEvolver

class TextTools:
    
    def get_instance(text):
        return TextTools(text)

    def __init__ (self, text: str):
        tokens = tokenize(text)
        self.counter = TextCounter.get_instance(tokens)
        self.calc = ProbabilityCalculator.get_instance(self.counter)
        self.DNA = DNA.get_instance()
        self.evolver = DNAPoolEvolver.get_instance(self.DNA)
        
    def get_text(file_name):
        return read_file(file_name)

    def get_encoded_tokens(text: str, mapping=None):
        if mapping is None:
            mapping = DNA.get_instance().default_dna
        tokens = tokenize(text)
        encoded_tokens = TextTransformer.encode_tokens(tokens, mapping)
        return encoded_tokens