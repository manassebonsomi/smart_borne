import re
from services.token import Token
from services.reserved_words import RESERVED_WORDS
from services.command_suggester import CommandSuggester


class LexicalAnalyzer:

    IGNORED_WORDS = {
        "LE",
        "LA",
        "LES",
        "DE",
        "DU",
        "DES",
        "UN",
        "UNE",
        "ET",
        "D",
        "L"
    }

    @staticmethod
    def tokenize(command):

        command = command.upper()
        words = re.findall(r'\d+|[A-Z]+', command)
        tokens = []

        for word in words:
            if word in LexicalAnalyzer.IGNORED_WORDS:
                continue

            if word.isdigit():
                tokens.append(
                    Token("NUMERO", int(word)))

            elif word in RESERVED_WORDS:
                tokens.append(Token(RESERVED_WORDS[word], word))

            else:
                suggestion = CommandSuggester.suggest(word)

                if suggestion:
                    raise Exception(
                        f"Token inconnu : "
                        f"{word}. "
                        f"Voulez-vous dire "
                        f"'{suggestion}' ?"
                    )
                raise Exception(
                    f"Token inconnu : {word}"
                )

        tokens.append(
            Token("EOF","EOF"))
        
        return tokens