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
    v_typical_emotional_reactions = ", ".join(value.typical_emotional_reactions)
    v_associated_actions = ", ".join(value.associated_actions_and_behaviors)
    v_influencing_factors = ", ".join(value.influencing_factors)
    v_observable_indicators = ", ".join(value.observable_indicators)
    v_factual_scenarios = ", ".join(value.factual_scenarios)
    v_opposite_aspect = ", ".join(value.aspect_negatif)

    definition: str

    return f"""
Rédigez un court scénario factuel de EXACTEMENT 60 mots.
Ce scénario doit illustrer la situation correspondant à : {value.definition}
sans mentionner explicitement cette valeur ni utiliser un langage normatif.
Utilisez les éléments suivants pour guider la description :
- Mots-clés descriptifs : {v_descriptive_keywords}
- Schémas observés : {v_common_patterns}
- Caractéristiques contextuelles : {v_contextual_features}
- Actions associées : {v_associated_actions}
- Émotions typiques : {v_typical_emotional_reactions}
- Facteurs d'influence : {v_influencing_factors}
- Indicateurs observables : {v_observable_indicators}
- Scénarios factuels : {v_factual_scenarios}
- Les aspects opposés et rejetés : {v_opposite_aspect}
Le texte doit être simple, clair et permettre au lecteur de se projeter dans la situation.
Terminez par une phrase complète.
"""


#########################
#  STEP 2: Combine Two Scenarios
#########################

def combine_scenarios_prompt(scenarioA: str, scenarioB: str, hypothesis_type: HypothesisType,
                             value_pair: ValuePair) -> str:
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
    À partir des deux scénarios suivants :
    Scénario A : {scenarioA}
    Scénario B : {scenarioB}

    Rédigez une vignette de EXACTEMENT 110 mots qui présente deux trajectoires de vie alternatives 
    et réelles dans lesquelles le protagoniste peut s'engager (au travail, en famille, dans ses interactions 
    sociales). Le récit doit clairement montrer que ces deux trajectoires s'opposent et que s'engager dans 
    le scénario A exclut activement la possibilité de vivre le scénario B. Le protagoniste choisit le scénario 
    A car il attache plus d'importance à la valeur {value_pair.value1.name} qu'à la valeur {value_pair.value2.name}. 
    Le texte doit rester neutre, factuel et sans langage normatif. N’utilisez PAS le mot "valeur" ni les noms 
    des valeurs. Assurez-vous que le scénario A, choisi par le protagoniste, soit une illustration compréhensible 
    de la valeur {value_pair.value1.name}, définie comme : {value_pair.value1.definition} et que le scénario B 
    soit une illustration compréhensible de la valeur {value_pair.value2.name}, définie comme : {value_pair.value2.definition}.
    Terminez par une phrase complète.
    """

    elif hypothesis_type == HypothesisType.H2:
        return f"""
    À partir des deux scénarios suivants :
    Scénario A (manifestation quotidienne d'un engagement structuré et cohérent) : {scenarioA}
    Scénario B (manifestation d'aspects négligés ou indifférents dans le quotidien) : {scenarioB}

    Rédigez un extrait de roman biographique de EXACTEMENT 110 mots qui raconte l'histoire et illustre le charactère d'un protagoniste 
    dont la vie quotidienne (au travail, en famille, dans ses interactions) révèle une préférence constante 
    pour le scénario A ou des éléments semblables et une négligence ou une certaine indifférence pour le scénario B ou des éléments semblables. 
    Le récit doit montrer comment ces deux mondes s'inscrivent naturellement dans son parcours, 
    avec une préférence évidente pour le scénario A et une négligence voir une certain indiférence pour le scénario B.
    Le texte doit rester neutre, factuel et sans langage normatif. N’utilisez PAS le mot "valeur" ni les noms des valeurs. 
    Terminez par une phrase complète.
    """

    elif hypothesis_type == HypothesisType.H3:
        return f"""
    À partir des deux scénarios suivants :
    Scénario A (illustrant concrètement un engagement positif) : {scenarioA}
    Scénario B (illustrant concrètement un autre engagement positif) : {scenarioB}

    Rédigez un extrait de roman biographique de EXACTEMENT 110 mots qui raconte l'histoire et illustre le charactère d'un protagoniste 
    dont la vie quotidienne (au travail, en famille, dans ses interactions) révèle un rejet actif des deux scénarios présentées. 
    Bien que ces scénarios incarnent respectivement {value_pair.value1.name} et {value_pair.value2.name}, le protagoniste adopte, 
    de manière récurrente, des comportements opposés à ces engagements et renverse les normes qui y sont associées. 
    Le récit doit montrer comment, dans sa vie professionnelle, familiale et sociale, il ne fait aucun compromis sur ces attitudes contraires. 
    Le texte doit rester neutre et factuel. N’utilisez PAS le mot "valeur" ni les noms des valeurs ni aucune forme de jugement de valeurs.
    Terminez par une phrase complète.
    """

    elif hypothesis_type == HypothesisType.H4:
        return f"""
    A partir de ces deux scénarios suivants :
    Scénario A : {scenarioA}
    Scénario B : {scenarioB}

    Écrivez une courte histoire (max 120 mots) où un observateur assiste à une situation où la première pratique du scénario A est 
    compromise au profit de la seconde du scénario B. Montrez l'impact sur les personnes concernées. L'histoire doit sembler spontanée, 
    sans révéler sa construction autour d'un point de vue témoin et sans mention de valeurs ni la nature des scénarios.
    """

    elif hypothesis_type == HypothesisType.H5:
        return f"""
    A partir de ces deux scénarios suivants :
    Scénario A : {scenarioA}
    Scénario B : {scenarioB}

    Écrivez une courte histoire (max 120 mots) présentant une situation où la pratique du premier scénario est menacée par 
    celle du second. Montrez les enjeux concrets sans jugement. L'histoire doit sembler authentique, sans révéler 
    sa construction autour d'un conflit et sans mention de valeurs ni la nature des scénarios.
    """

    else:  # HypothesisType.H6
        return f"""
    A partir de ces deux scénarios suivants :
    Scénario A : {scenarioA}
    Scénario B : {scenarioB}

    Écrivez une courte histoire (max 120 mots) où un protagoniste menace la pratique du scénario A en privilégiant le scénario B, et ou un observateur 
    réagit, par son indignation, aux actions du protagoniste privilégiant le scénario B au détriment du scénario A.
    Décrivez leur réaction de manière factuelle. L'histoire doit sembler naturelle, sans révéler qu'elle est construite autour d'une réaction.
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
Pour la vignette suivante :

{vignette}

Formulez une question simple (max 20 mots) demandant au participant qui lit la vignette s'il choisirait ou agirait 
de la même manière que le protagoniste de la vignette, sur une échelle de 0 à 100. La question doit sembler spontanée et utiliser une échelle de 0 à 100.
"""


def generate_question_prompt_h2(vignette: str, value_pair: ValuePair) -> str:
    """
    Produit une instruction demandant de générer UNE courte question
    (<= 20 mots) visant à mesurer l’indignation du participant sur une échelle de 0 à 100
    face au fait que Sophie néglige le principe décrit par 'descriptive_label_b' 
    dans la vignette. Évite le langage moral ou fondé sur les valeurs.
    """
    kw1 = (
        value_pair.value1.descriptive_keywords
        if value_pair.value1.descriptive_keywords
        else "aspectA"
    )
    kw2 = (
        value_pair.value2.descriptive_keywords
        if value_pair.value2.descriptive_keywords
        else "aspectB"
    )

    return f"""
Pour la vignette suivante :

{vignette}

Identifiez bien les éléments concrets A, non normatifs, associés aux principes [{kw1}] et
les élémentes concrets B, non normatifs, associés aux principes[{kw2}]. Formulez une question simple et courte (max 20 mots), 
demandant au participant avec quelle probabilitlé, sur une échelle de 0-100, 
la négligence ou l'indifférence du protagoniste décrite dans la vignette pour les éléments concrets B et ses elements 
{kw2} suciterait, chez le participant, une émotion d'indignation ou de colère s'il connaissait le protagoniste.
La question doit sembler naturelle et bien utiliser une échelle de 0 à 100 pour déterminer la catégorie de l'émotion, non son intensité.
"""


def generate_question_prompt_h3(vignette: str, value_pair: ValuePair) -> str:
    kw1 = (
        value_pair.value1.descriptive_keywords
        if value_pair.value1.descriptive_keywords
        else "aspectA"
    )
    kw2 = (
        value_pair.value2.descriptive_keywords
        if value_pair.value2.descriptive_keywords
        else "aspectB"
    )

    return f"""
Pour la vignette suivante :

{vignette}

Identifiez bien les éléments concrets A, non normatifs, de cette vignette exemplifiant une violation de [{kw1}] et
les élémentes concrets B, non normatifs, de la vignette montrant que le protagoniste viole aussi les principes [{kw2}]. Choisissez un élément 
de [{kw1}] - principe A - et un élément de [{kw2}] - principe B - qui chacun décrit le mieux ce qui est violé 
par le comportement du protagoniste de la vignette. Formulez une question simple (max 20 mots) demandant au participant à quel point, 
sur une échelle de 0-100, son indignation ressentie face à la violation des éléments concrets A par le protagoniste de la 
vignette est plus intense que la violation des éléments concrets B par le protagoniste de la vignette. 
La question doit sembler naturelle et utiliser une échelle de 0 à 100.
"""


def generate_question_prompt_h4(vignette: str, value_pair: ValuePair) -> str:
    kw1 = value_pair.value1.name if value_pair.value1.name else "focusA"
    kw2 = value_pair.value2.name if value_pair.value2.name else "focusB"
    return f"""
En vous référant au scénario :

{vignette}

Formulez une question simple (max 20 mots) sur le sentiment d'indignation ou désapprobation ressenti comme témoin. La question doit paraître naturelle et utiliser une échelle de 0 à 100.
"""


def generate_question_prompt_h5(vignette: str, value_pair: ValuePair) -> str:
    kw1 = value_pair.value1.descriptive_keywords if value_pair.value1.descriptive_keywords else "optionA"
    kw2 = value_pair.value2.descriptive_keywords if value_pair.value2.descriptive_keywords else "optionB"
    return f"""
Pour la vignette suivante :

{vignette}

Choisissez un element de {kw1} et un element de {kw2} qui résume le mieux les deux scenarios, actions, décisions 
ou états de choses de la vignette. Formulez ensuite une phrase normative très courte (max 10 mots) et concise, avec une formulation déontique forte, 
indiquant comme dans la vignette que le principe choisi dans [{kw1}] doit/devrait primer sur le principe choisi dans [{kw2}]. 
Enfin, ajoutez immédiatement une question simple (max 20 mots) demandant : "Sur une échelle de 0 à 100, 
à quel point êtes-vous d'accord avec cette proposition ?". 
Votre réponse finale doit consister UNIQUEMENT en la phrase normative suivie de la question.
"""


def generate_question_prompt_h6(vignette: str, value_pair: ValuePair) -> str:
    kw1 = value_pair.value1.descriptive_keywords[0] if value_pair.value1.descriptive_keywords else "optionA"
    return f"""
Pour la vignette suivante :

{vignette}

Formulez une question simple (max 20 mots) en demandant au participant si l'émotion d'indignation ou de désapprobation 
ressentie par l'observateur et décrite dans la vignette est justifiée, sur une échelle de 0 à 100. La question doit sembler 
spontanée et utiliser une échelle de 0 à 100.

"""
