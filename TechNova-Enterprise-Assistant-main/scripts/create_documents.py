from pathlib import Path
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "documents"

DOCS_DIR.mkdir(exist_ok=True)

styles = getSampleStyleSheet()


def create_pdf(filename, title, paragraphs):
    doc = SimpleDocTemplate(str(DOCS_DIR / filename))

    story = [Paragraph(f"<b>{title}</b>", styles["Title"])]

    for para in paragraphs:
        story.append(Paragraph(para, styles["BodyText"]))

    doc.build(story)


# ============================================================
# Employee Handbook
# ============================================================

create_pdf(
    "Employee_Handbook.pdf",
    "TechNova Employee Handbook",
    [
        "Welcome to TechNova Pvt Ltd. We believe in innovation, collaboration and continuous learning.",
        "Employees are expected to maintain professionalism while interacting with clients and colleagues.",
        "All employees should complete mandatory security and compliance training every year.",
        "Employees should maintain confidentiality of company information.",
        "Company assets should only be used for business purposes.",
        "Employees should follow all HR and IT security policies.",
    ],
)


# ============================================================
# Leave Policy
# ============================================================

create_pdf(
    "Leave_Policy.pdf",
    "Leave Policy",
    [
        "Every employee is entitled to 12 Casual Leaves every calendar year.",
        "Employees are entitled to 10 Sick Leaves every calendar year.",
        "Earned Leave accumulates according to company policy.",
        "Leave requests must be approved by the reporting manager.",
        "Rejected leave requests are not counted against the employee.",
        "Employees can view all leave history through the HR portal.",
    ],
)


# ============================================================
# Promotion Policy
# ============================================================

create_pdf(
    "Promotion_Policy.pdf",
    "Promotion Policy",
    [
        "Employees become eligible for promotion after completing at least 3 years in the company.",
        "The latest performance review rating must be at least 4.5 out of 5.",
        "Mandatory annual training must be completed.",
        "Final promotion approval is given by department management and HR.",
        "Promotion also depends on business requirements and role availability.",
    ],
)


# ============================================================
# Work From Home Policy
# ============================================================

create_pdf(
    "WFH_Policy.pdf",
    "Work From Home Policy",
    [
        "Employees may work remotely up to two days per week.",
        "Managers may approve additional remote work under exceptional circumstances.",
        "Employees must remain available during business hours while working remotely.",
        "Sensitive company information must never be accessed from unsecured devices.",
        "Attendance records are maintained regardless of work location.",
    ],
)


# ============================================================
# Expense Policy
# ============================================================

create_pdf(
    "Expense_Policy.pdf",
    "Expense Reimbursement Policy",
    [
        "Business travel expenses are reimbursable after approval.",
        "Employees must submit original bills within 15 days.",
        "Meal expenses are reimbursed according to company limits.",
        "Personal expenses are not reimbursable.",
        "Finance department reviews all submitted claims.",
    ],
)


# ============================================================
# Database Glossary
# ============================================================

create_pdf(
    "Database_Glossary.pdf",
    "Enterprise Database Glossary",
    [
        "CL stands for Casual Leave.",
        "SL stands for Sick Leave.",
        "EL stands for Earned Leave.",
        "Training Completed indicates whether mandatory annual training has been finished.",
        "Performance ratings are given on a scale of 1 to 5.",
        "Department heads manage their respective departments.",
        "Attendance work modes include Office, Hybrid and Remote.",
    ],
)

print("=" * 50)
print("Enterprise documents created successfully!")
print("=" * 50)

for pdf in DOCS_DIR.iterdir():
    print(pdf.name)