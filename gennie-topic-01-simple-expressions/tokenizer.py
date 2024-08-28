 # tokenizer

"""
break character stream into tokens, provide a token stream
"""

import re #regular expression

patterns = [
    ["\\+", "+" ], #if you find a plus, add a plus token
    ["\\-", "-" ]
]

for pattern in patterns:
    pattern[0] = re.compile(pattern[0])

def tokenize(characters):
    tokens = []
    position = 0 #position in string is 0
    while position < len(characters): #we still have a character left to work with
        for pattern, tag in patterns:
            match = pattern.match(characters, position) #if reg ex matches string of characters, we got a match!
            if match:
                break
        assert match
        token = {
            'tag':tag,
            'value': match.group(0),
            'position': position,
        }
        tokens.append(token)
        position = match.end()
    return tokens

def test_simple_tokens():
    print("testing simple tokens")
    assert tokenize("+") == [{'tag': '+', 'value': '+', 'position': 0}]
    assert tokenize("-") == [{'tag': '-', 'value': '-', 'position': 0}]
    i = 0
    for char in "+-*/":
        tokens = tokenize(char)
        print(tokens)
        assert tokens[0]["tag"] == char
        assert tokens[0]["value"] == char
        assert tokens[0]["position"] == i

if __name__ == "__main__": #if this is the main program...
    test_simple_tokens()
    print("done.")