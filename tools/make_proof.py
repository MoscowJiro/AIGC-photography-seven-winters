from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]
pages=sorted((root/'tmp'/'pdfs').glob('v2-*.jpg'))
tw,th,cols,gap=296,420,8,10
rows=(len(pages)+cols-1)//cols
sheet=Image.new('RGB',(gap+cols*(tw+gap),gap+rows*(th+32+gap)),'#686764')
draw=ImageDraw.Draw(sheet)
try: font=ImageFont.truetype('arial.ttf',17)
except OSError: font=ImageFont.load_default()
for i,path in enumerate(pages,1):
    img=Image.open(path).convert('RGB'); img.thumbnail((tw,th),Image.Resampling.LANCZOS)
    x=gap+(i-1)%cols*(tw+gap); y=gap+(i-1)//cols*(th+32+gap)
    sheet.paste(img,(x+(tw-img.width)//2,y)); draw.text((x,y+th+5),f'P{i:02d}',font=font,fill='#efede6')
sheet.save(root/'tmp'/'pdfs'/'v2-proof.jpg',quality=91)
