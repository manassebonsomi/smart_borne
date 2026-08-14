"""
Configuration centralisée de la correction intelligente
des commandes.
"""


class CorrectionConfig:

    # SEUILS DE SIMILARITÉ
    # Score à partir duquel une correction est considérée comme suffisamment fiable pour être automatique.
    AUTO_CORRECT_THRESHOLD = 0.90
    # Score minimal pour proposer une suggestion à l'utilisateur.
    SUGGEST_THRESHOLD = 0.60
    # Nombre maximum de suggestions retournées.
    MAX_SUGGESTIONS = 3

    # MODES
    AUTO_CORRECT = "AUTO_CORRECT"
    SUGGEST = "SUGGEST"
    REFORMULATE = "REFORMULATE"

    # VALIDATION
    @classmethod
    def validate(cls):

        if not (
            0.0
            <= cls.SUGGEST_THRESHOLD
            <= cls.AUTO_CORRECT_THRESHOLD
            <= 1.0
        ):

            raise ValueError(
                "Les seuils de correction " 
                "sont invalides."
            )

        if cls.MAX_SUGGESTIONS < 1:
            raise ValueError(
                "MAX_SUGGESTIONS doit être "
                "supérieur ou égal à 1."
            )

        return True