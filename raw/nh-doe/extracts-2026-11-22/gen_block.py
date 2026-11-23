import sys, re, json
sys.path.insert(0,'/home/claude')
from school_data import SCHOOLS, DISTRICT
from town_enroll import ROWS as TR
N=None
out=[]
def P(name, vals, start=2018, comment=None):
    vals=[None if v=='C' else v for v in vals]
    out.append('put(%r, per(%s%s))'%(name, json.dumps(vals).replace('null','None'), '' if start==2018 else ', start=%d'%start))
out.append('')
out.append('# ---- Added Nov 22, 2026 (second data sweep) ----')
out.append('# Town enrollment: NH DOE iPlatform "Town Level Enrollment By Grade" (ReportID 12), public-school students living in each town, Oct 1 count; FY27 = preliminary Oct 1, 2026 run.')
towns={'dur':0,'lee':1,'mad':2}
for t,i in towns.items():
    tot=[];k4=[];ms=[];hs=[];ps=[]
    for y in range(2018,2028):
        c=[int(x) for x in TR[y][i].split(',')[2:]]  # PS,KG,G1..G12,PG,Total
        PS,KG,G=c[0],c[1],c[2:14]; PG,T=c[14],c[15]
        assert PS+KG+sum(G)+PG==T,(y,t,PS+KG+sum(G)+PG,T)
        tot.append(T); k4.append(KG+sum(G[0:4])); ms.append(sum(G[4:8])); hs.append(sum(G[8:12])); ps.append(PS+PG)
    P('en_'+t,tot); P('en_'+t+'_k4',k4); P('en_'+t+'_ms',ms); P('en_'+t+'_hs',hs); P('en_'+t+'_ps',ps)
out.append('# School-level and district indicators: NH DOE iExplore (Compare dashboard, *Download Compare), DOE years 2018-2026 (2016-2017 not used); COVID-year gaps are None.')
for s,d in SCHOOLS.items():
    sl=lambda a:[x for x in a][2:]
    for key,fld in [('ela_p','ela'),('mat_p','mat'),('ela_g','gela'),('mat_g','gmat'),('cert','cert'),('exp','exp'),('cslr','cslr'),('swd','swd'),('enr','enr'),('nts','nts')]:
        if key in d: P('sc_%s_%s'%(s.lower(),fld), sl(d[key]))
D=DISTRICT
P('exp_doe', D['exp'][2:]); P('exp_doe_nh',[85.79,85.74,85.06,84.95,84.55,83.78,83.54,83.68,83.36])
P('nts', D['nts'][2:]); P('nts_nh',[N,N,N,22.18,23.45,24.80,22.78,21.81,21.05])
P('tts', D['tts'][2:]); P('tts_nh',[N,N,N,0.67,0.68,0.68,0.67,0.67,0.66])
out.append('# FTE staff by category, NH DOE iPlatform "Full Time Equivalent Staff Count by District" (ReportID 38), Oyster River Coop, Oct 1 counts')
fte={2018:(175.1,100.1,4.0,27.9,8.4,39.6),2019:(181.1,92.3,4.0,36.8,9.2,72.8),2020:(182.1,83.8,4.0,44.7,9.2,71.2),2021:(179.1,77.8,4.0,30.7,9.2,74.2),2022:(179.1,98.0,4.0,36.2,10.2,59.4),2023:(180.2,83.2,4.0,52.9,10.2,54.0),2024:(178.6,72.0,4.0,54.3,5.6,65.4),2025:(180.0,77.4,4.0,51.1,10.2,73.7),2026:(178.0,85.0,4.0,46.0,10.4,41.5)}
for i,nm in enumerate(['ft_teach','ft_aide','ft_lib','ft_spec','ft_adm','ft_oth']):
    P(nm,[fte[y][i] for y in range(2018,2027)])
out.append('# IDEA indicator 5 (iReport IDEA Report): share of students with IEPs ages 6-21 in regular class 80%+ of the day (5A), under 40% (5B), separate facilities (5C). DOE repeats prior-year values in 2018-19 and 2019-20 (state too), so those are left blank.')
P('incl',[69.90,N,72.96,82.84,89.26,90.91,90.32,91.09]); P('incl_nh',[70.81,N,N,73.75,75.42,78.03,80.20,82.13])
P('incl_lt40',[4.84,N,N,4.10,4.03,1.30,0.65,0.66]); P('incl_lt40_nh',[9.05,N,N,8.95,8.38,6.97,5.43,4.53])
P('incl_sep',[4.91,N,N,1.49,4.03,0.97,0.32,0.33]); P('incl_sep_nh',[2.84,N,N,2.46,1.95,1.52,1.24,1.10])
out.append('# NH suspension rates, iReport ESSA profile for State of NH (All Students), % of students')
P('iss_nh',[3.62,3.72,2.56,0.89,3.22,3.48,3.67,3.29,2.90]); P('oss_nh',[3.98,4.15,3.03,1.37,3.98,4.12,4.11,4.41,4.05])
out.append('# NH habitual truancy: sum of habitually truant students over sum of school enrollment, all NH schools in the DOE School Safety workbooks (2017-18 to 2024-25), per 100 students')
P('trunt_nh',[10.40,13.94,11.19,17.14,17.23,16.41,17.12,18.79])
# ESSA ratings
rat={}
for l in open('/home/claude/essa_ratings.txt'):
    m=re.match(r'^(HS|MS|MW|MO)\.(\w+) (.+)$',l.strip())
    if m: rat[(m.group(1),m.group(2))]=m.group(3).split(',')
def cell(v):
    return int(v) if v.isdigit() else None
out.append('# State ESSA ratings 1-4 per school (iReport ESSA - Indicators (District)); None = not rated (COVID years), suppressed (<11 students) or not applicable')
for (s,m),v in sorted(rat.items()):
    P('es_%s_%s'%(s.lower(),m),[cell(x) for x in v])
def avg(ms_,i):
    xs=[cell(rat[k][i]) for k in rat if k[1]==ms_]
    xs=[x for x in xs if x is not None]
    return round(sum(xs)/len(xs),2) if xs else None
P('es_ach',[avg('ach',i) for i in range(9)]); P('es_eq',[avg('eq',i) for i in range(9)]); P('es_gro',[avg('gro',i) for i in range(9)])
out.append('put("drop", {**RC["drop"], 2026: 0})  # FY26: iExplore dropout rate 0.00% (NH DOE)')
open('/home/claude/block.py','w').write('\n'.join(out)+'\n')
print(len(out)); print('\n'.join(out[-14:])[:1800])
