from difflib import get_close_matches


from services.reserved_words import RESERVED_WORDS


class CommandSuggester:

    @staticmethod
    def suggest(word):
        mots = list(
            RESERVED_WORDS.keys()
        )

        suggestion = get_close_matches(
            word,
            mots,
            n=1,
            cutoff=0.6
        )

        if suggestion:
            return suggestion[0]
        return None