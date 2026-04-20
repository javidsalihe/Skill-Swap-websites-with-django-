from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from django.conf import settings
import os


def generate_exchange_pdf(exchange, negotiations, ratings, doc_type, filename):
    folder = os.path.join(settings.MEDIA_ROOT, 'exchange_documents')
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, filename)

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # تعریف یک استایل خاص برای متون حقوقی ریزتر و رسمی‌تر
    legal_style = ParagraphStyle(
        'LegalStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        alignment=4,  # Justified
        spaceAfter=10
    )

    elements = []

    # -------- HEADER --------
    elements.append(Paragraph(
        f"<b>SkillSwap Official Document</b>", styles['Title']
    ))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph(
        f"<b>Document type:</b> {doc_type.upper()}", styles['Normal']
    ))
    elements.append(Paragraph(
        f"<b>Exchange UUID:</b> {exchange.uuid}", styles['Normal']
    ))
    elements.append(Paragraph(
        f"<b>Generated at:</b> {exchange.updated_at}", styles['Normal']
    ))
    elements.append(Spacer(1, 20))

    # -------- LEGAL TERMS & CONDITIONS (بخش جدید حقوقی) --------
    elements.append(Paragraph("<b>1. Legal Terms & Binding Agreement</b>", styles['Heading3']))

    legal_text = """
    By participating in this skill exchange, both parties (User X and User Y) hereby acknowledge that this 
    document constitutes a legally binding agreement. Participants agree to perform the services described 
    in the negotiation history with professional due diligence and mutual respect. This platform serves as 
    a facilitator, and the responsibility for service delivery lies solely with the participants.
    """
    elements.append(Paragraph(legal_text, legal_style))

    # بخش جریمه (Double Penalty Clause)
    penalty_text = """
    <b>2. Default and Breach of Contract:</b> In the event that one party has fulfilled their obligation 
    (provided the skill/work) and the second party fails, refuses, or neglects to fulfill their reciprocal 
    obligation without a valid legal reason, the defaulting party shall be held in breach of contract. 
    The aggrieved party shall have the right to file an official complaint. <b>Upon verification, the 
    defaulting party shall be legally required to compensate the aggrieved party with an amount equal 
    to DOUBLE (2x) the estimated market value of the work performed.</b>
    """
    elements.append(Paragraph(penalty_text, legal_style))
    elements.append(Spacer(1, 15))

    # -------- USERS --------
    elements.append(Paragraph("<b>Participants</b>", styles['Heading2']))

    user_table = Table([
        ["Role", "Name", "Email"],
        ["User X", exchange.user_x.get_full_name(), exchange.user_x.email],
        ["User Y", exchange.user_y.get_full_name(), exchange.user_y.email],
    ])

    user_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))

    elements.append(user_table)
    elements.append(Spacer(1, 20))

    # -------- EXCHANGE DETAILS --------
    elements.append(Paragraph("<b>Exchange Details</b>", styles['Heading2']))

    details = [
        ["Status", exchange.status],
        ["Location Type", exchange.location_type],
        ["Scheduled At", exchange.scheduled_at or "-"],
        ["Completed At X", exchange.completed_at_x or "-"],
        ["Completed At Y", exchange.completed_at_y or "-"],
        ["Duration X (min)", exchange.duration_minutes_x or "-"],
        ["Duration Y (min)", exchange.duration_minutes_y or "-"],
        ["Final Agreement", "Yes" if exchange.final_agreement_reached else "No"],
    ]

    elements.append(Table(details, colWidths=[200, 300], style=TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])))
    elements.append(Spacer(1, 20))

    # -------- NEGOTIATIONS --------
    elements.append(Paragraph("<b>Negotiation History</b>", styles['Heading2']))

    if negotiations.exists():
        for n in negotiations:
            elements.append(Paragraph(
                f"<b>{n.created_at.strftime('%Y-%m-%d %H:%M')}</b> - {n.proposer.get_full_name()}: {n.message}",
                styles['Normal']
            ))
            elements.append(Spacer(1, 6))
    else:
        elements.append(Paragraph("No negotiations record found for this exchange.", styles['Italic']))

    # -------- RATINGS (Completion only) --------
    if doc_type == 'completion':
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("<b>Final Ratings & Feedback</b>", styles['Heading2']))

        for r in ratings:
            elements.append(Paragraph(
                f"<b>{r.author.get_full_name()}</b> rated <b>{r.target_user.get_full_name()}</b>: "
                f"{r.score}/5 stars", styles['Normal']
            ))
            if r.comment:
                elements.append(Paragraph(f"Comment: {r.comment}", styles['Italic']))
            elements.append(Spacer(1, 6))

    # -------- FOOTER --------
    elements.append(Spacer(1, 40))
    elements.append(Paragraph(
        "CONFIDENTIAL: This document is digitally verified and remains valid as legal evidence in case of disputes.",
        styles['Italic']
    ))

    doc.build(elements)

    return f"exchange_documents/{filename}"