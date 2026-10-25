# Radar de Perfumes

Comparador y rastreador de precios de perfumes. Funciona solo en GitHub:

- **La página** (`index.html`) se publica con GitHub Pages.
- **La pasada automática** (`.github/workflows/radar.yml`) corre cada 30 minutos, 24/7. En cada pasada:
  - revisa los 35 perfumes que llevan más tiempo sin revisar (la lista completa se recorre cada ~3 horas);
  - lee las fichas guardadas de cada tienda y apunta el precio del tamaño exacto;
  - lee los chollos de perfumes de Chollometro;
  - guarda todo en `data/`.
- `data/estado.json` dice, de cada tienda, cuántas fichas se leyeron bien, cuántas bloquearon la lectura y cuántas se descartaron por precio raro.

## Montarlo (una vez)

1. En GitHub: **New repository**. Nombre: `radar-perfumes`, tipo **Public** (Pages gratis solo funciona en repos públicos).
2. **Add file → Upload files**. Arrastra todo el contenido del zip, incluida la carpeta `.github`, y pulsa **Commit changes**.
3. **Settings → Pages**: en Source elige **Deploy from a branch**, rama `main`, carpeta `/ (root)`, y pulsa **Save**. La página quedará en `https://<tu-usuario>.github.io/radar-perfumes/`.
4. **Settings → Actions → General → Workflow permissions**: elige **Read and write permissions** y pulsa **Save**.
5. **Actions → Pasada de precios → Run workflow** para lanzar la primera pasada ya. Después se lanza sola.

### Si la carpeta `.github` no se sube

Windows y Mac esconden las carpetas que empiezan por punto. Si en **Actions** no aparece «Pasada de precios», crea el archivo a mano:

1. **Add file → Create new file**.
2. Como nombre escribe `.github/workflows/radar.yml`.
3. Pega esto y pulsa **Commit changes**:

```yaml
name: Pasada de precios

on:
  schedule:
    - cron: "*/30 * * * *"   # cada 30 min, 24/7 (GitHub puede retrasarla unos minutos)
  workflow_dispatch: {}      # botón "Run workflow" para lanzarla a mano

permissions:
  contents: write

concurrency:
  group: radar
  cancel-in-progress: false

jobs:
  pasada:
    runs-on: ubuntu-latest
    timeout-minutes: 25
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt
      - run: python scraper/test_radar.py
      - run: python scraper/radar.py
      - name: Guardar datos
        run: |
          git config user.name "radar-bot"
          git config user.email "radar-bot@users.noreply.github.com"
          git add data/
          git diff --cached --quiet && exit 0
          git commit -m "Pasada $(TZ=Europe/Madrid date '+%Y-%m-%d %H:%M')"
          git pull --rebase --autostash
          git push
```

## Añadir perfumes al rastreo

Edita `data/perfumes.json` en GitHub. Copia un bloque existente y cambia `brand`, `name`, `conc`, `ml` e `id`. En `urls` pon la ficha de cada tienda, si la tienes.

Los perfumes que añades desde la página se guardan solo en tu navegador, y la pasada automática no los rastrea.

## Probar el extractor

```
python scraper/test_radar.py
```
