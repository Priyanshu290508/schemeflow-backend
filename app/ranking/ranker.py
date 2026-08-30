# Recommendation and Ranking Engine with Near-Miss Feedback
from typing import Any
from app.core.config import settings
from app.schemas.scheme import ProfileData, SchemeRecommendation, RuleCriterionResult, SuccessStory
from app.rules.engine import RuleEngine

class RecommendationEngine:
    """
    Ranks schemes based on weighted rule evaluation, mandatory disqualifier gating,
    and generates clear explainable insights and proactive Near-Miss guidance.
    """

    DIMENSION_WEIGHTS = {
        "age": settings.WEIGHT_AGE,              # 20
        "annual_income": settings.WEIGHT_INCOME,  # 25
        "business_type": settings.WEIGHT_BUSINESS_TYPE, # 25
        "state": settings.WEIGHT_LOCATION,        # 15
        "loan_required": settings.WEIGHT_FINANCIAL_NEED, # 15
        "investment_required": 10.0,
        "gender": 10.0,
        "category": 10.0,
        "employment_status": 10.0,
        "business_status": 15.0
    }

    @classmethod
    def generate_near_miss_tips(cls, scheme: dict[str, Any], profile: ProfileData, criteria_results: list[RuleCriterionResult]) -> list[str]:
        """
        Generates actionable, proactive advice if a scheme almost matches or can be optimized.
        """
        tips: list[str] = []
        scheme_id = scheme.get("id", "")
        scheme_name = scheme.get("name", "")

        for res in criteria_results:
            # 1. Income Near-Miss
            if res.field == "annual_income" and res.status == "FAIL":
                try:
                    user_inc = float(profile.annual_income or 0)
                    rule_inc = float(res.required_value or 0)
                    if user_inc > rule_inc and (user_inc - rule_inc) <= (rule_inc * 0.35):
                        delta = user_inc - rule_inc
                        tips.append(f"💡 Near-Miss Guidance: If your reported annual income were ₹{int(delta):,} lower (below ₹{int(rule_inc):,}), you would qualify for full subsidy under this scheme.")
                except Exception:
                    pass

            # 2. Age Near-Miss
            if res.field == "age" and res.status == "FAIL":
                try:
                    user_age = int(profile.age or 0)
                    req_age = int(res.required_value or 18)
                    if user_age == 17:
                        tips.append("💡 Age Proximity: You will reach the mandatory 18-year threshold within the next few months to unlock this scheme.")
                    elif user_age > req_age and (user_age - req_age) <= 3:
                        tips.append(f"💡 Special Exemption: Candidates from SC/ST/Women/Ex-Servicemen categories often receive a 3–5 year relaxation on the {req_age}-year age limit.")
                except Exception:
                    pass

            # 3. Loan Ceiling Near-Miss
            if res.field == "loan_required" and res.status == "FAIL":
                try:
                    loan_val = float(profile.loan_required or 0)
                    if isinstance(res.required_value, list) and len(res.required_value) == 2:
                        min_l, max_l = float(res.required_value[0]), float(res.required_value[1])
                        if loan_val > max_l and (loan_val - max_l) <= 200000:
                            tips.append(f"💡 Scope Adjustment: Your requested loan (₹{int(loan_val):,}) is slightly above the Kishore limit of ₹{int(max_l):,}. Consider applying under the MUDRA Tarun category (₹5L–₹10L) instead.")
                except Exception:
                    pass

        # 4. Proactive Scheme-Specific Optimizations
        if "pmegp" in scheme_id.lower():
            if profile.category == "General":
                tips.append("💡 Subsidy Booster: In rural areas, General category gets 25% subsidy. Partnering with a Woman or SC/ST/OBC co-applicant raises your margin money subsidy to 35%.")
            else:
                tips.append("💡 Rural Location Advantage: Setting up your project in a rural block awards you the maximum 35% non-repayable margin money subsidy.")

        elif "stand_up" in scheme_id.lower():
            if profile.gender not in ["Female", "Women"]:
                tips.append("💡 Co-Founder Tip: Stand-Up India requires at least 51% shareholding by a Woman or SC/ST entrepreneur. Co-founding with a female partner qualifies your enterprise.")

        elif "cgtmse" in scheme_id.lower():
            tips.append("💡 Women Enterprise Perk: Women-owned micro-enterprises receive an elevated 85% credit guarantee cover (vs 75% for general) and 10% lower annual guarantee fees.")

        elif "vishwakarma" in scheme_id.lower():
            tips.append("💡 Family Allocation Tip: Only one member per family can avail the ₹15,000 toolkit voucher and ₹3 Lakh 5% loan benefit.")

        return tips

    @classmethod
    def rank_schemes(cls, schemes: list[dict[str, Any]], profile: ProfileData) -> list[SchemeRecommendation]:
        recommendations: list[SchemeRecommendation] = []

        for scheme in schemes:
            mandatory_eligible, criteria_results = RuleEngine.evaluate_scheme(scheme, profile)

            # Calculate weighted score
            total_possible_weight = 0.0
            earned_weight = 0.0

            matched_count = 0
            why_this_scheme: list[str] = []
            missing_conditions: list[str] = []
            needs_verification: list[str] = []

            # Track which core dimensions are tested
            evaluated_fields = set()

            for res in criteria_results:
                weight = cls.DIMENSION_WEIGHTS.get(res.field, 10.0)
                total_possible_weight += weight
                evaluated_fields.add(res.field)

                if res.status == "PASS":
                    earned_weight += weight
                    matched_count += 1
                    why_this_scheme.append(f"✓ {res.label}: {res.reason}")
                elif res.status == "FAIL":
                    if res.required:
                        missing_conditions.append(f"✗ Disqualifier on {res.label}: {res.reason}")
                    else:
                        missing_conditions.append(f"⚠ {res.label}: {res.reason}")
                elif res.status == "MISSING_INFORMATION":
                    missing_conditions.append(f"○ Missing {res.label}: Provide this to refine match.")
                elif res.status == "NEEDS_VERIFICATION":
                    needs_verification.append(f"ℹ {res.label}: Needs official document check.")

            # Check coverage for location if not in explicit rule list
            if "state" not in evaluated_fields and profile.state:
                coverage = scheme.get("coverage", ["ALL"])
                if isinstance(coverage, str):
                    coverage = [coverage]
                state_match = "ALL" in coverage or profile.state in coverage
                total_possible_weight += cls.DIMENSION_WEIGHTS["state"]
                if state_match:
                    earned_weight += cls.DIMENSION_WEIGHTS["state"]
                    why_this_scheme.append(f"✓ Location: Scheme is active across your state ({profile.state}).")
                else:
                    missing_conditions.append(f"✗ Location: Scheme not active in {profile.state}.")

            # Compute final normalized score (0 - 100)
            if total_possible_weight > 0:
                raw_score = (earned_weight / total_possible_weight) * 100
            else:
                raw_score = 50.0

            # Mandatory Disqualifier Law:
            if not mandatory_eligible:
                final_score = min(int(raw_score * 0.4), 45)
            else:
                final_score = min(int(round(raw_score)), 100)

            # Determine Label
            if not mandatory_eligible:
                match_label = "Ineligible (Mandatory Rule Failed)"
            elif final_score >= 85:
                match_label = "Excellent Match"
            elif final_score >= 70:
                match_label = "Good Match"
            elif final_score >= 50:
                match_label = "Possible Match"
            else:
                match_label = "Low Match"

            # Generate Near-Miss Feedback
            near_miss_tips = cls.generate_near_miss_tips(scheme, profile, criteria_results)

            # Success Story extraction if present
            success_story_obj = None
            if scheme.get("success_story"):
                s_story = scheme["success_story"]
                success_story_obj = SuccessStory(
                    name=s_story.get("name", ""),
                    location=s_story.get("location", ""),
                    enterprise=s_story.get("enterprise", ""),
                    before_metric=s_story.get("before_metric", ""),
                    after_metric=s_story.get("after_metric", ""),
                    subsidy_or_loan_received=s_story.get("subsidy_or_loan_received", ""),
                    story_quote=s_story.get("story_quote", "")
                )

            rec = SchemeRecommendation(
                scheme_id=scheme["id"],
                scheme_name=scheme["name"],
                slug=scheme.get("slug", scheme["id"]),
                department=scheme.get("department", ""),
                ministry=scheme.get("ministry"),
                category=scheme.get("category", "General"),
                summary=scheme.get("summary", ""),
                match_score=final_score,
                match_label=match_label,
                mandatory_eligible=mandatory_eligible,
                criteria_results=criteria_results,
                matched_criteria_count=matched_count,
                total_criteria_count=len(criteria_results),
                why_this_scheme=why_this_scheme,
                missing_conditions=missing_conditions,
                needs_verification=needs_verification,
                near_miss_tips=near_miss_tips,
                deadline=scheme.get("deadline", "March 31, 2027 (FY 2026-27 Active)"),
                processing_timeline=scheme.get("processing_timeline", "15–30 Days"),
                success_story=success_story_obj,
                max_benefit=scheme.get("max_benefit"),
                benefit_type=scheme.get("benefit_type"),
                benefits=scheme.get("benefits", []),
                documents=scheme.get("documents", []),
                application_url=scheme.get("application_url"),
                source_url=scheme.get("source_url"),
                last_verified_at=scheme.get("last_verified_at", "2026-08-15"),
                status=scheme.get("status", "VERIFIED")
            )
            recommendations.append(rec)

        # Sort: Mandatory eligible first, then by match_score descending
        recommendations.sort(key=lambda r: (r.mandatory_eligible, r.match_score), reverse=True)
        return recommendations
