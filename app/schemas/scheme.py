from typing import Optional, Any
from pydantic import BaseModel, Field

class RuleCriterionResult(BaseModel):
    field: str
    label: str
    status: str  # PASS, FAIL, NEEDS_VERIFICATION, MISSING_INFORMATION, NOT_APPLICABLE
    user_value: Any = None
    required_value: Any = None
    reason: str
    points: float = 0.0
    required: bool = True
    source_reference: Optional[str] = None

class SuccessStory(BaseModel):
    name: str
    location: str
    enterprise: str
    before_metric: str
    after_metric: str
    subsidy_or_loan_received: str
    story_quote: str

class SchemeRecommendation(BaseModel):
    scheme_id: str
    scheme_name: str
    slug: str
    department: str
    ministry: Optional[str] = None
    category: str
    summary: str
    match_score: int  # 0 to 100
    match_label: str  # Excellent Match, Good Match, Possible Match, Low Match
    mandatory_eligible: bool
    criteria_results: list[RuleCriterionResult] = []
    matched_criteria_count: int = 0
    total_criteria_count: int = 0
    why_this_scheme: list[str] = []
    missing_conditions: list[str] = []
    needs_verification: list[str] = []
    near_miss_tips: list[str] = []  # Proactive actionable guidance for near matches
    deadline: str = "Active (FY 2026-27 Ongoing)"
    processing_timeline: str = "15–30 Days"
    success_story: Optional[SuccessStory] = None
    max_benefit: Optional[str] = None
    benefit_type: Optional[str] = None
    benefits: list[dict[str, Any]] = []
    documents: list[dict[str, Any]] = []
    application_url: Optional[str] = None
    source_url: Optional[str] = None
    last_verified_at: str = "2026-08-15"
    status: str = "VERIFIED"

class ProfileData(BaseModel):
    age: Optional[int] = Field(None, ge=0, le=120)
    gender: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    annual_income: Optional[float] = Field(None, ge=0)
    employment_status: Optional[str] = None
    business_type: Optional[str] = None
    business_status: Optional[str] = None  # New / Proposed, Existing
    business_size: Optional[str] = None
    investment_required: Optional[float] = Field(None, ge=0)
    loan_required: Optional[float] = Field(None, ge=0)
    category: Optional[str] = None  # General, OBC, SC, ST, Minority, Women
    is_differently_abled: Optional[bool] = False
    extra_data: Optional[dict[str, Any]] = None

class SearchQuery(BaseModel):
    query: str
    category: Optional[str] = None
    state: Optional[str] = None
    limit: int = 10

class AssistantMessageInput(BaseModel):
    message: str
    session_id: Optional[str] = "default_session"
    current_profile: Optional[ProfileData] = None

class AssistantMessageResponse(BaseModel):
    reply: str
    extracted_profile: Optional[ProfileData] = None
    extracted_facts: list[dict[str, Any]] = []
    needs_confirmation: bool = False
    recommended_schemes: list[SchemeRecommendation] = []
    suggested_followups: list[str] = []

class TrackingStep(BaseModel):
    title: str
    status: str  # COMPLETED, IN_PROGRESS, PENDING, REJECTED
    date: str
    officer_remark: str

class ApplicationStatusResponse(BaseModel):
    tracking_id: str
    scheme_name: str
    applicant_name: str
    applied_date: str
    current_stage: str
    overall_status: str  # UNDER_REVIEW, APPROVED, DISBURSED, ACTION_REQUIRED
    progress_percentage: int
    steps: list[TrackingStep] = []
    next_action_due: str
