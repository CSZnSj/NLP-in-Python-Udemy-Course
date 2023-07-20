#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


# In[ ]:


import re
def tokenize(text: str) -> list:
    """Processes the text in the given file and returns a list of tokens."""
    # Compile a regular expression to replace non-alpha characters
    regex = re.compile('[^a-zA-Z]')
    
    # Replace all non-alpha characters with space
    text = regex.sub(' ', text)
    
    # Split the text into tokens and lowercase them
    tokens = text.lower().split()
    
    return tokens

