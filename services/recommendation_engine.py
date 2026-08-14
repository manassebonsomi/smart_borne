class RecommendationEngine:

    PARCOURS = [
        "Découverte Numérique",
        "Scratch Junior",
        "Scratch Avancé",
        "Python Débutant",
        "Mentor Junior"
    ]

    @staticmethod
    def generate(age, niveau_scolaire, reponses):

        # INITIALISATION DES SCORES
        scores = {
            "Découverte Numérique": 0,
            "Scratch Junior": 0,
            "Scratch Avancé": 0,
            "Python Débutant": 0,
            "Mentor Junior": 0
        }

        # AGE
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

        # NIVEAU SCOLAIRE
        niveau = str(niveau_scolaire).strip().lower()

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

        # ANALYSE DES RÉPONSES
        for reponse in reponses or []:

            if isinstance(reponse, dict):
                valeur = reponse.get("valeur", "")
            else:
                valeur = reponse

            valeur = str(valeur).strip().lower()

            # JEU
            if "jeu" in valeur:
                scores["Scratch Junior"] += 15
                scores["Scratch Avancé"] += 10

            # ANIMATION
            if "animation" in valeur:
                scores["Scratch Junior"] += 15
                scores["Scratch Avancé"] += 10

            # PROGRAMMER
            if "programmer" in valeur:
                scores["Python Débutant"] += 20

            # PROBLÈME
            if ("problème" in valeur or "probleme" in valeur):
                scores["Python Débutant"] += 15
                scores["Mentor Junior"] += 10

            # ENSEIGNER
            if "enseigner" in valeur:
                scores["Mentor Junior"] += 20

            # CRÉER
            if ("créer" in valeur or "creer" in valeur):
                scores["Scratch Avancé"] += 15

        # DÉTERMINATION DU PARCOURS
        parcours = max(scores, key=scores.get)

        # SCORE FINAL
        score_final = scores[parcours]

        # RÉSULTAT
        return {
            "parcours": parcours,
            "scores": scores,
            "score_final": score_final
        }