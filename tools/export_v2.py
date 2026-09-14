from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output'
TMP=ROOT/'tmp'/'pdfs'
EDGE=Path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')

def export_pdf():
    target=OUT/'seven-winters-zine-v2.pdf'
    cmd=[str(EDGE),'--headless','--disable-gpu','--no-sandbox','--no-pdf-header-footer','--run-all-compositor-stages-before-draw',f'--print-to-pdf={target}',(ROOT/'seven-winters-zine-v2-reader.html').as_uri()]
    subprocess.run(cmd,check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)

def contact_sheet():
    files=sorted((ROOT/'selected').glob('*.png'))
    cols,cell_w,cell_h=4,520,385
    rows=(len(files)+cols-1)//cols
    sheet=Image.new('RGB',(cols*cell_w,rows*cell_h),'#171717')
    draw=ImageDraw.Draw(sheet)
    try:
        label=ImageFont.truetype('arial.ttf',20)
        num=ImageFont.truetype('arialbd.ttf',25)
    except OSError: label=num=ImageFont.load_default()
    for i,path in enumerate(files,1):
        img=Image.open(path).convert('RGB')
        img.thumbnail((cell_w-32,cell_h-70),Image.Resampling.LANCZOS)
        x=(i-1)%cols*cell_w; y=(i-1)//cols*cell_h
        framed=ImageOps.expand(img,border=3,fill='#efede6')
        sheet.paste(framed,(x+16,y+12))
        draw.text((x+16,y+cell_h-46),f'{i:02d}',font=num,fill='#8d1d19')
        draw.text((x+58,y+cell_h-42),path.name,font=label,fill='#efede6')
    sheet.save(OUT/'seven-winters-v2-contact-sheet.jpg',quality=94,subsampling=0)

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True); TMP.mkdir(parents=True,exist_ok=True)
    export_pdf(); contact_sheet()
