"""Build the GitHub Pages site (repo root) from the sources in build/.

  python3 make_data.py     # raw per-year values (rc_data.py, doe25.py, ...) -> orcsd_years.json
  python3 build_pages.py   # -> ../index.html, ../app.js, ../data/*.json, ../dist/*.html

index.html loads data/orcsd_years.json and data/sources.json at runtime and then app.js.
dist/ORCSD_Ten_Years_at_a_Glance.html is the same page as one file with the data inlined
(works from disk or as an email attachment).
"""
import json, pathlib, hashlib, re, os
b = pathlib.Path(__file__).parent
root = b.parent
css = (b/'page.css').read_text()
html = (b/'page.html').read_text()
js = (b/'page.js').read_text()
data = json.loads((b/'orcsd_years.json').read_text())
sources = json.loads((b/'sources.json').read_text())
dump = lambda o: json.dumps(o, separators=(',', ':'), ensure_ascii=False)

shim = """var STORE = { years: window.__DATA.rows };
var DRAWS = {};
window.dash = {
  data: function (id) { return { status: STORE[id] ? 'ok' : 'missing', data: STORE[id] || [] }; },
  calc: function (id, o) { STORE[id] = o.fn.apply(null, o.inputs.map(function (i) { return STORE[i]; })); },
  draw: function (name, fn) {
    if (typeof fn === 'function') DRAWS[name] = fn;
    var f = DRAWS[name];
    if (f) document.querySelectorAll('[data-draw="' + name + '"]').forEach(function (el) { f(el); });
  }
};
var rsz; window.addEventListener('resize', function () { clearTimeout(rsz); rsz = setTimeout(function () { Object.keys(DRAWS).forEach(function (n) { dash.draw(n); }); }, 120); });
"""
head = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ORCSD Ten Years at a Glance</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Source+Serif+4:opsz,wght@8..60,400&display=swap">
<style>
:root{--color-fg:#1f1a1b;--color-fg-muted:#675f61;--color-bg:#fbf9f8;--color-panel:#f4f0ee;--color-border-line:#e2dad7;--cds-surface-popover:#ffffff;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--color-fg:#efe9e7;--color-fg-muted:#a89fa1;--color-bg:#161314;--color-panel:#1f1b1c;--color-border-line:#3a3335;--cds-surface-popover:#262122;color-scheme:dark}}
body{margin:0;background:var(--color-bg);color:var(--color-fg);padding-block:32px 48px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.os-loaderr{max-width:640px;margin:48px auto;padding:16px;border:1px solid var(--color-border-line);border-radius:8px}
""" + css + "</style>\n</head>\n<body>\n"

# --- data files (served as-is by GitHub Pages) ---
(root/'data').mkdir(exist_ok=True)
(root/'data'/'orcsd_years.json').write_text(dump(data))
(root/'data'/'sources.json').write_text(dump(sources))
ver = hashlib.sha1((dump(data) + dump(sources) + js + shim).encode()).hexdigest()[:10]

# --- app.js: shim + page script (needs window.__DATA and window.__SRC) ---
(root/'app.js').write_text(shim + js)

boot = """<script>
(function () {
  function fail(e) { var d = document.createElement('div'); d.className = 'os-loaderr'; d.textContent = 'Could not load the data files (' + e + '). Open the single-file version in the dist folder, or try again.'; document.body.insertBefore(d, document.body.firstChild); }
  Promise.all([fetch('data/orcsd_years.json?v=%(v)s'), fetch('data/sources.json?v=%(v)s')]).then(function (rs) {
    rs.forEach(function (r) { if (!r.ok) throw new Error(r.status + ' ' + r.url); });
    return Promise.all(rs.map(function (r) { return r.json(); }));
  }).then(function (j) {
    window.__DATA = j[0]; window.__SRC = j[1];
    var s = document.createElement('script'); s.src = 'app.js?v=%(v)s'; s.onerror = function () { fail('app.js'); };
    document.body.appendChild(s);
  }).catch(fail);
})();
</script>
""" % {'v': ver}
(root/'index.html').write_text(head + html + boot + "</body>\n</html>\n")

# --- single-file build, data inlined, lightly compacted ---
inline = "<script>\nwindow.__DATA = " + dump(data) + ";\nwindow.__SRC = " + dump(sources) + ";\n" + shim + js + "</script>\n"
single = head + html + inline + "</body>\n</html>\n"
single = re.sub(r'\n[ \t]+', '\n', single); single = re.sub(r'\n{2,}', '\n', single)
(root/'dist').mkdir(exist_ok=True)
(root/'dist'/'ORCSD_Ten_Years_at_a_Glance.html').write_text(single)

# --- hosted artifact copy (Claude data-artifact format; optional) ---
hp = os.environ.get('HOSTED_OUT')
if hp:
    # hosted copy only: shorten the long repeated URL prefixes (256 KB document limit)
    PFX = {'A': 'https://www.education.nh.gov/sites/g/files/ehbemt326/files/inline-documents/sonh/',
           'B': 'https://www.orcsd.org/departments/business-office/files/documents/Annual%20Reports/',
           'C': 'https://www.education.nh.gov/sites/g/files/ehbemt326/files/inline-documents/'}
    sj = dump(sources)
    for k in ('A', 'B', 'C'): sj = sj.replace(PFX[k], '@' + k + '@')
    pre = "var __P = " + dump(PFX) + ";\nwindow.__SRC = JSON.parse(" + dump(sj) + ".replace(/@([ABC])@/g, function (m, k) { return __P[k]; }));\n"
    # the hosted harness allows only dash.draw to write the page, so the runtime deep-link script is left out of this copy
    _a = js.index('  // ---- Deep links'); _b = js.index('\n  })();\n', _a) + len('\n  })();\n')
    hjs = js[:_a] + js[_b:]
    hjs = re.sub(r'(?m)^[ \t]*//[^\n]*\n', '', hjs)
    hcss = re.sub(r'/\*.*?\*/', '', css, flags=re.S); hcss = re.sub(r'\s*([{};,>])\s*', r'\1', hcss); hcss = re.sub(r'\n+', '', hcss)
    hosted = '<meta name="dash-one-writer">\n<style>\n' + hcss + '</style>\n' + html + '<script>\n' + pre + hjs + '</script>\n'
    # hosted copy only: trim repeated legend-swatch attributes (moved to CSS) to stay under the 256 KB document limit
    hosted = hosted.replace('<svg width="30" height="12" viewBox="0 0 30 12" aria-hidden="true">', '<svg viewBox="0 0 30 12">').replace(' stroke-linecap="round"', '')
    # hosted copy only: the repeated legend swatches become <use> references to symbols defined once (static markup, no script)
    import collections
    _sv = collections.Counter(re.findall(r'<svg viewBox="0 0 30 12">(.*?)</svg>', hosted, flags=re.S))
    _gl = [x for x, n in _sv.most_common() if n > 2]
    for i, x in enumerate(_gl): hosted = hosted.replace('<svg viewBox="0 0 30 12">' + x + '</svg>', '<svg viewBox="0 0 30 12"><use href="#g%d"/></svg>' % i)
    _defs = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + ''.join('<symbol id="g%d" viewBox="0 0 30 12">%s</symbol>' % (i, x.replace('<line ', '<line stroke-linecap="round" ')) for i, x in enumerate(_gl)) + '</svg>\n'
    hosted = hosted.replace('</style>\n', '</style>\n' + _defs, 1)
    hosted = hosted.replace('<style>\n', '<style>\n.os-legend .lk svg{width:30px;height:12px}.os-legend .lk svg line{stroke-linecap:round}\n', 1)
    hosted = re.sub(r'(<div class="os-src" data-draw="src-[a-z0-9]+">)Data:.*?(</div>)', r'\1—\2', hosted, flags=re.S)
    hosted = re.sub(r'\n[ \t]+', '\n', hosted); hosted = re.sub(r'\n{2,}', '\n', hosted)
    pathlib.Path(hp).write_text(hosted)
print('version', ver, 'index', (root/'index.html').stat().st_size, 'app.js', (root/'app.js').stat().st_size, 'single', len(single))
