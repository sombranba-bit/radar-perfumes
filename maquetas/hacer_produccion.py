"""Pasa la maqueta Fragans (Calco) a la página principal: index.html + app/. Guarda la portada previa en anterior.html si no existe."""
import os, re, shutil, subprocess
ROOT = os.path.join(os.path.dirname(__file__), '..')
V2 = os.path.join(ROOT, 'maquetas', 'v2')
os.makedirs(os.path.join(ROOT, 'app'), exist_ok=True)
for f in ('estela.css', 'estela.js', 'olfato.js'):
    shutil.copy(os.path.join(V2, f), os.path.join(ROOT, 'app', f))
if not os.path.exists(os.path.join(ROOT, 'anterior.html')):
    old = subprocess.run(['git', 'show', 'HEAD:index.html'], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    open(os.path.join(ROOT, 'anterior.html'), 'w').write(old)
s = open(os.path.join(V2, 'fragans-o1.html')).read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a[:70], s.count(a))
    s = s.replace(a, b)
DESC = 'Compara el precio de tu perfume en las perfumerías españolas: dónde cuesta menos hoy, cuáles bajan y cómo huele cada uno.'
rep('<title>Fragans · Calco</title>', '<title>Fragans · Comparador de precios de perfume</title>')
s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">\n<meta property="og:title" content="Fragans · Comparador de precios de perfume"><meta property="og:description" content="{DESC}">\n<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 32 32\'><rect width=\'32\' height=\'32\' rx=\'8\' fill=\'%238a2335\'/><circle cx=\'14\' cy=\'14\' r=\'7\' fill=\'none\' stroke=\'white\' stroke-width=\'2.4\'/><path d=\'m19.5 19.5 6 6\' stroke=\'white\' stroke-width=\'2.8\' stroke-linecap=\'round\'/><path d=\'M14 10.2c1.9 2.2 2.8 3.6 2.8 4.8a2.8 2.8 0 0 1-5.6 0c0-1.2.9-2.6 2.8-4.8Z\' fill=\'white\'/></svg>">', s, count=1)
rep("localStorage.getItem('fragans-pal')||'burdeos'", "'burdeos'")
rep("localStorage.getItem('fragans-cards')||'fundida'", "'fundida'")
V = __import__('time').strftime('%Y%m%d%H%M')  # cambia en cada publicación: el navegador no se queda con la versión vieja
rep('href="estela.css"', f'href="app/estela.css?v={V}"')
rep('<script src="estela.js"></script>', f'<script src="app/estela.js?v={V}"></script>')
rep('<script src="olfato.js"></script>', f'<script src="app/olfato.js?v={V}"></script>')
rep("../core.js?v=", "maquetas/core.js?v=")
rep('&family=Instrument+Serif', '')  # Fragans usa Fraunces para los titulares
s = re.sub(r'const V=\[.*?\],R=E\.R;', 'const V=[],R=E.R;', s, count=1, flags=re.S)
rep("E.start({name:'fragans-o1.html',variants:V,home,catalog}).then(addPal);", "E.DATA='data/';E.OLD='anterior.html';\nE.start({name:'index.html',variants:V,home,catalog});")
open(os.path.join(ROOT, 'index.html'), 'w').write(s)
print('index.html listo')
