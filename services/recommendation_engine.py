class RecommendationEngine:

    @staticmethod
    def generate(age, niveau_scolaire, reponses):

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

        # ANALYSE DES REPONSES

        for reponse in reponses:

            valeur = str(reponse["valeur"]).upper()

            points = 0

            if valeur == "NON":
                points = 0

            elif valeur == "UN PEU":
                points = 2

            elif valeur == "MOYEN":
                points = 3

            elif valeur == "BEAUCOUP":
                points = 5

            elif valeur == "OUI":
                points = 5

            categorie = reponse["categorie"]

            # Catégorie 1
            # Découverte Numérique

            if categorie == 8:
                scores["Découverte Numérique"] += points

            # Catégorie 2
            # Scratch Junior

            elif categorie == 9:
                scores["Scratch Junior"] += points

            # Catégorie 3
            # Scratch Avancé

            elif categorie == 10:
                scores["Scratch Avancé"] += points

            # Catégorie 4
            # Python Débutant

            elif categorie == 11:
                scores["Python Débutant"] += points


            # Catégorie 5
            # Mentor Junior

            elif categorie == 12:
                scores["Mentor Junior"] += points

        # RECHERCHE DU MEILLEUR SCORE
        parcours = max(
            scores,
            key=scores.get
        )
        score_final = scores[parcours]

        return {
            "parcours":parcours,
            "score":score_final
        }