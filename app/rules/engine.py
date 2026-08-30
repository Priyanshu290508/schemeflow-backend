# Deterministic Rule Engine for SchemeFlow
import json
from typing import Any
from app.schemas.scheme import ProfileData, RuleCriterionResult

class RuleEngine:
    """
    Deterministic rule engine that evaluates a user's normalized profile against
    structured scheme eligibility rules.
    Outputs criteria results, mandatory eligibility status, and explanatory data.
    """

    @staticmethod
    def evaluate_criterion(rule: dict[str, Any], profile: ProfileData) -> RuleCriterionResult:
        field = rule.get("field", "")
        operator = rule.get("operator", "EQ").upper()
        rule_value = rule.get("value")
        required = rule.get("required", True)
        label = rule.get("label") or field.replace("_", " ").title()
        source_ref = rule.get("source_reference", "Official Guidelines")

        # Extract user value for the specified field
        user_val = getattr(profile, field, None)
        if user_val is None and profile.extra_data:
            user_val = profile.extra_data.get(field)

        # Handle Missing Information
        if user_val is None or user_val == "":
            return RuleCriterionResult(
                field=field,
                label=label,
                status="MISSING_INFORMATION",
                user_value=None,
                required_value=rule_value,
                reason=f"Please provide your {label.lower()} to verify this condition.",
                points=0.0,
                required=required,
                source_reference=source_ref
            )

        # Parse rule value if it's stored as JSON string
        parsed_rule_val = rule_value
        if isinstance(rule_value, str):
            try:
                if (rule_value.startswith("[") and rule_value.endswith("]")) or (rule_value.startswith("{") and rule_value.endswith("}")):
                    parsed_rule_val = json.loads(rule_value)
            except Exception:
                parsed_rule_val = rule_value

        # Operator Evaluation
        is_pass = False
        reason = ""
        user_display = user_val

        try:
            if operator == "LTE":
                # User value <= Rule value
                num_user = float(user_val)
                num_rule = float(parsed_rule_val)
                is_pass = (num_user <= num_rule)
                if is_pass:
                    reason = f"Your value ({user_val}) is within the limit (max {parsed_rule_val})."
                else:
                    reason = f"Your value ({user_val}) exceeds the maximum allowed limit ({parsed_rule_val})."

            elif operator == "LT":
                num_user = float(user_val)
                num_rule = float(parsed_rule_val)
                is_pass = (num_user < num_rule)
                reason = f"Your value ({user_val}) {'satisfies' if is_pass else 'exceeds'} limit (< {parsed_rule_val})."

            elif operator == "GTE":
                num_user = float(user_val)
                num_rule = float(parsed_rule_val)
                is_pass = (num_user >= num_rule)
                if is_pass:
                    reason = f"Your value ({user_val}) meets the minimum requirement (min {parsed_rule_val})."
                else:
                    reason = f"Your value ({user_val}) is below the required minimum ({parsed_rule_val})."

            elif operator == "GT":
                num_user = float(user_val)
                num_rule = float(parsed_rule_val)
                is_pass = (num_user > num_rule)
                reason = f"Your value ({user_val}) {'satisfies' if is_pass else 'is below'} threshold (> {parsed_rule_val})."

            elif operator == "EQ":
                str_user = str(user_val).strip().lower()
                str_rule = str(parsed_rule_val).strip().lower()
                is_pass = (str_user == str_rule) or (str_rule in ["any", "all", "*"])
                reason = f"Matched requirement: {parsed_rule_val}." if is_pass else f"Requires {parsed_rule_val} (you selected {user_val})."

            elif operator == "NEQ":
                str_user = str(user_val).strip().lower()
                str_rule = str(parsed_rule_val).strip().lower()
                is_pass = (str_user != str_rule)
                reason = f"Requirement met ({user_val} is not {parsed_rule_val})." if is_pass else f"Excluded: {parsed_rule_val}."

            elif operator == "BETWEEN":
                num_user = float(user_val)
                if isinstance(parsed_rule_val, (list, tuple)) and len(parsed_rule_val) >= 2:
                    min_val, max_val = float(parsed_rule_val[0]), float(parsed_rule_val[1])
                elif isinstance(parsed_rule_val, str) and ".." in parsed_rule_val:
                    parts = parsed_rule_val.split("..")
                    min_val, max_val = float(parts[0]), float(parts[1])
                elif isinstance(parsed_rule_val, str) and "-" in parsed_rule_val:
                    parts = parsed_rule_val.split("-")
                    min_val, max_val = float(parts[0]), float(parts[1])
                else:
                    min_val, max_val = 0, float(parsed_rule_val)

                is_pass = (min_val <= num_user <= max_val)
                if is_pass:
                    reason = f"Your value ({user_val}) falls within the required range ({min_val}–{max_val})."
                else:
                    reason = f"Your value ({user_val}) is outside the required range ({min_val}–{max_val})."

            elif operator in ["IN", "ANY_OF", "CONTAINS"]:
                str_user = str(user_val).strip().lower()
                if isinstance(parsed_rule_val, list):
                    options = [str(x).strip().lower() for x in parsed_rule_val]
                else:
                    options = [str(x).strip().lower() for x in str(parsed_rule_val).split(",")]

                if "all" in options or "any" in options or "*" in options:
                    is_pass = True
                else:
                    is_pass = any(str_user == opt or opt in str_user or str_user in opt for opt in options)

                if is_pass:
                    reason = f"Your selection ({user_val}) is eligible under this program."
                else:
                    reason = f"Eligible categories: {', '.join(options[:4])}."

            elif operator == "NOT_IN":
                str_user = str(user_val).strip().lower()
                if isinstance(parsed_rule_val, list):
                    options = [str(x).strip().lower() for x in parsed_rule_val]
                else:
                    options = [str(x).strip().lower() for x in str(parsed_rule_val).split(",")]
                is_pass = not any(str_user == opt for opt in options)
                reason = f"Your category ({user_val}) is eligible." if is_pass else f"Excluded categories: {parsed_rule_val}."

            else:
                # Default match check
                is_pass = (str(user_val).strip().lower() == str(parsed_rule_val).strip().lower())
                reason = f"Evaluated against condition {parsed_rule_val}."

        except (ValueError, TypeError) as e:
            return RuleCriterionResult(
                field=field,
                label=label,
                status="NEEDS_VERIFICATION",
                user_value=user_display,
                required_value=rule_value,
                reason=f"Criterion requires document verification: {rule.get('description', '')}",
                points=0.0,
                required=required,
                source_reference=source_ref
            )

        status = "PASS" if is_pass else "FAIL"

        return RuleCriterionResult(
            field=field,
            label=label,
            status=status,
            user_value=user_display,
            required_value=rule_value,
            reason=reason,
            points=1.0 if is_pass else 0.0,
            required=required,
            source_reference=source_ref
        )

    @classmethod
    def evaluate_scheme(cls, scheme_dict: dict[str, Any], profile: ProfileData) -> tuple[bool, list[RuleCriterionResult]]:
        """
        Evaluates all rules of a scheme for a given profile.
        Returns:
            (mandatory_eligible: bool, criteria_results: list[RuleCriterionResult])
        """
        rules = scheme_dict.get("eligibility_rules", [])
        criteria_results: list[RuleCriterionResult] = []
        mandatory_eligible = True

        for rule in rules:
            res = cls.evaluate_criterion(rule, profile)
            criteria_results.append(res)
            # If a REQUIRED rule fails, mark scheme not mandatory_eligible
            if res.required and res.status == "FAIL":
                mandatory_eligible = False

        return mandatory_eligible, criteria_results
