from reportlab.pdfgen import canvas


def generate_receipt(payment):
    file_name = f"receipt_{payment.order_id}.pdf"
    c = canvas.Canvas(file_name)

    c.drawString(100, 750, f"Order ID: {payment.order_id}")
    c.drawString(100, 730, f"Amount: {payment.amount}")
    c.drawString(100, 710, f"Status: {payment.status}")

    c.save()

    return file_name