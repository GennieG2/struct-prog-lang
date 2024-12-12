I decided to implemented the power operator (^) because it is an important arithmetic operator that we did not implement. I extended the tokenizer, parser, and evaluator and implemented new functionality with respect to the correct order of operations. 
I compiled and ran the program; it compiled successfully and executed without any errors. 
I know I have succeeded because my newly added evaluation test succeeded: this test contains multiple scenarios of using the power operator including using complex expressions as an operand. Every comment in the code with the prefix "FINAL" is a comment intended to show the work I added for my project. 
However, the same descriptions can be found below.

Tokenizer.py
  I added pattern for power operator:
  line 31: [r"\^", "^"] 

Parser.py 
  I changed the EBNF definition (please make a note that because we added a new operator with higher precedence, it changed our grammar):
  line 16: arithmetic_power_operand = complex_expression ;
  line 17: arithmetic_factor = arithmetic_power_operand { ("^") arithmetic_power_operand } 

  I introduced a new function parse_arithmetic_power_operand(tokens) to return AST for the last in chain operand. 
  Having that power operator has the highest precendence, the calling of parse_complex_expression now moved here from parse_arithmeic_factor.
  line 447: def parse_arithmetic_power_operand(tokens):
                """
                arithmetic_power_operand = complex_expression ;
                """
                return parse_complex_expression(tokens)

  I tested parse_arithmetic_power_operand() function to make sure that the operand is a valid complex expression
  line 455: def test_parse_arithmetic_power_operand():
                """
                arithmetic_power_operand = complex_expression ;
                """
                print("testing parse_arithmetic_power_operand...")
                for expression in ["1", "1.2", "true", "x", "-1"]:
                    t = tokenize(expression)
                    assert parse_arithmetic_power_operand(t)[0] == parse_complex_expression(t)[0]

  Now when I introduced power operator, parse_arithmetic_factor() is not last in chain. So I modified it.
  parse_arithmetic_factor() first calls parse_arithmetic_power_operand() to get the AST for the left operand,
  and then if the next token is power operator it calls parse_arithmetic_power_operand() function a second time for the right operand,
  and returns a constructed AST for the power operator
  line 468: def parse_arithmetic_factor(tokens):
                """
                arithmetic_factor = arithmetic_power_operand { ("^") arithmetic_power_operand } ;
                """
                node, tokens = parse_arithmetic_power_operand(tokens)
                while tokens[0]["tag"] in ["^"]:
                    tag = tokens[0]["tag"]
                    next_node, tokens = parse_arithmetic_power_operand(tokens[1:])
                    node = {"tag": tag, "left": node, "right": next_node}
                return node, tokens

  test_parse_arithmetic_factor() makes sure that if the factor contains the power operator, the correct AST for the power operator is returned. 
  line 480: def test_parse_arithmetic_factor():
                """
                arithmetic_factor = arithmetic_power_operand { ("^") arithmetic_power_operand } ; 
                """
                print("testing parse_arithmetic_factor...")
                ast, tokens = parse_arithmetic_factor(tokenize("x"))
                assert ast == {"tag": "identifier", "value": "x"}
            
                ast, tokens = parse_arithmetic_factor(tokenize("x^y"))
                assert ast == {
                    "tag": "^",
                    "left": {"tag": "identifier", "value": "x"},
                    "right": {"tag": "identifier", "value": "y"}
                }

  I added the test function calls to the bottom of the file. 

Evaluator.py
  I added the power operator interpretaion for AST node.
  line 40: if ast["tag"] == "^":
              left_value, _ = evaluate(ast["left"], environment)
              right_value, _ = evaluate(ast["right"], environment)
              assert right_value != 0 or left_value !=0, "Invalid power operands"
              return pow(left_value, right_value), False

  I added a test for power operator using different scenarios where operands are numbers or even expressions.
  line 233: def test_evaluate_power():
                print("test evaluate power")
                equals("4^2", {}, 16, {})
                equals("2^5", {}, 32, {})
                equals("((2+3)*2)^2", {}, 100, {})

  I added the test function call to the bottom of the file. 
