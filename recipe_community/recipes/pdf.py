import io
from datetime import date

from reportlab.pdfgen import canvas


def makeHeader(canvas, user):
    if user.is_authenticated:
        canvas.drawString(40, 100, 'User first name: ' + user.first_name)
        canvas.drawString(40, 120, 'User last name: ' + user.last_name)
        canvas.drawString(40, 140, 'Username: ' + user.username)
    canvas.drawString(40, 160, 'Date: ' + str(date.today()))


def BuildPdf(data, user):
    """" Creates PDF file."""
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, bottomup=0)
    makeHeader(p, user)
    textobject = p.beginText()
    textobject.setTextOrigin(40, 250)
    textobject.setFont('Helvetica', 12)
    textobject.textLine('Shopping list:')
    textobject.textLine('')
    for ingredient, inf in data.items():
        textobject.textLine(text=ingredient + ' - '
                            + str(inf[0]) + ' ' + inf[1])

    p.drawText(textobject)
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
