# Application Status Tracker Router (Feature 2)
from fastapi import APIRouter
from app.schemas.scheme import ApplicationStatusResponse, TrackingStep

router = APIRouter(prefix="/tracker", tags=["Application Tracker"])

SIMULATED_TRACKING_DATABASE = {
    "PMEGP-2026-WB-8921": ApplicationStatusResponse(
        tracking_id="PMEGP-2026-WB-8921",
        scheme_name="Prime Minister's Employment Generation Programme (PMEGP)",
        applicant_name="Priyanka Mondal",
        applied_date="12 Aug 2026",
        current_stage="Financing Bank Credit Appraisal",
        overall_status="UNDER_REVIEW",
        progress_percentage=65,
        next_action_due="Attend 5-day EDP Training Module at RSETI Hub",
        steps=[
            TrackingStep(
                title="Application & DPR Submitted on e-Portal",
                status="COMPLETED",
                date="12 Aug 2026, 11:30 AM",
                officer_remark="Online application received with project cost ₹12.5 Lakh and Aadhaar e-KYC."
            ),
            TrackingStep(
                title="District Level Task Force (DLTFC) Scrutiny",
                status="COMPLETED",
                date="18 Aug 2026, 03:45 PM",
                officer_remark="Project DPR vetted and cleared with 35% rural special category subsidy eligibility."
            ),
            TrackingStep(
                title="Financing Bank Appraisal & Field Inspection",
                status="IN_PROGRESS",
                date="24 Aug 2026, 02:15 PM",
                officer_remark="Branch manager physical verification of dairy shed site completed. Credit sanction letter under preparation."
            ),
            TrackingStep(
                title="Entrepreneurship Development Programme (EDP)",
                status="PENDING",
                date="Estimated: 05 Sep 2026",
                officer_remark="Mandatory 5-day training schedule assigned at District RSETI centre."
            ),
            TrackingStep(
                title="Loan Disbursement & Margin Money Escrow Credit",
                status="PENDING",
                date="Estimated: 15 Sep 2026",
                officer_remark="95% composite loan disbursal and 35% margin money subsidy lock-in."
            )
        ]
    ),
    "MUDRA-2026-KISHORE-4492": ApplicationStatusResponse(
        tracking_id="MUDRA-2026-KISHORE-4492",
        scheme_name="PM MUDRA Yojana (Kishore Category)",
        applicant_name="Rajesh Kumar Sharma",
        applied_date="19 Aug 2026",
        current_stage="Sanctioned & Ready for Disbursal",
        overall_status="APPROVED",
        progress_percentage=85,
        next_action_due="Sign loan agreement and activate MUDRA RuPay Debit Card",
        steps=[
            TrackingStep(
                title="Application Submitted via Udyamimitra",
                status="COMPLETED",
                date="19 Aug 2026",
                officer_remark="Applied for ₹3.5 Lakh term loan + inventory credit with Udyam Certificate."
            ),
            TrackingStep(
                title="CIBIL / Credit Scoring & Business Verification",
                status="COMPLETED",
                date="22 Aug 2026",
                officer_remark="Credit score 740 verified. Shop premises inspected by Field Officer."
            ),
            TrackingStep(
                title="Credit Facility Sanctioned",
                status="COMPLETED",
                date="26 Aug 2026",
                officer_remark="₹3,50,000 sanctioned at 9.25% p.a. without collateral security."
            ),
            TrackingStep(
                title="Fund Disbursement & MUDRA Card Activation",
                status="IN_PROGRESS",
                date="30 Aug 2026",
                officer_remark="Disbursement order generated. MUDRA RuPay card dispatched."
            )
        ]
    ),
    "VISHWAKARMA-2026-3120": ApplicationStatusResponse(
        tracking_id="VISHWAKARMA-2026-3120",
        scheme_name="PM Vishwakarma Scheme",
        applicant_name="Sunil Karmakar",
        applied_date="05 Aug 2026",
        current_stage="Toolkit Voucher Disbursed",
        overall_status="APPROVED",
        progress_percentage=90,
        next_action_due="Apply for 1st Tranche Loan (₹1,00,000 @ 5%)",
        steps=[
            TrackingStep(
                title="CSC Biometric Registration",
                status="COMPLETED",
                date="05 Aug 2026",
                officer_remark="Aadhaar biometrics and trade certification (Blacksmith / Carpentry) registered."
            ),
            TrackingStep(
                title="Gram Panchayat Level-1 Vetting",
                status="COMPLETED",
                date="08 Aug 2026",
                officer_remark="Local trade practice confirmed."
            ),
            TrackingStep(
                title="5-Day Basic Skill Training & Stipend",
                status="COMPLETED",
                date="15 Aug 2026",
                officer_remark="Basic skill certification awarded. ₹2,500 daily stipend credited."
            ),
            TrackingStep(
                title="₹15,000 Digital Toolkit e-RUPI Voucher Issued",
                status="COMPLETED",
                date="20 Aug 2026",
                officer_remark="Digital voucher delivered to registered mobile number for tool purchase."
            )
        ]
    )
}

@router.get("/{tracking_id}", response_model=ApplicationStatusResponse)
def get_application_status(tracking_id: str):
    tid = tracking_id.strip().upper()
    if tid in SIMULATED_TRACKING_DATABASE:
        return SIMULATED_TRACKING_DATABASE[tid]
    
    # Generate dynamic simulated application status for newly submitted demo applications
    return ApplicationStatusResponse(
        tracking_id=tid,
        scheme_name="Government Welfare & Subsidy Programme",
        applicant_name="Demo Applicant",
        applied_date="28 Aug 2026",
        current_stage="Document Scrutiny & Field Appraisal",
        overall_status="UNDER_REVIEW",
        progress_percentage=45,
        next_action_due="District verification officer will schedule on-site verification within 3 business days",
        steps=[
            TrackingStep(
                title="Online Application Submitted",
                status="COMPLETED",
                date="28 Aug 2026, 10:15 AM",
                officer_remark="Application successfully logged into national database."
            ),
            TrackingStep(
                title="Aadhaar & KYC Authentication",
                status="COMPLETED",
                date="28 Aug 2026, 10:18 AM",
                officer_remark="UIDAI authentication verified successfully."
            ),
            TrackingStep(
                title="District Screening & Field Appraisal",
                status="IN_PROGRESS",
                date="30 Aug 2026",
                officer_remark="Application currently under review by District Task Force."
            ),
            TrackingStep(
                title="Bank Credit Sanction & Subsidy Disbursal",
                status="PENDING",
                date="Estimated in 10 days",
                officer_remark="Pending completion of field verification."
            )
        ]
    )
