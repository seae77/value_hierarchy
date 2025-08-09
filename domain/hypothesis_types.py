# domain/hypothesis_types.py

from enum import Enum


class HypothesisType(Enum):
    H1 = "H1"  # Consistency in Value Hierarchies
    H2 = "H2"  # Emotional Consistency (Anger arises from value violations)
    H3 = "H3"  # Emotional Strength (Higher values elicit stronger responses)
    H4 = "H4"  # Vicarious Emotional Responses to Value Hierarchies
    H5 = "H5"  # Strength of Normative Language Reflecting Value Importance
    H6 = "H6"  # Perceived Justification of Emotional Reactions
