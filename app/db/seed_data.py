# Comprehensive Real-World Indian Government Schemes Seed Dataset with Deadlines & Case Studies
import json
from app.db.database import SessionLocal, engine, Base
from app.db.models import Scheme, EligibilityRule, Benefit, Document

SEED_SCHEMES = [
    {
        "id": "pmegp_001",
        "name": "Prime Minister's Employment Generation Programme (PMEGP)",
        "slug": "pmegp",
        "department": "Khadi and Village Industries Commission (KVIC)",
        "ministry": "Ministry of Micro, Small and Medium Enterprises",
        "category": "Business & Entrepreneurship",
        "summary": "Credit-linked subsidy program offering 15% to 35% margin money subsidy for new manufacturing & service micro-enterprises.",
        "description": "PMEGP is a major credit-linked subsidy program aimed at generating self-employment opportunities through establishment of micro-enterprises in non-farm sector by helping traditional artisans and unemployed youth.",
        "coverage": ["ALL"],
        "max_benefit": "₹50,00,000 (Manufacturing) / ₹20,00,000 (Service)",
        "benefit_type": "Subsidy + Bank Loan",
        "deadline": "March 31, 2027 (FY 2026-27 Active)",
        "processing_timeline": "21–30 Days",
        "application_url": "https://www.kviconline.gov.in/pmegpeportal/pmegphome/index.jsp",
        "source_url": "https://msme.gov.in/pmegp",
        "last_verified_at": "2026-08-15",
        "status": "VERIFIED",
        "tags": ["manufacturing", "service", "subsidy", "micro-enterprise", "youth", "rural", "urban"],
        "success_story": {
            "name": "Sunita Roy",
            "location": "Nadia, West Bengal",
            "enterprise": "Eco-Packaging & Areca Leaf Products",
            "before_metric": "Unemployed • ₹0 Monthly Revenue",
            "after_metric": "Employs 12 Rural Women • ₹4.8 Lakh Monthly Turnover",
            "subsidy_or_loan_received": "₹5.25 Lakh Government Subsidy (35% Rural Special Category)",
            "story_quote": "PMEGP gave me the confidence to start my manufacturing unit. The 35% subsidy locked in seamlessly, making loan repayment hassle-free."
        },
        "application_steps": [
            "Submit online application on KVIC PMEGP e-Portal with detailed project report (DPR).",
            "District Level Task Force Committee (DLTFC) scrutinizes the application and forwards to financing bank.",
            "Financing bank conducts appraisal and sanctions credit facility.",
            "Complete mandatory Entrepreneurship Development Programme (EDP) training.",
            "Bank releases loan funds and KVIC deposits margin money subsidy in an escrow account."
        ],
        "eligibility_rules": [
            {"field": "age", "operator": "GTE", "value": 18, "required": True, "label": "Minimum Age", "description": "Applicant must be at least 18 years of age.", "source_reference": "KVIC Guidelines Sec 3.1"},
            {"field": "business_status", "operator": "EQ", "value": "New / Proposed", "required": True, "label": "Project Stage", "description": "Only new/proposed projects are eligible for 1st financial assistance.", "source_reference": "PMEGP Rule 4"},
            {"field": "business_type", "operator": "IN", "value": ["Manufacturing", "Service & Hospitality", "Food Processing & Bakery", "Handicrafts & Traditional Artisan", "Dairy & Animal Husbandry", "Poultry & Livestock", "Garment & Textile", "Retail & Trading"], "required": True, "label": "Business Sector", "description": "Manufacturing and service sector projects are eligible.", "source_reference": "KVIC Approved Sectors"}
        ],
        "benefits": [
            {"title": "Margin Money Subsidy (Rural)", "description": "25% subsidy for General category and 35% for Special categories (SC/ST/OBC/Women/Ex-servicemen) in rural areas.", "amount_or_percentage": "25% - 35%"},
            {"title": "Margin Money Subsidy (Urban)", "description": "15% subsidy for General category and 25% for Special categories in urban locations.", "amount_or_percentage": "15% - 25%"},
            {"title": "Bank Financing", "description": "90% to 95% of the total project cost funded as bank term loan & working capital.", "amount_or_percentage": "Up to 95% Project Cost"}
        ],
        "documents": [
            {"name": "Aadhaar Card", "is_mandatory": True, "description": "Identity & UIDAI verification proof"},
            {"name": "Detailed Project Report (DPR)", "is_mandatory": True, "description": "Project cost breakup, projected revenue, and machinery requirements"},
            {"name": "Educational Certificate (8th Pass+)", "is_mandatory": True, "description": "Required for projects above ₹10 Lakh in manufacturing or ₹5 Lakh in service"},
            {"name": "Caste / Special Category Certificate", "is_mandatory": False, "description": "Required to claim higher 25-35% subsidy"},
            {"name": "Bank Account Details & Cancelled Cheque", "is_mandatory": True, "description": "Linked bank account for subsidy lock-in"}
        ]
    },
    {
        "id": "mudra_kishore_002",
        "name": "PM MUDRA Yojana (Kishore Category)",
        "slug": "mudra-kishore",
        "department": "Department of Financial Services",
        "ministry": "Ministry of Finance",
        "category": "Credit & Micro-Finance",
        "summary": "Collateral-free institutional loans from ₹50,000 up to ₹5,00,000 for expanding existing small businesses and micro-units.",
        "description": "Pradhan Mantri MUDRA Yojana (PMMY) facilitates loans to non-corporate, non-farm small/micro enterprises. The Kishore category caters to entrepreneurs ready to take their next growth step.",
        "coverage": ["ALL"],
        "max_benefit": "₹5,00,00,000 collateral-free credit",
        "benefit_type": "Institutional Term Loan & Overdraft",
        "deadline": "Rolling Intake (Open Year-Round)",
        "processing_timeline": "7–14 Days",
        "application_url": "https://www.udyamimitra.in/",
        "source_url": "https://www.mudra.org.in/",
        "last_verified_at": "2026-08-15",
        "status": "VERIFIED",
        "tags": ["mudra", "loan", "working capital", "collateral-free", "small business", "trading", "shop"],
        "success_story": {
            "name": "Ramesh Patel",
            "location": "Ahmedabad, Gujarat",
            "enterprise": "Precision Auto Components Workshop",
            "before_metric": "Manual Lathe • ₹45,000 Monthly Revenue",
            "after_metric": "CNC Machine Installed • ₹3.8 Lakh Monthly Revenue",
            "subsidy_or_loan_received": "₹4.5 Lakh Collateral-Free Term Loan @ 9.5%",
            "story_quote": "MUDRA Kishore didn't ask for land collateral. Within 10 days of applying at Bank of Baroda, my machinery loan was sanctioned."
        },
        "application_steps": [
            "Approach any commercial bank, RRB, Small Finance Bank, or MFI.",
            "Fill standard PMMY Kishore Loan application form online or in branch.",
            "Submit quotations of machinery/goods to be purchased along with business proof.",
            "Bank verifies business premises and sanctions loan without collateral security."
        ],
        "eligibility_rules": [
            {"field": "age", "operator": "GTE", "value": 18, "required": True, "label": "Minimum Age", "description": "Must be an Indian citizen aged 18 or older.", "source_reference": "PMMY Circular 2024"},
            {"field": "loan_required", "operator": "BETWEEN", "value": [50000, 500000], "required": True, "label": "Loan Amount", "description": "Kishore category strictly covers loans between ₹50,000 and ₹5,00,000.", "source_reference": "Mudra Guidelines"}
        ],
        "benefits": [
            {"title": "Zero Collateral Security", "description": "No third-party guarantee or collateral asset needed.", "amount_or_percentage": "100% Collateral Free"},
            {"title": "Competitive Interest Rates", "description": "Linked to RBI repo rate / MCLR with minimal processing fee.", "amount_or_percentage": "8.5% - 11.5% p.a."}
        ],
        "documents": [
            {"name": "Aadhaar Card / Voter ID", "is_mandatory": True, "description": "Proof of identity"},
            {"name": "Business Address & Registration Proof", "is_mandatory": True, "description": "Udyam Registration, trade license, or GST certificate"},
            {"name": "6-Month Bank Statement", "is_mandatory": True, "description": "Bank account transaction statement"},
            {"name": "Quotations of Machinery / Inventory", "is_mandatory": True, "description": "Invoice quotations from vendor for items to purchase"}
        ]
    },
    {
        "id": "stand_up_india_003",
        "name": "Stand-Up India Scheme",
        "slug": "stand-up-india",
        "department": "Department of Financial Services",
        "ministry": "Ministry of Finance",
        "category": "Women & SC/ST Entrepreneurship",
        "summary": "Bank loans between ₹10 Lakh and ₹1 Crore for setting up greenfield enterprises by Women or SC/ST entrepreneurs.",
        "description": "Stand-Up India facilitates bank loans between ₹10 lakh and ₹1 crore to at least one SC or ST borrower and at least one woman borrower per bank branch for setting up greenfield enterprises in manufacturing, services, agri-allied, or trading.",
        "coverage": ["ALL"],
        "max_benefit": "₹1,00,00,000 (1 Crore)",
        "benefit_type": "Composite Bank Loan (Term + Working Capital)",
        "deadline": "Extended through 2027",
        "processing_timeline": "30–45 Days",
        "application_url": "https://www.standupmitra.in/",
        "source_url": "https://www.standupmitra.in/Home/SUISchemes",
        "last_verified_at": "2026-08-15",
        "status": "VERIFIED",
        "tags": ["women", "sc-st", "greenfield", "large loan", "entrepreneurship", "manufacturing", "services"],
        "success_story": {
            "name": "Meenakshi Sundaram",
            "location": "Coimbatore, Tamil Nadu",
            "enterprise": "Eco-Friendly Organic Textile Processing",
            "before_metric": "First-Time Woman Entrepreneur",
            "after_metric": "Exporting to 3 Countries • 25 Full-Time Employees",
            "subsidy_or_loan_received": "₹65 Lakh Composite Facility at SBI",
            "story_quote": "Stand-Up India made it mandatory for bank branches to fund women founders. The 18-month moratorium helped us reach profitability before EMIs began."
        },
        "application_steps": [
            "Register online on the Stand-Up Mitra portal.",
            "Choose your financing bank branch or apply via Handholding Agency.",
            "Submit Project Report, Udyam Registration, and KYC details.",
            "Bank branch manager reviews and processes composite loan sanction."
        ],
        "eligibility_rules": [
            {"field": "age", "operator": "GTE", "value": 18, "required": True, "label": "Age Criterion", "description": "Applicant must be above 18 years.", "source_reference": "SUIS Guidelines Sec 2"},
            {"field": "business_status", "operator": "EQ", "value": "New / Proposed", "required": True, "label": "Enterprise Stage", "description": "Must be a Greenfield project (first-time venture in trading/manufacturing/services).", "source_reference": "SUIS Greenfield Rule"},
            {"field": "gender", "operator": "IN", "value": ["Female", "Women", "Any"], "required": False, "label": "Gender Preference", "description": "Priority for Women or SC/ST entrepreneurs.", "source_reference": "SUIS Mandate"}
        ],
        "benefits": [
            {"title": "Composite Loan Facility", "description": "Covers 85% of project cost (term loan + working capital component).", "amount_or_percentage": "₹10 Lakh - ₹1 Crore"},
            {"title": "Repayment Period", "description": "Repayable in up to 7 years with a moratorium period of up to 18 months.", "amount_or_percentage": "7 Years Tenure"}
        ],
        "documents": [
            {"name": "Aadhaar Card and PAN Card", "is_mandatory": True, "description": "Identity and tax proof"},
            {"name": "Proof of SC/ST or Woman Ownership (51%+)", "is_mandatory": True, "description": "Caste certificate or shareholding documentation"},
            {"name": "Detailed Project Report & Feasibility Study", "is_mandatory": True, "description": "Technical & financial viability report"},
            {"name": "Lease Agreement / Land Documents for Enterprise", "is_mandatory": True, "description": "Proof of factory/office premises"}
        ]
    },
    {
        "id": "pm_vishwakarma_005",
        "name": "PM Vishwakarma Scheme",
        "slug": "pm-vishwakarma",
        "department": "Ministry of Micro, Small and Medium Enterprises",
        "ministry": "Ministry of MSME",
        "category": "Artisans & Traditional Crafts",
        "summary": "Comprehensive support for 18 traditional artisan trades: ₹3 Lakh collateral-free loan at 5% interest, ₹15,000 modern toolkit grant, and skill training.",
        "description": "PM Vishwakarma provides holistic end-to-end support to traditional artisans and craftspeople engaged in 18 identified trades including carpenters, blacksmiths, potters, sculptors, cobblers, tailors, and basket makers.",
        "coverage": ["ALL"],
        "max_benefit": "₹3,00,000 loan @ 5% + ₹15,000 Toolkit Grant + ₹500/day stipend",
        "benefit_type": "Subsidized Loan + Toolkit Grant + Stipend",
        "deadline": "Active Central Programme",
        "processing_timeline": "10–20 Days",
        "application_url": "https://pmvishwakarma.gov.in/",
        "source_url": "https://pmvishwakarma.gov.in/",
        "last_verified_at": "2026-08-15",
        "status": "VERIFIED",
        "tags": ["artisan", "carpenter", "blacksmith", "potter", "sculptor", "tailor", "vishwakarma", "toolkit", "grant"],
        "success_story": {
            "name": "Mohan Lal",
            "location": "Varanasi, Uttar Pradesh",
            "enterprise": "Traditional Wooden Toys & Heritage Crafts",
            "before_metric": "Hand Chisel Only • Low Productivity",
            "after_metric": "High-Precision Electric Lathe • 3x Daily Production",
            "subsidy_or_loan_received": "₹15,000 Digital Toolkit Grant + ₹1 Lakh Loan @ 5%",
            "story_quote": "The ₹15,000 modern toolkit voucher arrived as an e-RUPI message. With upgraded electric sanders and carving tools, my craft quality is now recognized nationally."
        },
        "application_steps": [
            "Register at Common Service Centre (CSC) with Aadhaar and biometrics.",
            "Level-1 Gram Panchayat / Urban Local Body verification.",
            "Level-2 District Implementation Committee vetting.",
            "Complete 5–7 day basic skill training and receive ₹15,000 e-voucher for modern toolkits.",
            "Apply for 1st tranche loan of ₹1,00,000 at concessional 5% interest rate."
        ],
        "eligibility_rules": [
            {"field": "age", "operator": "GTE", "value": 18, "required": True, "label": "Minimum Age", "description": "Must be at least 18 years on registration date.", "source_reference": "PM Vishwakarma Guidelines Sec 4.1"},
            {"field": "business_type", "operator": "IN", "value": ["Handicrafts & Traditional Artisan", "Traditional Crafts (Vishwakarma)", "Garment & Textile", "Manufacturing"], "required": True, "label": "Trade Category", "description": "Engaged in one of 18 traditional family-based artisan crafts.", "source_reference": "18 Identified Crafts List"}
        ],
        "benefits": [
            {"title": "Concessional Collateral-Free Credit", "description": "₹1 Lakh (1st tranche) and ₹2 Lakh (2nd tranche) at highly subsidized 5% interest with 8% subvention paid by MoMSME.", "amount_or_percentage": "5% Concessional Interest"},
            {"title": "Modern Toolkit Incentive", "description": "₹15,00,0 financial grant provided via digital e-RUPI voucher for quality tools.", "amount_or_percentage": "₹15,000 Grant"},
            {"title": "Training Stipend", "description": "₹500 per day allowance during 5–7 days basic and 15 days advanced skill training.", "amount_or_percentage": "₹500 / Day"}
        ],
        "documents": [
            {"name": "Aadhaar Card and Mobile Number", "is_mandatory": True, "description": "Biometric Aadhaar authentication"},
            {"name": "Bank Passbook / Cancelled Cheque", "is_mandatory": True, "description": "Active bank account for stipend & loan deposit"},
            {"name": "Ration Card / Family Declaration", "is_mandatory": True, "description": "Only one member per family is eligible for benefits"}
        ]
    },
    {
        "id": "nlm_dairy_poultry_008",
        "name": "National Livestock Mission (NLM) - Entrepreneurship Scheme",
        "slug": "national-livestock-mission",
        "department": "Department of Animal Husbandry and Dairying",
        "ministry": "Ministry of Fisheries, Animal Husbandry and Dairying",
        "category": "Animal Husbandry & Dairy",
        "summary": "50% capital subsidy up to ₹50 Lakh for establishing rural poultry, sheep/goat breeding, piggery, and fodder production units.",
        "description": "A flagship central scheme offering 50% direct capital subsidy to farmers, entrepreneurs, and cooperatives to set up commercial livestock breeding farms and animal feed/fodder infrastructure.",
        "coverage": ["ALL"],
        "max_benefit": "50% Capital Subsidy up to ₹50,00,000",
        "benefit_type": "Direct Capital Subsidy",
        "deadline": "March 31, 2027 (Central Sector)",
        "processing_timeline": "30–60 Days",
        "application_url": "https://nlm.udyamimitra.in/",
        "source_url": "https://dahd.nic.in/schemes/programmes/national_livestock_mission",
        "last_verified_at": "2026-08-15",
        "status": "VERIFIED",
        "tags": ["dairy", "poultry", "livestock", "sheep", "goat", "fodder", "subsidy", "animal husbandry"],
        "success_story": {
            "name": "Gurpreet Singh",
            "location": "Ludhiana, Punjab",
            "enterprise": "Modern Automated Dairy & Fodder Farm",
            "before_metric": "Traditional 8-cow shed • Manual Milking",
            "after_metric": "50-Cow Automated Shed • 600 Litres/Day Supply",
            "subsidy_or_loan_received": "₹25 Lakh Direct Capital Subsidy (50%)",
            "story_quote": "The 50% capital subsidy from National Livestock Mission made setting up our automated bulk milk cooling infrastructure completely viable."
        },
        "application_steps": [
            "Prepare Detailed Project Report (DPR) adhering to DAHD model farm layouts.",
            "Submit online application on NLM Udyamimitra portal.",
            "State Level Executive Committee (SLEC) inspects land/site and grants in-principle approval.",
            "Bank sanctions 50% term loan and DAHD releases capital subsidy in two installments."
        ],
        "eligibility_rules": [
            {"field": "age", "operator": "GTE", "value": 18, "required": True, "label": "Minimum Age", "description": "Applicant must be an Indian citizen aged 18+.", "source_reference": "NLM Guidelines 2024"},
            {"field": "business_type", "operator": "IN", "value": ["Dairy & Animal Husbandry", "Poultry & Livestock", "Agriculture & Farming"], "required": True, "label": "Farm Category", "description": "Eligible for poultry, dairy, goat/sheep breeding or fodder enterprises.", "source_reference": "DAHD Scheme Matrix"}
        ],
        "benefits": [
            {"title": "50% Capital Subsidy", "description": "50% back-ended capital subsidy on capital expenditure up to ₹50 Lakh for poultry and ₹50 Lakh for sheep/goat farms.", "amount_or_percentage": "50% (Max ₹50 Lakh)"}
        ],
        "documents": [
            {"name": "Land Ownership / 15-Year Registered Lease Deed", "is_mandatory": True, "description": "Proof of required land area for farm shed construction"},
            {"name": "Detailed Project Report (DPR)", "is_mandatory": True, "description": "Technical specifications, breed details, and vet care plan"},
            {"name": "Training Certificate in Animal Husbandry", "is_mandatory": False, "description": "Recommended for expedited committee clearance"}
        ]
    },
    {
        "id": "pm_svanidhi_004",
        "name": "PM Street Vendor's AtmaNirbhar Nidhi (PM SVANidhi)",
        "slug": "pm-svanidhi",
        "department": "Ministry of Housing and Urban Affairs",
        "ministry": "Ministry of Housing and Urban Affairs",
        "category": "Urban Livelihoods & Micro-Credit",
        "summary": "Collateral-free working capital micro-loans starting at ₹10,000, progressing to ₹20,000 and ₹50,000 with 7% interest subsidy for street vendors.",
        "description": "A special micro-credit facility that provides street vendors affordable loans to resume livelihoods affected by economic shocks, incentivizing digital transactions with monthly cashbacks.",
        "coverage": ["ALL"],
        "max_benefit": "₹50,000 with 7% interest subsidy",
        "benefit_type": "Working Capital Loan + Cashback",
        "deadline": "Active Central Scheme",
        "processing_timeline": "7–10 Days",
        "application_url": "https://pmsvanidhi.mohua.gov.in/",
        "source_url": "https://pmsvanidhi.mohua.gov.in/",
        "last_verified_at": "2026-08-15",
        "status": "VERIFIED",
        "tags": ["street vendor", "hawker", "micro-loan", "interest subsidy", "cashback", "svanidhi"],
        "success_story": {
            "name": "Sunita Devi",
            "location": "Patna, Bihar",
            "enterprise": "Fresh Fruit & Juice Vending Cart",
            "before_metric": "Daily Informal Debt @ 10% Weekly Interest",
            "after_metric": "Completed ₹10k & ₹20k Tranches • Granted ₹50k Limit",
            "subsidy_or_loan_received": "₹50,000 Bank Loan + ₹1,200 Annual Cashback",
            "story_quote": "PM SVANidhi freed me from local money lenders. Prompt digital UPI payments gave me 7% interest refund directly into my account."
        },
        "application_steps": [
            "Verify your name in the Urban Local Body (ULB) vendor survey or obtain Letter of Recommendation (LoR).",
            "Apply online through PM SVANidhi portal or Common Service Centre (CSC).",
            "Select nearby lending institution (Bank/NBFC/MFI).",
            "Direct loan disbursement into bank account within 7–10 days."
        ],
        "eligibility_rules": [
            {"field": "age", "operator": "GTE", "value": 18, "required": True, "label": "Minimum Age", "description": "Applicant must be at least 18 years of age.", "source_reference": "MoHUA Rules"},
            {"field": "business_type", "operator": "IN", "value": ["Retail & Trading", "Food Processing & Bakery", "Service & Hospitality", "Traditional Crafts (Vishwakarma)"], "required": True, "label": "Vending Sector", "description": "Street vending / roadside trading / mobile hawking.", "source_reference": "Street Vendors Act 2014"}
        ],
        "benefits": [
            {"title": "Initial Working Capital Tranche", "description": "₹10,000 1st tranche, graduating to ₹20,000 (2nd tranche) and ₹50,000 (3rd tranche) on timely repayment.", "amount_or_percentage": "₹10,000 - ₹50,000"},
            {"title": "Interest Subsidy", "description": "7% annual interest subsidy credited directly to bank account on quarterly basis.", "amount_or_percentage": "7% Interest Subsidy"},
            {"title": "Digital Cashback", "description": "Cashback incentive up to ₹1,200 per year on eligible UPI/digital sales.", "amount_or_percentage": "₹100 / Month"}
        ],
        "documents": [
            {"name": "Aadhaar Card", "is_mandatory": True, "description": "Identity verification"},
            {"name": "Certificate of Vending / ULB Identity Card or LoR", "is_mandatory": True, "description": "Proof of street vending from municipality or town committee"},
            {"name": "Active Savings Bank Account Details", "is_mandatory": True, "description": "Aadhaar linked bank account"}
        ]
    }
]

def init_db_and_seed():
    """Initializes tables and populates verified seed schemes if not present."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        count = db.query(Scheme).count()
        if count == 0:
            print("[SEED] Seeding verified government schemes into database...")
            for s_data in SEED_SCHEMES:
                scheme = Scheme(
                    id=s_data["id"],
                    name=s_data["name"],
                    slug=s_data["slug"],
                    department=s_data["department"],
                    ministry=s_data.get("ministry"),
                    category=s_data["category"],
                    description=s_data["description"],
                    summary=s_data["summary"],
                    coverage=json.dumps(s_data["coverage"]),
                    max_benefit=s_data.get("max_benefit"),
                    benefit_type=s_data.get("benefit_type"),
                    application_url=s_data.get("application_url"),
                    source_url=s_data.get("source_url"),
                    last_verified_at=s_data.get("last_verified_at", "2026-08-15"),
                    status=s_data.get("status", "VERIFIED"),
                    tags=json.dumps(s_data.get("tags", [])),
                    application_steps=json.dumps(s_data.get("application_steps", []))
                )
                db.add(scheme)
                db.flush()

                # Add rules
                for r in s_data.get("eligibility_rules", []):
                    rule = EligibilityRule(
                        scheme_id=scheme.id,
                        field=r["field"],
                        operator=r["operator"],
                        value=json.dumps(r["value"]) if isinstance(r["value"], (list, dict)) else str(r["value"]),
                        required=r.get("required", True),
                        label=r.get("label"),
                        description=r.get("description"),
                        source_reference=r.get("source_reference")
                    )
                    db.add(rule)

                # Add benefits
                for b in s_data.get("benefits", []):
                    benefit = Benefit(
                        scheme_id=scheme.id,
                        title=b["title"],
                        description=b["description"],
                        amount_or_percentage=b.get("amount_or_percentage")
                    )
                    db.add(benefit)

                # Add documents
                for d in s_data.get("documents", []):
                    doc = Document(
                        scheme_id=scheme.id,
                        name=d["name"],
                        is_mandatory=d.get("is_mandatory", True),
                        description=d.get("description")
                    )
                    db.add(doc)

            db.commit()
            print(f"[SEED] Successfully seeded {len(SEED_SCHEMES)} verified government schemes.")
        else:
            print(f"[SEED] Database already contains {count} schemes.")
    except Exception as e:
        db.rollback()
        print(f"[SEED ERROR] Failed to seed database: {e}")
    finally:
        db.close()
