"""NH statewide revenue/expenditure shares from the DOE 'State Summary Revenue and Expenditures of School Districts' files.
Reads raw/nh-doe/*summary*rev*exp* (FY18-FY25). Prints put() lines for rc_data.py; `--check` compares with rc_data.py."""
import csv,re,sys,os
RAW=os.environ.get('NH_RAW','raw/nh-doe/inline-documents__')  # run from the repo root
F={2018:'state_summary_rev_exp17_18.csv',2019:'state-summary18-19.csv',2020:'sonh__summaryrevexp-2019-2020web.csv',2021:'sonh__summary-of-rev.-exp-fy2021.csv',
2022:'sonh__summary-of-rev-exp-fy2022.csv',2023:'sonh__summary-of-rev-exp-fy2023.csv',2024:'sonh__summary-of-rev-exp-fy2024.csv',2025:'sonh__summary-of-rev-exp-fy2025.csv'}
def n(s):
    s=re.sub(r'[$,\s]','',s)
    return float(s) if re.fullmatch(r'-?\d+(\.\d+)?',s) else None
def load(p):
    d={}
    for r in csv.reader(open(p,encoding='utf-8-sig',errors='replace')):
        if len(r)>1 and r[0].strip() and n(r[1]) is not None: d.setdefault(r[0].strip().rstrip('*').strip(),n(r[1]))
    return d
OUT={}
for fy,f in F.items():
    d=load(RAW+f)
    rec=d['Total Recurring Expenditures']; rev=d['Total Net Revenues']
    adm=d['General Administration and Business']+d['School Administration']+d['Business Services']
    OUT[fy]=dict(adm=adm/rec*100,spec=d['Special Programs']/rec*100,
      local=d['Local Taxation']/rev*100,state=(d['Equitable Education Aid']+d['Other State Sources'])/rev*100,fed=d['Federal Sources']/rev*100,
      plant=d['Plant Operations']/rec*100,trans=d['Pupil Transportation']/rec*100,debt=d['Bond & Note Interest']/rec*100,
      instr=(d['Regular Instruction']+d['Special Programs']+d['Vocational Programs']+d['Other Instructional Programs'])/rec*100)
if __name__=='__main__':
    for k in ['adm','spec','instr','local','state','fed','plant','trans','debt']:
        print("put('nh_%s_sh', per([%s]))"%(k,', '.join(str(round(OUT[y][k],3)) for y in range(2018,2026))))
