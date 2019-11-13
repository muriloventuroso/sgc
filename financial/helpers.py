from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import locale
import calendar
import io
from django.utils.translation import ugettext_lazy as _
from datetime import datetime, time
from dateutil.relativedelta import relativedelta
from financial.models import Transaction, MonthlySummary, TransactionContent
from congregations.models import Congregation, CongregationRole
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
pdfmetrics.registerFont(TTFont('Roboto', 'static/fonts/RobotoSlab-Regular.ttf'))
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'
DEFAULT_EXPENSES = [
    '5cbdaa89b9c49b000c671da8', '5ccc447cc75dbf6e6bb40a9d', '5ccc447cc75dbf6e6bb40a9d', '5d94edcec75dbf593d8a886f',
    '5ccc4130c75dbf6b6f2ab1ca'
]


def stringWidth2(pdf, string, font, size, charspace):
    width = pdf.stringWidth(string, font, size)
    width += (len(string) - 1) * charspace
    return width


class TransactionSheetPdf(object):
    def __init__(self, month, balance, congregation_id, checks=[], data_off={}):
        self.balance = balance
        self.checks = checks
        self.data_off = data_off
        self.congregation = Congregation.objects.get(pk=congregation_id)
        self.start_date = datetime.combine(month, time.min)
        self.last_day = calendar.monthrange(self.start_date.year, self.start_date.month)[1]
        self.end_date = datetime.combine(self.start_date.replace(day=self.last_day), time.max)
        if not self.balance:
            summary = MonthlySummary.objects.filter(
                congregation_id=congregation_id,
                date__range=[
                    self.start_date - relativedelta(months=1),
                    self.end_date - relativedelta(months=1)]).first()
            if summary:
                self.balance = summary.final_balance
        self.transactions = Transaction.objects.filter(
            date__range=[self.start_date, self.end_date], congregation_id=congregation_id, hide_from_sheet=False)
        self.stream = io.BytesIO()
        self.pdf = canvas.Canvas(self.stream)
        self.pdf.setTitle('Transaction Sheet')
        self.pdf.setFont("Roboto", 7)
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
        self.pdf.setFont("Roboto", 7)
        self.pdf.drawImage('financial/templates/pdf/S26-2.png', 0, 0, width=600, height=850)

    def set_sum(self, sum_a, sum_b, sum_c, sum_d, y):
        self.pdf.setFont("Roboto", 9)
        value = "{0:.2f}".format(sum_a).replace('.', ',')
        x = 318 - stringWidth2(self.pdf, value, "Roboto", 9, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_b).replace('.', ',')
        x = 371 - stringWidth2(self.pdf, value, "Roboto", 9, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_c).replace('.', ',')
        x = 424 - stringWidth2(self.pdf, value, "Roboto", 9, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_d).replace('.', ',')
        x = 474 - stringWidth2(self.pdf, value, "Roboto", 9, 1)
        self.pdf.drawString(x, y, value)

    def generate_header(self):
        self.pdf.setFont("Roboto", 11)
        self.pdf.drawString(25, 795, self.congregation.name + " / " + self.congregation.circuit)
        self.pdf.drawString(220, 795, self.congregation.city)
        self.pdf.drawString(380, 795, self.congregation.state)
        self.pdf.drawString(450, 795, self.start_date.strftime("%B").upper())
        self.pdf.drawString(545, 795, self.start_date.strftime("%Y"))

    def generate_transactions(self):

        count, sum_a, sum_b, sum_c, sum_d = 0, 0, 0, 0, 0

        y = 729.0

        for transaction in self.transactions:
            self.pdf.setFont("Roboto", 9)
            self.pdf.drawString(25, y, transaction.date.strftime("%d"))
            self.pdf.setFont("Roboto", 7)
            self.pdf.drawString(45, y, transaction.description)
            self.pdf.setFont("Roboto", 9)
            self.pdf.drawString(253, y, transaction.tc)
            value = "%.2f" % transaction.value
            value = value.replace('.', ',')
            if transaction.tt == 'R':
                if transaction.td == "I":
                    x = 316 - stringWidth2(self.pdf, value, "Roboto", 9, 1)
                    self.pdf.drawString(x, y, value)
                    sum_a += float(transaction.value)
                    self.sum_r_i += float(transaction.value)
                else:
                    x = 369 - stringWidth2(self.pdf, value, "Roboto", 9, 1)
                    self.pdf.drawString(x, y, value)
                    sum_b += float(transaction.value)
                    self.sum_r_o += float(transaction.value)
            if transaction.tt == 'C':
                if transaction.td == "OI":
                    x = 369 - stringWidth2(self.pdf, value, "Roboto", 9, 1)
                    self.pdf.drawString(x, y, value)
                    x = 421 - stringWidth2(self.pdf, value, "Roboto", 9, 1)
                    self.pdf.drawString(x, y, value)
                    sum_b += float(transaction.value)
                    sum_c += float(transaction.value)
                    self.sum_r_o += float(transaction.value)
                    self.sum_c_i += float(transaction.value)
                elif transaction.td == "I":
                    x = 422 - stringWidth2(self.pdf, value, "Roboto", 9, 1)
                    self.pdf.drawString(x, y, value)
                    sum_c += float(transaction.value)
                    self.sum_c_i += float(transaction.value)
                else:
                    x = 473 - stringWidth2(self.pdf, value, "Roboto", 9, 1)
                    self.pdf.drawString(x, y, value)
                    sum_d += float(transaction.value)
                    self.sum_c_o += float(transaction.value)
            for sub_transaction in transaction.sub_transactions:
                y -= 12.8
                count += 1
                self.pdf.setFont("Roboto", 7)
                self.pdf.drawString(50, y, sub_transaction.description)
                sub_value = ' [' + "%.2f" % sub_transaction.value + ']'
                x = 253 - stringWidth2(self.pdf, sub_value, "Roboto", 7, 1)
                self.pdf.drawString(x, y, sub_value)
                self.pdf.setFont("Roboto", 9)
                self.pdf.drawString(253, y, sub_transaction.tc)
                if count == 51:
                    self.set_sum(sum_a, sum_b, sum_c, sum_d, 55)
                    self.pdf.showPage()
                    self.set_page1()
                    y = 729
                    self.pdf.setFont("Roboto", 7)
                    self.pdf.drawString(50, y, "Totais da primeira folha")
                    self.pdf.setFont("Roboto", 9)
                    self.set_sum(sum_a, sum_b, sum_c, sum_d, y)
            y -= 12.8
            count += 1
            if count == 52:
                self.set_sum(sum_a, sum_b, sum_c, sum_d, 55)
                self.pdf.showPage()
                self.set_page1()
                y = 729
                self.pdf.setFont("Roboto", 7)
                self.pdf.drawString(50, y, "Totais da primeira folha")
                self.pdf.setFont("Roboto", 9)
                self.set_sum(sum_a, sum_b, sum_c, sum_d, y)
        self.set_sum(sum_a, sum_b, sum_c, sum_d, 55)
        self.set_page2()

    def generate_confrontation(self):
        self.pdf.setFont("Roboto", 10)
        self.pdf.drawString(300, 772, datetime.now().strftime('%d de %B de %Y'))

        item1 = float(self.balance) + self.sum_c_i - self.sum_c_o + self.sum_r_i - self.sum_r_o

        self.pdf.setFont("Roboto", 9)
        self.pdf.drawString(250, 730, "{0:.2f}".format(item1).replace('.', ','))
        item2 = 0.0
        if 'deposits' in self.data_off and self.data_off["deposits"]:
            item2 = float(self.data_off["deposits"])
            self.pdf.drawString(250, 705, "{0:.2f}".format(item2).replace('.', ','))
        item3 = 0.0
        if 'bank_fees' in self.data_off and self.data_off["bank_fees"]:
            item3 = float(self.data_off["bank_fees"])
            self.pdf.drawString(250, 690, "{0:.2f}".format(item3).replace('.', ','))
        item4 = item1 + item2 + item3
        self.pdf.drawString(250, 676, "{0:.2f}".format(item4).replace('.', ','))

        y = 621
        item6 = 0.0
        self.pdf.setFont("Roboto", 8)
        for check in self.checks:
            self.pdf.drawString(35, y, check["n_confirmation"])
            self.pdf.drawString(190, y, "{0:.2f}".format(float(check["value"])).replace('.', ','))
            item6 += float(check["value"])
            y -= 15
        self.pdf.setFont("Roboto", 10)
        if item6:
            self.pdf.drawString(250, 498, "{0:.2f}".format(item6).replace('.', ','))
        item7 = 0.0
        if 'bank_interest' in self.data_off and self.data_off["bank_interest"]:
            item7 = float(self.data_off["bank_interest"])
            self.pdf.drawString(250, 483, "{0:.2f}".format(item7).replace('.', ','))

        item8 = 0.0
        if 'eletronic' in self.data_off and self.data_off["eletronic"]:
            item8 = float(self.data_off["eletronic"])
            self.pdf.drawString(250, 457, "{0:.2f}".format(item8).replace('.', ','))

        sum_off = item6 + item7 + item8

        item9 = item4 - sum_off

        self.pdf.drawString(250, 434, "{0:.2f}".format(item9).replace('.', ','))

        self.pdf.drawString(170, 357, self.end_date.strftime('%d de %B de %Y'))
        self.pdf.drawString(190, 320, "0,00")
        self.pdf.drawString(190, 305, "{0:.2f}".format(self.sum_r_i).replace('.', ','))
        self.pdf.drawString(190, 290, "{0:.2f}".format(self.sum_r_o).replace('.', ','))
        self.pdf.drawString(250, 275, "{0:.2f}".format(self.sum_r_i - self.sum_r_o).replace('.', ','))

        self.pdf.drawString(190, 238, str(self.balance).replace('.', ','))
        self.pdf.drawString(190, 223, "{0:.2f}".format(self.sum_c_i - sum_off).replace('.', ','))
        self.pdf.drawString(190, 208, "{0:.2f}".format(self.sum_c_o).replace('.', ','))
        self.pdf.drawString(250, 190, "{0:.2f}".format(
            float(self.balance) + self.sum_c_i - self.sum_c_o - sum_off).replace('.', ','))

        self.pdf.drawString(250, 88, "{0:.2f}".format(
            float(self.balance) + self.sum_c_i - self.sum_c_o + self.sum_r_i - self.sum_r_o - sum_off
        ).replace('.', ','))

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
        self.month = month
        self.balance = balance
        self.congregation_id = congregation_id
        self.start_date = datetime.combine(month, time.min)
        self.last_day = calendar.monthrange(self.start_date.year, self.start_date.month)[1]
        self.end_date = datetime.combine(self.start_date.replace(day=self.last_day), time.max)
        if not self.balance:
            summary = MonthlySummary.objects.filter(
                congregation_id=congregation_id,
                date__range=[
                    self.start_date - relativedelta(months=1),
                    self.end_date - relativedelta(months=1)]).first()
            if summary:
                self.balance = summary.final_balance
        self.congregation = Congregation.objects.get(pk=congregation_id)
        account_servant = CongregationRole.objects.filter(
            congregation_id=congregation_id, role="account_servant").first()
        if account_servant:
            self.account_servant_name = account_servant.publisher.full_name
        else:
            self.account_servant_name = ""

        self.transactions = Transaction.objects.filter(
            date__range=[self.start_date, self.end_date], congregation_id=congregation_id).select_related('category')
        self.stream = io.BytesIO()
        self.pdf = canvas.Canvas(self.stream)
        self.pdf.setTitle('Monthly Report')
        self.pdf.setFont("Roboto", 10)
        self.set_page1()
        self.sum_receipts = 0
        self.sum_receipts_eletronic = 0
        self.sum_expenses = 0
        self.sum_world_wide = 0
        self.sum_specific_objective = 0
        self.sum_construction_subsidiary = 0
        self.a, self.b, self.c, self.d, self.e, self.f, self.g, self.h, self.i = 0, 0, 0, 0, 0, 0, 0, 0, 0

    def set_page1(self):
        self.pdf.drawImage('financial/templates/pdf/S30-1.png', 0, 0, width=600, height=850)

    def set_page2(self):
        self.num_page = 2
        self.pdf.showPage()
        self.pdf.setFont("Roboto", 7)
        self.pdf.drawImage('financial/templates/pdf/S30-2.png', 0, 0, width=600, height=850)

    def set_sum(self, sum_a, sum_b, sum_c, sum_d, y):
        value = "{0:.2f}".format(sum_a).replace('.', ',')
        x = 318 - stringWidth2(self.pdf, value, "Roboto", 7, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_b).replace('.', ',')
        x = 371 - stringWidth2(self.pdf, value, "Roboto", 7, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_c).replace('.', ',')
        x = 424 - stringWidth2(self.pdf, value, "Roboto", 7, 1)
        self.pdf.drawString(x, y, value)

        value = "{0:.2f}".format(sum_d).replace('.', ',')
        x = 474 - stringWidth2(self.pdf, value, "Roboto", 7, 1)
        self.pdf.drawString(x, y, value)

    def generate_header(self):
        self.pdf.setFont("Roboto", 11)
        self.pdf.drawString(120, 706, self.congregation.name + " / " + self.congregation.circuit)
        self.pdf.drawString(420, 706, self.start_date.strftime("%B").upper() + " / " + self.start_date.strftime("%Y"))
        self.pdf.drawString(494, 688, str(self.balance).replace('.', ','))

    def generate_transactions(self):
        self.pdf.setFont("Roboto", 10)
        receipt_cats = {}
        expense_cats = {}

        self.a = float(self.balance)

        for transaction in self.transactions:
            if transaction.tc in ('C', 'O', 'F', 'CE', 'OE'):
                if transaction.category_id:
                    if str(transaction.category_id) not in receipt_cats:
                        receipt_cats[str(transaction.category_id)] = {'name': transaction.category.name, 'value': 0}
                    if transaction.tc == "C":
                        receipt_cats[str(transaction.category_id)]['value'] += float(transaction.value)
                if transaction.tc == "O":
                    self.sum_world_wide += float(transaction.value)
                elif transaction.tc == "F":
                    self.sum_construction_subsidiary += float(transaction.value)
                elif transaction.tc == "C":
                    self.sum_receipts += float(transaction.value)
                elif transaction.tc == "CE":
                    self.sum_receipts_eletronic += float(transaction.value)
                elif transaction.tc == "OE":
                    self.sum_specific_objective += float(transaction.value)
            elif transaction.tc == 'G':
                if transaction.category_id:
                    if str(transaction.category_id) not in expense_cats:
                        expense_cats[str(transaction.category_id)] = {'name': transaction.category.name, 'value': 0}
                    expense_cats[str(transaction.category_id)]['value'] += float(transaction.value)
                self.sum_expenses += float(transaction.value)
            for sub_transaction in transaction.sub_transactions:
                if sub_transaction.tc == 'G':
                    if sub_transaction.category_id:
                        if str(sub_transaction.category_id) not in expense_cats:
                            expense_cats[str(sub_transaction.category_id)] = {
                                'name': sub_transaction.category.name, 'value': 0}
                        expense_cats[str(sub_transaction.category_id)]['value'] += float(sub_transaction.value)
                    self.sum_expenses += float(sub_transaction.value)
        self.pdf.drawString(355, 633, "{0:.2f}".format(self.sum_receipts).replace('.', ','))
        self.pdf.drawString(355, 618, "{0:.2f}".format(self.sum_receipts_eletronic).replace('.', ','))
        y = 603
        for key, value in receipt_cats.items():
            self.pdf.drawString(60, y, value['name'])
            self.pdf.drawString(355, y, "{0:.2f}".format(value['value']).replace('.', ','))
            y -= 15
        self.b = self.sum_receipts + self.sum_receipts_eletronic + self.sum_specific_objective
        self.pdf.drawString(420, 577, "{0:.2f}".format(self.b).replace('.', ','))

        self.pdf.drawString(355, 545, "{0:.2f}".format(self.sum_world_wide).replace('.', ','))
        self.pdf.drawString(59, 529, str(_("Donates to Construction of the Subsidiary")))
        self.pdf.drawString(355, 530, "{0:.2f}".format(self.sum_construction_subsidiary).replace('.', ','))
        self.c = self.sum_world_wide + self.sum_construction_subsidiary
        self.pdf.drawString(420, 498, "{0:.2f}".format(self.c).replace('.', ','))
        self.d = self.b + self.c
        self.pdf.drawString(494, 482, "{0:.2f}".format(self.d).replace('.', ','))

        if '5cbdaa89b9c49b000c671da8' in expense_cats:
            self.pdf.drawString(355, 431, "{0:.2f}".format(
                expense_cats['5cbdaa89b9c49b000c671da8']['value']).replace('.', ','))
        if '5d94f8afc75dbf5bb53000c7' in expense_cats:
            self.pdf.drawString(355, 416, "{0:.2f}".format(
                expense_cats['5d94f8afc75dbf5bb53000c7']['value']).replace('.', ','))
        if '5ccc447cc75dbf6e6bb40a9d' in expense_cats:
            self.pdf.drawString(355, 390, "{0:.2f}".format(
                expense_cats['5ccc447cc75dbf6e6bb40a9d']['value']).replace('.', ','))
        if '5d94edcec75dbf593d8a886f' in expense_cats:
            self.pdf.drawString(355, 375, "{0:.2f}".format(
                expense_cats['5d94edcec75dbf593d8a886f']['value']).replace('.', ','))
        if '5ccc4130c75dbf6b6f2ab1ca' in expense_cats:
            self.pdf.drawString(355, 348, "{0:.2f}".format(
                expense_cats['5ccc4130c75dbf6b6f2ab1ca']['value']).replace('.', ','))
        y = 333
        for key, value in expense_cats.items():
            if key in DEFAULT_EXPENSES:
                continue
            self.pdf.drawString(60, y, value['name'])
            self.pdf.drawString(355, y, "{0:.2f}".format(value['value']).replace('.', ','))
            y -= 15
        self.e = self.sum_expenses
        self.pdf.drawString(420, 305, "{0:.2f}".format(self.e).replace('.', ','))

        self.pdf.drawString(355, 278, "{0:.2f}".format(self.sum_world_wide).replace('.', ','))
        self.pdf.drawString(59, 263, str(_("Donates to Construction of the Subsidiary")))
        self.pdf.drawString(355, 263, "{0:.2f}".format(self.sum_construction_subsidiary).replace('.', ','))
        self.f = self.sum_world_wide + self.sum_construction_subsidiary

        self.pdf.drawString(420, 235, "{0:.2f}".format(self.f).replace('.', ','))

        self.g = self.e + self.f

        self.pdf.drawString(492, 222, "{0:.2f}".format(self.g).replace('.', ','))

        self.h = self.d - self.g

        self.pdf.drawString(492, 205, "{0:.2f}".format(self.h).replace('.', ','))
        self.i = self.a + self.h

        self.pdf.drawString(492, 185, "{0:.2f}".format(self.i).replace('.', ','))

        self.pdf.drawString(492, 95, "{0:.2f}".format(self.i).replace('.', ','))
        self.pdf.setFont("Roboto", 11)
        self.pdf.drawString(300, 70, self.account_servant_name)

    def generante_announcement(self):
        self.pdf.setFont("Roboto", 11)
        self.pdf.drawString(150, 681, self.start_date.strftime("%B").upper())
        self.pdf.drawString(495, 681, "{0:.2f}".format(self.b).replace('.', ','))
        self.pdf.drawString(360, 650, "{0:.2f}".format(self.e).replace('.', ','))
        self.pdf.drawString(125, 617, "{0:.2f}".format(self.i).replace('.', ','))
        self.pdf.drawString(490, 617, "{0:.2f}".format(self.f).replace('.', ','))

    def generate_summary(self):
        transactions = []
        transactions_tc = {}
        for transaction in self.transactions:
            tc = transaction.tc
            if tc:
                if tc not in transactions_tc:
                    transactions_tc[tc] = TransactionContent(tc=tc, count=0, value=0)
                transactions_tc[tc].count += 1
                transactions_tc[tc].value += float(transaction.value)
            for sub_transaction in transaction.sub_transactions:
                tc = sub_transaction.tc
                if tc:
                    if tc not in transactions_tc:
                        transactions_tc[tc] = TransactionContent(tc=tc, count=0, value=0)
                    transactions_tc[tc].count += 1
                    transactions_tc[tc].value += float(sub_transaction.value)
        for key, value in transactions_tc.items():
            transactions.append(value)
        summary = MonthlySummary.objects.filter(
            congregation_id=self.congregation_id, date__range=[self.start_date, self.end_date]).first()
        if not summary:
            summary = MonthlySummary(congregation_id=self.congregation_id)
        summary.date = datetime.now().replace(month=self.start_date.month)
        summary.carried_balance = float(self.balance)
        summary.final_balance = float(float(self.balance) + self.sum_receipts - self.sum_expenses)
        summary.transactions = transactions
        summary.save()

    def generate(self):
        self.generate_header()
        self.generate_transactions()
        self.set_page2()
        self.generante_announcement()
        self.generate_summary()

    def save(self):
        self.pdf.save()
        ret_pdf = self.stream.getvalue()
        self.stream.close()
        return ret_pdf
