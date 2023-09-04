import io
from reportlab.pdfgen import canvas
from bson.objectid import ObjectId


def get_page_body(boxes):
    for box in boxes:
        if box.element_tag == 'body':
            return box

        return get_page_body(box.all_children())


class DesignationsSheetPdf(object):
    def __init__(self, meetings):
        self.meetings = meetings
        self.stream = io.BytesIO()
        self.pdf = canvas.Canvas(self.stream)
        self.pdf.setTitle('Designations')
        self.pdf.setFont("Roboto", 7)
        self.set_page1()

    def set_page1(self):
        self.pdf.drawImage('meetings/templates/pdf/S-89_s-Mlt_T-1.png',
                           0, 0, width=600, height=850)
    
    def add_page(self):
        self.pdf.showPage()
        self.set_page1()
    
    def generate(self):
        count = 0
        data = self.generate_data()
        
        for d in data:
            if count > 0 and count % 4 == 0:
                self.add_page()
                count = 0
            if count == 0:
                self.pdf.setFont("Roboto", 11)
                self.pdf.drawString(80, 760, d["name"])
                if d["assistant"]:
                    self.pdf.drawString(98, 737, d["assistant"])
                self.pdf.drawString(75, 712, d["date"])
                self.pdf.setFont("Roboto", 8)
                if d["designation"] == "revisit":
                    self.pdf.drawString(54, 630, "X")
                    if d["description"]:
                        self.pdf.drawString(70, 622, d["description"])
                elif d["designation"] == "conversation":
                    self.pdf.drawString(54, 653, "X")
                    if d["description"]:
                        self.pdf.drawString(70, 643, d["description"])
                elif d["designation"] == "study":
                    self.pdf.drawString(170, 663, "X")
                elif d["designation"] == "speech":
                    self.pdf.drawString(170, 653, "X")
                elif d["designation"] == "reading":
                    self.pdf.drawString(54, 663, "X")
                elif d["designation"] == "other":
                    self.pdf.drawString(170, 641, "X")
                    if d["description"]:
                        self.pdf.drawString(212, 644, d["description"])

                if d["room"] == "A":
                    self.pdf.drawString(54, 589, "X")
                elif d["room"] == "B":
                    self.pdf.drawString(54, 578, "X")
                elif d["room"] == "C":
                    self.pdf.drawString(54, 568, "X")
            elif count == 1:
                self.pdf.setFont("Roboto", 11)
                self.pdf.drawString(380, 760, d["name"])
                if d["assistant"]:
                    self.pdf.drawString(398, 737, d["assistant"])
                self.pdf.drawString(375, 712, d["date"])
                self.pdf.setFont("Roboto", 8)
                if d["designation"] == "revisit":
                    self.pdf.drawString(354, 630, "X")
                    if d["description"]:
                        self.pdf.drawString(370, 622, d["description"])
                elif d["designation"] == "conversation":
                    self.pdf.drawString(354, 653, "X")
                    if d["description"]:
                        self.pdf.drawString(370, 643, d["description"])
                elif d["designation"] == "study":
                    self.pdf.drawString(470, 663, "X")
                elif d["designation"] == "speech":
                    self.pdf.drawString(470, 653, "X")
                elif d["designation"] == "reading":
                    self.pdf.drawString(354, 663, "X")
                elif d["designation"] == "other":
                    self.pdf.drawString(470, 641, "X")
                    if d["description"]:
                        self.pdf.drawString(512, 644, d["description"])

                if d["room"] == "A":
                    self.pdf.drawString(354, 589, "X")
                elif d["room"] == "B":
                    self.pdf.drawString(354, 578, "X")
                elif d["room"] == "C":
                    self.pdf.drawString(354, 568, "X")
            elif count == 2:
                self.pdf.setFont("Roboto", 11)
                self.pdf.drawString(80, 335, d["name"])
                if d["assistant"]:
                    self.pdf.drawString(98, 312, d["assistant"])
                self.pdf.drawString(75, 287, d["date"])
                self.pdf.setFont("Roboto", 8)
                if d["designation"] == "revisit":
                    self.pdf.drawString(54, 205, "X")
                    if d["description"]:
                        self.pdf.drawString(70, 197, d["description"])
                elif d["designation"] == "conversation":
                    self.pdf.drawString(54, 228, "X")
                    if d["description"]:
                        self.pdf.drawString(70, 218, d["description"])
                elif d["designation"] == "study":
                    self.pdf.drawString(170, 238, "X")
                elif d["designation"] == "speech":
                    self.pdf.drawString(170, 228, "X")
                elif d["designation"] == "reading":
                    self.pdf.drawString(54, 238, "X")
                elif d["designation"] == "other":
                    self.pdf.drawString(170, 216, "X")
                    if d["description"]:
                        self.pdf.drawString(212, 219, d["description"])

                if d["room"] == "A":
                    self.pdf.drawString(54, 164, "X")
                elif d["room"] == "B":
                    self.pdf.drawString(54, 153, "X")
                elif d["room"] == "C":
                    self.pdf.drawString(54, 143, "X")
            elif count == 3:
                self.pdf.setFont("Roboto", 11)
                self.pdf.drawString(380, 335, d["name"])
                if d["assistant"]:
                    self.pdf.drawString(398, 312, d["assistant"])
                self.pdf.drawString(375, 287, d["date"])
                self.pdf.setFont("Roboto", 8)
                if d["designation"] == "revisit":
                    self.pdf.drawString(354, 205, "X")
                    if d["description"]:
                        self.pdf.drawString(370, 197, d["description"])
                elif d["designation"] == "conversation":
                    self.pdf.drawString(354, 653, "X")
                    if d["description"]:
                        self.pdf.drawString(370, 228, d["description"])
                elif d["designation"] == "study":
                    self.pdf.drawString(470, 238, "X")
                elif d["designation"] == "speech":
                    self.pdf.drawString(470, 228, "X")
                elif d["designation"] == "reading":
                    self.pdf.drawString(354, 238, "X")
                elif d["designation"] == "other":
                    self.pdf.drawString(470, 216, "X")
                    if d["description"]:
                        self.pdf.drawString(512, 219, d["description"])

                if d["room"] == "A":
                    self.pdf.drawString(354, 164, "X")
                elif d["room"] == "B":
                    self.pdf.drawString(354, 153, "X")
                elif d["room"] == "C":
                    self.pdf.drawString(354, 143, "X")
            count += 1
    
    def generate_data(self):
        data = []
        for meeting in self.meetings:
            for t in meeting.midweek_content.treasures:
                if t.reading and t.person_treasure:
                    data.append({
                        "name": str(t.person_treasure),
                        "assistant": "",
                        "date": meeting.date.strftime("%d/%m/%Y"),
                        "designation": "reading",
                        "room": t.room_treasure
                    })
            for a in meeting.midweek_content.apply_yourself:
                if a.student:
                    data.append({
                        "name": str(a.student),
                        "assistant": str(a.assistant) if a.assistant else "",
                        "date": meeting.date.strftime("%d/%m/%Y"),
                        "designation": self.get_apply_designation(a.title_apply),
                        "description": self.get_apply_description(a.title_apply),
                        "room": a.room_apply
                    })
        return data

    def get_apply_designation(self, value):
        if "revisita" in value.lower():
            return "revisit"
        elif "discurso" in value.lower():
            return "speech"
        elif "conversa" in value.lower():
            return "conversation"
        elif "estudo" in value.lower():
            return "study"
        else:
            return "other"
    
    def get_apply_description(self, value):
        if "revisita" in value.lower():
            if "—" in value:
                return value.split("—")[1].strip()
            return ""
        elif "discurso" in value.lower():
            return ""
        elif "conversa" in value.lower():
            if "—" in value:
                return value.split("—")[1].strip()
            return ""
        elif "estudo" in value.lower():
            return ""
        else:
            return value

    def save(self):
        self.pdf.save()
        ret_pdf = self.stream.getvalue()
        self.stream.close()
        return ret_pdf

def get_names(publishers, ids):
    names = []
    for p_id in ids:
        for p in publishers:
            if p._id == ObjectId(p_id):
                names.append(p.name)
    return names