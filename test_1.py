from services.grammar_analyzer import GrammarAnalyzer
from services.ll1_table import LL1Table

GrammarAnalyzer.display()

LL1Table.display()

result = LL1Table.validate()

print(result)