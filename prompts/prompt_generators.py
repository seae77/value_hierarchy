# prompts/prompt_generators.py

from domain.values import Value, ValuePair
from domain.hypothesis_types import HypothesisType

SINGLE_SCENARIO_WORD_COUNT = 60
COMBINED_SCENARIO_WORD_COUNT = 110
MAX_QUESTION_WORDS = 20


#########################
#  STEP 1: Single Scenario
#########################

def generate_single_scenario_prompt(value: Value) -> str:
    """
    Génère un court scénario (par exemple, exactement 60 mots) illustrant une seule valeur,
    sans langage normatif ni mention directe du nom de la valeur ou du mot 'value'.
    """
    if not value.descriptive_keywords:
        raise ValueError("La Value doit avoir au moins un mot-clé descriptif.")

    v_descriptive_keywords = ", ".join(value.descriptive_keywords)
    v_common_patterns = ", ".join(value.common_observed_patterns)
    v_contextual_features = ", ".join(value.contextual_features)
    v_associated_actions = ", ".join(value.associated_actions_and_behaviors)
    v_influencing_factors = ", ".join(value.influencing_factors)
    v_observable_indicators = ", ".join(value.observable_indicators)
    v_factual_scenarios = ", ".join(value.factual_scenarios)
    v_example_factual_questions = ", ".join(value.example_factual_questions)

    return f"""
Rédigez un court scénario de EXACTEMENT 60 mots.
Ce scénario doit dépeindre une situation de la vie quotidienne intégrant des éléments tels que :
- mots-clés descriptifs : {v_descriptive_keywords}
- schémas courants observés : {v_common_patterns}
- caractéristiques contextuelles : {v_contextual_features}
- actions associées : {v_associated_actions}
- facteurs d’influence : {v_influencing_factors}
- indicateurs observables : {v_observable_indicators}
- scénarios factuels : {v_factual_scenarios}
- questions factuelles : {v_example_factual_questions}

N’utilisez PAS de langage normatif ou évaluatif (par ex. « bien », « mal »).
N’utilisez PAS le mot « value » ni le nom « {value.name} ».
Terminez par une phrase complète.
"""


#########################
#  STEP 2: Combine Two Scenarios
#########################

def combine_scenarios_prompt(scenarioA: str, scenarioB: str, hypothesis_type: HypothesisType) -> str:
    """
    Génère une instruction demandant à GPT de fusionner deux scénarios validés
    (chacun illustrant une valeur distincte) dans une vignette finale, selon
    les contraintes spécifiques de l’hypothèse (H1-H6).
    Le texte final doit rester neutre, sans langage moral ou normatif,
    sans mention de « value » ni des noms des valeurs d’origine, et comporter
    exactement 110 mots (ou la longueur souhaitée).

    Chaque vignette doit commencer par un personnage confronté à deux scénarios
    et révélant sa préférence.
    """

    if hypothesis_type == HypothesisType.H1:
        return f"""
    Considérez les deux scénarios suivants :
    Scénario A : {scenarioA}
    Scénario B : {scenarioB}

    Vous écrivez un roman et devez décrire une situation en EXACTEMENT 110 mots où un personnage nommé Pierre
    est confronté à un choix entre le scénario A et le scénario B.
    Montrez la préférence de Pierre à travers ses actions ou ses pensées, sans mentionner de valeurs ni la nature des scénarios.
    Reflétez le conflit de manière naturelle dans le récit, en veillant à ce que la décision de Pierre soit évidente à travers son comportement.
    Conservez un ton neutre et factuel, en terminant par une phrase complète, exactement à 110 mots.
    """

    elif hypothesis_type == HypothesisType.H2:
        return f"""
    Considérez les deux scénarios suivants :
    Situation 1 : {scenarioA}
    Situation 2 : {scenarioB}

    Rédigez un récit de EXACTEMENT 110 mots, mettant en scène Sophie. Elle connaît et comprend les deux approches (A et B), 
    mais choisit délibérément et régulièrement l’approche de Scénario A, au point de négliger concrètement l’approche de Scénario B. 
    Aucun tiers ne la contraint ou ne l’influence : c’est sa préférence personnelle. Montrez ce comportement dans un contexte réaliste, 
    sans employer de langage moral ni le mot « valeur ». Évitez « bien », « mal » et restez factuel. 
    Terminez sur une phrase complète, précisément 110 mots.
    """

    elif hypothesis_type == HypothesisType.H3:
        return f"""
    Une jeune femme nommée Isabelle envisage deux voies différentes.
    Voie 1 : {scenarioA}
    Voie 2 : {scenarioB}

    Rédigez un récit de EXACTEMENT 110 mots où le protagoniste (Isabelle) commet deux actions distinctes, 
    chacune négligeant ou contredisant l’une des deux approches (A et B). Décrivez précisément ces violations, sans employer de langage moral 
    ni le mot « valeur ». Montrez comment Isabelle agit librement sans pression extérieure, ignorant d’abord un aspect de Voie 1, 
    puis un aspect de Voie 2. Restez factuel, sans juger. 
    Terminez par une phrase complète, précisément 110 mots.
    """

    elif hypothesis_type == HypothesisType.H4:
        return f"""
    Dans un café tranquille à Fribourg, deux amis, Claude et Jean-Pierre, discutent.
    Claude décrit une situation où il a dû choisir entre deux options.
    Choix de Claude : {scenarioA}
    Option alternative : {scenarioB}

    Construisez un récit de EXACTEMENT 110 mots, situé dans un contexte suisse/français, où Claude explique son choix
    à Jean-Pierre. Montrez comment les actions ou l’attitude de Claude reflètent sa décision, et décrivez la réaction
    de Jean-Pierre à travers son comportement sans évoquer ses émotions. Assurez-vous que la conversation intègre
    naturellement les deux scénarios comme des options mutuellement exclusives auxquelles Claude était confronté.
    Évitez un langage moral ou normatif, et ne nommez pas les options explicitement.
    Maintenez un ton neutre et factuel, en terminant par une phrase complète, exactement à 110 mots.
    """

    elif hypothesis_type == HypothesisType.H5:
        return f"""
    Au cœur de Berne, une femme nommée Marie repense à une décision récente qu’elle a prise.
    Elle devait choisir entre deux options.
    Choix de Marie : {scenarioA}
    Option alternative : {scenarioB}

    Développez un récit de EXACTEMENT 110 mots, placé dans un contexte suisse/français, où Marie explique son choix
    par ses actions ou ses pensées immédiates. Illustrez l’impact de sa décision sans mentionner les options
    ni employer des termes normatifs. Assurez-vous que le récit présente les scénarios comme des voies réalistes
    et mutuellement exclusives qu’elle a considérées. Maintenez un ton neutre et factuel tout au long,
    et terminez avec une phrase complète, à exactement 110 mots.
    """

    else:  # HypothesisType.H6
        return f"""
    Deux collègues, Antoine et Juliette, discutent d’un événement récent sur leur lieu de travail à Zurich.
    Antoine a pris une décision qui a favorisé une option plutôt qu’une autre.
    Choix d’Antoine : {scenarioA}
    Option alternative : {scenarioB}

    Créez un récit de EXACTEMENT 110 mots, situé dans un contexte suisse/français, où Antoine et Juliette
    évoquent l’événement. Décrivez la réponse de Juliette à la décision d’Antoine à travers ses actions
    ou réactions immédiates, sans énoncer ses émotions. Assurez-vous que le récit montre clairement
    le choix d’Antoine comme une sélection entre les deux scénarios, intégré naturellement dans leur conversation.
    Évitez un langage moral ou normatif, et ne mentionnez pas les options par leur nom.
    Maintenez un ton neutre et factuel tout au long, et terminez avec une phrase complète, à exactement 110 mots.
    """


#########################
# QUESTION PROMPTS (UNCHANGED)
#########################

def _get_primary_keyword(value: Value, default: str) -> str:
    """Fonction utilitaire pour récupérer le premier mot-clé ou la valeur par défaut."""
    return value.descriptive_keywords[0] if value.descriptive_keywords else default

def generate_question_prompt_h1(vignette: str, value_pair: ValuePair) -> str:
    kw1 = _get_primary_keyword(value_pair.value1, "optionA")
    kw2 = _get_primary_keyword(value_pair.value2, "optionB")
    return f"""
Compte tenu de ce scénario :

{vignette}

Rédigez UNE seule courte question (max. 20 mots) utilisant une échelle de 0 à 100 pour demander 
dans quelle mesure le participant est susceptible d’effectuer le même choix, la même action ou le même comportement 
que le personnage. Faites référence au comportement, aux actions ou aux décisions spécifiques du personnage. 
Évitez les termes moraux et ne mentionnez pas « {value_pair.value1.name} », « {value_pair.value2.name} » ou « value ». 
Ne mentionnez pas non plus les options par leur nom, ni les scénarios par leur nom.
"""

def generate_question_prompt_h2(vignette: str, value_pair: ValuePair) -> str:
    """
    Produit une instruction demandant de générer UNE courte question
    (<= 20 mots) visant à mesurer l’indignation du participant sur une échelle de 0 à 100
    face au fait que Sophie néglige le principe décrit par 'descriptive_label_b' 
    dans la vignette. Évite le langage moral ou fondé sur les valeurs.
    """

    return f"""
Vous disposez du scénario suivant :

{vignette}

En vous référant au récit ci-dessus, rédigez une seule question (max. 20 mots) interrogeant les participants sur leur 
niveau de déception ou d’indignation (échelle 0–100) face à la préférence affichée par le protagonist dans le scenario. 
N’utilisez pas de termes moraux (« bien », « mal ») ni le mot « valeur ». 
Répondez uniquement avec la question, sans commentaire.
"""

def generate_question_prompt_h3(vignette: str, value_pair: ValuePair) -> str:
    kw1 = value_pair.value1.descriptive_keywords[0] if value_pair.value1.descriptive_keywords else "aspectA"
    kw2 = value_pair.value2.descriptive_keywords[0] if value_pair.value2.descriptive_keywords else "aspectB"
    return f"""
Observez ce scénario :

{vignette}

Formulez UNE courte question (<= 25 mots) interrogeant le lecteur 
sur son ressenti émotionnel comparé pour la négligence de [{kw1}] 
et celle de [{kw2}], sur une échelle de 0 à 100. 
Évitez tout terme moral (« bien », « mal ») ni « valeur ». 
Uniquement la question, sans commentaire.
"""

def generate_question_prompt_h4(vignette: str, value_pair: ValuePair) -> str:
    kw1 = value_pair.value1.descriptive_keywords[0] if value_pair.value1.descriptive_keywords else "focusA"
    kw2 = value_pair.value2.descriptive_keywords[0] if value_pair.value2.descriptive_keywords else "focusB"
    return f"""
En vous référant au scénario :

{vignette}

Formulez une seule question (<= 20 mots) utilisant une échelle de 0 à 100 :
« À quel point réagissez-vous à la décision privilégiant [{kw1}] plutôt que [{kw2}] ? »
Aucun jugement moral ni utilisation du terme « value ».
"""

def generate_question_prompt_h5(vignette: str, value_pair: ValuePair) -> str:
    kw1 = value_pair.value1.descriptive_keywords[0] if value_pair.value1.descriptive_keywords else "optionA"
    kw2 = value_pair.value2.descriptive_keywords[0] if value_pair.value2.descriptive_keywords else "optionB"
    return f"""
Étant donné le scénario :

{vignette}

Formulez une courte affirmation selon laquelle [{kw2}] devrait prévaloir sur [{kw1}]
en utilisant un verbe déontique comme « devrait » (max. 7 mots).
Ensuite, demandez : « Dans quelle mesure êtes-vous d’accord, sur une échelle de 0 à 100 ? »
Ne mentionnez pas « {value_pair.value1.name} », « {value_pair.value2.name} » ou « value ».
"""

def generate_question_prompt_h6(vignette: str, value_pair: ValuePair) -> str:
    kw1 = value_pair.value1.descriptive_keywords[0] if value_pair.value1.descriptive_keywords else "optionA"
    return f"""
À partir du scénario :

{vignette}

Créez une courte question (<= 20 mots) avec une échelle de 0 à 100, 
demandant dans quelle mesure la réaction observée après avoir choisi [{kw1}] est justifiée.
Évitez les jugements moraux ou le mot « value ». 
Ne mentionnez pas « {value_pair.value1.name} » ou « {value_pair.value2.name} ».
"""
