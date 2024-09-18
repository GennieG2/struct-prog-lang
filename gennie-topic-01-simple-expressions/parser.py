"""
parser.py -- implement parser for simple expressions
Accept a string of tokens, return an AST expressed as a stack of dictionaries 
""" 

""" 
EBNF:
simple_expression = number | "("expression")" | "-" simple_expression

#A factor can be a simple expression
factor = simple_expression

#A term can be a factor possibly followed by 0 or more factors which have to be *, /,
term = factor {"*"|"/" factor }

#An expression is a term or optionally plus or minus term
expression = term { "+"|"-" term}

Example:
    2  + 4  * 5  - 6
    se + se * se - se
    fa + fa * fa - fa
    T  +    T    - T    #a term can be just a factor
          E

T     T       T     T      
2 + 3 * 5 + 4 * 7 + 6
F  F    F   F   F   F
"""
from pprint import pprint

from tokenizer import tokenize

def parse_simple_expression(tokens):
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    if tokens[0]["tag"] == "number":
        return tokens[0], tokens[1:]
    if tokens[0]["tag"] == "(":
        node, tokens = parse_expression(tokens[1:])
        assert tokens[0]["tag"] == ")", "Error: expected ')'"
        return node, tokens[1:]
    if tokens[0]["tag"] == "-":
        node, tokens = parse_simple_expression(tokens[1:])
        node = {"tag":"negate", "value":node}
        return node, tokens


def parse_expression(tokens):
    return parse_simple_expression(tokens)

def test_parse_simple_expression():
    """
    simple_expression = number | "(" expression ")" | "-" simple_expression
    """
    print("testing parse_simple_expression")
    tokens = tokenize("2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast)
    tokens = tokenize("(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 2
    # pprint(ast)
    tokens = tokenize("-2")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 1, "tag": "number", "value": 2},
    }
    # pprint(ast)
    tokens = tokenize("-(2)")
    ast, tokens = parse_simple_expression(tokens)
    assert ast == {
        "tag": "negate",
        "value": {"position": 2, "tag": "number", "value": 2},
    }
    # pprint(ast)

    tokens = tokenize("1.23")
    ast, tokens = parse_simple_expression(tokens)
    assert ast["tag"] == "number"
    assert ast["value"] == 1.23


def parse_factor(tokens):
    """
    factor = simple_expression
    """
    return parse_simple_expression(tokens)

def test_parse_factor():
    """
    factor = simple_expression
    """
    print("testing parse_factor")
    for s in ["2", "(2)", "-2"]:
        assert parse_factor(tokenize(s)) == parse_simple_expression(tokenize(s))
    
    for x in ["123.45","1.", ".1", "123"]:
        assert parse_factor(tokenize(x)) == parse_simple_expression(tokenize(x))

def parse_term(tokens):
    """
    term = factor { "*"|"/" factor }
    """
    node, tokens = parse_factor(tokens)
    while tokens[0]["tag"] in ["*", "/"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_factor(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node} #shift the node we're saving over by one
    return node, tokens


def test_parse_term():
    """
    term = factor { "*"|"/" factor }
    """
    print("testing parse_term")

    tokens = tokenize("2*3/4*5")
    ast, tokens = parse_term(tokens)
    assert ast == {
        "left": {
            "left": {
                "left": {"position": 0, "tag": "number", "value": 2},
                "right": {"position": 2, "tag": "number", "value": 3},
                "tag": "*",
            },
            "right": {"position": 4, "tag": "number", "value": 4},
            "tag": "/",
        },
        "right": {"position": 6, "tag": "number", "value": 5},
        "tag": "*",
    }

    exp = "23"
    originalTokens = tokenize(exp)
    node, tokens = parse_term(originalTokens)
    assert node == originalTokens[0]

    exp = "2+3"
    originalTokens = tokenize(exp)
    node, tokens = parse_term(originalTokens)
    assert node == originalTokens[0]

    exp = "2*3"
    originalTokens = tokenize(exp)
    node, tokens = parse_term(originalTokens)
    assert node == {
        "tag": "*",
        "left": originalTokens[0],
        "right": originalTokens[2]
    }

    exp = "2*3+18"
    originalTokens = tokenize(exp)
    node, tokens = parse_term(originalTokens)
    assert node == {
        "tag": "*",
        "left": originalTokens[0],
        "right": originalTokens[2]
    }

    exp = "3*(2+8)+7"
    originalTokens = tokenize(exp)
    node, tokens = parse_term(originalTokens)
    assert node["left"]["value"] == 3
    assert node["right"]["left"]["value"] == 2
    assert node["right"]["right"]["value"] == 8
    


def parse_expression(tokens):
    """
    expression = term { "+"|"-" term }
    """
    node, tokens = parse_term(tokens)
    while tokens[0]["tag"] in ["+", "-"]:
        tag = tokens[0]["tag"]
        right_node, tokens = parse_term(tokens[1:])
        node = {"tag": tag, "left": node, "right": right_node}
    return node, tokens


def test_parse_expression():
    """
    expression = term { "+"|"-" term }
    """
    print("testing parse_expression")
    exp = "3*(2+8)+7"
    originalTokens = tokenize(exp)
    node, tokens = parse_expression(originalTokens)
    assert node['tag'] == "+"

    assert node['right']['tag'] == "number"
    assert node['right']['value'] == 7

    assert node['left']['tag'] == "*"

    assert node["left"]["left"]["tag"] == "number"
    assert node["left"]["left"]["value"] == 3

    assert node["left"]["right"]["tag"] == "+"

    assert node["left"]["right"]["left"]["tag"] == "number"  
    assert node["left"]["right"]["left"]["value"] == 2

    assert node["left"]["right"]["right"]["tag"] == "number"
    assert node["left"]["right"]["right"]["value"] == 8

def parse(tokens):
    ast, tokens = parse_expression(tokens)
    return ast

def test_parse():
    print("testing parse")
    tokens = tokenize("2+3*4+5")
    ast, _ = parse_expression(tokens)
    assert parse(tokens) == ast

if __name__ == "__main__":
    test_parse_simple_expression()
    test_parse_factor()
    test_parse_term()
    test_parse_expression()
    test_parse()
    print("done")