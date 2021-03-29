import io
from datetime import date

from reportlab.pdfgen import canvas

CNT_ON_PAGE = 35


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
    cur_cnt = 0
    sorted_data = sorted(data.items(), key=lambda x: x[0])
    for ingredient, inf in sorted_data:
        textobject.textLine(text=ingredient + ' - '
                            + str(inf[0]) + ' ' + inf[1])
        cur_cnt += 1
        if cur_cnt >= CNT_ON_PAGE:
            p.drawText(textobject)
            textobject = p.beginText()
            textobject.setTextOrigin(40, 100)
            textobject.setFont('Helvetica', 12)
            textobject.textLine('Shopping list:')
            textobject.textLine('')
            p.showPage()
            cur_cnt = 0

    p.drawText(textobject)
    p.showPage()
    p.save()

    buffer.seek(0)
    return buffer
