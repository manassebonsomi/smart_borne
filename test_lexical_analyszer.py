from services.lexical_analyzer \
    import LexicalAnalyzer

from services.ll1_parser \
    import LL1Parser

tokens = \
    LexicalAnalyzer.tokenize(
        "Afficher statistiques"
    )

print(tokens)
print("==========")
print(
    LL1Parser.parse(tokens)
)