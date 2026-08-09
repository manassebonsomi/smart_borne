# services/command_suggester.py

from difflib import get_close_matches

from services.reserved_words import RESERVED_WORDS


class CommandSuggester:

    @staticmethod
    def suggest(word):

        if not word:
            return None

        word = word.upper()

        mots = list(
            RESERVED_WORDS.keys()
        )

        suggestions = get_close_matches(
            word,
            mots,
            n=1,
            cutoff=0.60
        )

        if suggestions:

            return suggestions[0]

        return None