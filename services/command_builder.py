from services.command_model import Command
from services.grammar import EOF

class CommandBuilder:

    # CONSTRUCTION D'UNE COMMANDE
    @classmethod
    def build(cls, tokens):
        """
        Transforme une liste de tokens en Command structurée.
        Le Parser LL(1) doit avoir validé les tokens
        avant l'appel à cette méthode.
        """
        if not tokens:
            raise ValueError("Aucun token fourni.")

        # Suppression de EOF
        meaningful_tokens = [token for token in tokens if token.type != EOF]
        if not meaningful_tokens:
            raise ValueError("Aucun token exploitable.")

        # Types des tokens
        token_types = [token.type  for token in meaningful_tokens]

        # Valeurs
        values = [ str(token.value).upper() for token in meaningful_tokens]

        # ACTION
        action = token_types[0]
        subject = None
        arguments = {}

        # AFFICHER
        if action == "AFFICHER":
            if len(token_types) >= 2:
                subject = token_types[1]

        # MODIFIER
        elif action == "MODIFIER":
            if len(token_types) >= 2:
                subject = token_types[1]
            for token in meaningful_tokens:
                if token.type == "NUMERO":
                    arguments["numero"] = int(token.value)

        # SUPPRIMER
        elif action == "SUPPRIMER":
            if len(token_types) >= 2:
                subject = token_types[1]
            for token in meaningful_tokens:
                if token.type == "NUMERO":
                    arguments["numero"] = int(token.value)

        # AJOUTER
        elif action == "AJOUTER":
            if len(token_types) >= 2:
                subject = token_types[1]

        # CHERCHER
        elif action == "CHERCHER":
            if len(token_types) >= 2:
                subject = token_types[1]

            # On conserve les éléments complémentaires.
            arguments["tokens"] = token_types[2:]

        # LANCER
        elif action == "LANCER":
            if len(token_types) >= 2:
                subject = token_types[1]

            if len(values) >= 3:
                arguments["nom"] = values[2]

        # EXPORTER
        elif action == "EXPORTER":
            if len(token_types) >= 2:
                subject = token_types[1]

        # RECOMMENCER
        elif action == "RECOMMENCER":
            if len(token_types) >= 2:
                subject = token_types[1]

        # QUITTER
        elif action == "QUITTER":
            subject = None

        # AUTRE
        else:
            if len(token_types) >= 2:
                subject = token_types[1]

        # RAW
        raw = " ".join(values)

        # COMMAND
        return Command(
            action=action,
            subject=subject,
            arguments=arguments,
            tokens=meaningful_tokens,
            raw=raw
        )