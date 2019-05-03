from reportlab.pdfgen import canvas
import locale
import calendar
import io
from datetime import datetime, time
from financial.models import Transaction
from congregations.models import Congregation, CongregationRole
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def stringWidth2(pdf, string, font, size, charspace):
    width = pdf.stringWidth(string, font, size)
    width += (len(string) - 1) * charspace
    return width


class TransactionSheetPdf(object):
    def __init__(self, month, balance, congregation_id):
        self.balance = balance
        self.congregation = Congregation.objects.get(pk=congregation_id)
        self.start_date = datetime.combine(month, time.min)
        self.last_day = calendar.monthrange(self.start_date.year, self.start_date.month)[1]
        self.end_date = datetime.combine(self.start_date.replace(day=self.last_day), time.max)
        self.transactions = Transaction.objects.filter(
            date__range=[self.start_date, self.end_date], congregation_id=congregation_id)
        self.stream = io.BytesIO()
        self.pdf = canvas.Canvas(self.stream)
        self.pdf.setTitle('Transaction Sheet')
        self.pdf.setFont("Helvetica", 10)
        self.set_page1()
        self.num_page = 1
        self.sum_r_i = 0
        self.sum_r_o = 0
        self.sum_c_i = 0
        self.sum_c_o = 0

    def set_page1(self):
        self.pdf.drawImage('financial/templates/pdf/S26-1.png', 0, 0, width=600, height=850)

    def set_page2(self):
        self.num_page = 2
        self.pdf.showPage()
        self.pdf.setFont("Helvetica", 10)
        self.pdf.drawImage('financial/templates/pdf/S26-2.png', 0, 0, width=600, height=850)

    def set_sum(self, sum_a, sum_b, sum_c, sum_d, y):
        value = "{0:.2f}".format(sum_a).replace('.', ',')
        x = 318 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_b).replace('.', ',')
        x = 371 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_c).replace('.', ',')
        x = 424 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_d).replace('.', ',')
        x = 474 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
        self.pdf.drawString(x, y, value)

    def generate_header(self):
        self.pdf.drawString(25, 795, self.congregation.name + " / " + self.congregation.circuit)
        self.pdf.drawString(220, 795, self.congregation.city)
        self.pdf.drawString(380, 795, self.congregation.state)
        self.pdf.drawString(450, 795, self.start_date.strftime("%B").upper())
        self.pdf.drawString(545, 795, self.start_date.strftime("%Y"))

    def generate_transactions(self):

        count, sum_a, sum_b, sum_c, sum_d = 0, 0, 0, 0, 0
        page = 1

        y = 729

        for transaction in self.transactions:
            self.pdf.drawString(25, y, transaction.date.strftime("%d"))
            self.pdf.drawString(45, y, transaction.description)
            self.pdf.drawString(253, y, transaction.tc)
            value = transaction.value.replace('.', ',')
            if transaction.tt == 'R':
                x = 317 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
                self.pdf.drawString(x, y, value)
                sum_a += float(transaction.value)
                self.sum_r_i += float(transaction.value)
            if transaction.tt == 'C':
                if transaction.td == "OI":
                    x = 371 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
                    self.pdf.drawString(x, y, value)
                    x = 424 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
                    self.pdf.drawString(x, y, value)
                    sum_b += float(transaction.value)
                    sum_c += float(transaction.value)
                    self.sum_r_o += float(transaction.value)
                    self.sum_c_i += float(transaction.value)
                elif transaction.td == "I":
                    x = 424 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
                    self.pdf.drawString(x, y, value)
                    sum_c += float(transaction.value)
                    self.sum_c_i += float(transaction.value)
                else:
                    x = 474 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
                    self.pdf.drawString(x, y, value)
                    sum_d += float(transaction.value)
                    self.sum_c_o += float(transaction.value)
            y -= 13
            count += 1
            if count == 47:
                page = 2
                self.set_sum(sum_a, sum_b, sum_c, sum_d, 55)
                self.set_page2()
                self.set_sum(sum_a, sum_b, sum_c, sum_d, 763)
                sum_a, sum_b, sum_c, sum_d = 0
                y = 729
        if page == 1:
            self.set_sum(sum_a, sum_b, sum_c, sum_d, 55)
            self.set_page2()
            if count < 47:
                self.set_sum(sum_a, sum_b, sum_c, sum_d, 763)
                self.set_sum(sum_a, sum_b, sum_c, sum_d, 463)
        else:
            self.set_sum(sum_a, sum_b, sum_c, sum_d, 463)

    def generate_confrontation(self):
        self.pdf.drawString(180, 403, self.end_date.strftime('%d de %B de %Y'))

        self.pdf.drawString(148, 350, "{0:.2f}".format(self.sum_r_i).replace('.', ','))
        self.pdf.drawString(148, 337, "{0:.2f}".format(self.sum_r_o).replace('.', ','))
        self.pdf.drawString(235, 324, "{0:.2f}".format(self.sum_r_i - self.sum_r_o).replace('.', ','))

        self.pdf.drawString(148, 270, str(self.balance).replace('.', ','))
        self.pdf.drawString(148, 257, "{0:.2f}".format(self.sum_c_i).replace('.', ','))
        self.pdf.drawString(148, 244, "{0:.2f}".format(self.sum_c_o).replace('.', ','))
        self.pdf.drawString(235, 231, "{0:.2f}".format(
            float(self.balance) + self.sum_c_i - self.sum_c_o).replace('.', ','))

        self.pdf.drawString(235, 110, "{0:.2f}".format(
            float(self.balance) + self.sum_c_i - self.sum_c_o + self.sum_r_i - self.sum_r_o).replace('.', ','))

    def generate(self):
        self.generate_header()
        self.generate_transactions()
        self.generate_confrontation()

    def save(self):
        self.pdf.save()
        ret_pdf = self.stream.getvalue()
        self.stream.close()
        return ret_pdf


class MonthlyReportPdf(object):
    def __init__(self, month, balance, congregation_id):
        self.balance = balance
        self.congregation = Congregation.objects.get(pk=congregation_id)
        account_servant = CongregationRole.objects.filter(
            congregation_id=congregation_id, role="account_servant").first()
        if account_servant:
            self.account_servant_name = account_servant.publisher.full_name
        else:
            self.account_servant_name = ""
        self.start_date = datetime.combine(month, time.min)
        self.last_day = calendar.monthrange(self.start_date.year, self.start_date.month)[1]
        self.end_date = datetime.combine(self.start_date.replace(day=self.last_day), time.max)
        self.transactions = Transaction.objects.filter(
            date__range=[self.start_date, self.end_date], congregation_id=congregation_id).select_related('category')
        self.stream = io.BytesIO()
        self.pdf = canvas.Canvas(self.stream)
        self.pdf.setTitle('Monthly Report')
        self.pdf.setFont("Helvetica", 10)
        self.set_page1()
        self.sum_receipts = 0
        self.sum_expenses = 0
        self.sum_world_wide = 0

    def set_page1(self):
        self.pdf.drawImage('financial/templates/pdf/S30-1.png', 0, 0, width=600, height=850)

    def set_page2(self):
        self.num_page = 2
        self.pdf.showPage()
        self.pdf.setFont("Helvetica", 10)
        self.pdf.drawImage('financial/templates/pdf/S30-2.png', 0, 0, width=600, height=850)

    def set_sum(self, sum_a, sum_b, sum_c, sum_d, y):
        value = "{0:.2f}".format(sum_a).replace('.', ',')
        x = 318 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_b).replace('.', ',')
        x = 371 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_c).replace('.', ',')
        x = 424 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_d).replace('.', ',')
        x = 474 - stringWidth2(self.pdf, value, "Helvetica", 10, 1)
        self.pdf.drawString(x, y, value)

    def generate_header(self):
        self.pdf.drawString(120, 702, self.congregation.name + " / " + self.congregation.circuit)
        self.pdf.drawString(420, 702, self.start_date.strftime("%B").upper() + " / " + self.start_date.strftime("%Y"))
        self.pdf.drawString(490, 617, str(self.balance).replace('.', ','))

    def generate_transactions(self):

        receipt_cats = {}
        expense_cats = {}

        for transaction in self.transactions:
            if transaction.tc in ('C', 'O'):
                if str(transaction.category_id) not in receipt_cats:
                    receipt_cats[str(transaction.category_id)] = {'name': transaction.category.name, 'value': 0}
                receipt_cats[str(transaction.category_id)]['value'] += float(transaction.value)
                self.sum_receipts += float(transaction.value)
                if transaction.tc == "O":
                    self.sum_world_wide += float(transaction.value)
            elif transaction.tc == 'D':
                if str(transaction.category_id) not in expense_cats:
                    expense_cats[str(transaction.category_id)] = {'name': transaction.category.name, 'value': 0}
                expense_cats[str(transaction.category_id)]['value'] += float(transaction.value)
                self.sum_expenses += float(transaction.value)
        y = 553
        for key, value in receipt_cats.items():
            self.pdf.drawString(60, y, value['name'])
            self.pdf.drawString(300, y, "{0:.2f}".format(value['value']).replace('.', ','))
            y -= 15

        self.pdf.drawString(390, 480, "{0:.2f}".format(self.sum_receipts).replace('.', ','))

        y = 430
        for key, value in expense_cats.items():
            self.pdf.drawString(60, y, value['name'])
            self.pdf.drawString(300, y, "{0:.2f}".format(value['value']).replace('.', ','))
            y -= 15

        self.pdf.drawString(390, 285, "{0:.2f}".format(self.sum_expenses).replace('.', ','))

        self.pdf.drawString(490, 265, "{0:.2f}".format(self.sum_receipts - self.sum_expenses).replace('.', ','))

        self.pdf.drawString(490, 247, "{0:.2f}".format(
            float(self.balance) + self.sum_receipts - self.sum_expenses).replace('.', ','))

        self.pdf.drawString(490, 105, "{0:.2f}".format(
            float(self.balance) + self.sum_receipts - self.sum_expenses).replace('.', ','))

    def generate_confrontation(self):
        self.pdf.drawString(490, 767, str(self.balance).replace('.', ','))

        self.pdf.drawString(300, 717, "{0:.2f}".format(self.sum_receipts).replace('.', ','))
        self.pdf.drawString(300, 681, "{0:.2f}".format(self.sum_world_wide).replace('.', ','))
        self.pdf.drawString(390, 628, "{0:.2f}".format(self.sum_receipts).replace('.', ','))

        self.pdf.drawString(300, 578, "{0:.2f}".format(self.sum_expenses).replace('.', ','))
        self.pdf.drawString(300, 540, "{0:.2f}".format(self.sum_world_wide).replace('.', ','))
        self.pdf.drawString(390, 503, "{0:.2f}".format(self.sum_expenses).replace('.', ','))

        self.pdf.drawString(487, 450, "{0:.2f}".format(
            float(self.balance) + self.sum_receipts - self.sum_expenses).replace('.', ','))
        self.pdf.drawString(400, 410, self.account_servant_name)

    def generante_announcement(self):
        self.pdf.drawString(140, 251, self.start_date.strftime("%B").upper())
        self.pdf.drawString(395, 251, "{0:.2f}".format(self.sum_receipts).replace('.', ','))
        self.pdf.drawString(230, 221, "{0:.2f}".format(self.sum_expenses).replace('.', ','))
        self.pdf.drawString(490, 221, "{0:.2f}".format(
            float(self.balance) + self.sum_receipts - self.sum_expenses).replace('.', ','))
        self.pdf.drawString(180, 160, "{0:.2f}".format(self.sum_world_wide).replace('.', ','))

    def generate(self):
        self.generate_header()
        self.generate_transactions()
        self.set_page2()
        self.generate_confrontation()
        self.generante_announcement()

    def save(self):
        self.pdf.save()
        ret_pdf = self.stream.getvalue()
        self.stream.close()
        return ret_pdf
