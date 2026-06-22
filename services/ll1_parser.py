from services.grammar import GRAMMAR


class LL1Parser:

    @staticmethod
    def parse(tokens):

        types = [
            token.type
            for token in tokens
            if token.type != "EOF"
        ]

        if not types:
            return False

        action = types[0]

        if action not in GRAMMAR:
            return False

        productions = GRAMMAR[action]

        for production in productions:
            # correspondance exacte
            if types == production:
                return True

            # support commandes avec NUMERO
            if (
                len(types) >= len(production)
                and
                types[:len(production)] == production
            ):

                return True

        return False