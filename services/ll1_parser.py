from services.grammar import GRAMMAR


class LL1Parser:

    @staticmethod
    def parse(tokens):

        types = [
            token.type
            for token in tokens
            if token.type != "EOF"
        ]

        if len(types) == 0:
            return False

        action = types[0]

        if action not in GRAMMAR:
            return False

        productions = GRAMMAR[action]

        for production in productions:
            if types == production:
                return True

        return False