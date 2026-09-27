from pathlib import Path
import json, html, re
ROOT=Path(__file__).resolve().parents[1]
cards=json.loads((ROOT/'data/cards.json').read_text(encoding='utf-8'))
opps=[c for c in cards if c['kind']=='opportunity']
apps=[c for c in cards if c['kind']=='appendix']
tpls=json.loads((ROOT/'data/templates.json').read_text(encoding='utf-8'))
repo='alalmaiesa-glitch/ehsan-project-portfolio'
raw=f'https://raw.githubusercontent.com/{repo}/main/docs'
repo_url=f'https://github.com/{repo}'
pages='https://alalmaiesa-glitch.github.io/ehsan-project-portfolio/'
COMMON={
'أسري واجتماعي': [('استقرار 12 شهرًا','كفالة مرحلية مرتبطة بخطة استقرار مالي وتعليمي للأسرة.'),('تمكين من المنزل','تدريب وأداة إنتاج أو عمل رقمي مناسب مع متابعة دخل.'),('مدير حالة للأسرة','تنسيق السكن والتعليم والصحة والتمكين بدل الدعم المتفرق.')],
'سكني ومعيشي': [('قسيمة احتياج مرنة','قسائم شراء مقيدة بالفئة تمنح المستفيد حرية الاختيار.'),('حزمة موسمية مستهدفة','توريد حزم وفق الموسم والعمر والمنطقة مع ضبط المقاسات.'),('توزيع منظم بالباركود','نظام تسليم يمنع الازدواجية ويقيس التغطية.')],
'صحي وتأهيلي': [('بروتوكول خدمة','تصميم خدمة موثقة مع مزود مرخص وخطة متابعة.'),('حزمة الخدمة والتعافي','الخدمة مع الفحوص والتأهيل القصير والمتابعة.'),('شراء جماعي مؤسسي','اتفاق مسبق مع مزودين بأسعار مؤسسية.')],
'تعليمي وتنموي': [('مسار الطالب المستمر','حزمة تمنع الانقطاع وتغطي الاحتياج التعليمي.'),('التفوق الموجه','اختبارات تشخيصية وخطة تعلم ومتابعة تحسن.'),('دعم تعليمي رقمي','اشتراكات أو محتوى أو أجهزة مرتبطة بخطة دراسية.')],
'ديني وضيوف الرحمن': [('خدمة ميسرة للمستحق','تغطية الاحتياج الأساسي مع خدمة منظمة من البداية للنهاية.'),('نسك ميسر لذوي الإعاقة','نقل وسكن ومرافقة وتجهيزات وصول مناسبة.'),('استجابة للمنقطعين','مساعدة طارئة موثقة عند انقطاع الوسيلة.')],
'بيئي ومائي': [('تحديد الموقع والمصدر','تحليل الحاجة الفنية والجهة المسؤولة عن التشغيل.'),('تصميم فني وكميات','مواصفات وعقود تشغيل وصيانة واختبارات جودة.'),('تشغيل مستدام بعقد','تضمين التمويل الرأسمالي وتشغيل طويل المدى.')],
'اجتماعي عام': [('تصميم نطاق واضح','عدد المستفيدين والأنشطة والمؤشرات قبل التقديم.'),('تنفيذ بعقود محددة','متابعة تقدم دورية وتوثيق لكل دفعة ومخرج.'),('قياس بخط أساس','مقارنة النتائج بخط الأساس والتكلفة لكل مستفيد.')],
'مؤسسي وتشغيلي': [('تشغيل مرتبط بالمخرجات','تمويل تكاليف مباشرة لخدمة محددة مع مؤشرات شهرية.'),('تشغيل انتقالي','تمويل لفترة محدودة مع خطة تنويع دخل.'),('تمويل وظيفة أثر','ربط الراتب بوظيفة حرجة ومخرجات قابلة للقياس.')],
'تمكين اقتصادي': [('أصل إنتاجي جاهز','معدات مجهزة وترخيص وتدريب وتشغيل تجريبي.'),('مجمع مشترك','موقع منظم وخدمات مشتركة تخفض التكاليف.'),('قناة رقمية مكملة','ربط البيع الميداني بطلبات رقمية وتوصيل.')],
'وقف وتنمية مستدامة': [('مخصص سنوي من العوائد','توجيه جزء من الريع لخدمة محددة ذات أولوية.'),('صندوق متجدد','تمويل متكرر دون استهلاك أصل الوقف.'),('تمكين تدريجي','نقل المستفيد من الاعتماد إلى الاستقلال.')]
}
STAGE={'idea':'stage-idea','verify':'stage-verify','execute':'stage-execute','close':'stage-close'}

def e(x): return html.escape(str(x))

def links(card):
    parts=['<div class="model-title">نماذج دورة المشروع - 11 نموذج Word</div><div class="model-grid">']
    for t in tpls:
        href=f"{raw}/{card['id']}/{t['key']}.docx"
        parts.append(f'<a class="model {STAGE[t["stage"]]}" href="{href}">{e(t["emoji"])} {e(t["label"])}</a>')
    parts.append(f'<a class="model repo" href="{repo_url}/tree/main/docs/{card["id"]}">GitHub ↗</a>')
    parts.append('</div>')
    return ''.join(parts)

def opp_card(c):
    ideas=COMMON.get(c['field'],COMMON['أسري واجتماعي'])
    z='<div class="warning">تنبيه زكوي: التحقق من أهلية المصرف والمستفيد وآلية الصرف إلزامي قبل التنفيذ.</div>' if c['fund']=='زكاة' else ''
    rows=''.join(f'<tr><td>{i}</td><td>{e(a)}</td><td>{e(b)}</td></tr>' for i,(a,b) in enumerate(ideas,1))
    return f'''<section class="card" id="{c['id']}"><h3>{c['n']}. {e(c['name'])}</h3><div class="meta">المجال: {e(c['field'])} | التمويل: {e(c['fund'])}</div><table><thead><tr><th>#</th><th>فكرة مشروع</th><th>القيمة/الوصف</th></tr></thead><tbody>{rows}</tbody></table>{z}<div class="gate">بوابة الجاهزية: توثيق الحاجة، الاستحقاق، الميزانية، مسؤول التنفيذ، المؤشرات، المخاطر، وخطة الإغلاق.</div>{links(c)}</section>'''

def app_card(c):
    return f'''<section class="card appendix" id="{c['id']}"><h3>{c['n']}. {e(c['name'])}</h3><p><strong>الوصف:</strong> {e(c['desc'])}</p><p><strong>الميزانية التقديرية:</strong> {e(c['budget'])}</p><p><strong>المدة:</strong> {e(c['months'])}</p><div class="gate">بوابة ما قبل التنفيذ: إثبات الاحتياج والاستحقاق، اعتماد النطاق والميزانية، التحقق من الموافقات، وإقفال التعاقد قبل بدء الصرف.</div><p><strong>الإغلاق:</strong> تقرير فني ومالي، محاضر الاستلام، قائمة المستفيدين/الأصول، نتائج المؤشرات، قياس بعدي، تسوية الالتزامات، أرشفة الأدلة، وخطة الاستدامة.</p>{links(c)}</section>'''

registry=''.join(f'<tr><td>{c["n"]}</td><td><a href="#{c["id"]}">{e(c["name"])}</a></td><td>{e(c["fund"])}</td><td>{e(c["field"])}</td><td>{c["count"]}</td></tr>' for c in opps)
opphtml=''.join(opp_card(c) for c in opps)
sections=[]
last=None
for c in apps:
    if c['section']!=last:
        sections.append(f'<h2>{e(c["section"])}</h2>'); last=c['section']
    sections.append(app_card(c))
apphtml=''.join(sections)
disability=[('بيتي باستقلالية','تهيئة المنزل وظيفيًا: وصول، حمام، أبواب، مسارات، سلامة وتحكم بسيط.'),('زواج واستقرار','حزمة زواج وسكن مهيأ وإرشاد أسري ومالي.'),('مركبتي باستقلال','تعديل مركبة قائمة أو توفير حلول نقل مهيأ.'),('منزلي الذكي','حلول تحكم وإضاءة وأبواب وتنبيهات.'),('حمام آمن','تهيئة دورات المياه لتقليل السقوط.'),('مطبخي المستقل','تعديل ارتفاعات ومساحات وأدوات المطبخ.'),('عودة للعمل','تقييم وظيفي وتدريب وأدوات مساعدة.'),('أول بيت','تهيئة سكن مستقل للشباب القادرين.'),('أبوة وأمومة مهيأة','تعديلات منزلية لرعاية الأطفال.'),('نسك ميسر','خدمة عمرة/حج مهيأة بالنقل والمرافقة.'),('راحة مقدم الرعاية','ساعات رعاية بديلة أو خدمة إسناد مؤقت.'),('وصول تعليمي','أجهزة وبرمجيات مساعدة ووصول رقمي.')]
disrows=''.join(f'<tr><td>{i}</td><td>{e(a)}</td><td>{e(b)}</td></tr>' for i,(a,b) in enumerate(disability,1))

css='''@font-face{font-family:NotoNaskh;src:local("Noto Naskh Arabic")}*{box-sizing:border-box}html{direction:rtl}body{font-family:NotoNaskh,"Arial",sans-serif;direction:rtl;text-align:right;color:#1a1a1a;margin:0 auto;max-width:1000px;padding:28px;line-height:1.65;font-size:14pt}.cover{min-height:92vh;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;background:linear-gradient(135deg,#0d5c4a,#0a4638);color:white;padding:50px;border-radius:12px;page-break-after:always}.cover h1{font-size:34pt;margin:0 0 12px}.cover h2{color:#e2bd43;font-size:20pt}.cover a{color:#e8f3ef}.cover .stats{margin-top:28px;background:rgba(255,255,255,.1);padding:14px 24px;border-radius:10px}.callout,.gate,.warning{padding:12px 15px;border-radius:6px;margin:12px 0}.callout{background:#faf3dd;border-right:5px solid #c9a227}.gate{background:#e8f3ef;border-right:5px solid #0d5c4a;color:#0d5c4a;font-weight:bold}.warning{background:#fff6d9;border-right:5px solid #c9a227;color:#765b0d}h1{color:#0d5c4a;border-bottom:3px solid #c9a227;padding-bottom:7px;margin-top:36px;font-size:22pt;page-break-after:avoid}h2{color:#0d5c4a;background:#e8f3ef;padding:8px 13px;border-right:5px solid #0d5c4a;font-size:17pt;page-break-after:avoid}h3{color:#0d5c4a;font-size:15pt;margin:0 0 8px;page-break-after:avoid}.toc{background:#f8f9fa;border:1px solid #ddd;padding:18px 24px;border-radius:8px}.toc a{color:#0d5c4a;text-decoration:none}table{width:100%;border-collapse:collapse;margin:10px 0;font-size:10.5pt;direction:rtl}th{background:#0d5c4a;color:white;padding:7px;border:1px solid #0d5c4a;text-align:right}td{padding:6px 7px;border:1px solid #d4d4d4;vertical-align:top}tr:nth-child(even) td{background:#fafafa}.card{border:1px solid #d4d4d4;border-radius:8px;padding:15px 18px;margin:15px 0;background:#fff;page-break-inside:avoid}.card .meta{font-size:10.5pt;background:#e8f3ef;color:#0d5c4a;padding:6px 10px;border-radius:6px;margin-bottom:8px;font-weight:bold}.appendix p{margin:5px 0}.model-title{font-size:9.5pt;font-weight:bold;color:#0d5c4a;margin-top:10px;padding-top:8px;border-top:1px dashed #ccc}.model-grid{display:flex;flex-wrap:wrap;gap:5px;margin-top:5px}.model{display:inline-block;text-decoration:none;padding:4px 7px;border-radius:12px;font-size:8.2pt;font-weight:bold;border:1px solid}.stage-idea{background:#e7f4ed;color:#17663b;border-color:#9bc9ae}.stage-verify{background:#fff6d9;color:#8a6814;border-color:#dec56d}.stage-execute{background:#e7f0fb;color:#225d9b;border-color:#9abce0}.stage-close{background:#f1e8f7;color:#6b3b87;border-color:#c6a6d8}.repo{background:#f2f2f2;color:#444;border-color:#bbb}.legend{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:14px 0}.legend div{padding:9px;border-radius:6px;font-size:10pt;font-weight:bold}.l1{background:#e7f4ed;color:#17663b}.l2{background:#fff6d9;color:#8a6814}.l3{background:#e7f0fb;color:#225d9b}.l4{background:#f1e8f7;color:#6b3b87}.footer-note{font-size:9pt;color:#666;border-top:1px solid #ddd;margin-top:30px;padding-top:10px}@page{size:A4;margin:12mm}@media print{body{padding:0;font-size:11pt;max-width:none}.cover{border-radius:0}.card{box-shadow:none;margin:10px 0;padding:11px 13px}.model{font-size:6.8pt;padding:3px 5px}.model-title{font-size:7.5pt}table{font-size:8pt}.legend{grid-template-columns:repeat(4,1fr)}a{color:inherit}}'''

html_doc=f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>محفظة مشاريع وفرص منصة إحسان</title><style>{css}</style></head><body>
<section class="cover"><h1>محفظة مشاريع وفرص منصة إحسان</h1><h2>بالشراكة مع الجمعيات الأهلية</h2><p>بنك الفرص + بنك الأفكار + دورة المشروع من الفكرة إلى الإغلاق</p><div class="stats">96 فرصة + 80 مشروعًا = <strong>176 بطاقة</strong><br>11 نموذج Word لكل بطاقة = <strong>1,936 نموذجًا</strong></div><p>إعداد: عيسى بن عبدالله الألمعي<br><a href="https://alalmaiesa.site">alalmaiesa.site</a><br><a href="{repo_url}">GitHub: ehsan-project-portfolio</a><br>الإصدار 6.0 | 27 سبتمبر 2026</p></section>
<div class="callout"><strong>صفة الوثيقة:</strong> وثيقة عمل داخلية لإعداد مشاريع قابلة للتقديم عبر فرص منصة إحسان والمانحين. ليست وثيقة صادرة عن منصة إحسان، وتخضع كل فرصة للتوفر الفعلي وضوابط المنصة والجهة والأنظمة وقت التقديم.</div>
<div class="toc"><h1>الفهرس</h1><ol><li><a href="#use">كيف تستخدم المحفظة</a></li><li><a href="#gov">الإطار التنفيذي والحوكمي</a></li><li><a href="#registry">سجل الفرص الـ96</a></li><li><a href="#bank">بنك الأفكار والنماذج</a></li><li><a href="#disability">محفظة نوعية لذوي الإعاقة</a></li><li><a href="#appendix">الملحق - 80 مشروعًا مطورًا</a></li><li><a href="#management">قوالب الإدارة والتقييم</a></li></ol></div>
<h1 id="use">1. كيف تستخدم هذه المحفظة</h1><p>يبدأ العمل بفكرة موثقة، ثم التحقق من الاستحقاق، والتصميم، والميزانية والتعاقد، ثم التنفيذ والرقابة، فقياس الأثر والإغلاق. تحت كل بطاقة توجد 11 وصلة لنماذج Word مرتبطة مباشرة بمستودع GitHub.</p>
<table><thead><tr><th>المرحلة</th><th>بوابة القرار</th><th>المخرج الإلزامي</th></tr></thead><tbody><tr><td>الفكرة</td><td>هل تعالج مشكلة موثقة؟</td><td>بطاقة فكرة + دراسة + ميثاق</td></tr><tr><td>التحقق</td><td>هل المستفيد مؤهل؟</td><td>معايير استحقاق + بحث اجتماعي</td></tr><tr><td>التنفيذ</td><td>هل الشراء والتنفيذ منضبطان؟</td><td>مقارنة عروض + استلام + تقارير + مخاطر</td></tr><tr><td>الإغلاق</td><td>هل أغلقت ماليًا وفنيًا؟</td><td>تقرير إغلاق + قائمة أدلة</td></tr></tbody></table>
<div class="legend"><div class="l1">🟢 الفكرة: 3 نماذج</div><div class="l2">🟡 التحقق: نموذجان</div><div class="l3">🔵 التنفيذ: 4 نماذج</div><div class="l4">🟣 الإغلاق: نموذجان</div></div>
<h1 id="gov">2. الإطار التنفيذي والحوكمي المشترك</h1><ul><li>الاستحقاق: معايير مكتوبة ووثائق إثبات ومنع الازدواجية.</li><li>الشراء والتعاقد: مواصفات فنية ومقارنة عروض أو دراسة سوق.</li><li>الصرف: دفعات مرتبطة بالإنجاز ومحاضر الاستلام.</li><li>التوثيق: ملف إلكتروني للمستفيد والعقود والفواتير والأدلة.</li><li>قياس الأثر: خط أساس ومؤشرات مخرج ونتيجة.</li><li>إدارة المخاطر: سجل مخاطر ومالك لكل خطر وإجراء استجابة.</li><li>تعارض المصالح: إفصاح ومراجعة قبل الترسية.</li><li>الإغلاق: إقفال مالي وفني ودروس واستدامة.</li></ul>
<h1 id="registry">3. سجل جميع الفرص (96 فرصة)</h1><table><thead><tr><th>#</th><th>الفرصة</th><th>مسار التمويل</th><th>المجال</th><th>عدد الأفكار</th></tr></thead><tbody>{registry}</tbody></table>
<h1 id="bank">4. بنك الأفكار لكل فرصة + النماذج</h1><p>كل بطاقة في هذا الفصل مرتبطة بمجلد مستقل داخل GitHub يحتوي 11 نموذج Word يغطي دورة المشروع كاملة.</p>{opphtml}
<h1 id="disability">5. محفظة نوعية لذوي الإعاقة</h1><table><thead><tr><th>#</th><th>الفكرة</th><th>الوصف النوعي</th></tr></thead><tbody>{disrows}</tbody></table><div class="gate">معيار الاختيار: الأولوية للمشروع الذي يرفع الاستقلال والاندماج ويملك نتيجة قابلة للقياس.</div>
<h1 id="appendix">6. الملحق التفصيلي - 80 مشروعًا مطورًا</h1><p>لكل مشروع مطور 11 نموذج Word خاص به، بالإضافة إلى بيانات الميزانية والمدة والوصف.</p>{apphtml}
<h1 id="management">7. قوالب الإدارة والتقييم</h1><h2>7.1 بوابة قرار التفعيل</h2><table><thead><tr><th>السؤال</th><th>نعم/لا</th><th>الدليل</th></tr></thead><tbody>{''.join('<tr><td>'+x+'</td><td></td><td></td></tr>' for x in ['هل الفرصة متاحة وقت التقديم؟','هل المستفيد/الموقع مؤهل؟','هل الحاجة موثقة؟','هل توجد الموافقات اللازمة؟','هل الميزانية مدعومة بعروض؟','هل المؤشرات قابلة للقياس؟','هل توجد جهة تتحمل التشغيل؟','هل مخاطر السلامة مضبوطة؟'])}</tbody></table><h2>7.2 مصفوفة التقييم قبل الرفع</h2><table><thead><tr><th>المعيار</th><th>الوزن</th><th>الدرجة 1-5</th><th>الدليل</th></tr></thead><tbody>{''.join('<tr><td>'+a+'</td><td>'+b+'</td><td></td><td></td></tr>' for a,b in [('وضوح المشكلة','10%'),('وضوح المستفيد والاستحقاق','10%'),('جودة التصميم وقابلية القياس','15%'),('واقعية الميزانية','15%'),('جودة الشراء والتعاقد','10%'),('خطة التنفيذ والرقابة','10%'),('مؤشرات الأثر وخط الأساس','10%'),('خطة الإغلاق والاستدامة','10%'),('إدارة المخاطر والخصوصية','10%')])}</tbody></table>
<div class="footer-note">المستودع: <a href="{repo_url}">{repo_url}</a> | GitHub Pages: <a href="{pages}">{pages}</a></div>
</body></html>'''
(ROOT/'index-static.html').write_text(html_doc,encoding='utf-8')
(ROOT/'index.html').write_text(html_doc,encoding='utf-8')
print('wrote',ROOT/'index-static.html', 'size', len(html_doc.encode('utf-8')))
