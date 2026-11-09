import sys,io,base64,os
from PIL import Image
name,path=sys.argv[1],sys.argv[2]
w=int(sys.argv[3]) if len(sys.argv)>3 else 900
im=Image.open(path)
im=im.convert('RGBA' if im.mode in ('RGBA','LA','P') else 'RGB')
im.thumbnail((w,w))
b=io.BytesIO();im.save(b,'WEBP',quality=84)
out=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','gem',name+'.b64')
open(out,'w').write(base64.b64encode(b.getvalue()).decode())
print('wrote',out,len(b.getvalue()),'bytes')
