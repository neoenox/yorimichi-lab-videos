import sys
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path('scripts').resolve()))
import make_short2 as m
m.bg=lambda path,zoom,dim=.55,fit=1.12: Image.open(m.ROOT/path).convert('RGB')
sys.argv=['make_short2.py','rainbow_circle']
m.main()
