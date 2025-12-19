from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from pathlib import Path

print(">>> report_generator.py LOADED <<<")

def generate_pdf_report(context):
    print(">>> generate_pdf_report() CALLED <<<")
    """
    Generate a professional PDF A/B test report using ReportLab.
    This version is hardened and guaranteed to write the file.
    """

    output_dir = Path("reports")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "ab_test_report.pdf"

    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4
    y = height - 50

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, context.get("experiment_name", "A/B Test Report"))
    y -= 30

    # Description
    c.setFont("Helvetica", 11)
    c.drawString(50, y, context.get("description", ""))
    y -= 40

    # Frequentist Results
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Frequentist Results")
    y -= 20

    c.setFont("Helvetica", 10)
    for r in context.get("frequentist_results", []):
        line = (
            f"{r['metric']} | {r['test_used']} | "
            f"p={r['p_value']} | effect={r['effect_size']}"
        )
        c.drawString(50, y, line)
        y -= 15

        if y < 100:
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 10)

    # Bayesian Results
    y -= 20
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Bayesian Results")
    y -= 20

    c.setFont("Helvetica", 10)
    c.drawString(
        50, y,
        f"Expected Lift: {context.get('bayesian_lift')}"
    )
    y -= 15
    c.drawString(
        50, y,
        f"Probability Test > Control: {context.get('bayesian_prob')}"
    )

    # Recommendation
    y -= 30
    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y, "Final Recommendation")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(
        50, y,
        context.get("recommendation", "")
    )

    # 🔴 THIS IS THE CRITICAL LINE
    c.save()

    print(f"PDF successfully written to: {output_path.resolve()}")
