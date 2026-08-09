from services.lexical_analyzer import LexicalAnalyzer
from services.ll1_parser import LL1Parser

tokens = LexicalAnalyzer.tokenize(
    "MODIFIER QUESTION 3"
)

result = LL1Parser.parse(
    tokens,
    return_trace=True
)

print(result)


