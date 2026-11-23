"""Check the Durham / Lee / Madbury local-education and total tax rates shown on the page (make_data.py _chk, keyed by school-year end)
against the NH DRA 'Tax Rate Calculation Data' workbooks kept in raw/nh-dra/ (tax year N -> school year N/N+1 -> key N+1)."""
import openpyxl,os,sys,re
RAW=os.environ.get('RAW','raw/nh-dra/')  # run from the repo root
F={2022:'inline-documents__sonh__municipal-property__2021-tax-rate-calculation-data.xlsx',2023:'inline-documents__sonh__municipal-property__2022-tax-rate-caluclation-data.xlsx',
2024:'inline-documents__sonh__2023-tax-rate-calculation-data.xlsx',2025:'documents__2024-tax-rate-calculation-data.xlsx',2026:'documents__2025-tax-rate-calculation-data.xlsx'}
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'make_data.py')).read()
chk=eval(re.search(r'^_chk=(\{.*\})$',src,re.M).group(1))
bad=0
for key,f in F.items():
    ws=openpyxl.load_workbook(RAW+f,data_only=True).worksheets[0]
    hdr=None;got={}
    for r in ws.iter_rows(values_only=True):
        if r and r[0] in('Durham','Lee','Madbury'):
            vals=[c for c in r if c is not None]
            got[r[0]]=r
        if r and r[0] and 'Unincorporated' in str(r[0]): hdr=[str(c).replace('\n',' ') for c in r]
    li=[i for i,h in enumerate(hdr) if h.strip()=='Local Education Tax Rate'][0]
    ti=[i for i,h in enumerate(hdr) if h.strip()=='Total Tax Rate'][0] if any(h.strip()=='Total Tax Rate' for h in hdr) else None
    loc=tuple(round(float(got[t][li]),2) for t in('Durham','Lee','Madbury'))
    ok=loc==chk[key][0]
    tot=None
    if ti is not None: tot=tuple(round(float(got[t][ti]),2) for t in('Durham','Lee','Madbury')); ok=ok and tot==chk[key][1]
    print(key,f,'local',loc,'total',tot,'OK' if ok else 'MISMATCH page=%s'%(chk[key],)); bad+=0 if ok else 1
sys.exit(1 if bad else 0)
