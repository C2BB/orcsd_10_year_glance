import csv,re,sys,statistics,subprocess,os,openpyxl
import os
D=os.environ.get('NH_RAW','raw/nh-doe/inline-documents__')  # run from the repo root
def num(s):
    s=str(s).replace('$','').replace(',','').strip()
    try: return float(s)
    except: return None
def sectioned(path):
    out={'S':{},'A':{},'B':{}}; cur=None
    for r in csv.reader(open(path,encoding='utf-8-sig',errors='replace')):
        if not r: continue
        h=r[0].strip()
        if h.startswith('Superintendents'): cur='S'; continue
        if h.startswith('Assistant Superintendents'): cur='A'; continue
        if h.startswith('Business Administrators'): cur='B'; continue
        if cur and len(r)>=3:
            m=re.match(r'\s*(\d+)-(.*)',r[1].strip())
            v=num(r[2])
            if m and v and int(m.group(1))<200: out[cur].setdefault(int(m.group(1)),[]).append(v)
    return out
def flat(path,posc,valc,sauc=0,skip=0):
    out={'S':{},'A':{},'B':{}}
    for r in csv.reader(open(path,encoding='utf-8-sig',errors='replace')):
        if len(r)<=max(posc,valc): continue
        try: sid=int(r[sauc])
        except: continue
        if sid>=200: continue
        p=r[posc].lower(); v=num(r[valc])
        if not v: continue
        k='A' if 'assistant' in p else 'S' if ('superintendent' in p or 'senior education official' in p) else 'B' if 'business' in p else None
        if k: out[k].setdefault(sid,[]).append(v)
    return out
def xl(path):
    out={'S':{},'A':{},'B':{}}
    wb=openpyxl.load_workbook(path,data_only=True)
    for ws in wb:
        for r in ws.iter_rows(values_only=True):
            if r and isinstance(r[0],int) and r[0]<200 and isinstance(r[3],(int,float)):
                p=str(r[2]).lower()
                k='A' if 'assistant' in p else 'S' if ('superintendent' in p or 'senior education' in p) else 'B' if 'business' in p else None
                if k: out[k].setdefault(r[0],[]).append(float(r[3]))
    return out
def pdf(path):
    t=subprocess.run(['pdftotext','-layout',path,'-'],capture_output=True,text=True).stdout
    out={'S':{},'A':{},'B':{}}
    for l in t.splitlines():
        m=re.match(r'\s*(\d+)\s+(.+?)\s{2,}(Business Administrator|Assistant Senior Education Official|Senior Education Official)\s+([\d,]+\.\d\d)',l)
        if m and int(m.group(1))<200:
            k={'Business Administrator':'B','Assistant Senior Education Official':'A','Senior Education Official':'S'}[m.group(3)]
            out[k].setdefault(int(m.group(1)),[]).append(num(m.group(4)))
    return out
Y={2018:sectioned(D+'salaries17-18.csv'),2019:sectioned(D+'salaries18-19.csv'),
2020:flat(D+'salaries19-20.csv',2,5),2021:flat(D+'sonh__salaries20-21_1.csv',2,3),
2022:flat(D+'sonh__admin-sal-21-22.csv',2,3),2023:flat(D+'sonh__admin-sal-22-23.csv',2,3),
2024:flat(D+'sonh__admin-sal-23-24.csv',2,3),2025:pdf(D+'sonh__admin-sal-24-25.pdf'),2026:xl(D+'sonh__admin-sal-25-26.xlsx')}
res={}
for fy,d in sorted(Y.items()):
    row={}
    for k in 'SAB':
        vals={s:max(v) for s,v in d[k].items()}
        o=vals.get(5)
        al=sorted(vals.values(),reverse=True)
        row[k]=dict(oy=o,n=len(al),med=statistics.median(al),avg=round(statistics.mean(al)),rank=(al.index(o)+1 if o in al else None))
    res[fy]=row
    print(fy,{k:(r['oy'],r['n'],r['med'],r['avg'],r['rank']) for k,r in row.items()})
if '--json' in sys.argv:
    import json;json.dump(res,open('/tmp/w/admin_pay.json','w'))
