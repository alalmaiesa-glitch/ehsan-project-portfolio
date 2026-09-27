from pathlib import Path
import re, json
ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'source/portfolio.html').read_text(encoding='utf-8')
opp_pat=re.compile(r'\\{n:(\\d+),\\s*name:\"([^\"]+)\",\\s*field:\"([^\"]*)\",\\s*fund:\"([^\"]*)\",\\s*count:(\\d+)\\}')
opps=[]
for m in opp_pat.finditer(src):
    n,name,field,fund,count=m.groups(); n=int(n)
    if 1<=n<=96 and not any(x['n']==n for x in opps): opps.append({'id':f'opp-{n:03d}','kind':'opportunity','n':n,'name':name,'field':field,'fund':fund,'count':int(count)})
opp_block=src.split('const APPENDIX_DATA = [',1)[1].split('];\\n\\nfunction buildAppendix',1)[0]
section_pat=re.compile(r'\\{\\s*title:\\s*\"([^\"]+)\",\\s*projects:\\s*\\[(.*?)\\]\\s*\\}',re.S)
proj_pat=re.compile(r'\\{n:(\\d+),\\s*name:\"([^\"]+)\",\\s*desc:\"([^\"]*)\",\\s*budget:\"([^\"]*)\",\\s*months:\"([^\"]*)\"\\}')
apps=[]
for sm in section_pat.finditer(opp_block):
    section=sm.group(1)
    for pm in proj_pat.finditer(sm.group(2)):
        n,name,desc,budget,months=pm.groups(); n=int(n)
        field=re.sub(r'^المحور [^:]+:\\s*','',section)
        apps.append({'id':f'app-{n:03d}','kind':'appendix','n':n,'name':name,'section':section,'desc':desc,'budget':budget,'months':months,'field':field,'fund':'تبرعات/عام'})
cards=sorted(opps,key=lambda x:x['n'])+sorted(apps,key=lambda x:x['n'])
templates=[
 {'key':'idea-card','label':'بطاقة الفكرة','stage':'idea','emoji':'🟢'},
 {'key':'project-study','label':'دراسة المشروع','stage':'idea','emoji':'🟢'},
 {'key':'project-charter','label':'ميثاق المشروع','stage':'idea','emoji':'🟢'},
 {'key':'eligibility','label':'معايير الاستحقاق','stage':'verify','emoji':'🟡'},
 {'key':'social-research','label':'البحث الاجتماعي','stage':'verify','emoji':'🟡'},
 {'key':'offers-comparison','label':'مقارنة العروض','stage':'execute','emoji':'🔵'},
 {'key':'acceptance-minutes','label':'محضر الاستلام','stage':'execute','emoji':'🔵'},
 {'key':'progress-report','label':'التقرير المرحلي','stage':'execute','emoji':'🔵'},
 {'key':'risk-register','label':'سجل المخاطر','stage':'execute','emoji':'🔵'},
 {'key':'closure-report','label':'تقرير الإغلاق','stage':'close','emoji':'🟣'},
 {'key':'evidence-checklist','label':'قائمة الأدلة','stage':'close','emoji':'🟣'}]
(ROOT/'data').mkdir(exist_ok=True)
(ROOT/'data/cards.json').write_text(json.dumps(cards,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'data/templates.json').write_text(json.dumps(templates,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Prepared {len(cards)} cards and {len(templates)} templates')
