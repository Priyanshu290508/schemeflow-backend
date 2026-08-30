# Semantic and Natural Language Search Engine
import re
import math
from typing import Any
from collections import Counter
from app.schemas.scheme import ProfileData, SchemeRecommendation
from app.ranking.ranker import RecommendationEngine

QUERY_EXPANSIONS = {
    "dairy": ["milk", "cattle", "livestock", "animal husbandry", "cow", "buffalo", "poultry", "farm"],
    "farm": ["farmer", "agriculture", "crop", "horticulture", "kisan", "cultivation", "seeds"],
    "poultry": ["chicken", "livestock", "egg", "broiler", "meat", "animal husbandry"],
    "bakery": ["food processing", "food", "manufacturing", "flour", "confectionery", "fssai"],
    "street vendor": ["svanidhi", "vendor", "hawker", "micro loan", "working capital", "small business"],
    "vendor": ["hawker", "svanidhi", "cart", "daily", "micro credit"],
    "women": ["mahila", "woman", "female", "shg", "stand-up india", "self help group"],
    "woman": ["women", "mahila", "female", "shg", "stand-up india"],
    "startup": ["seed fund", "innovation", "technology", "dpiit", "incubator", "early stage", "tech"],
    "loan": ["credit", "subsidy", "finance", "capital", "fund", "mudra", "cgtmse", "bank"],
    "subsidy": ["grant", "financial assistance", "concession", "margin money", "pmegp"],
    "artisan": ["vishwakarma", "handicraft", "carpenter", "weaver", "blacksmith", "craftsman", "tools", "traditional"],
    "fish": ["fisheries", "matsya", "aquaculture", "boat", "marine", "pond"],
    "fisheries": ["matsya", "fish", "pond", "aquaculture", "hatchery"],
    "solar": ["renewable", "energy", "rooftop", "power", "grid", "panel"],
}

class SearchEngine:
    """
    Intelligent semantic and keyword search engine with domain query expansion
    and profile-aware ranking.
    """

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return re.findall(r'\b[a-zA-Z0-9_-]+\b', text.lower())

    @classmethod
    def _expand_query(cls, query: str) -> list[str]:
        tokens = cls._tokenize(query)
        expanded = set(tokens)
        for token in tokens:
            if token in QUERY_EXPANSIONS:
                expanded.update(QUERY_EXPANSIONS[token])
            for k, syns in QUERY_EXPANSIONS.items():
                if k in query.lower():
                    expanded.update(syns)
        return list(expanded)

    @classmethod
    def search(
        cls,
        schemes: list[dict[str, Any]],
        query: str,
        category: str = None,
        state: str = None,
        profile: ProfileData = None
    ) -> list[dict[str, Any]]:
        query_terms = cls._expand_query(query) if query else []
        results = []

        for s in schemes:
            # Category filter
            if category and category.lower() not in ["all", "any", ""]:
                if s.get("category", "").lower() != category.lower():
                    continue

            # State coverage filter
            if state and state.lower() not in ["all", "any", ""]:
                coverage = s.get("coverage", ["ALL"])
                if isinstance(coverage, str):
                    coverage = [coverage]
                if "ALL" not in coverage and state not in coverage:
                    continue

            # Compute text relevance score
            doc_text = " ".join([
                s.get("name", ""),
                s.get("description", ""),
                s.get("summary", ""),
                s.get("department", ""),
                s.get("ministry", "") or "",
                s.get("category", ""),
                " ".join(s.get("tags", [])) if isinstance(s.get("tags"), list) else "",
                " ".join([b.get("title", "") + " " + b.get("description", "") for b in s.get("benefits", [])])
            ]).lower()

            relevance_score = 0.0
            if query_terms:
                doc_tokens = cls._tokenize(doc_text)
                doc_counts = Counter(doc_tokens)
                for term in query_terms:
                    count = doc_counts.get(term, 0)
                    if count > 0:
                        # Term frequency weighting with higher weight for exact name matches
                        weight = 5.0 if term in s.get("name", "").lower() else 1.5
                        relevance_score += (1.0 + math.log(count)) * weight
            else:
                relevance_score = 1.0

            results.append({
                "scheme": s,
                "relevance_score": relevance_score
            })

        # Sort by relevance
        results.sort(key=lambda x: x["relevance_score"], reverse=True)
        return [r["scheme"] for r in results]
