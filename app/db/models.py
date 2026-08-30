import json
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.database import Base

class Scheme(Base):
    __tablename__ = "schemes"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    slug = Column(String, unique=True, index=True)
    department = Column(String, nullable=False)
    ministry = Column(String, nullable=True)
    category = Column(String, index=True)  # Business, Agriculture, Credit, Women, Education, etc.
    description = Column(Text, nullable=False)
    summary = Column(String, nullable=False)
    coverage = Column(Text, default="ALL")  # JSON or comma-separated states/districts
    max_benefit = Column(String, nullable=True)  # e.g., "₹50,00,000 subsidy / loan"
    benefit_type = Column(String, nullable=True)  # Subsidy, Loan, Credit Guarantee, Training, Grant
    application_url = Column(String, nullable=True)
    source_url = Column(String, nullable=True)
    last_verified_at = Column(String, default="2026-08-15")
    status = Column(String, default="VERIFIED")  # VERIFIED, NEEDS_REVIEW, OUTDATED, INACTIVE
    tags = Column(Text, default="[]")  # JSON array
    application_steps = Column(Text, default="[]")  # JSON array of step descriptions
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    eligibility_rules = relationship("EligibilityRule", back_populates="scheme", cascade="all, delete-orphan")
    benefits = relationship("Benefit", back_populates="scheme", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="scheme", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "slug": self.slug or self.id,
            "department": self.department,
            "ministry": self.ministry,
            "category": self.category,
            "description": self.description,
            "summary": self.summary,
            "coverage": json.loads(self.coverage) if self.coverage.startswith("[") else [self.coverage],
            "max_benefit": self.max_benefit,
            "benefit_type": self.benefit_type,
            "application_url": self.application_url,
            "source_url": self.source_url,
            "last_verified_at": self.last_verified_at,
            "status": self.status,
            "tags": json.loads(self.tags) if self.tags.startswith("[") else [],
            "application_steps": json.loads(self.application_steps) if self.application_steps.startswith("[") else [],
            "eligibility_rules": [r.to_dict() for r in self.eligibility_rules],
            "benefits": [b.to_dict() for b in self.benefits],
            "documents": [d.to_dict() for d in self.documents]
        }

class EligibilityRule(Base):
    __tablename__ = "eligibility_rules"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scheme_id = Column(String, ForeignKey("schemes.id"), nullable=False, index=True)
    field = Column(String, nullable=False)  # age, annual_income, state, business_type, business_status, loan_required, gender, category
    operator = Column(String, nullable=False)  # LTE, GTE, BETWEEN, EQ, IN, CONTAINS, ANY_OF, NOT_IN
    value = Column(Text, nullable=False)  # JSON or scalar representation
    unit = Column(String, nullable=True)  # INR, years, acres, etc.
    required = Column(Boolean, default=True)  # mandatory condition (hard filter)
    label = Column(String, nullable=True)  # Human-readable rule title e.g. "Age Limit"
    description = Column(String, nullable=True)  # e.g., "Must be between 18 and 45 years old"
    source_reference = Column(String, nullable=True)

    scheme = relationship("Scheme", back_populates="eligibility_rules")

    def to_dict(self):
        val = self.value
        try:
            val = json.loads(self.value)
        except Exception:
            pass
        return {
            "id": self.id,
            "scheme_id": self.scheme_id,
            "field": self.field,
            "operator": self.operator,
            "value": val,
            "unit": self.unit,
            "required": self.required,
            "label": self.label or self.field.replace("_", " ").title(),
            "description": self.description,
            "source_reference": self.source_reference
        }

class Benefit(Base):
    __tablename__ = "benefits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scheme_id = Column(String, ForeignKey("schemes.id"), nullable=False, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    amount_or_percentage = Column(String, nullable=True)
    benefit_type = Column(String, nullable=True)

    scheme = relationship("Scheme", back_populates="benefits")

    def to_dict(self):
        return {
            "id": self.id,
            "scheme_id": self.scheme_id,
            "title": self.title,
            "description": self.description,
            "amount_or_percentage": self.amount_or_percentage,
            "benefit_type": self.benefit_type
        }

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scheme_id = Column(String, ForeignKey("schemes.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    is_mandatory = Column(Boolean, default=True)
    description = Column(String, nullable=True)
    alternatives = Column(Text, default="[]")

    scheme = relationship("Scheme", back_populates="documents")

    def to_dict(self):
        alts = []
        try:
            alts = json.loads(self.alternatives)
        except Exception:
            pass
        return {
            "id": self.id,
            "scheme_id": self.scheme_id,
            "name": self.name,
            "is_mandatory": self.is_mandatory,
            "description": self.description,
            "alternatives": alts
        }

class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(String, primary_key=True, default="default_user")
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)  # Male, Female, Other, Any
    state = Column(String, nullable=True)
    district = Column(String, nullable=True)
    annual_income = Column(Float, nullable=True)
    employment_status = Column(String, nullable=True)  # Unemployed, Self-employed, Salaried, Student, Farmer, Business Owner
    business_type = Column(String, nullable=True)  # Manufacturing, Service, Trading, Agriculture, Dairy, Food Processing, Tech, Artisan, Other
    business_status = Column(String, nullable=True)  # New / Proposed, Existing
    business_size = Column(String, nullable=True)  # Micro, Small, Medium, Individual
    investment_required = Column(Float, nullable=True)
    loan_required = Column(Float, nullable=True)
    category = Column(String, nullable=True)  # General, OBC, SC, ST, Minority, Women, Ex-Servicemen
    is_differently_abled = Column(Boolean, default=False)
    extra_data = Column(Text, default="{}")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SavedScheme(Base):
    __tablename__ = "saved_schemes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, default="default_user", index=True)
    scheme_id = Column(String, ForeignKey("schemes.id"), nullable=False)
    saved_at = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text, nullable=True)
