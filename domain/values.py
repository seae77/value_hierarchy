from dataclasses import dataclass, field
from typing import List
import random


@dataclass
class Value:
    """
    Représente une valeur unique avec des champs descriptifs détaillés et une
    dichotomie implicite en intégrant l'aspect positif et son opposé (vice).
    Cette structure permet une génération de scénarios approfondie et non normative,
    en se basant sur le modèle des fondements moraux de Jonathan Haidt.
    """
    name: str
    definition: str
    descriptive_keywords: List[str]
    example_phrases: List[str]
    common_observed_patterns: List[str] = field(default_factory = list)
    contextual_features: List[str] = field(default_factory = list)
    typical_emotional_reactions: List[str] = field(default_factory = list)
    institutional_or_group_contexts: List[str] = field(default_factory = list)
    cultural_variations_and_history: List[str] = field(default_factory = list)
    associated_actions_and_behaviors: List[str] = field(default_factory = list)
    influencing_factors: List[str] = field(default_factory = list)
    observable_indicators: List[str] = field(default_factory = list)
    factual_scenarios: List[str] = field(default_factory = list)
    example_factual_questions: List[str] = field(default_factory = list)
    # Nouveau champ pour intégrer la dimension négative (vice) correspondant à la dichotomie Haidt
    aspect_negatif: List[str] = field(default_factory = list)

    def as_dict(self) -> dict:
        """
        Renvoie un dictionnaire représentant cette Value,
        utile pour la sérialisation JSON ou le logging.
        """
        return {
            "name": self.name,
            "definition": self.definition,
            "descriptive_keywords": self.descriptive_keywords,
            "example_phrases": self.example_phrases,
            "common_observed_patterns": self.common_observed_patterns,
            "contextual_features": self.contextual_features,
            "typical_emotional_reactions": self.typical_emotional_reactions,
            "institutional_or_group_contexts": self.institutional_or_group_contexts,
            "cultural_variations_and_history": self.cultural_variations_and_history,
            "associated_actions_and_behaviors": self.associated_actions_and_behaviors,
            "influencing_factors": self.influencing_factors,
            "observable_indicators": self.observable_indicators,
            "factual_scenarios": self.factual_scenarios,
            "example_factual_questions": self.example_factual_questions,
            "aspect_negatif": self.aspect_negatif,
        }


@dataclass
class ValuePair:
    """
    Représente une paire de valeurs distinctes utilisées pour créer un conflit,
    un contraste ou une synergie dans des vignettes ou lors de la génération de scénarios.
    """
    value1: Value
    value2: Value

    def as_dict(self) -> dict:
        """
        Renvoie un dictionnaire pour un accès plus facile ou pour la sérialisation JSON.
        """
        return {
            "value1": self.value1.as_dict(),
            "value2": self.value2.as_dict(),
        }


values = [
    Value(
        name = "Care",
        definition = (
            "Fondation morale centrée sur la bienveillance, l'empathie et la protection des autres. "
            "Elle implique la sensibilité à la souffrance d'autrui et la volonté d'y remédier par la compassion "
            "et la douceur, nourrissant les valeurs de gentillesse et de soutien mutuel."
        ),
        descriptive_keywords = [
            "empathie",
            "compassion",
            "protection",
            "bienveillance",
            "solidarité",
            "sensibilité",
            "soutien"
        ],
        example_phrases = [
            "Écouter attentivement un ami en difficulté et lui offrir un réconfort",
            "S'engager dans une association d'aide humanitaire locale",
            "Proposer son aide à une personne âgée pour porter ses courses",
            "Offrir un soutien moral à un collègue qui traverse une période difficile",
            "Rendre visite à un proche hospitalisé pour lui remonter le moral",
            "Faire du bénévolat dans un refuge pour animaux"
        ],
        common_observed_patterns = [
            "Aide proactive envers les personnes vulnérables",
            "Recherche de solutions pour alléger la souffrance d'autrui",
            "Manifestation fréquente de gestes de tendresse ou de réconfort",
            "Sensibilité émotionnelle accrue lorsqu'une injustice ou une douleur est perçue",
            "Tendance à valoriser la solidarité et la protection des plus faibles",
            "Recherche de moyens concrets pour améliorer le bien-être collectif"
        ],
        contextual_features = [
            "Environnements médicaux et de soins (hôpitaux, cliniques, etc.)",
            "Organisations caritatives ou à but non lucratif centrées sur l'aide",
            "Programmes d'entraide communautaires (alimentaires, vestimentaires, etc.)",
            "Institutions éducatives valorisant la coopération et la bienveillance",
            "Groupes de soutien psychologique ou forums d'entraide en ligne",
            "Communautés religieuses ou laïques proposant un accompagnement moral"
        ],
        typical_emotional_reactions = [
            "Empathie et compassion face à la détresse d'autrui",
            "Satisfaction ressentie après avoir aidé ou soutenu quelqu'un",
            "Tristesse lorsque l'on est témoin d'une souffrance non résolue",
            "Culpabilité ou regret si l'on n'a pas pu assister une personne vulnérable",
            "Réconfort mutuel lors d'échanges empreints d'écoute et de gentillesse",
            "Motivation à faire plus d'efforts pour soulager la souffrance perçue"
        ],
        institutional_or_group_contexts = [
            "ONG et associations humanitaires (Croix-Rouge, Secours Populaire, etc.)",
            "Programmes de responsabilisation sociale en entreprise",
            "Structures médico-sociales (EHPAD, foyers d'accueil, etc.)",
            "Centres communautaires proposant des permanences sociales",
            "Collectifs citoyens organisant des maraudes pour les sans-abris",
            "Églises, mosquées, temples ou groupes spirituels prônant l'entraide"
        ],
        cultural_variations_and_history = [
            "Différentes cultures valorisant plus ou moins l'expression publique de l'empathie",
            "Évolutions historiques des droits de l'enfant, de la femme et des personnes vulnérables",
            "Importance traditionnelle du care dans certaines sociétés matriarcales ou collectivistes",
            "Rôle des philosophies et religions dans la promotion de la charité et du soutien mutuel",
            "Naissance et développement des systèmes de sécurité sociale et de protection",
            "Émergence des mouvements de défense animale qui élargissent la notion de care"
        ],
        associated_actions_and_behaviors = [
            "Offrir un accompagnement psychologique ou matériel",
            "Créer ou rejoindre des initiatives de soutien local (banques alimentaires, etc.)",
            "Élaborer des politiques publiques pour protéger les populations vulnérables",
            "Multiplier les temps d'écoute et d'échanges personnalisés",
            "Mettre en place des formations sur l'empathie et la prévention du harcèlement",
            "Valoriser les professions du care (infirmiers, aidants, éducateurs)"
        ],
        influencing_factors = [
            "Degré de sensibilisation aux problématiques sociales",
            "Expériences personnelles de vulnérabilité ou de souffrance",
            "Encouragement institutionnel au bénévolat ou aux actions caritatives",
            "Contexte familial valorisant l'empathie et l'entraide",
            "Visibilité médiatique des causes humanitaires",
            "Politiques publiques facilitant le soutien aux plus démunis"
        ],
        observable_indicators = [
            "Fréquence et constance de l'aide concrète apportée (dons, visites, soutien moral)",
            "Qualité d'écoute et de compréhension lors d'échanges interpersonnels",
            "Participation à des projets d'entraide ou à des collectes de fonds",
            "Adaptation du langage et du comportement pour ménager la sensibilité d'autrui",
            "Attitudes protectrices envers les personnes ou êtres vivants fragilisés",
            "Propension à défendre la cause d'une personne injustement critiquée"
        ],
        factual_scenarios = [
            "Une jeune femme monte une association pour soutenir des familles monoparentales en difficulté",
            "Un voisinage s'organise pour cuisiner et livrer des repas à un habitant isolé",
            "Un collègue se propose d'accompagner un nouvel arrivant dans l'entreprise pour faciliter son intégration",
            "Un étudiant rend visite chaque semaine à une personne âgée pour rompre sa solitude",
            "Un refuge pour animaux recrute des bénévoles afin de prendre soin de chiens abandonnés",
            "Un enseignant met en place un système de tutorat entre élèves pour favoriser l'entraide"
        ],
        example_factual_questions = [
            "Quelles ressources sont mobilisées pour venir en aide aux personnes en situation de détresse ?",
            "Comment la communauté s'organise-t-elle pour apporter un soutien concret ?",
            "De quelle manière les sentiments d'empathie sont-ils déclenchés ou encouragés dans cette situation ?",
            "Quels outils de communication facilitent la mise en place d'initiatives bienveillantes ?",
            "Comment les individus évaluent-ils leurs capacités à soutenir autrui avant de s'engager ?",
            "Quels indicateurs permettent de mesurer l'impact réel des actions d'aide sur les bénéficiaires ?"
        ],
        aspect_negatif = [
            "Indifférence à la souffrance d'autrui : Absence d'empathie et manque de réactivité face à la douleur ou au désespoir des autres.",
            "Comportements nuisibles : Actes intentionnels ou par négligence qui causent de la souffrance physique ou psychologique.",
            "Cruauté et maltraitance : Manifestation de comportements violents, abusifs ou exploitants, sans considération pour l'intégrité ou le bien-être d'autrui.",
            "Négligence active : Refus ou incapacité à intervenir pour prévenir ou atténuer la souffrance, laissant les personnes vulnérables dans des situations dangereuses.",
            "Priorisation de l'intérêt personnel : Tendance à mettre ses propres besoins ou désirs au détriment du bien-être collectif, même si cela engendre des dommages pour les autres.",
            "Absence de soutien ou de solidarité : Manque de volonté de venir en aide, de partager ou de soutenir autrui dans les moments difficiles.",
            "Justification de la violence : Rationalisation ou acceptation de comportements agressifs et destructeurs comme moyens d'atteindre des objectifs personnels.",
            "Dénégation de la dignité humaine : Rejet ou minimisation de la valeur intrinsèque de chaque individu, pouvant conduire à la déshumanisation et au mépris."
        ]

    ),
    Value(
        name = "Fairness",
        definition = (
            "Fondation morale tournée vers la justice, l'équité et les droits de chacun. "
            "Elle s'appuie sur l'idée de réciprocité, de respect mutuel et de transparence, "
            "assurant une distribution équitable des ressources et des responsabilités."
        ),
        descriptive_keywords = [
            "justice",
            "équité",
            "droits",
            "réciprocité",
            "transparence",
            "proportionnalité",
            "impartialité"
        ],
        example_phrases = [
            "Répartir des tâches de manière équilibrée dans une équipe de travail",
            "Vérifier que chacun ait accès aux mêmes informations avant de décider",
            "Appliquer un barème clair pour allouer des ressources ou des avantages",
            "Réclamer de la transparence dans l'attribution de subventions ou de bourses",
            "Insister pour que toutes les candidatures soient évaluées sur les mêmes critères",
            "Mettre en place des règles garantissant un temps de parole équitable"
        ],
        common_observed_patterns = [
            "Vérification de la conformité aux règlements ou procédures préétablies",
            "Obligation morale de signaler les situations de tricherie ou de favoritisme",
            "Réaction forte face à des pratiques discriminatoires ou injustes",
            "Recours à des instances de médiation ou de régulation pour rétablir l'équité",
            "Prise en compte des besoins individuels tout en préservant l'impartialité générale",
            "Application de sanctions ou de correctifs en cas de non-respect de l'égalité de traitement"
        ],
        contextual_features = [
            "Tribunaux, instances disciplinaires, organes de contrôle",
            "Politiques d'égalité des chances dans le domaine de l'emploi ou de l'éducation",
            "Programmes de responsabilité sociale et de diversité en entreprise",
            "Règles de répartition (quotas, points, tirage au sort) dans les organisations",
            "Codes de conduite professionnels ou déontologiques",
            "Comités indépendants chargés de valider des décisions potentielles sources de conflits"
        ],
        typical_emotional_reactions = [
            "Satisfaction et sentiment de sécurité lorsque les décisions sont équitables",
            "Colère ou frustration lorsqu'un cas de discrimination ou d'injustice est révélé",
            "Volonté de corriger la situation ou de réparer le tort subi",
            "Confiance renforcée envers les institutions jugées transparentes",
            "Désir de promouvoir des initiatives garantissant davantage d'équité",
            "Méfiance accrue si les décisions semblent manquer de clarté ou de neutralité"
        ],
        institutional_or_group_contexts = [
            "Systèmes légaux et cours de justice",
            "Organisations internationales prônant l'équité (Nations Unies, ONG diverses)",
            "Collectifs citoyens contrôlant la bonne application des lois",
            "Entreprises soumises à des audits pour vérifier le respect de la diversité",
            "Syndicats ou associations défendant les droits de groupes spécifiques",
            "Instances professionnelles de régulation (ordres, chambres) assurant une discipline"
        ],
        cultural_variations_and_history = [
            "Évolution des notions de justice et d'égalité à travers le temps (droit romain, Magna Carta, etc.)",
            "Cultures où la redistribution solidaire est valorisée (systèmes tribaux, coutumes locales)",
            "Influences des mouvements sociaux (droits civiques, égalité femmes-hommes) sur l'idée d'équité",
            "Approches différenciées de la « justice corrective » vs la « justice distributive »",
            "Débats historiques autour des quotas et de la discrimination positive",
            "Rôle des religions et courants philosophiques (ex. contractualisme) dans la définition de la justice"
        ],
        associated_actions_and_behaviors = [
            "Propositions de lois visant à réduire les inégalités",
            "Création de comités d'éthique ou de transparence",
            "Organisation de procès publics ou de débats contradictoires",
            "Publication de rapports sur l'égalité des salaires et des chances",
            "Veille citoyenne ou associative pour dénoncer les irrégularités",
            "Éducation et sensibilisation à la citoyenneté et aux droits fondamentaux"
        ],
        influencing_factors = [
            "Cadres juridiques et politiques en vigueur",
            "Culture organisationnelle et valeurs internes",
            "Moyens financiers pour contrôler et sanctionner",
            "Niveau d'information du public et des médias",
            "Existence d'acteurs indépendants (ONG, syndicats, presse libre)",
            "Pressions sociales et historiques (mouvements de protestation, plaidoyers)"
        ],
        observable_indicators = [
            "Existence de règles transparentes et accessibles à tous",
            "Mise en place de mécanismes de contrôle indépendants",
            "Statistiques montrant une répartition équitable des ressources",
            "Témoignages et retours d'expérience soulignant la justesse des décisions",
            "Faible taux de contentieux lié à des accusations d'injustice",
            "Réputation d'intégrité des instances ou organisations concernées"
        ],
        factual_scenarios = [
            "Un concours ouvert à tous les candidats, sélectionnés sur des critères anonymisés",
            "Une commission municipale qui publie ses comptes-rendus pour justifier ses choix budgétaires",
            "Une entreprise adoptant une politique de non-discrimination stricte dans ses recrutements",
            "Des bourses étudiantes attribuées selon un système de points défini et vérifiable",
            "Un jury citoyen tiré au sort pour participer à l'élaboration d'un plan d'urbanisme",
            "Une organisation humanitaire distribuant équitablement des vivres sans distinction d'origine"
        ],
        example_factual_questions = [
            "Quelles règles ou procédures garantissent l'équité dans ce scénario ?",
            "Comment l'attribution des ressources est-elle contrôlée et validée ?",
            "Quels mécanismes permettent de contester une décision jugée injuste ?",
            "Comment les données (statistiques, documents) sont-elles rendues accessibles au public ?",
            "Quelles sanctions ou réparations sont prévues en cas de non-respect de la fairness ?",
            "Comment la transparence et la clarté renforcent-elles la confiance des acteurs impliqués ?"
        ],
        aspect_negatif = [
            "Manipulation des règles : Violation délibérée des normes d'équité pour obtenir des avantages injustifiés.",
            "Tricherie systématique : Recours fréquent à des moyens malhonnêtes pour contourner les critères établis.",
            "Favoritisme : Accord de traitements de faveur à certains individus au détriment de l'égalité des chances.",
            "Opacité des procédures : Manque de transparence dans la prise de décision, menant à des pratiques inéquitables.",
            "Exploitation des failles : Usage abusif des vulnérabilités du système pour obtenir un gain personnel non mérité.",
            "Détournement de ressources : Accaparement injustifié de ressources ou d'opportunités sans considération pour l'équité.",
            "Absence de réciprocité : Comportement unilatéral où l'intérêt personnel prévaut sur un échange équitable.",
            "Refus de responsabilité : Dénégation ou minimisation des comportements malhonnêtes, empêchant la correction des injustices."
        ]

    ),
    Value(
        name = "Loyalty",
        definition = (
            "Fondation morale liée à la fidélité et à la solidarité envers un groupe, une communauté ou une cause. "
            "Elle reflète le sentiment d'appartenance et le désir de coopérer, de défendre et de soutenir ceux "
            "avec qui l'on partage un lien d'identité ou d'engagement commun."
        ),
        descriptive_keywords = [
            "fidélité",
            "solidarité",
            "appartenance",
            "collectif",
            "unité",
            "allégeance",
            "esprit de corps"
        ],
        example_phrases = [
            "Soutenir publiquement son équipe dans les moments de difficulté",
            "Participer à la défense d'un collègue injustement critiqué",
            "Partager spontanément des ressources avec les membres de son groupe",
            "Faire preuve de solidarité lors de conflits externes pour protéger sa communauté",
            "Être fier de son affiliation à une association ou un club et le représenter avec respect",
            "Organiser des événements fédérateurs qui renforcent l'esprit d'équipe"
        ],
        common_observed_patterns = [
            "Importance accordée aux symboles (drapeaux, chants, couleurs) pour exprimer l'appartenance",
            "Recours à une identité commune pour souder les individus dans des projets collectifs",
            "Tolérance plus grande envers les défauts ou erreurs internes, volonté de protéger le groupe",
            "Réactions fortes contre toute forme de trahison ou de rupture d'engagement",
            "Mise en avant du « nous » pour renforcer la cohésion interne",
            "Coordination ou synchronisation d'actions communes pour consolider la loyauté"
        ],
        contextual_features = [
            "Groupes sportifs, équipes de travail, organisations militantes",
            "Communautés religieuses ou ethniques valorisant la cohésion",
            "Armées ou corps d'élite axés sur la fraternité et la fidélité mutuelle",
            "Groupes d'entreprises partenaires agissant de concert dans un même secteur",
            "Cercles associatifs ou fraternités étudiantes",
            "Comités ou guildes en ligne où la solidarité virtuelle est de mise"
        ],
        typical_emotional_reactions = [
            "Fierté et exaltation lorsqu'on sent l'appui de son groupe",
            "Colère ou sentiment de trahison lorsqu'un membre rompt le pacte de loyauté",
            "Sécurité émotionnelle du fait de se sentir soutenu",
            "Motivation accrue pour défendre la réputation ou l'intérêt commun",
            "Empathie renforcée envers ceux qui partagent la même bannière ou le même but",
            "Sentiment d'appartenance et d'acceptation lorsqu'on est reconnu comme membre à part entière"
        ],
        institutional_or_group_contexts = [
            "Armées, corps policiers, organisations sécuritaires",
            "Entreprises prônant la culture d'équipe et la loyauté interne",
            "Groupes de supporters sportifs, clubs de fans",
            "Partis politiques et mouvements idéologiques",
            "Associations ou fraternités valorisant le sentiment d'unité",
            "Syndicats défendant les droits et intérêts de leurs adhérents"
        ],
        cultural_variations_and_history = [
            "Groupes tribaux ou claniques ancrant la solidarité dans la parenté",
            "Émergence de nationalismes et de patriotismes à différentes époques",
            "Phénomènes de coalitions et d'alliances stratégiques dans l'histoire militaire",
            "Rôle de la loyauté dans l'essor de grandes corporations ou dynasties royales",
            "Existence de serments de fidélité dans les guildes médiévales ou les confréries religieuses",
            "Impact de la mondialisation sur les identités collectives et la loyauté"
        ],
        associated_actions_and_behaviors = [
            "Signatures de pactes ou de contrats internes pour sceller l'union",
            "Participation à des rituels ou cérémonies de cohésion",
            "Port d'un uniforme, d'un badge ou de signes distinctifs du groupe",
            "Communication défensive ou protectrice face à des critiques extérieures",
            "Engagement dans des manifestations de soutien (financier, moral, etc.)",
            "Valorisation de la coopération et du partage d'informations entre membres"
        ],
        influencing_factors = [
            "Organisation hiérarchique ou horizontale du groupe",
            "Histoire et vécu collectif (traumatismes, victoires, héritage commun)",
            "Leadership et charisme des figures d'autorité ou de référence",
            "Pression extérieure (concurrents, adversaires, critiques publiques)",
            "Représentation médiatique et reconnaissance externe du groupe",
            "Bénéfices concrets à être fidèle (avantages, protection, reconnaissance)"
        ],
        observable_indicators = [
            "Taux d'engagement et de participation aux activités collectives",
            "Réactions immédiates de soutien ou de défense mutuelle",
            "Valorisation publique des succès partagés",
            "Utilisation récurrente des termes 'nous', 'notre équipe', 'nos valeurs'",
            "Faible taux de démissions ou de ruptures de contrats (dans un cadre professionnel)",
            "Expression de gratitude envers les membres qui contribuent à l'effort commun"
        ],
        factual_scenarios = [
            "Des collègues s'allient pour défendre un des leurs accusé à tort par un client",
            "Un groupe de supporters organisant des tifos pour encourager leur équipe de football",
            "Un syndicat qui négocie un accord pour améliorer les conditions de tous ses adhérents",
            "Une brigade de pompiers soude ses membres autour d'entraînements et de traditions communes",
            "Une grande famille qui met en place une cagnotte pour aider un proche en difficulté",
            "Un collectif d'artistes partageant régulièrement leurs ressources et opportunités"
        ],
        example_factual_questions = [
            "Comment le groupe manifeste-t-il son unité et son esprit collectif ?",
            "Quels rituels ou symboles renforcent la loyauté entre les membres ?",
            "De quelle manière la communauté réagit-elle face à une possible trahison ?",
            "Quels bénéfices concrets tirent les individus de leur appartenance ?",
            "Comment l'histoire commune ou les épreuves passées cimentent-elles la cohésion ?",
            "Quels mécanismes empêchent ou limitent la défection au sein du groupe ?"
        ],
        aspect_negatif = [
            "Violation de la confiance : Abandon ou trahison de la confiance placée en soi par un groupe ou un individu.",
            "Déloyauté flagrante : Acte de trahison manifeste envers des engagements partagés ou des alliances.",
            "Abandon dans les moments critiques : Fuite ou retrait quand le soutien est le plus nécessaire.",
            "Double jeu : Agir en duplicité en cachant ses véritables intentions et en soutenant des intérêts opposés.",
            "Détournement des liens : Utilisation abusive des relations personnelles pour servir des intérêts personnels au détriment du groupe.",
            "Exploitation de la vulnérabilité : Profiter de la faiblesse ou de la dépendance d'autrui pour avancer ses propres fins.",
            "Rupture des alliances : Mise en péril des relations de solidarité et de fidélité par des actes de trahison.",
            "Manipulation des engagements : Rompre des promesses ou des accords dans un but d'avantage personnel sans considération pour le collectif."
        ]

    ),
    Value(
        name = "Authority",
        definition = (
            "Fondation morale façonnée par les interactions hiérarchiques et le respect des rôles établis. "
            "Elle valorise la légitimité du leadership, la déférence envers les figures d'autorité, la tradition "
            "et l'ordre social, tout en reconnaissant les responsabilités réciproques entre dirigeants et dirigés."
        ),
        descriptive_keywords = [
            "hiérarchie",
            "leadership",
            "tradition",
            "ordre",
            "déférence",
            "structure",
            "responsabilité"
        ],
        example_phrases = [
            "Suivre les consignes d'un supérieur en qui l'on reconnaît une légitimité",
            "Respecter les règles établies par une institution officielle",
            "Souligner l'importance de la chaîne de commandement dans une unité militaire",
            "Transmettre un savoir-faire traditionnel selon des méthodes validées par l'expérience",
            "Défendre la nécessité d'un leadership ferme pour maintenir la cohésion",
            "Exiger la responsabilité des dirigeants envers ceux qu'ils dirigent"
        ],
        common_observed_patterns = [
            "Recherche d'un cadre structuré et ordonné pour la vie en société",
            "Appréciation des traditions et des modes de gouvernance éprouvés",
            "Formation de relations verticales : enseignants-élèves, chefs-équipiers, etc.",
            "Attente de respect mutuel entre ceux qui commandent et ceux qui obéissent",
            "Préférence pour des décisions prises par des figures jugées compétentes",
            "Protection du statut et de la réputation des autorités lorsqu'elles sont remises en cause"
        ],
        contextual_features = [
            "Institutions publiques (gouvernements, administrations)",
            "Organisations militaires et forces de l'ordre",
            "Entreprises à structure hiérarchique claire",
            "Écoles et universités avec un organigramme d'enseignants et de direction",
            "Communautés traditionnelles ou patriarcales mettant l'accent sur les aînés",
            "Religions avec une clergie ou un magistère influent"
        ],
        typical_emotional_reactions = [
            "Sentiment de sécurité et de stabilité lorsqu'un leadership fiable est en place",
            "Confiance accrue envers des figures d'autorité respectées",
            "Inquiétude ou rejet face à l'anarchie ou au désordre",
            "Attachement à des symboles, des cérémonies, des protocoles marquant l'autorité",
            "Frustration si l'autorité est remise en cause de manière jugée illégitime",
            "Soulagement lorsque les dirigeants assument leurs responsabilités et protègent le groupe"
        ],
        institutional_or_group_contexts = [
            "Gouvernements nationaux, parlements, tribunaux",
            "Entreprises multinationales dirigées par un conseil d'administration",
            "Organisations syndicales ou professionnelles avec un bureau dirigeant",
            "Ordres religieux ou confréries monastiques",
            "Armée et forces de police avec des grades et une chaîne de commandement",
            "Systèmes scolaires, universités ou instituts de recherche avec une gouvernance formelle"
        ],
        cultural_variations_and_history = [
            "Différentes formes de gouvernance à travers les époques (monarchies, républiques, etc.)",
            "Place de la tradition dans la transmission du pouvoir (dynasties, rites de succession)",
            "Variations culturelles sur la notion de respect envers les aînés et les chefs",
            "Impact des révolutions et des réformes sur l'acceptation de l'autorité",
            "Mouvements historiques remettant en cause la légitimité de certaines élites",
            "Débats contemporains sur la verticalité vs la horizontalité dans les organisations"
        ],
        associated_actions_and_behaviors = [
            "Prêter serment ou contracter un engagement formel envers une institution",
            "Obéir aux directives ou aux lois, même en présence de désaccord personnel",
            "Donner des ordres clairs et assumer la responsabilité d'un groupe",
            "Sanctionner ou récompenser les membres selon leur respect des règles",
            "Répondre de ses actes devant une juridiction ou une instance disciplinaire",
            "Maintenir des rituels ou des traditions symbolisant la permanence de l'ordre établi"
        ],
        influencing_factors = [
            "Structure légale et réglementaire du pays ou de l'organisation",
            "Formation et culture d'entreprise (management paternaliste, participatif, etc.)",
            "Héritage historique ou religieux valorisant la hiérarchie",
            "Perception de la compétence et de l'efficacité des leaders",
            "Pression sociale ou familiale pour respecter l'autorité",
            "Risques et conséquences liés à la désobéissance ou à la contestation"
        ],
        observable_indicators = [
            "Existence de procédures formelles de prise de décision",
            "Reconnaissance officielle de titres, de rôles ou de grades",
            "Organisation claire de la hiérarchie (organigrammes, symboles, uniforme)",
            "Usage d'un langage respectueux envers les figures d'autorité",
            "Stabilité institutionnelle et faible taux de contestation ouverte",
            "Présence de protocoles pour l'accueil et l'assermentation des nouveaux membres"
        ],
        factual_scenarios = [
            "Une armée fonctionnant sous des ordres stricts et clairs pour chaque rang",
            "Un conseil d'administration votant les grandes orientations d'une multinationale",
            "Une école avec un directeur fixant le règlement intérieur et une équipe enseignante le relayant",
            "Une communauté traditionnelle où le chef de clan arbitre les conflits",
            "Un ordre religieux où les moines suivent la règle établie depuis des siècles",
            "Un gouvernement local prenant des décisions communales avec l'assentiment de la population"
        ],
        example_factual_questions = [
            "Comment les rôles et responsabilités sont-ils définis dans cette organisation ?",
            "Quelles règles et procédures renforcent la légitimité de l'autorité ?",
            "Comment la formation ou l'expérience justifient-elles la position hiérarchique ?",
            "De quelle manière les leaders rendent-ils compte de leurs décisions ?",
            "Quels rituels ou symboles marquent l'entrée dans la structure d'autorité ?",
            "Quelles sont les conséquences en cas de désobéissance ou de remise en question de l'ordre établi ?"
        ],
        aspect_negatif = [
            "Contestations de l'autorité légitime : Remise en question ou rejet systématique des hiérarchies établies.",
            "Déstabilisation de l'ordre : Actes visant à perturber l'organisation et la stabilité institutionnelle.",
            "Soutien aux révolutions non constructives : Encouragement de révoltes ou de mouvements qui sapent les structures sans proposer de solutions alternatives.",
            "Dévalorisation des traditions : Dénigrement ou rejet des valeurs traditionnelles et des normes historiques.",
            "Incitation à la désobéissance : Encouragement de comportements non conformistes qui nuisent à la cohésion et à la discipline.",
            "Manipulation des règles pour miner l'ordre : Exploitation des failles du système afin de saper l'autorité sans viser une réforme constructive.",
            "Promotion de l'anarchie : Diffusion d'idées visant à abolir toute forme d'autorité organisée, conduisant à une absence de structure sociale.",
            "Infiltration subversive : Usage de stratégies clandestines pour affaiblir et déstabiliser les institutions de manière insidieuse."
        ]

    ),
    Value(
        name = "Sanctity",
        definition = (
            "Fondation morale inspirée par l'idée de pureté, de transcendance et de respect pour tout ce qui est considéré "
            "comme sacré ou vénérable. Elle peut impliquer des pratiques de préservation, d'hygiène spirituelle et de "
            "recherche d'une élévation au-delà de la simple matérialité, valorisant la dignité et la noblesse d'âme."
        ),
        descriptive_keywords = [
            "pureté",
            "transcendance",
            "sacré",
            "vénération",
            "dignité",
            "élan spirituel",
            "respect profond"
        ],
        example_phrases = [
            "Respecter les rites de purification avant une cérémonie religieuse",
            "S'abstenir de certains comportements jugés 'impurs' ou 'dégradants'",
            "Se recueillir en silence dans un lieu considéré comme sacré",
            "Valoriser la dignité du corps et de l'esprit à travers des pratiques ascétiques",
            "Éviter la banalisation de symboles ou d'objets jugés sacrés",
            "Célébrer la noblesse de l'homme à travers l'art et la philosophie"
        ],
        common_observed_patterns = [
            "Pratiques de purification ou de nettoyage symbolique",
            "Alimentation ou mode de vie tournés vers l'idée de pureté (végétarisme, jeûnes, etc.)",
            "Forte sensibilité au profane, à la souillure ou au sacrilège",
            "Rituels réguliers visant à se rapprocher d'un idéal moral ou spirituel",
            "Évitement de certains lieux, pratiques ou produits considérés comme corrupteurs",
            "Célébration de la beauté intérieure et du respect pour le sacré"
        ],
        contextual_features = [
            "Lieux de culte, sanctuaires, temples",
            "Institutions religieuses mettant l'accent sur les rites de purification",
            "Groupes ou ordres spirituels valorisant l'élévation de l'âme",
            "Approches philosophiques et artistiques centrées sur la pureté ou la sublimation",
            "Mouvements prônant une vie saine, sobre et épurée",
            "Communautés cherchant une communion avec la nature dans sa dimension sacrée"
        ],
        typical_emotional_reactions = [
            "Respect profond, voire sentiment de solennité, face à un objet sacré",
            "Dégoût moral ou spirituel envers ce qui est perçu comme dégradant",
            "Élévation ou plénitude lors de pratiques rituelles ou contemplatives",
            "Révolte face à la profanation de valeurs ou de lieux sacrés",
            "Recherche de la sérénité intérieure par la méditation ou l'ascèse",
            "Fierté d'adhérer à des principes considérés comme plus 'hauts' ou 'purs'"
        ],
        institutional_or_group_contexts = [
            "Religions formelles avec un système de dogmes et de rites",
            "Sociétés secrètes ou ésotériques respectant des initiations sacrées",
            "Monastères ou centres de retraite spirituelle",
            "Mouvements écospirituels valorisant la préservation de la nature comme sanctuaire",
            "Associations philosophiques ou artistiques glorifiant la beauté et la dignité humaine",
            "Écoles ou groupes promouvant la méditation et la maîtrise de soi"
        ],
        cultural_variations_and_history = [
            "Traditions de purification (ablutions, carêmes, ramadan, etc.) dans diverses religions",
            "Concepts de chasteté, d'ascèse ou de sainteté dans l'histoire spirituelle",
            "Mouvements de réforme morale valorisant la pureté des mœurs",
            "Débats sur la laïcité et la place du sacré dans l'espace public",
            "Influence de la révolution scientifique et du matérialisme sur la notion de sanctité",
            "Évolutions contemporaines de la sensibilité au sacré (spiritualités alternatives, etc.)"
        ],
        associated_actions_and_behaviors = [
            "Observation scrupuleuse de prescriptions alimentaires ou vestimentaires",
            "Réalisation de pèlerinages ou de retraites pour se purifier l'esprit",
            "Pratique de disciplines corporelles (yoga, qi gong, etc.) visant l'harmonie spirituelle",
            "Forte valorisation de la chasteté, de la sobriété ou de la tempérance",
            "Organisation de festivals ou de célébrations autour de la sacralité d'un élément naturel",
            "Création d'œuvres d'art sacrées ou de musiques liturgiques"
        ],
        influencing_factors = [
            "Croyances religieuses ou spirituelles héritées",
            "Éducation familiale et normes culturelles liées au sacré",
            "Présence de leaders spirituels charismatiques",
            "Exposition aux textes, récits et traditions sacrées",
            "Contextes historiques marqués par une ferveur religieuse ou mystique",
            "Recherche personnelle d'une forme d'excellence morale ou spirituelle"
        ],
        observable_indicators = [
            "Participation régulière à des rites de purification ou de consécration",
            "Respect visible des codes vestimentaires, alimentaires ou comportementaux sacrés",
            "Réactions de dégoût ou d'indignation face à la banalisation de symboles sacrés",
            "Pratique de la méditation ou de la prière à des moments dédiés de la journée",
            "Investissement dans la préservation et l'entretien des lieux sacrés",
            "Utilisation fréquente d'un langage valorisant la dignité, la pureté ou la noblesse"
        ],
        factual_scenarios = [
            "Un groupe organise régulièrement des cérémonies de purification dans un temple local",
            "Une famille adhère à un régime alimentaire strict pour préserver la 'pureté' du corps",
            "Des moines pratiquent des rituels matinaux de méditation pour élever l'esprit",
            "Une communauté dénonce comme blasphématoire l'exploitation commerciale d'un symbole sacré",
            "Un artiste crée une œuvre inspirée de la transcendance et exposée dans une galerie spirituelle",
            "Un mouvement écologique milite pour la préservation d'une forêt considérée comme sacrée"
        ],
        example_factual_questions = [
            "Quels sont les rituels de purification observés dans ce contexte ?",
            "De quelle façon la communauté perçoit-elle le sacrilège ou la banalisation des symboles sacrés ?",
            "Comment les pratiques de sanctification influencent-elles le mode de vie quotidien ?",
            "Quels principes éthiques soutiennent la quête de pureté et d'élévation morale ?",
            "Comment l'histoire de la région ou du groupe a-t-elle façonné ce rapport au sacré ?",
            "Quelles adaptations sont mises en place face à des évolutions sociales ou technologiques ?"
        ],
        aspect_negatif = [
            "Contestations de l'autorité légitime : Remise en question ou rejet systématique des hiérarchies établies.",
            "Déstabilisation de l'ordre : Actes visant à perturber l'organisation et la stabilité institutionnelle.",
            "Soutien aux révolutions non constructives : Encouragement de révoltes ou de mouvements qui sapent les structures sans proposer de solutions alternatives.",
            "Dévalorisation des traditions : Dénigrement ou rejet des valeurs traditionnelles et des normes historiques.",
            "Incitation à la désobéissance : Encouragement de comportements non conformistes qui nuisent à la cohésion et à la discipline.",
            "Manipulation des règles pour miner l'ordre : Exploitation des failles du système afin de saper l'autorité sans viser une réforme constructive.",
            "Promotion de l'anarchie : Diffusion d'idées visant à abolir toute forme d'autorité organisée, conduisant à une absence de structure sociale.",
            "Infiltration subversive : Usage de stratégies clandestines pour affaiblir et déstabiliser les institutions de manière insidieuse."
        ]

    ),
    Value(
        name = "Liberty",
        definition = (
            "Fondation morale relative à l'aspiration à l'autonomie, l'indépendance et la libération des contraintes injustes. "
            "Elle se manifeste par la volonté de s'affranchir d'un contrôle excessif, de défendre l'initiative individuelle "
            "et de protéger la liberté d'agir et de penser contre toute oppression."
        ),
        descriptive_keywords = [
            "autonomie",
            "indépendance",
            "libération",
            "initiative individuelle",
            "anti-oppression",
            "droits fondamentaux",
            "choix"
        ],
        example_phrases = [
            "Revendiquer le droit de décider de ses propres actions sans contrainte arbitraire",
            "Protester contre une autorité jugée trop restrictive ou abusive",
            "Soutenir les libertés civiles comme la liberté d'expression ou de culte",
            "Refuser de se soumettre à des règles perçues comme oppressives",
            "Participer à des mouvements d'émancipation ou de droits civiques",
            "Valoriser l'entrepreneuriat individuel et la créativité personnelle"
        ],
        common_observed_patterns = [
            "Sensibilité à la domination et à la coercition qu'elle soit institutionnelle ou sociale",
            "Réactions de colère ou d'indignation face aux pratiques jugées tyranniques",
            "Promotion d'initiatives privées pour s'affranchir de systèmes centralisés",
            "Soutien aux lanceurs d'alerte ou à ceux qui dénoncent des abus de pouvoir",
            "Défense de la liberté d'information et de circulation des connaissances",
            "Mise en avant de la responsabilité individuelle liée à la liberté de chacun"
        ],
        contextual_features = [
            "Régimes démocratiques garantissant les libertés publiques",
            "Mouvements de contestation (manifestations, grèves, sit-in)",
            "ONG et associations défendant les droits de l'homme et les libertés fondamentales",
            "Plates-formes en ligne promouvant la libre expression et la transparence",
            "Initiatives d'autogestion ou d'entrepreneuriat social",
            "Espaces culturels ou académiques valorisant la liberté de création et de recherche"
        ],
        typical_emotional_reactions = [
            "Empowerment et fierté lorsqu'on parvient à s'émanciper de contraintes jugées illégitimes",
            "Colère face à l'injustice ou à la coercition arbitraire",
            "Désir de révolte ou de résistance contre l'oppression",
            "Solidarité avec ceux qui luttent pour leurs droits et libertés",
            "Crainte de perdre des acquis en cas de menaces totalitaires",
            "Soulagement lorsque l'on obtient une reconnaissance officielle de ses droits"
        ],
        institutional_or_group_contexts = [
            "Parlements et gouvernements démocratiques",
            "Organisations internationales de défense des droits (Amnesty International, etc.)",
            "Médias et presse indépendante servant de contre-pouvoir",
            "Communautés en ligne favorisant l'anonymat et l'expression libre",
            "Entreprises proposant des solutions de décentralisation ou d'émancipation économique",
            "Collectifs d'artistes ou de chercheurs revendiquant l'autonomie créative"
        ],
        cultural_variations_and_history = [
            "Grands mouvements historiques de libération (décolonisation, suffrage universel, etc.)",
            "Philosophies politiques autour du libéralisme, de l'anarchisme, du républicanisme",
            "Révolutions marquantes (1789, 1917, etc.) contre des pouvoirs centralisés",
            "Développement des droits civiques (mouvement pour l'égalité raciale, droits des femmes)",
            "Évolution des libertés numériques et de la question de la surveillance de masse",
            "Influence des réseaux sociaux dans la mobilisation pour la liberté d'expression"
        ],
        associated_actions_and_behaviors = [
            "Organisation de protestations ou de pétitions pour faire valoir ses droits",
            "Soutien financier ou moral à des causes d'émancipation",
            "Interventions publiques (tribunes, interviews) dénonçant l'autoritarisme",
            "Création de coopératives ou d'initiatives collectives pour réduire la dépendance à un pouvoir central",
            "Aide juridique ou assistance aux personnes poursuivies pour raisons politiques",
            "Promotion de technologies sécurisées (chiffrement, VPN) pour protéger la liberté d'expression"
        ],
        influencing_factors = [
            "Degré d'ouverture ou d'autoritarisme du régime politique",
            "Exposition médiatique des affaires de corruption ou d'abus de pouvoir",
            "Niveau d'éducation et de conscience politique des populations",
            "Réseaux sociaux et facilités de communication interpersonnelle",
            "Ressources disponibles pour soutenir des actions de contestation",
            "Expériences historiques de lutte pour l'indépendance ou l'autonomie"
        ],
        observable_indicators = [
            "Existence de mouvements ou de groupes de protestation actifs",
            "Multiplication de contenus (articles, vidéos) dénonçant des atteintes aux libertés",
            "Adoption de lois protégeant la liberté d'expression, d'association, de culte",
            "Taux élevé de participation citoyenne (manifestations, débats publics)",
            "Initiatives communautaires visant l'autonomie économique ou logistique",
            "Présence d'instances de régulation ou de contre-pouvoir (organismes indépendants, syndicats)"
        ],
        factual_scenarios = [
            "Des citoyens organisent une marche pacifique pour protester contre une loi jugée liberticide",
            "Une plateforme de diffusion en ligne refuse de censurer des contenus critiques envers le gouvernement",
            "Un collectif met en place un système d'échanges de services pour se passer du monopole d'une grande entreprise",
            "Un journaliste indépendant enquête et révèle des pratiques illégitimes de surveillance de la population",
            "Une communauté adopte un statut d'autogestion pour se prémunir d'ingérences politiques",
            "Un groupe international de défense des droits intervient juridiquement pour protéger des activistes"
        ],
        example_factual_questions = [
            "Quelles sont les motivations exactes des acteurs qui revendiquent davantage de libertés ?",
            "Comment s'organise la résistance ou la protestation face à l'oppression ?",
            "De quelle manière les technologies actuelles facilitent-elles l'expression et la coordination ?",
            "Quels risques encourent les individus lorsqu'ils défient une autorité jugée abusive ?",
            "Comment les contre-pouvoirs institutionnels (justice, médias) interviennent-ils pour protéger la liberté ?",
            "Quelles stratégies de négociation ou de désobéissance civile sont mises en place pour obtenir satisfaction ?"
        ],
        aspect_negatif = [
            "Imposition de contraintes arbitraires : Application de règles restrictives qui limitent la liberté individuelle sans justification équitable.",
            "Contrôle autoritaire : Surveillance et régulation excessive du comportement et des choix individuels par des autorités centralisées.",
            "Répression des voix dissidentes : Empêchement ou punition de l'expression d'opinions divergentes ou de la critique des pouvoirs en place.",
            "Inégalités structurelles : Mise en place de systèmes hiérarchiques où certains groupes sont systématiquement désavantagés et privés de droits fondamentaux.",
            "Exploitation et privation des droits : Manipulation des ressources et des opportunités pour maintenir une domination sur des individus ou des groupes.",
            "Limitation de l'autonomie personnelle : Restreindre l'indépendance et la capacité d'agir librement, imposant des restrictions sur les décisions personnelles.",
            "Utilisation de la force pour maintenir le contrôle : Recours à la violence ou à des mesures coercitives pour étouffer toute forme d'émancipation.",
            "Absence de recours légitimes : Inaccessibilité ou non-reconnaissance des mécanismes de justice et de contestation pour les opprimés."
        ]

    ),
]


def generate_value_pair() -> List[ValuePair]:
    """
    Génère toutes les paires possibles de valeurs distinctes à partir de la liste globale 'values',
    sans répétition (valueA/valueB est identique à valueB/valueA).
    """
    all_pairs = []
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            all_pairs.append(ValuePair(value1 = values[i], value2 = values[j]))
    return all_pairs
