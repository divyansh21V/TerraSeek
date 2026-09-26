"""Deterministic ranking for TerraSeek candidates.

Ranking uses transparent, weighted signals — no ML confidence scores.
Every factor is inspectable by the analyst.
"""

from __future__ import annotations

# Weights for each ranking factor.
# These are explicit and documented — not learned.
RANKING_WEIGHTS: dict[str, float] = {
    "query_relevance": 0.20,
    "visual_change_strength": 0.25,
    "temporal_persistence": 0.20,
    "data_suitability": 0.10,
    "contextual_relevance": 0.10,
    "confounder_risk": 0.15,  # Inverted: low risk → high score
}

# Stop words removed before keyword matching.
STOP_WORDS: set[str] = {
    "a", "an", "the", "in", "on", "at", "to", "for", "of", "and", "or",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "shall", "should", "may", "might",
    "can", "could", "with", "from", "by", "this", "that", "these", "those",
    "it", "its", "my", "me", "i", "we", "our", "you", "your", "they",
    "them", "their", "what", "which", "who", "whom", "where", "when", "how",
    "find", "show", "search", "look", "get", "near", "between", "over",
    "last", "recent", "new", "any", "all", "some",
}


def compute_query_relevance(query: str, candidate_keywords: list[str]) -> float:
    """Score how well the query matches the candidate's keyword tags.

    Simple deterministic keyword overlap — not semantic search.
    Returns 0.0–1.0.
    """
    query_tokens = {
        w.lower().strip(".,!?\"'()[]")
        for w in query.split()
        if w.lower().strip(".,!?\"'()[]") not in STOP_WORDS
        and len(w.strip(".,!?\"'()[]")) > 2
    }
    if not query_tokens:
        return 0.5  # Neutral if no usable tokens

    candidate_kw = {k.lower() for k in candidate_keywords}
    matches = query_tokens & candidate_kw

    # Partial-match bonus: if a query token is a substring of a keyword
    partial = 0
    for qt in query_tokens - matches:
        for ck in candidate_kw:
            if qt in ck or ck in qt:
                partial += 0.5
                break

    score = (len(matches) + partial) / len(query_tokens)
    return min(score, 1.0)


def compute_ranking_score(signals: dict[str, float]) -> float:
    """Compute overall ranking score from priority signals.

    Returns 0.0–1.0, where higher is higher investigation priority.
    confounder_risk is inverted: low risk → high contribution.
    """
    total = 0.0
    for key, weight in RANKING_WEIGHTS.items():
        value = signals.get(key, 0.5)
        if key == "confounder_risk":
            value = 1.0 - value  # Invert: low risk is good
        total += weight * value
    return round(total, 3)


def priority_label(score: float) -> str:
    """Map a ranking score to a human-readable priority label."""
    if score >= 0.75:
        return "HIGH"
    elif score >= 0.50:
        return "MODERATE"
    elif score >= 0.30:
        return "LOW"
    else:
        return "MINIMAL"
