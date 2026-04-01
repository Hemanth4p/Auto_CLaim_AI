from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)
from reportlab.lib.units import inch
import os

REPORTS_DIR = "data/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)


def generate_pdf_report(
    claim_id: str,
    vehicle_make: str,
    vehicle_model: str,
    vehicle_year: int,
    damages: list,
    policy_type: str,
    shap_result: dict
) -> str:

    pdf_path = os.path.join(REPORTS_DIR, f"claim_{claim_id}.pdf")
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)

    styles = getSampleStyleSheet()
    elements = []

    title_style = ParagraphStyle(
        "title",
        fontSize=20,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1B4F8A"),
        spaceAfter=6
    )
    heading_style = ParagraphStyle(
        "heading",
        fontSize=13,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1B4F8A"),
        spaceBefore=12,
        spaceAfter=4
    )
    normal_style = ParagraphStyle(
        "normal_custom",
        fontSize=10,
        fontName="Helvetica",
        spaceAfter=3
    )
    green_style = ParagraphStyle(
        "green",
        fontSize=12,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#1D9E75")
    )

    elements.append(
        Paragraph("AutoClaim AI — Insurance Claim Report", title_style)
    )
    elements.append(
        Paragraph(
            "Intelligent Vehicle Insurance Claim Engine",
            normal_style
        )
    )
    elements.append(HRFlowable(width="100%", thickness=2,
                                color=colors.HexColor("#1B4F8A")))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph("Claim Details", heading_style))
    claim_data = [
        ["Claim ID", claim_id],
        ["Vehicle", f"{vehicle_make} {vehicle_model} {vehicle_year}"],
        ["Policy Type", policy_type],
        ["Vehicle Age", f"{2026 - vehicle_year} years"],
    ]
    claim_table = Table(claim_data, colWidths=[2 * inch, 4 * inch])
    claim_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1),
         colors.HexColor("#EBF3FB")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(claim_table)
    elements.append(Spacer(1, 0.15 * inch))

    elements.append(Paragraph("Damage Assessment", heading_style))
    damage_headers = [
        "Part", "Damage Type", "Cause", "Severity", "Covered"
    ]
    damage_rows = [damage_headers]
    for d in damages:
        covered_text = "YES" if d.get("covered", True) else "NO"
        damage_rows.append([
            d.get("part", "").replace("_", " ").title(),
            d.get("damage_type", "").title(),
            d.get("cause", "accident").title(),
            d.get("severity", "high").title(),
            covered_text
        ])
    damage_table = Table(
        damage_rows,
        colWidths=[1.4*inch, 1.2*inch, 1.0*inch, 1.0*inch, 0.8*inch]
    )
    damage_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#1B4F8A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#F5F9FF")]),
    ]))
    elements.append(damage_table)
    elements.append(Spacer(1, 0.15 * inch))

    elements.append(Paragraph("Financial Summary", heading_style))
    financial_data = [
        ["Repair Cost", f"Rs. {shap_result['base_repair_cost']:,.0f}"],
        ["Insured Declared Value (IDV)",
         f"Rs. {shap_result['idv']:,.0f}"],
        ["Compulsory Deductible",
         f"Rs. {shap_result['deductible']:,.0f}"],
        ["FINAL CLAIMABLE AMOUNT",
         f"Rs. {shap_result['final_claimable']:,.0f}"],
    ]
    fin_table = Table(financial_data, colWidths=[3 * inch, 3 * inch])
    fin_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1),
         colors.HexColor("#EBF3FB")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (0, 3), (-1, 3), "Helvetica-Bold"),
        ("BACKGROUND", (0, 3), (-1, 3),
         colors.HexColor("#E1F5EE")),
        ("TEXTCOLOR", (0, 3), (-1, 3),
         colors.HexColor("#085041")),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CCCCCC")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(fin_table)
    elements.append(Spacer(1, 0.15 * inch))

    elements.append(
        Paragraph("SHAP Explainability — Why This Amount?",
                  heading_style)
    )
    elements.append(
        Paragraph(
            "The following explains how each factor contributed "
            "to the final claim amount:",
            normal_style
        )
    )
    for explanation in shap_result.get("explanations", []):
        elements.append(
            Paragraph(f"• {explanation}", normal_style)
        )
    elements.append(Spacer(1, 0.15 * inch))

    elements.append(HRFlowable(
        width="100%", thickness=1,
        color=colors.HexColor("#CCCCCC")
    ))
    elements.append(Spacer(1, 0.1 * inch))
    elements.append(
        Paragraph(
            "This report was generated by AutoClaim AI. "
            "All decisions are based on policy terms and "
            "IRDAI guidelines.",
            normal_style
        )
    )

    doc.build(elements)
    return pdf_path