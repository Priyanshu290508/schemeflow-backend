# Conversational Assistant Service with Profile Extraction & Grounded RAG
import re
from typing import Any
from app.schemas.scheme import ProfileData, AssistantMessageResponse, SchemeRecommendation
from app.retrieval.search import SearchEngine
from app.ranking.ranker import RecommendationEngine

INDIAN_STATES = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa",
    "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala",
    "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland",
    "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura",
    "Uttar Pradesh", "Uttarakhand", "West Bengal", "Delhi", "Jammu and Kashmir", "Ladakh"
]

BUSINESS_KEYWORDS = {
    "dairy": "Dairy & Animal Husbandry",
    "milk": "Dairy & Animal Husbandry",
    "cattle": "Dairy & Animal Husbandry",
    "cow": "Dairy & Animal Husbandry",
    "poultry": "Poultry & Livestock",
    "chicken": "Poultry & Livestock",
    "bakery": "Food Processing & Bakery",
    "food": "Food Processing",
    "restaurant": "Service & Hospitality",
    "cafe": "Service & Hospitality",
    "catering": "Food Processing & Service",
    "grocery": "Retail & Trading",
    "shop": "Retail & Trading",
    "store": "Retail & Trading",
    "artisan": "Handicrafts & Traditional Artisan",
    "carpenter": "Traditional Crafts (Vishwakarma)",
    "potter": "Traditional Crafts (Vishwakarma)",
    "blacksmith": "Traditional Crafts (Vishwakarma)",
    "tailor": "Garment & Textile",
    "textile": "Garment & Textile",
    "tech": "Technology & Innovation",
    "software": "Technology & Innovation",
    "startup": "Innovation & Startup",
    "agriculture": "Agriculture & Farming",
    "farming": "Agriculture & Farming",
    "fisheries": "Fisheries & Aquaculture",
    "fish": "Fisheries & Aquaculture",
    "manufacturing": "Manufacturing",
    "solar": "Renewable Energy & Solar"
}

class AssistantService:
    """
    Extracts profile attributes from conversation, confirms extracted facts,
    retrieves grounded scheme records, and formats explainable answers.
    """

    @classmethod
    def extract_profile_facts(cls, message: str, current_profile: ProfileData = None) -> tuple[ProfileData, list[dict[str, Any]]]:
        profile = current_profile.model_copy() if current_profile else ProfileData()
        extracted_facts = []
        lower_msg = message.lower()

        # 1. Extract Age
        age_match = re.search(r'\b(?:i am|age is|age|i\'m)\s*(\d{2})\b|\b(\d{2})\s*(?:years? old|yrs? old|y\/o)\b', lower_msg)
        if age_match:
            age_val = int(age_match.group(1) or age_match.group(2))
            if 15 <= age_val <= 100:
                profile.age = age_val
                extracted_facts.append({"field": "age", "label": "Age", "value": f"{age_val} years"})

        # 2. Extract State
        for state in INDIAN_STATES:
            if state.lower() in lower_msg:
                profile.state = state
                extracted_facts.append({"field": "state", "label": "State", "value": state})
                break

        # 3. Extract Gender / Demographic
        if "female" in lower_msg or "woman" in lower_msg or "women" in lower_msg or "mahila" in lower_msg:
            profile.gender = "Female"
            extracted_facts.append({"field": "gender", "label": "Gender", "value": "Female"})
        elif "male" in lower_msg or "man" in lower_msg or "boy" in lower_msg:
            profile.gender = "Male"
            extracted_facts.append({"field": "gender", "label": "Gender", "value": "Male"})

        # 4. Extract Category
        if "sc/st" in lower_msg or "sc " in lower_msg or " st " in lower_msg or "scheduled" in lower_msg:
            profile.category = "SC/ST"
            extracted_facts.append({"field": "category", "label": "Category", "value": "SC/ST"})
        elif "obc" in lower_msg:
            profile.category = "OBC"
            extracted_facts.append({"field": "category", "label": "Category", "value": "OBC"})
        elif "minority" in lower_msg:
            profile.category = "Minority"
            extracted_facts.append({"field": "category", "label": "Category", "value": "Minority"})

        # 5. Extract Business Type
        for kw, btype in BUSINESS_KEYWORDS.items():
            if kw in lower_msg:
                profile.business_type = btype
                extracted_facts.append({"field": "business_type", "label": "Business/Sector", "value": btype})
                break

        # 6. Extract Business Status (New vs Existing)
        if any(w in lower_msg for w in ["start a new", "new business", "starting", "proposed", "launch", "fresh"]):
            profile.business_status = "New / Proposed"
            extracted_facts.append({"field": "business_status", "label": "Business Stage", "value": "New / Proposed"})
        elif any(w in lower_msg for w in ["expand", "existing business", "current shop", "already running"]):
            profile.business_status = "Existing"
            extracted_facts.append({"field": "business_status", "label": "Business Stage", "value": "Existing"})

        # 7. Extract Loan / Financial Need Amount
        amt_match = re.search(r'(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*(lakh|lac|cr|crore|k|thousand)?\s*(?:loan|investment|support|capital|funds|needed|required)', lower_msg)
        if not amt_match:
            amt_match = re.search(r'(?:loan|investment|capital|budget|need of)\s*(?:of|is)?\s*(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*(lakh|lac|cr|crore|k|thousand)?', lower_msg)

        if amt_match:
            val = float(amt_match.group(1))
            unit = (amt_match.group(2) or "").lower()
            if unit in ["lakh", "lac"]:
                amt_inr = val * 100000
            elif unit in ["cr", "crore"]:
                amt_inr = val * 10000000
            elif unit in ["k", "thousand"]:
                amt_inr = val * 1000
            else:
                amt_inr = val if val > 1000 else val * 100000

            profile.loan_required = amt_inr
            extracted_facts.append({"field": "loan_required", "label": "Financial Requirement", "value": f"₹{amt_inr:,.0f}"})

        return profile, extracted_facts

    @classmethod
    def process_message(
        cls,
        message: str,
        current_profile: ProfileData,
        all_schemes: list[dict[str, Any]]
    ) -> AssistantMessageResponse:
        profile, facts = cls.extract_profile_facts(message, current_profile)

        # 1. Search candidate schemes based on query message & profile
        candidate_schemes = SearchEngine.search(
            schemes=all_schemes,
            query=message,
            category=None,
            state=profile.state,
            profile=profile
        )

        # 2. Evaluate with Rule Engine and Rank
        recommendations = RecommendationEngine.rank_schemes(candidate_schemes, profile)
        top_recs = [r for r in recommendations if r.mandatory_eligible][:3]

        # 3. Generate grounded response
        if facts:
            fact_summary = ", ".join([f"{f['label']}: **{f['value']}**" for f in facts])
            reply_header = f"I understood the following about your profile: {fact_summary}.\n\n"
        else:
            reply_header = ""

        if top_recs:
            top_names = [f"**{r.scheme_name}** ({r.match_score}/100 Match)" for r in top_recs]
            reply_body = (
                f"Based on verified government guidelines, here are the most relevant schemes for you:\n\n"
                + "\n".join([f"- **{r.scheme_name}**: {r.summary} — *Max benefit: {r.max_benefit or 'Financial subsidy & credit'}*" for r in top_recs])
                + "\n\nYou can click on any scheme card below to inspect the complete eligibility breakdown, required documents checklist, and official application steps."
            )
            suggested = [
                f"What documents do I need for {top_recs[0].scheme_name}?",
                f"How do I apply for {top_recs[0].scheme_name}?",
                "How can I improve my match score?"
            ]
        else:
            reply_body = (
                "I couldn't find a direct scheme match for this exact query with the current profile data. "
                "Could you tell me your approximate age, state, and specific business type or financial requirement?"
            )
            suggested = [
                "I want a loan of ₹2 Lakh to start a dairy unit in West Bengal",
                "I am a woman entrepreneur looking for an artisan grant",
                "Explore all youth entrepreneurship schemes"
            ]

        return AssistantMessageResponse(
            reply=reply_header + reply_body,
            extracted_profile=profile,
            extracted_facts=facts,
            needs_confirmation=bool(facts),
            recommended_schemes=top_recs,
            suggested_followups=suggested
        )
