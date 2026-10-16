from pathlib import Path
import subprocess, sys, urllib.request
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether

ROOT=Path(__file__).resolve().parent; FONT_DIR=ROOT/'fonts'; OUT=ROOT/'output_pdf'
FONT_DIR.mkdir(exist_ok=True); OUT.mkdir(exist_ok=True)
FONTS={
 'AnthropicLight':'AnthropicSerif-Text-Light-Static',
 'AnthropicRegular':'AnthropicSerif-Text-Regular-Static',
 'AnthropicSemibold':'AnthropicSerif-Text-Semibold-Static'}
BASE_URL='https://pnhouse.it/assets/fonts/'

def setup_fonts():
    for alias,stem in FONTS.items():
        otf=FONT_DIR/f'{stem}.otf'; ttf=FONT_DIR/f'{stem}.ttf'
        if not otf.exists() or otf.stat().st_size < 10000:
            print(f'Download {otf.name}...'); urllib.request.urlretrieve(BASE_URL+otf.name,otf)
        if not ttf.exists() or ttf.stat().st_mtime < otf.stat().st_mtime:
            print(f'Conversione {otf.name} -> {ttf.name}...')
            script=f'Open("{otf}"); Generate("{ttf}"); Quit();'
            subprocess.run(['fontforge','-lang=ff','-c',script],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
        pdfmetrics.registerFont(TTFont(alias,str(ttf)))

PINE=HexColor('#21372E'); DARK=HexColor('#17241E'); CREAM=HexColor('#F5F0E7'); SAND=HexColor('#D8C3A5'); RUST=HexColor('#9A6647'); INK=HexColor('#20231F'); MUTED=HexColor('#66736C'); WHITE=colors.white
NAMES=['Carsulae','Cascata delle Marmore','Lago di Piediluco','Narni e Narni Sotterranea','Le Mole di Narni','Cisterne Romane di Amelia e tour della città','Montefalco','Todi','Spoleto','Assisi','Orvieto','Civita di Bagnoregio','Ponte Tibetano di Sellano','Perugia','Foligno','Norcia','Cascia','Roma']
DISTS=['4,3 km','15,6 km','19,1 km','9,5 km','circa 14 km','circa 25 km','33,2 km','22,4 km','21,9 km','52,3 km','37,1 km','34,8 km','44,7 km','57,8 km','41,2 km','50,2 km','41,2 km','78,0 km']
URLS=['https://carsulae.info/','https://cascatadellemarmore.info/','https://www.umbriatourism.it/it/w/lago-di-piediluco','https://www.narnisotterranea.it/','https://lemole.it/','https://ameliamusei.it/cisterna-romana/','https://www.montefalco.it/','https://www.google.com/maps/search/?api=1&query=Todi%20PG','https://www.google.com/maps/search/?api=1&query=Spoleto%20PG','https://www.google.com/maps/search/?api=1&query=Assisi%20PG','https://www.duomodiorvieto.it/','https://www.civita-di-bagnoregio.info/','https://www.visitsellano.info/it/scopri-sellano/il-ponte-tibetano','https://www.google.com/maps/search/?api=1&query=Perugia%20centro%20storico','https://www.google.com/maps/search/?api=1&query=Foligno%20centro%20storico','https://www.umbriatourism.it/it/valnerina-cascia','https://www.umbriatourism.it/it/valnerina-cascia','https://www.google.com/maps/search/?api=1&query=Colosseo%20Roma']
TYPES=['Archeologia','Natura','Natura e paesaggio','Borgo e storia','Natura','Archeologia e borgo','Borgo, arte e Sagrantino','Borgo','Arte e cultura','Arte e spiritualità','Arte e cultura','Borgo','Avventura','Capoluogo, arte e storia','Città d’arte','Valnerina e tradizioni','Spiritualità e Valnerina','Città eterna']
DESC=['Antica città romana immersa nel paesaggio umbro, ideale per una visita tra storia e natura.','Uno dei simboli dell’Umbria: sentieri, belvedere e la spettacolare caduta delle acque.','Borgo affacciato sul lago, perfetto per una passeggiata e una sosta panoramica.','Centro medievale e ambienti sotterranei da scoprire con visita guidata.','Acque turchesi e paesaggio fluviale lungo il Nera, una meta suggestiva all’aperto.','Complesso idraulico romano sotto Piazza Matteotti, da abbinare al tour culturale della città.','Un balcone sull’Umbria, celebre per il centro storico, l’arte e il Sagrantino.','Elegante città collinare raccolta intorno a Piazza del Popolo.','Rocca, Ponte delle Torri, vicoli e piazze in una delle principali città d’arte umbre.','La città di San Francesco, con la Basilica e panorami sulla valle umbra.','Il Duomo, il tufo e la città sotterranea rendono Orvieto una tappa di grande fascino.','Spettacolare borgo arroccato raggiungibile dal celebre ponte pedonale.','Esperienza panoramica e adrenalinica nel paesaggio della Valnerina.','Palazzi, musei, scorci medievali e atmosfera vivace nel capoluogo umbro.','Piazze e palazzi nel centro della valle umbra, comoda base per esplorare.','Borgo della Valnerina noto per il paesaggio montano e le tradizioni gastronomiche.','Meta spirituale legata a Santa Rita, circondata dai paesaggi della Valnerina.','Possibile escursione giornaliera verso il patrimonio storico e artistico della Capitale.']
LANG={
'IT':('Esplora i dintorni','Borghi, natura, archeologia e città d’arte<br/>a partire da San Gemini','Apri informazioni e indicazioni','Prima di partire','Una guida pensata per gli ospiti','GUIDA ESPLORA'),
'EN':('Explore the surroundings','Villages, nature, archaeology and art cities<br/>from San Gemini','Open information and directions','Before you leave','A guide created for our guests','EXPLORE GUIDE'),
'FR':('Explorez les environs','Villages, nature, archéologie et villes d’art<br/>au départ de San Gemini','Informations et itinéraire','Avant de partir','Un guide conçu pour nos hôtes','GUIDE D’EXPLORATION'),
'ES':('Explora los alrededores','Pueblos, naturaleza, arqueología y ciudades de arte<br/>desde San Gemini','Información e indicaciones','Antes de salir','Una guía para nuestros huéspedes','GUÍA EXPLORA'),
'DE':('Entdecken Sie die Umgebung','Dörfer, Natur, Archäologie und Kunststädte<br/>rund um San Gemini','Informationen und Route','Vor der Abfahrt','Ein Reiseführer für unsere Gäste','ENTDECKER-GUIDE'),
'RU':('Исследуйте окрестности','Города, природа, археология и искусство<br/>из Сан-Джемини','Информация и маршрут','Перед поездкой','Путеводитель для наших гостей','ПУТЕВОДИТЕЛЬ')}
NOTICE='Orari, biglietti, prenotazioni e condizioni di accesso possono cambiare. Consulta sempre il sito collegato nella scheda.'
CURRENT={}
def styles():
    s=getSampleStyleSheet()
    for name,font,size,lead,color,after in [('PNTitle','AnthropicSemibold',25,30,DARK,8),('PNSub','AnthropicRegular',11,17,INK,8),('PNCard','AnthropicSemibold',12.5,15,DARK,2),('PNMeta','AnthropicLight',7,9,RUST,4),('PNBody','AnthropicRegular',9,13.5,INK,5),('PNLink','AnthropicSemibold',7.5,10,PINE,0),('PNSmall','AnthropicLight',8,11,DARK,0)]:
        s.add(ParagraphStyle(name=name,fontName=font,fontSize=size,leading=lead,textColor=color,spaceAfter=after,alignment=TA_CENTER if name=='PNSmall' else 0))
    return s
class NC(canvas.Canvas):
    def __init__(self,*a,**k): super().__init__(*a,**k); self.saved=[]
    def showPage(self): self.saved.append(dict(self.__dict__)); self._startPage()
    def save(self):
        n=len(self.saved)
        for st in self.saved: self.__dict__.update(st); self.footer(n); canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)
    def footer(self,n):
        if self._pageNumber>1:
            w,h=A4; self.setStrokeColor(SAND); self.line(18*mm,14*mm,w-18*mm,14*mm); self.setFont('AnthropicLight',7); self.setFillColor(MUTED); self.drawString(18*mm,9*mm,'PN HOUSE - Loc. Cimignano 165, San Gemini (TR)'); self.drawRightString(w-18*mm,9*mm,f'{self._pageNumber} / {n}')
def bg(c,d):
    w,h=A4; c.setFillColor(CREAM); c.rect(0,0,w,h,fill=1,stroke=0)
    if d.page>1: c.setFont('AnthropicLight',7); c.setFillColor(RUST); c.drawRightString(w-18*mm,h-29*mm,CURRENT['head']); c.setStrokeColor(SAND); c.line(18*mm,h-32*mm,w-18*mm,h-32*mm)
def card(i,S,link):
    num=Table([[Paragraph(f'{i+1:02d}',ParagraphStyle('PNNum',fontName='AnthropicSemibold',fontSize=9,textColor=WHITE,alignment=TA_CENTER))]],colWidths=[11*mm],rowHeights=[11*mm]); num.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),PINE),('VALIGN',(0,0),(-1,-1),'MIDDLE')]))
    txt=[Paragraph(escape(NAMES[i]),S['PNCard']),Paragraph(f'{escape(TYPES[i]).upper()} · {escape(DISTS[i])}',S['PNMeta']),Paragraph(escape(DESC[i]),S['PNBody']),Paragraph(f'<link href="{URLS[i]}"><u>{escape(link)}</u></link>',S['PNLink'])]
    inn=Table([[num,txt]],colWidths=[15*mm,145*mm]); inn.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(0,0),4*mm),('TOPPADDING',(0,0),(-1,-1),0),('BOTTOMPADDING',(0,0),(-1,-1),0)]))
    out=Table([[inn]],colWidths=[170*mm]); out.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),WHITE),('BOX',(0,0),(-1,-1),.55,SAND),('LEFTPADDING',(0,0),(-1,-1),4*mm),('RIGHTPADDING',(0,0),(-1,-1),4*mm),('TOPPADDING',(0,0),(-1,-1),3.6*mm),('BOTTOMPADDING',(0,0),(-1,-1),3.6*mm)])); return KeepTogether([out,Spacer(1,3*mm)])
def make(code,data,S):
    global CURRENT
    title,sub,link,before,guest,head=data; CURRENT={'head':head}
    path=OUT/f'PN_HOUSE_Explore_Guide_{code}.pdf'; doc=SimpleDocTemplate(str(path),pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=60*mm,bottomMargin=19*mm,title=f'PN HOUSE Explore Guide {code}',author='PN HOUSE')
    story=[Paragraph('PN HOUSE',ParagraphStyle('PNLogoText',fontName='AnthropicSemibold',fontSize=34,leading=38,textColor=DARK,alignment=TA_CENTER)),Spacer(1,8*mm),Paragraph(title,ParagraphStyle('PNCover',parent=S['PNTitle'],fontSize=29,leading=33,alignment=TA_CENTER)),Paragraph(sub,ParagraphStyle('PNCoverSub',parent=S['PNSub'],fontSize=13,leading=19,alignment=TA_CENTER)),Spacer(1,11*mm)]
    box=Table([[Paragraph(f'<b>{escape(guest)}</b><br/>{escape(NOTICE)}',S['PNBody'])]],colWidths=[150*mm]); box.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),WHITE),('BOX',(0,0),(-1,-1),.6,SAND),('LEFTPADDING',(0,0),(-1,-1),8*mm),('RIGHTPADDING',(0,0),(-1,-1),8*mm),('TOPPADDING',(0,0),(-1,-1),7*mm),('BOTTOMPADDING',(0,0),(-1,-1),7*mm)])); story += [box,Spacer(1,14*mm),Paragraph('Loc. Cimignano 165 · San Gemini (TR) · pnhouse.it',S['PNSmall']),PageBreak(),Paragraph(title,S['PNTitle']),Paragraph('Seleziona una meta e usa il collegamento presente in ogni scheda per organizzare la visita.',S['PNSub']),Spacer(1,3*mm)]
    for i in range(18): story.append(card(i,S,link))
    story += [Paragraph(before,S['PNTitle']),Paragraph(NOTICE,S['PNSub'])]
    doc.build(story,onFirstPage=bg,onLaterPages=bg,canvasmaker=NC); print('Creato:',path.name)
def main():
    setup_fonts(); S=styles()
    for code,data in LANG.items(): make(code,data,S)
    print('Completato:',OUT)
if __name__=='__main__':
    try: main()
    except subprocess.CalledProcessError as e:
        print('ERRORE conversione FontForge:',e.stderr,file=sys.stderr); sys.exit(1)
    except Exception as e: print('ERRORE:',e,file=sys.stderr); sys.exit(1)
