from services.token import Token
from services.reserved_words import RESERVED_WORDS
from services.grammar import EOF


class LexerError(Exception):

    def __init__(self, message, position=None, character=None):
        self.message = message
        self.position = position
        self.character = character
        super().__init__(message)


class Lexer:

    # CARACTERES AUTORISES
    @staticmethod
    def is_letter(character):
        return (("A" <= character <= "Z") or ("a" <= character <= "z"))

    @staticmethod
    def is_digit(character):
        return "0" <= character <= "9"

    # TOKENISATION
    @classmethod
    def tokenize(cls, text):
        if text is None:
            raise LexerError("Entrée lexicale vide.", position=0)

        tokens = []
        position = 0
        length = len(text)

        while position < length:
            character = text[position]

            # ESPACES
            if character.isspace():
                position += 1
                continue

            # NUMERO
            if cls.is_digit(character):
                start = position

                while (position < length and cls.is_digit(text[position])):
                    position += 1
                value = text[start:position]

                tokens.append(
                    Token("NUMERO", value, start))

                continue

            # MOT
            if cls.is_letter(character):
                start = position

                while (position < length and (cls.is_letter(text[position]) or cls.is_digit(text[position]) or text[position] == "_")):
                    position += 1
                word = text[start:position]
                normalized = word.upper()

                # MOT RESERVE
                if normalized in RESERVED_WORDS:
                    token_type = (RESERVED_WORDS[normalized])

                    tokens.append(Token(token_type, word, start))
                    continue


                # MOT INCONNU
                raise LexerError((f"Mot inconnu : " f"'{word}'."), position=start, character=word)

            # CARACTERE INVALIDE
            raise LexerError((f"Caractère invalide : " f"'{character}'."), position=position, character=character)

        # EOF
        tokens.append(Token(EOF, EOF, position))
        return tokens


    # AFFICHAGE
    @classmethod
    def display_tokens(cls, text):
        try:
            tokens = cls.tokenize(text)
            print()
            print("=" * 70)
            print("TOKENS")
            print("=" * 70)

            for token in tokens:
                print(f"{token.type} -> " f"{token.value}")
            return tokens
        except LexerError as error:
            print("ERREUR LEXICALE : " + str(error))
            return None