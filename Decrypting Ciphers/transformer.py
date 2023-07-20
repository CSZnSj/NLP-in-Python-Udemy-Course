class TextTransformer():
    
    def encode_tokens(tokens: list, mapping):
        result = ["".join(mapping.get(char, char) for char in token) for token in tokens]
        return result
    
    def decode_tokens(tokens: list, mapping: dict):
        result = ["".join(mapping.get(char, char) for char in token) for token in tokens]
        return result