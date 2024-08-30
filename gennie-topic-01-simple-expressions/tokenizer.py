 # tokenizer

"""
break character stream into tokens, provide a token stream
"""

import re #regular expressions

patterns = [
    ["\\(", "("], #if you find an open parathesis, add an open parathesis
    ["\\)", ")"],
    ["\\+", "+" ], #if you find a plus, add a plus token
    ["\\-", "-" ],
    ["\\*", "*"],
    ["\\/", "/"],
    ["(\\d+\\.\\d*)|(\\d*\\.\\d+)|(\\d+)", "number"] #if you find a floating point #, add a floating point #
]

for pattern in patterns: #for each element in patterns
    #replaces first part of the two-part element (patterns[i][0]) by corresponding regEx searcher/matcher object which is capable to search any string for corresponding pattern 
    pattern[0] = re.compile(pattern[0]) 

def tokenize(characters): #our input string (array of any characters (Ex: 6*(2+3.5)+7))
    tokens = [] #resulting array of parsed token objects initialized
    position = 0 #position in string is 0
    while position < len(characters): #we still have a character left to work with
        for pattern, tag in patterns: #go thru all elements of patterns array and assign pattern = patterns[i][0], tag = patterns[i][1]
                            #pattern is a searcher for particular allowed combination of characters
                            # pattern.match(stringToSearch, positionToStart) function searches entire character string starting from position for associated combo of char
            match = pattern.match(characters, position) #if reg ex matches string of characters, we got a match!
            if match:
                break
        assert match
        token = {
            'tag':tag,
            'value': match.group(0),
            'position': position,
        }
        tokens.append(token) #add token structure to the resulting array
        position = match.end() #change position to next character after token ends
        
    #    for token in tokens:
     #       if token["tag"] == "number":
      #          if "." in token["value"]:
      #              token["value"] = float(token["value"])
       #         else:
       #             token["value"] = int(token["value"])
    return tokens

def test_simple_tokens():
    print("testing simple tokens")
    assert tokenize("+") == [{"tag": "+", "value": "+", "position": 0}]
    assert tokenize("-") == [{"tag": "-", "value": "-", "position": 0}]
    i = 0
    for char in "+-*/()":
        tokens = tokenize(char)
        assert tokens[0]["tag"] == char
        assert tokens[0]["value"] == char
        assert tokens[0]["position"] == i
    for characters in ["+","-"]:
        tokens = tokenize(characters)
        assert tokens[0]["tag"] == characters
        assert tokens[0]["value"] == characters
    for number in ["123.45","1.", ".1", "123"]:
        tokens = tokenize(number)
        assert tokens[0]["tag"] == "number"
     #   assert tokens[0]["value"] == float(number)

    atokens = tokenize("6*(2+5)+7")    
    for t in atokens:
        print(t["value"])



if __name__ == "__main__": #if this is the main program...
    test_simple_tokens()
   # tokens = tokenize("123.45*+1234*/123*()***34235****")
    #print(tokens)




    print("done.")