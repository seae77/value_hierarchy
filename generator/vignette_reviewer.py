import logging
from domain.values import ValuePair
from generator.openai_client import OpenAIClient

class VignetteReviewer:
    """
    A class designed to review and minimally reformulate vignettes to ensure they
    align with specific criteria for different hypotheses, focusing on value 
    violations, emotional responses, and normative language, all while maintaining
    a neutral and factual tone.
    """

    def __init__(self, openai_client: OpenAIClient):
        """
        Initializes the VignetteReviewer with an OpenAI client.

        :param openai_client: An instance of OpenAIClient for interacting with the OpenAI API.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.openai_client = openai_client

    def review_vignette_h1(self, vignette_text: str, value_pair: ValuePair) -> str:
        """
        Reviews the given vignette text to ensure it meets Hypothesis 1 (H1) requirements:
        - H1 posits that individuals opt for the action aligned with their 'top-tier' value 
          in a dilemma, reflecting a consistent preference hierarchy.
        - The vignette should depict a protagonist consistently favoring one value in a choice scenario, 
          without moral terms (e.g., « bien », « mal », « valeur »), 
          and acting freely (no external pressures).
        - The text must remain neutral and factual, describing only what happens 
          and showing a clear preference for one option over the other.
        - If the text violates these criteria, it should be minimally reformulated 
          while preserving style and length as much as possible.
        """

        system_prompt = (
            "Tu es ChatGPT. Tu vas recevoir un texte (vignette) destiné à illustrer l'Hypothèse 1 (H1). "
            "Selon H1, on met en scène un individu qui opte de façon cohérente pour l'option reflétant sa valeur prioritaire, "
            "dans un conflit ou un dilemme entre deux valeurs. "
            "Le texte doit : "
            "1) Montrer que la protagoniste fait un choix cohérent aligné sur l'une des valeurs du pair, "
            "2) Ne pas employer de mots comme « bien », « mal », « valeur » ou de tournures moralisantes, "
            "3) Faire comprendre que la décision est libre, sans contrainte extérieure, "
            "4) Préserver un ton neutre et factuel. "
            "5) Ne pas utiliser le mot 'valeur' ni les noms des valeurs ni aucune forme de jugement de valeurs. "
            "6) Ne pas décrire les états d'âme du protagoniste, sa satisfaction ou ses émotions. "
            "Si ces conditions ne sont pas respectées, reformule légèrement le texte en gardant le style et la longueur. "
            "Réponds uniquement avec la version finale, sans commentaire."
        )

        user_prompt = f"""
Le texte ci-dessous est conçu pour illustrer l'Hypothèse 1 (H1) : 
{value_pair.value1.name} vs {value_pair.value2.name}.

Texte :
<<<
{vignette_text}
>>>
1) Assure-toi que les valeurs {value_pair.value1.name} et {value_pair.value2.name} sont illustrée aussi clairement que possible.
2) Vérifie qu'il y a un choix explicite du protagonistes, montrant une préférence cohérente pour l'une des deux valeurs.
3) Assure-toi qu'il n'y a pas d'expressions morales ('bien', 'mal', 'valeur') et que le style reste neutre.
4) Vérifie qu'aucune pression extérieure n'influence directement ce choix.
5) Si tout est correct, renvoie le texte inchangé. Sinon, reformule-le très légèrement pour être conforme à H1. 
Ne donne aucun commentaire supplémentaire, uniquement le texte final.
"""

        return self._review_vignette(system_prompt, user_prompt)

    
    def review_vignette_h2(self, vignette_text: str, value_pair: ValuePair) -> str:
        """
        Reviews the given vignette text to ensure it meets Hypothesis 2 (H2) requirements:
        - H2 posits that a clearly observed violation of a specific value elicits a consistent negative
          emotional reaction (e.g., colère, indignation) in individuals who hold that value.
        - The vignette must depict a single, distinct violation of one of the values in value_pair 
          (or show how the protagonist's behavior contradicts that value).
        - The text should be neutral, factual (no terms like 'bien', 'mal', 'valeur', or moralizing language).
        - The protagonist should act freely (no external pressure).
        - Keep the style and length consistent, only making minimal changes if needed.
        """

        system_prompt = (
            "Tu es ChatGPT. Tu vas recevoir un texte (vignette) destiné à illustrer l'Hypothèse 2 (H2). "
            "Dans H2, on s'intéresse à la réaction émotionnelle suscitée par la transgression d'une valeur. "
            "Le texte doit donc : "
            "1) Mettre en évidence une violation claire d'une seule valeur (parmi celles de value_pair), "
            "   pour que le lecteur puisse ressentir ou évaluer une colère ou indignation potentielle. "
            "2) Ne pas employer de mots tels que « bien », « mal », « valeur », ni de jugements moraux explicites. "
            "3) Indiquer que la protagoniste agit librement, sans contrainte extérieure. "
            "4) Rester factuel et succinct, sans commentaire moral. "
            "Si ces conditions ne sont pas respectées, reformule légèrement le texte pour répondre à ces exigences, "
            "en gardant le style et la longueur initiaux autant que possible. "
            "Renvoie UNIQUEMENT le texte final, sans commentaire supplémentaire."
        )

        user_prompt = f"""
        Veuillez examiner le texte ci-dessous, censé illustrer l'Hypothèse 2 (H2) : 
        une transgression d'une valeur, potentiellement suscitant une réaction négative (indignation, colère).
        Nous avons la paire de valeurs : {value_pair.value1.name} vs {value_pair.value2.name}.

        Texte :
        <<<
        {vignette_text}
        >>>

        Vérifiez :
        1) Qu'il y a bien une transgression claire d'une seule valeur, permettant de susciter une réaction négative.
        2) Que le protagonistes agit sans pression extérieure.
        3) Que le langage reste neutre (sans 'bien', 'mal', 'valeur', ni moralisation).
        Si c'est correct, renvoyez le texte inchangé. Sinon, reformulez-le légèrement pour qu'il respecte H2.
        Uniquement le texte final, sans commentaires.
        """

        return self._review_vignette(system_prompt, user_prompt)

    def review_vignette_h3(self, vignette_text: str, value_pair: ValuePair) -> str:
        """
        Reviews and reformulates a vignette for Hypothesis 3 (H3).

        Ensures the vignette demonstrates two distinct value violations related to the 
        given value pair, maintaining a neutral and factual tone without moralizing language.

        :param vignette_text: The original vignette text (approx. 110 words).
        :param value_pair: The ValuePair to check for distinct value violations.
        :return: The potentially reformulated vignette text meeting H3 criteria.
        """
        system_prompt = (
            "Vous êtes ChatGPT. Vous allez recevoir une courte vignette censée illustrer un scénario pour l'hypothèse 3."
            " L'hypothèse 3 exige de montrer DEUX violations de valeurs distinctes - une pour chaque valeur de la paire -"
            " et de s'assurer que le ton reste factuel, neutre et exempt de tout langage moralisateur. Évitez les mots"
            " 'valeur', 'bien', 'mal' ou les termes moraux directs. Veillez à ce qu'aucune pression extérieure n'oblige"
            " le protagonistes à agir. Veillez à ce que le texte final soit proche de la structure originale, en n'apportant"
            " que des changements minimes si nécessaire. Renvoyez UNIQUEMENT la vignette révisée sans commentaire supplémentaire."
        )

        user_prompt = f"""
        Veuillez examiner le texte ci-dessous, conçu pour Hypothesis 3 (H3), 
        qui compare deux violations de valeurs différentes. 
        Le texte doit :
        1) Assure-toi que les valeurs {value_pair.value1.name} et {value_pair.value2.name} sont illustrée aussi clairement que possible.
        2) Vérifie qu'il y a deux violations distinctes mais intégrées dans la même situation : l'une lié à {value_pair.value1.definition}, 
        l'autre liée à {value_pair.value2.definition}.
        3) Illustrer les valeurs {value_pair.value1.descriptive_keywords[0]} et {value_pair.value2.descriptive_keywords[0]} de manière aussi explicite que possible, sans les nommer.
        4) Rester neutre, sans mots comme « bien », « mal » ni « valeur ». 
        5) Dépeindre des actes réalisés sans pression extérieure (volontaires).
        6) Ne pas introduire de contradiction manifeste (par ex. adopter puis rejeter un même principe 
        de façon incohérente).
        7) Se limiter à EXACTEMENT 110 mots, ou très proche, sans dévier du style initial.
        8) Ne pas utiliser le mot "valeur" ni les noms des valeurs ni aucune forme de jugement de valeurs.

        Si tout est satisfaisant, renvoyez le texte inchangé. 
        Sinon, reformulez-le très légèrement pour corriger d'éventuels conflits, 
        assurer un ton factuel et clarifier les deux violations sans contradiction. 
        Fournissez UNIQUEMENT le texte final, sans commentaire supplémentaire.
        """

        return self._review_vignette(system_prompt, user_prompt)

    def review_vignette_h4(self, vignette_text: str, value_pair: ValuePair) -> str:
        """
        Reviews the given vignette text to ensure it meets Hypothesis 4 (H4) requirements:
        - H4 focuses on vicarious moral emotion: the participant witnesses a protagonist 
        violating or neglecting one value in favor of another, without being personally harmed.
        - The text must remain factual, neutral, and consistent (no contradictory references).
        - Protagonist acts freely, preferring or prioritizing Value A over Value B 
        in a way the participant only observes (not the victim).
        - Avoid moral language ('bien', 'mal', 'valeur'), keep 110 words or close, 
        and describe only what is observable.
        """
    
        system_prompt = (
        "Tu es ChatGPT. Tu vas recevoir un texte qui doit illustrer Hypothesis 4 (H4). "
        "Dans H4, le protagoniste viole ou néglige une valeur, préférant explicitement une autre, "
        "tandis que le lecteur n'est que témoin. "
        "Vérifie : "
        "1) Que la préférence du protagoniste (ex. confort plutôt que sacré) soit claire et cohérente, "
        "   sans contradiction (ne pas dire qu'il privilégie un principe, puis agit à l'opposé). "
        "2) Qu'aucune contrainte extérieure ne l'oblige. "
        "3) Que le texte ne contienne ni mots moraux ('bien', 'mal', 'valeur') ni jugement explicite. "
        "4) Qu'il reste proche de 110 mots et présente seulement des faits observables. "
        "Si le texte satisfait ces critères, renvoie-le tel quel. Sinon, reformule légèrement pour enlever toute contradiction "
        "et conserver un ton neutre. Réponds uniquement par le texte final, sans commentaire."
        )

        user_prompt = f"""
        Le texte ci-dessous doit illustrer H4 pour : {value_pair.value1.name} vs {value_pair.value2.name}.

    Texte :
    <<<
    {vignette_text}
    >>>

    1) Confirme qu'il existe une préférence nette pour l'un des deux principes (ex. {value_pair.value1.name} 
   au détriment de {value_pair.value2.name}), sans contradiction.
    2) Vérifie que cette préférence est libre (pas de pression extérieure) et que le lecteur est simple témoin.
    3) Vérifie l'absence de tournures morales ('bien', 'mal', etc.) ou du mot 'valeur'.
    4) Si tout est correct, renvoie le texte inchangé. Sinon, reformule-le pour respecter H4.

    Réponds UNIQUEMENT avec la version finale, sans commentaire.
    """

        return self._review_vignette(system_prompt, user_prompt)


    def review_vignette_h5(self, vignette_text: str, value_pair: ValuePair) -> str:
        """
        Reviews and reformulates a vignette for Hypothesis 5 (H5).

        Ensures the vignette sets up a tension between two values and anticipates 
        normative language use in a subsequent question, while remaining neutral.

        :param vignette_text: The original vignette text.
        :param value_pair: The ValuePair containing the two values in tension.
        :return: The potentially reformulated vignette text meeting H5 criteria.
        """
        system_prompt = (
            "Tu es ChatGPT. Tu vas recevoir un texte (vignette) conçu pour l'Hypothèse 5 (H5) de cette étude."
            "Selon H5, le langage normatif (par ex. « devrait », « il faut ») reflète la manière dont les individus"
            "classent leurs priorités ou leurs valeurs. "
            "La vignette doit : "
            "1) Présenter une situation où deux valeurs sont en tension (Value1 vs. Value2), "
            "sans employer de mots comme « valeur », « bien », « mal ». "
            "2) Décrire les actions ou décisions du protagonistes de façon neutre et factuelle, "
            "sans jugements moraux. "
            "3) Montrer que le protagonistes agit librement, sans pression extérieure. "
            "4) Préparer un contexte où, idéalement, la question associée incite le participant"
            "à formuler ou réagir à un énoncé normatif (ex. « devrait prévaloir… »). "
            "5) Rester conforme aux contraintes de longueur ou de style (si applicables), "
            "en évitant toute mention explicite du mot « valeur ». "
            "Si le texte viole l'un de ces critères ou ne souligne pas clairement la tension "
            "entre deux principes distincts, reformule-le légèrement. "
            "Sinon, renvoie-le inchangé. "
            "Fournis UNIQUEMENT la version finale du texte, sans commentaire additionnel."
        )

        user_prompt = f"""
        Veuillez analyser le texte ci-dessous, conçu pour l'Hypothèse 5 (H5) :
        Texte :
        <<<
        {vignette_text}
        >>>
        - Cette hypothèse s'intéresse à l'utilisation de langage normatif (ex. « devrait », « il faut »), 
        - Vérifiez que le texte met en scène deux principes ou objectifs en conflit, sans mot comme « valeur », 
        et qu'il reste neutre (pas de jugement moral explicite).
        - Assurez-vous que les actions décrites sont libres de toute contrainte extérieure.
        - Enfin, vérifiez qu'il n'y a ni tournures moralisantes ni termes interdits (« bien », « mal », « valeur »).

        Si tout est correct, renvoyez le texte inchangé. 
        Sinon, modifiez-le très légèrement pour qu'il réponde aux exigences ci-dessus 
        et pour qu'il anticipe la possibilité d'un énoncé normatif (ex. « on devrait faire… ») dans la question.

        Fournissez UNIQUEMENT le texte final reformulé, sans commentaire supplémentaire.
        """

        return self._review_vignette(system_prompt, user_prompt)

    def review_vignette_h6(self, vignette_text: str, value_pair: ValuePair) -> str:
        """
        Reviews and reformulates a vignette for Hypothesis 6 (H6).

        Focuses on the perceived appropriateness of an emotional response in a 
        value-related scenario, ensuring observable emotional reactions without explicit 
        moral or emotional labeling.

        :param vignette_text: The original vignette text.
        :param value_pair: The ValuePair relevant to the hypothesis.
        :return: The potentially reformulated vignette text meeting H6 criteria.
        """
        system_prompt = (
            "Tu es ChatGPT. Tu vas recevoir un texte (une vignette) destiné à l'Hypothèse 6 (H6). "
            "Dans H6, il s'agit d'évaluer à quel point la réaction émotionnelle d'un protagonistes est considérée "
            "comme appropriée ou justifiée. Le récit doit donc : "
            "1) Décrire une situation où un personnage réagit de manière observable à un événement, sans employer "
            " de termes explicitement moraux (p. ex. « bien », « mal ») ni le mot « valeur ». "
            "2) Montrer que l'émotion est affichée librement, sans contrainte extérieure, et sans que le texte "
            " qualifie la réaction de 'trop forte' ou 'acceptable' (cela doit être jugé par le lecteur). "
            "3) Maintenir un ton neutre et factuel, décrivant des gestes, un ton de voix, une posture, etc. "
            "4) Ne pas utiliser de mots comme « en colère », « heureux », ni d'autres étiquettes émotionnelles directes. "
            "5) Ne conserver que les éléments nécessaires pour un jugement ultérieur de l'adéquation de cette réaction. "
            "Si le texte ne respecte pas ces critères ou inclut un langage moral, reformule-le très légèrement tout "
            "en conservant la structure et la longueur. Sinon, renvoie-le inchangé. "
            "Fournis UNIQUEMENT la version finale du texte, sans commentaire supplémentaire."
        )

        user_prompt = f"""
        Veuillez examiner le texte ci-dessous, censé illustrer l'Hypothèse 6 (H6) : 
        - Le récit doit montrer une réaction émotionnelle de manière observable (ton, gestes, actes), 
         sans mots comme « en colère » ou « bien/mal » ni le terme « valeur ». 
        - Le protagonistes agit librement, sans pression extérieure. 
        - Le style doit rester neutre et factuel. 
        - Il faut permettre au lecteur d'évaluer si la réaction est proportionnée ou non, 
         sans l'indiquer textuellement dans le vignette.

        Texte :
        <<<
        {vignette_text}
        >>>
        1) Assure-toi que les valeurs {value_pair.value1.name} et {value_pair.value2.name} sont illustrée aussi clairement que possible.
        2) Vérifiez la présence d'une réaction émotionnelle clairement perceptible via des indices extérieurs (comportement, voix, gestes).
        3) Assurez-vous qu'aucun langage moral ni contraintes externes n'apparaissent.
        4) Si le texte répond à ces exigences, renvoyez-le tel quel. Sinon, reformulez-le légèrement pour respecter ces critères. 
        N'ajoutez pas de commentaire, renvoyez UNIQUEMENT la version finale.
        """

        return self._review_vignette(system_prompt, user_prompt)

    def _review_vignette(self, system_prompt: str, user_prompt: str) -> str:
        """
        Helper method to handle the common logic for reviewing vignettes.

        :param system_prompt: The system prompt for the OpenAI API.
        :param user_prompt: The user prompt for the OpenAI API.
        :return: The revised vignette text.
        """
        return self.openai_client._generate_content(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=self.openai_client.model_scenario,
            temperature=0.0,
            max_tokens=300
        )