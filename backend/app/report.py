"""
PDF report generation, ported verbatim from app.py's create_pdf_report(),
parameterized to take an explicit result dict instead of closing over
Streamlit page-level globals.
"""

from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def create_pdf_report(ctx: dict) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    elements = []

    elements.append(Paragraph("ThermoGuard AI", title_style))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("Wildfire Risk & Fire Source Analysis Report", styles["Heading2"]))
    elements.append(Spacer(1, 15))

    # ----------------------------------------------------
    # FIRE DETECTION + RISK SUMMARY
    # ----------------------------------------------------

    risk_data = [
        ["Fire Detected", "YES" if ctx["fire_detected"] else "NO"],
        ["Detection Method", "Preliminary Rule-Based Thermal Screening"],
        ["Brightness Difference", f"{ctx['brightness_difference']:.2f}"],
        ["Risk Level", str(ctx["predicted_risk"])],
        ["Risk Confidence", f"{ctx['confidence_score']:.2f}%"],
        ["Fire Source", str(ctx["fire_source"])],
        ["Source Confidence", f"{ctx['fire_source_confidence']:.2f}%"],
        ["Fire Intensity", ctx["intensity"]],
        ["Brightness", str(ctx["brightness"])],
        ["FRP", str(ctx["frp"])],
        ["Observation Date", str(ctx["observation_date"])],
        ["Observation Time", str(ctx["observation_time"])],
    ]

    risk_table = Table(risk_data, colWidths=[200, 280])
    risk_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )

    elements.append(risk_table)
    elements.append(Spacer(1, 20))

    # ----------------------------------------------------
    # INPUT PARAMETERS
    # ----------------------------------------------------

    elements.append(Paragraph("Input Parameters", styles["Heading2"]))

    input_pdf_data = [
        ["Parameter", "Value"],
        ["Latitude", str(ctx["latitude"])],
        ["Longitude", str(ctx["longitude"])],
        ["Brightness", str(ctx["brightness"])],
        ["Scan", str(ctx["scan"])],
        ["Track", str(ctx["track"])],
        ["Acquisition Time", str(ctx["acq_time"])],
        ["Brightness T31", str(ctx["bright_t31"])],
        ["FRP", str(ctx["frp"])],
        ["Confidence", str(ctx["confidence"])],
        ["Day / Night", str(ctx["daynight"])],
        ["Hotspot Type", str(ctx["fire_type"])],
        ["Satellite Version", str(ctx["version"])],
        ["Observation Date", str(ctx["observation_date"])],
        ["Observation Time", str(ctx["observation_time"])],
        ["Season", str(ctx["season"])],
    ]

    input_table = Table(input_pdf_data, colWidths=[220, 260])
    input_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(input_table)
    elements.append(Spacer(1, 20))

    # ----------------------------------------------------
    # RISK PROBABILITIES
    # ----------------------------------------------------

    elements.append(Paragraph("Risk Probabilities", styles["Heading2"]))

    probability_pdf_data = [["Risk Level", "Probability"]]

    for row in ctx["prediction_proba"]:
        probability_pdf_data.append([str(row["risk_level"]), f"{row['probability']:.2f}%"])

    probability_table = Table(probability_pdf_data, colWidths=[220, 260])
    probability_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(probability_table)
    elements.append(Spacer(1, 20))

    # ----------------------------------------------------
    # FIRE ANALYSIS
    # ----------------------------------------------------

    elements.append(Paragraph("Fire Analysis", styles["Heading2"]))

    elements.append(
        Paragraph(f"Fire Detection: {'YES' if ctx['fire_detected'] else 'NO'}", styles["BodyText"])
    )
    elements.append(
        Paragraph(f"Brightness Difference: {ctx['brightness_difference']:.2f}", styles["BodyText"])
    )
    elements.append(Paragraph(f"Fire Intensity: {ctx['intensity']}", styles["BodyText"]))
    elements.append(Paragraph(f"Thermal Status: {ctx['thermal_status']}", styles["BodyText"]))
    elements.append(
        Paragraph(
            f"Observation Period: {'Daytime' if ctx['daynight'] == 'D' else 'Nighttime'}",
            styles["BodyText"],
        )
    )

    elements.append(Spacer(1, 15))

    # ----------------------------------------------------
    # LIMITATION
    # ----------------------------------------------------

    elements.append(
        Paragraph(
            "<b>Important Limitation:</b> "
            "Fire Detection is a preliminary rule-based thermal hotspot screening "
            "and is not a separately trained binary Fire/No-Fire ML classifier. "
            "The current dataset also does not contain direct Forest / Agriculture / "
            "Industrial labels. Fire source categories are based on hotspot source "
            "classes available in the dataset.",
            styles["BodyText"],
        )
    )

    elements.append(Spacer(1, 15))
    elements.append(Paragraph("Generated by ThermoGuard AI", styles["BodyText"]))

    doc.build(elements)
    buffer.seek(0)

    return buffer
