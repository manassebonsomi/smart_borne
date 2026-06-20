class RecommendationEngine:

    @staticmethod
    def generate(
            age,
            niveau_scolaire,
            reponses
    ):

        scores = {

            "Découverte Numérique": 0,

            "Scratch Junior": 0,

            "Scratch Avancé": 0,

            "Python Débutant": 0,

            "Mentor Junior": 0
        }

        # =========================
        # AGE
        # =========================

        if age <= 7:

            scores["Découverte Numérique"] += 40

        elif age <= 10:

            scores["Scratch Junior"] += 40

        elif age <= 13:

            scores["Scratch Avancé"] += 40

        elif age <= 16:

            scores["Python Débutant"] += 40

        else:

            scores["Mentor Junior"] += 40

        # =========================
        # NIVEAU SCOLAIRE
        # =========================

        niveau = niveau_scolaire.lower()

        if niveau in [

            "1ere",
            "2eme",
            "3eme"

        ]:

            scores["Découverte Numérique"] += 20

        elif niveau in [

            "4eme",
            "5eme",
            "6eme"

        ]:

            scores["Scratch Junior"] += 20

        elif niveau in [

            "7eme",
            "8eme"

        ]:

            scores["Scratch Avancé"] += 20

        elif niveau in [

            "1ere secondaire",
            "2eme secondaire"

        ]:

            scores["Python Débutant"] += 20

        else:

            scores["Mentor Junior"] += 20

        # =========================
        # REPONSES
        # =========================

        for reponse in reponses:

            r = reponse.lower()

            if "jeu" in r:

                scores["Scratch Junior"] += 15
                scores["Scratch Avancé"] += 10

            if "animation" in r:

                scores["Scratch Junior"] += 15
                scores["Scratch Avancé"] += 10

            if "programmer" in r:

                scores["Python Débutant"] += 20

            if "problème" in r:

                scores["Python Débutant"] += 15
                scores["Mentor Junior"] += 10

            if "enseigner" in r:

                scores["Mentor Junior"] += 20

            if "créer" in r:

                scores["Scratch Avancé"] += 15

        # =========================
        # MEILLEUR PARCOURS
        # =========================

        parcours = max(
            scores,
            key=scores.get
        )

        score_final = scores[parcours]

        return {

            "parcours":
                parcours,

            "score":
                score_final
        }