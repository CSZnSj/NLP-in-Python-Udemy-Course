#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from collections import Counter

class TextCounter:
    
    def get_instance(train_tokens):
        return TextCounter(train_tokens)
    
    def __init__(self, train_tokens: list[str]):
        self.tokens = train_tokens
        self.char_count = self._count_chars()
        self.char_pair_count = self._count_char_pairs()
        self.n_chars = sum(self.char_count.values())
        self.v_chars = len(self.char_count)

        
    def _count_chars(self):
        return Counter(char for token in self.tokens for char in token)
    
    def _count_char_pairs(self):
        return Counter(pair for token in self.tokens for pair in zip(token, token[1:]))
       
    def occurrences_char(self, char: str) -> int:
        return self.char_count.get(char, 0)
   
    def occurrences_char_pair(self, char_pair: str) -> int:
        return self.char_pair_count.get(char_pair, 0)


# In[ ]:


from math import log
class ProbabilityCalculator:
    
    def get_instance(counter):
        return ProbabilityCalculator(counter)
    
    def __init__(self, counter):
        self.counter = counter
        self.k = 0.1   
        
    def _probability_of_char(self, char: str) -> float:
        char_occurrences = self.counter.occurrences_char(char)
        return log((char_occurrences + self.k) / (self.counter.n_chars + self.k * self.counter.v_chars))
    
    def _probability_of_char_pair(self, char_pair: tuple[str, str]) -> float:
        char_pair_occurrences = self.counter.occurrences_char_pair(char_pair)
        pre_occurrences = self.counter.occurrences_char(char_pair[0])
        return log((char_pair_occurrences + self.k) / (pre_occurrences + self.k * self.counter.v_chars))
    
    def _probability_of_token(self, token: str) -> float:
        probability = self._probability_of_char(token[0])
        for i in range(1, len(token)):
            char_pair = (token[i-1], token[i])
            probability += self._probability_of_char_pair(char_pair)
        return probability
    
    def calculate_prob(self, tokens: list[str]) -> float:
        token_probs = [self._probability_of_token(token) for token in tokens]
        return sum(token_probs)

