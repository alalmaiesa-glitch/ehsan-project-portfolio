from pathlib import Path
import json, html, zipfile

ROOT = Path(__file__).resolve().parents[1]
CARDS = json.loads((ROOT/'data/cards.json').read_text(encoding='utf-8'))
TEMPLATES = json.loads((ROOT/'data/templates.json').read_text(encoding='utf-8'))
OUT = ROOT/'docs'
OUT.mkdir(exist_ok=True)

PRIMARY='0D5C4A'; GOLD='C9A227'; BLUE='2F75B5'; PURPLE='7030A0'; GREEN='217346'

CT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
RELS='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
DOCRELS='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
STYLES='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/><w:sz w:val="28"/><w:szCs w:val="28"/><w:rtl/></w:rPr></w:rPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/><w:qFormat/><w:pPr><w:bidi/><w:jc w:val="right"/></w:pPr></w:style>
</w:styles>'''
CORE='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><dc:title>محفظة إحسان - نموذج مشروع</dc:title><dc:creator>عيسى بن عبدالله الألمعي</dc:creator><cp:lastModifiedBy>ChatGPT</cp:lastModifiedBy></cp:coreProperties>'''
APP='''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes"><Application>Microsoft Office Word</Application></Properties>'''

def esc(s): return html.escape(str(s), quote=False)

def run(text,bold=False,color=None,size=28):
    props=['<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:cs="Arial"/>','<w:rtl/>',f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/>']
    if bold: props.append('<w:b/>')
    if color: props.append(f'<w:color w:val="{color}"/>')
    return f'<w:r><w:rPr>{"".join(props)}</w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

def p(text='',bold=False,color=None,size=28,center=False,space_after=100):
    jc='center' if center else 'right'
    return f'<w:p><w:pPr><w:bidi/><w:jc w:val="{jc}"/><w:spacing w:after="{space_after}"/></w:pPr>{run(text,bold,color,size)}</w:p>'

def heading(text,color=PRIMARY): return p(text,True,color,32,False,120)
def bullet(text): return p('• '+text,False,None,28,False,60)

def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def tc(text,bold=False,fill=None,color=None,size=23):
    shd=f'<w:shd w:fill="{fill}"/>' if fill else ''
    return f'<w:tc><w:tcPr><w:tcW w:w="4500" w:type="dxa"/>{shd}<w:vAlign w:val="top"/></w:tcPr>{p(text,bold,color,size,False,40)}</w:tc>'

def table(headers,rows,head_color=PRIMARY,size=22):
    parts=['<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:bidiVisual/><w:tblBorders><w:top w:val="single" w:sz="4" w:color="B7B7B7"/><w:left w:val="single" w:sz="4" w:color="B7B7B7"/><w:bottom w:val="single" w:sz="4" w:color="B7B7B7"/><w:right w:val="single" w:sz="4" w:color="B7B7B7"/><w:insideH w:val="single" w:sz="4" w:color="D9D9D9"/><w:insideV w:val="single" w:sz="4" w:color="D9D9D9"/></w:tblBorders></w:tblPr>']
    parts.append('<w:tr>'+''.join(tc(h,True,head_color,'FFFFFF',size) for h in headers)+'</w:tr>')
    for row in rows:
        parts.append('<w:tr>'+''.join(tc(v,False,None,None,size) for v in row)+'</w:tr>')
    parts.append('</w:tbl>')
    return ''.join(parts)

def identity(card):
    return table(['الحقل','البيان'],[
        ['اسم المشروع/الفرصة',card['name']],['المجال',card.get('field','[يحدد]')],['مسار التمويل',card.get('fund','[يحدد]')],
        ['الجهة المشرفة','[اسم الجمعية]'],['النطاق الجغرافي','[المدينة/المنطقة]'],['عدد المستفيدين','[يحدد بعد التحقق]']
    ],PRIMARY,22)

def context(card):
    desc=card.get('desc') or f"مشروع مرتبط بفرصة {card['name']} ضمن مجال {card.get('field','')}، ويُخصص وفق احتياج المستفيدين وضوابط الجهة."
    return desc, card.get('budget','[يحدد بعد عروض الأسعار]'), card.get('months','[تحدد بعد اعتماد النطاق]')

def body(card,t):
    key=t['key']; label=t['label']; stage=t['stage']; desc,budget,duration=context(card)
    stage_color={'idea':GREEN,'verify':GOLD,'execute':BLUE,'close':PURPLE}[stage]
    out=[p(label,True,stage_color,36,True,80),p(card['name'],True,PRIMARY,30,True,60),p(f"رمز البطاقة: {card['id']} | وثيقة عمل داخلية",False,'666666',20,True,100),identity(card),p('يتضمن هذا النموذج في صفحاته الأخيرة ملحقًا بعنوان: مطالبة احترافية للذكاء الاصطناعي لتوليد دراسة المشروع من الفكرة إلى الإغلاق.',True,PRIMARY,22,False,120)]
    if key=='idea-card':
        out += [heading('ملخص الفكرة',GREEN),p(desc),table(['العنصر','المطلوب'],[[x,'[يستكمل]'] for x in ['المشكلة','الدليل على الاحتياج','الفئة المستهدفة','الحل المقترح','المخرجات','النتائج المتوقعة','التكلفة الأولية','الشركاء','المخاطر الأولية','قرار الانتقال للدراسة']],GREEN)]
    elif key=='project-study':
        out += [heading('1. المشكلة ومبررات التدخل',GREEN),p(desc),heading('2. الأهداف والمستفيدون',GREEN),bullet('إغلاق فجوة الاحتياج وتحقيق نتيجة قابلة للقياس.'),bullet('تحديد المستفيدين وفق معايير مكتوبة ومنع الازدواجية.'),heading('3. خطة التنفيذ',GREEN),table(['المرحلة','الأنشطة','المدة','المخرج'],[['التحقق','حصر وتحقق واستحقاق','1-2 أسبوع','قائمة معتمدة'],['التصميم','نطاق ومواصفات وخطة','2 أسبوع','ميثاق وخطة'],['التعاقد','عروض واعتماد مورد','2-4 أسبوع','عقد/أمر شراء'],['التنفيذ','تنفيذ ومتابعة واستلام',duration,'مخرجات موثقة'],['الإغلاق','قياس وإقفال','2 أسبوع','تقرير إغلاق']],GREEN),heading('4. الميزانية التقديرية',GREEN),p(f'التقدير المرجعي: {budget}. تعتمد الميزانية النهائية على الكميات وعروض الأسعار المعتمدة.'),table(['البند','الوحدة','الكمية','سعر الوحدة','الإجمالي'],[[x,'[ ]','[ ]','[ ]','[ ]'] for x in ['الخدمة/الأصل الأساسي','التجهيز والتنفيذ','اللوجستيات','قياس الأثر والتوثيق']],GREEN),heading('5. مؤشرات الأداء',GREEN),table(['المؤشر','خط الأساس','المستهدف','مصدر التحقق'],[[x,'[ ]','[ ]','[ ]'] for x in ['عدد المستفيدين المكتملين','نسبة الإنجاز المطابق','تكلفة المستفيد/الوحدة','رضا المستفيد','مؤشر النتيجة النهائية']],GREEN),heading('6. المخاطر والاستدامة',GREEN),p('تحدد المخاطر الفنية والمالية والتشغيلية ومالك كل خطر، مع خطة استدامة وصيانة/متابعة بعد الإغلاق.')]
    elif key=='project-charter':
        out += [heading('ميثاق المشروع',GREEN),table(['البند','الاعتماد'],[[x,'[يستكمل]'] for x in ['الهدف العام','النطاق داخل المشروع','خارج النطاق','المخرجات','المستفيدون','الميزانية المعتمدة','المدة','مدير المشروع','الجهات الشريكة','معايير القبول','صلاحيات التغيير','موافقات البدء']],GREEN)]
    elif key=='eligibility':
        out += [heading('معايير الاستحقاق',GOLD),table(['المعيار','الأولوية','دليل الإثبات','قرار'],[[x,'[ ]','[ ]','☐ مؤهل ☐ غير مؤهل'] for x in ['الانطباق على الفئة','الحاجة الفعلية','الدخل/القدرة المالية','عدم الازدواجية','النطاق الجغرافي','أولوية الحالة','الموافقات الخاصة']],GOLD),p('تنبيه: لمسارات الزكاة يجب توثيق أهلية المصرف والمستفيد وفق الضوابط المعتمدة لدى الجهة والمنصة.')]
    elif key=='social-research':
        out += [heading('نموذج البحث الاجتماعي',GOLD),table(['المحور','البيانات/الملاحظات'],[[x,'[يستكمل]'] for x in ['بيانات الأسرة الضرورية','الوضع السكني','الدخل والالتزامات','الحالة الصحية/التعليمية عند الصلة','مصادر الدعم الحالية','وصف الاحتياج','زيارة ميدانية/إثبات','توصية الباحث','قرار اللجنة']],GOLD)]
    elif key=='offers-comparison':
        out += [heading('مقارنة العروض',BLUE),table(['المعيار','المورد 1','المورد 2','المورد 3'],[[x,'[ ]','[ ]','[ ]'] for x in ['السعر الإجمالي','المواصفات','مدة التنفيذ','الضمان','شروط الدفع','خبرة المورد','الالتزام النظامي','الدرجة النهائية']],BLUE),p('قرار الترسية: [اسم المورد] — المبرر: [يستكمل] — تعارض المصالح: ☐ تم التحقق.')]
    elif key=='acceptance-minutes':
        out += [heading('محضر الاستلام',BLUE),table(['البند','الحالة','الملاحظة'],[[x,'☐ مطابق ☐ غير مطابق','[ ]'] for x in ['الكمية','المواصفات','الجودة','التركيب/التشغيل','السلامة','الضمان','المستندات']],BLUE),p('قرار الاستلام: ☐ نهائي ☐ مشروط ☐ مرفوض | أسماء وتوقيعات لجنة الاستلام: [يستكمل].')]
    elif key=='progress-report':
        out += [heading('التقرير المرحلي',BLUE),table(['المؤشر','المخطط','المنجز','الانحراف','الإجراء'],[[x,'[ ]','[ ]','[ ]','[ ]'] for x in ['الزمن','المخرجات','المستفيدون','الميزانية','الجودة','المخاطر']],BLUE),heading('أبرز الإنجازات والتحديات',BLUE),p('[يستكمل]')]
    elif key=='risk-register':
        out += [heading('سجل المخاطر',BLUE),table(['الخطر','الاحتمال','الأثر','التقييم','الاستجابة','المالك','الحالة'],[[f'خطر {i}','[1-5]','[1-5]','[ ]','[تجنب/تخفيف/نقل/قبول]','[ ]','[مفتوح/مغلق]'] for i in range(1,7)],BLUE)]
    elif key=='closure-report':
        out += [heading('تقرير الإغلاق',PURPLE),table(['القسم','النتيجة/الدليل'],[[x,'[يستكمل]'] for x in ['ملخص التنفيذ','النطاق المنجز','المستفيدون الفعليون','الميزانية والانحراف','العقود والالتزامات','الاستلام النهائي','نتائج المؤشرات','قياس الأثر','الأصول والضمانات','الدروس المستفادة','خطة الاستدامة']],PURPLE)]
    elif key=='evidence-checklist':
        out += [heading('قائمة الأدلة',PURPLE),table(['الدليل','مطلوب','مرفق','المرجع'],[[x,'☑','☐','[ ]'] for x in ['اعتماد المشروع','قائمة المستفيدين المحمية','إثباتات الاستحقاق','عروض الأسعار','العقد/أمر الشراء','الفواتير','محاضر الاستلام','صور/توثيق التنفيذ','تقارير التقدم','نتائج المؤشرات','تقرير الإغلاق']],PURPLE)]
    out.append(p('هذه الوثيقة قالب عمل داخلي قابل للتخصيص وليست نموذجًا رسميًا صادرًا عن منصة إحسان.',False,'777777',20,False,20))
    out.append(page_break())
    out.append(ai_prompt_appendix(card))
    return ''.join(out)

def ai_prompt_appendix(card):
    desc,budget,duration=context(card)
    zakat_note = 'هذا المشروع ضمن مسار الزكاة؛ افصل بوضوح بين ما يحتاج تحققًا شرعيًا/نظاميًا وبين الافتراضات، ولا تجزم بأهلية المصرف أو المستفيد دون دليل معتمد.' if card.get('fund')=='زكاة' else 'تحقق من مسار التمويل وضوابط الجهة والفرصة وقت التقديم، ولا تفترض متطلبات رسمية غير موثقة.'
    prompt_lines = [
        'أنت مستشار أول في تصميم وإدارة المشاريع التنموية وغير الربحية وقياس الأثر، ومهمتك تحويل الفكرة التالية إلى دراسة مشروع تنفيذية متكاملة من الفكرة حتى الإغلاق.',
        '',
        'بيانات المشروع المتاحة:',
        f"- اسم الفرصة/المشروع: {card['name']}",
        f"- المجال: {card.get('field','[يحدد]') or '[يحدد]'}",
        f"- مسار التمويل: {card.get('fund','[يحدد]') or '[يحدد]'}",
        f"- الوصف الأولي: {desc}",
        f"- الميزانية المرجعية إن وجدت: {budget}",
        f"- المدة المرجعية إن وجدت: {duration}",
        '',
        'قواعد إلزامية قبل الكتابة:',
        '1) لا تختلق أرقامًا أو نسبًا أو اشتراطات أو مصادر أو موافقات. أي معلومة غير متاحة ضع أمامها [يحتاج تحقق] أو [افتراض عمل] بحسب الحالة.',
        '2) افصل بوضوح بين: الحقائق المتاحة، الافتراضات، البيانات المطلوبة، والتوصيات.',
        '3) إذا كانت البيانات غير كافية، لا توقف العمل؛ أنشئ مسودة تنفيذية قابلة للاستكمال، ثم ضع قائمة قصيرة بالأسئلة الحرجة في النهاية.',
        '4) لا تنسب أي متطلب إلى منصة إحسان أو جهة تنظيمية إلا إذا زودتك به صراحة أو كان ضمن مصدر موثق مقدم لك.',
        f'5) {zakat_note}',
        '6) اجعل المخرجات عملية وقابلة للنسخ إلى ملف مشروع، مع جداول واضحة حيث يلزم.',
        '7) اربط كل هدف بمؤشر، وكل مؤشر بمصدر تحقق، وكل خطر بمالك وإجراء استجابة.',
        '8) ميّز بين المخرجات Outputs والنتائج Outcomes والأثر Impact، ولا تخلط بينها.',
        '9) راعِ حماية بيانات المستفيدين والخصوصية وتقليل البيانات الحساسة إلى الحد الضروري.',
        '',
        'أنشئ الدراسة بالترتيب التالي:',
        'أولًا: الملخص التنفيذي — تعريف مختصر بالمشكلة، الحل، المستفيدين، القيمة التنموية، المدة والتكلفة المرجعية.',
        'ثانيًا: تعريف المشكلة والاحتياج — وصف المشكلة، أسبابها، حجمها، الفجوة الحالية، وما الأدلة المطلوبة لإثباتها.',
        'ثالثًا: الفئة المستهدفة والاستحقاق — الشرائح، العدد المتوقع، النطاق الجغرافي، معايير الأهلية، الأولوية، منع الازدواجية، وآلية التحقق.',
        'رابعًا: نظرية التغيير — المدخلات، الأنشطة، المخرجات، النتائج قصيرة/متوسطة المدى، والأثر المتوقع، مع أهم الافتراضات.',
        'خامسًا: الهدف العام والأهداف التفصيلية — أهداف SMART قابلة للقياس ومتصلة بالمشكلة.',
        'سادسًا: نطاق المشروع — ما يدخل في المشروع وما يخرج منه، وحدود المسؤولية والتسليمات النهائية.',
        'سابعًا: نموذج التدخل والأنشطة — مسار المستفيد أو الخدمة خطوة بخطوة من التسجيل/الترشيح حتى الاستلام والمتابعة.',
        'ثامنًا: خطة التنفيذ والجدول الزمني — مراحل، أنشطة، مسؤوليات، تبعيات، معالم رئيسية، ومدة تقديرية.',
        'تاسعًا: أصحاب المصلحة والحوكمة — الجهة المالكة، مدير المشروع، الشركاء، الموردون، لجان الاعتماد والاستلام، ومصفوفة RACI مختصرة.',
        'عاشرًا: الميزانية — بنود التكلفة، الكميات، سعر الوحدة، الإجمالي، الاحتياطي إن لزم، وافصل ما هو تقديري عما يحتاج عروض أسعار.',
        'الحادي عشر: الشراء والتعاقد — المواصفات، آلية المقارنة، معايير الترسية، الضمان، الدفع مقابل الإنجاز، ومحاضر الاستلام.',
        'الثاني عشر: سجل المخاطر — المخاطر التشغيلية والمالية والفنية والسمعة والخصوصية والسلامة، الاحتمال، الأثر، الاستجابة، المالك، ومؤشرات الإنذار.',
        'الثالث عشر: مؤشرات الأداء وقياس الأثر — خط الأساس، المستهدف، طريقة الحساب، مصدر البيانات، دورية القياس، ومسؤول القياس.',
        'الرابع عشر: الجودة والمتابعة والتقارير — نقاط الرقابة، قبول المخرجات، التقارير المرحلية، إدارة التغيير والانحرافات.',
        'الخامس عشر: الاستدامة — التشغيل بعد التمويل، الصيانة، ملكية الأصول، الشراكات، التمويل المستمر، وخطة الخروج عند الحاجة.',
        'السادس عشر: خطة الإغلاق — الاستلام النهائي، الإقفال المالي والتعاقدي، قياس النتائج، توثيق الأصول والضمانات، الدروس المستفادة، وأرشفة الأدلة.',
        'السابع عشر: قائمة الأدلة المطلوبة — صنفها إلى: احتياج واستحقاق، تصميم واعتمادات، شراء وتعاقد، تنفيذ واستلام، مالية، قياس أثر، وإغلاق.',
        'الثامن عشر: بوابات القرار — ضع قرار Go / Revise / Stop عند نهاية مراحل الفكرة، التحقق، التصميم، الميزانية، التعاقد، التنفيذ والإغلاق، مع شروط كل قرار.',
        'التاسع عشر: قائمة النواقص والأسئلة الحرجة — لا تزيد على 12 سؤالًا، مرتبة حسب ما يمنع اعتماد المشروع.',
        '',
        'صيغة الإخراج المطلوبة:',
        '- اكتب بالعربية المهنية الواضحة وباتجاه منطقي مناسب للمستندات التنفيذية.',
        '- استخدم جداول للميزانية، الخطة الزمنية، المؤشرات، المخاطر، RACI، وقائمة الأدلة.',
        '- استخدم أرقامًا فقط إذا كانت مقدمة في البيانات أو عرّفها صراحة كافتراض قابل للتعديل.',
        '- ضع في نهاية الدراسة قسمًا بعنوان: سجل الافتراضات ونقاط التحقق.',
        '- اختم بصفحة تنفيذية بعنوان: جاهزية المشروع للرفع/التمويل، تشمل ما اكتمل وما بقي وما يمنع البدء.',
        '',
        'ابدأ الآن بإنتاج الدراسة كاملة وفق ما سبق، ولا تحذف أي مرحلة من مراحل دورة المشروع من الفكرة حتى الإغلاق.'
    ]
    out=[heading('ملحق: مطالبة احترافية للذكاء الاصطناعي',PRIMARY),p('إصدار الملحق: AI-APPENDIX-2 | مخصص تلقائيًا لهذه الفرصة/المشروع.',True,GOLD,20,False,60),
         p('الغرض: نسخ النص التالي إلى أي نموذج ذكاء اصطناعي لتوليد دراسة مشروع تنفيذية متكاملة ومخصصة لهذه الفرصة/المشروع.',False,'555555',22,False,100)]
    for line in prompt_lines:
        if line == '':
            out.append(p('',False,None,20,False,40))
        elif line.endswith(':') or line in ['قواعد إلزامية قبل الكتابة:','أنشئ الدراسة بالترتيب التالي:','صيغة الإخراج المطلوبة:','بيانات المشروع المتاحة:']:
            out.append(p(line,True,PRIMARY,24,False,60))
        else:
            out.append(p(line,False,None,22,False,40))
    out.append(p('ملاحظة استخدام: عند توفر مستندات أو ضوابط أو عروض أسعار أو بيانات مستفيدين، أرفقها مع المطالبة واطلب من النموذج الاعتماد عليها بوصفها المصدر الأساسي وعدم استكمال الفجوات من عنده.',False,'666666',20,False,80))
    return ''.join(out)

def write_docx(path,card,t):
    docxml=f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{body(card,t)}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="964" w:right="1020" w:bottom="964" w:left="1020"/></w:sectPr></w:body></w:document>'''
    path.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml',CT); z.writestr('_rels/.rels',RELS); z.writestr('word/document.xml',docxml); z.writestr('word/_rels/document.xml.rels',DOCRELS); z.writestr('word/styles.xml',STYLES); z.writestr('docProps/core.xml',CORE); z.writestr('docProps/app.xml',APP)

manifest=[]
for card in CARDS:
    for t in TEMPLATES:
        fp=OUT/card['id']/(t['key']+'.docx')
        write_docx(fp,card,t)
        manifest.append({'card_id':card['id'],'card_name':card['name'],'template':t['key'],'label':t['label'],'path':str(fp.relative_to(ROOT)).replace('\\','/')})
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Generated {len(manifest)} DOCX files')
