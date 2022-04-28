'''* @file PubMed_preprint_converter.py
   * @brief convert preprint files from ris to PubMed xml
   * @author Daniel
   * @date 2020-10-21 '''

import re

print('預刊版本')

filename = input('請輸入檔案名稱，例test.ris: ')
file = open(filename, mode='r', encoding='utf8')

lines = file.readlines()
records = []
temp, AU, KW = {}, [], []

count = 0

for line in lines:
        
    if(len(line) > 1):
        text = re.findall('(^[A-Z][A-Z\d])  - (.*)', line)[0]
        
        if(text[0]=='AU'):
            AU.append(text[1])
            
        elif(text[0]=='KW'):
            KW.append(text[1])
            
        elif(text[0]=='ER'):
            count += 1
            temp['AU'] = AU
            if(len(KW)) > 0:
                temp['KW'] = KW
            
            records.append(temp)
            temp, AU, KW = {}, [], []
            
        else:
            temp[text[0]] = text[1]

preprint_date = input('請輸入預刊日期，例2020-02-01： ')

pre_year, pre_mon, pre_day = preprint_date.split('-')

output = '''<!DOCTYPE ArticleSet PUBLIC "-//NLM//DTD PubMed 2.7//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/in/PubMed.dtd">
<ArticleSet>
'''

for record in records:
    output += '''<Article>
        <Journal>
            <PublisherName>Taiwan Society of Anesthesiologists</PublisherName>
            <JournalTitle>Asian J Anesthesiol.</JournalTitle>
            <Issn>2468-824X</Issn>'''
    output += '<Volume/><Issue/>'
    output += '<PubDate PubStatus="aheadofprint"><Year>{}</Year><Month>{}</Month><Day>{}</Day></PubDate>'.format(pre_year, pre_mon, pre_day)
    output += '</Journal><ArticleTitle>{}</ArticleTitle>'.format(record['T1'])
    output += '<FirstPage/><LastPage/>'
    output += '<ELocationID EIdType="doi">{}</ELocationID>'.format(record['DO'])
    output += '<Language>EN</Language>'
    
    output += '<AuthorList>'
    for author in record['AU']:
        name = author.split(' ')
        first_name = ' '.join(name[0:-1])
        last_name = name[-1]
    
        output += '<Author>'
        output += '<FirstName>{}</FirstName>'.format(first_name)
        output += '<LastName>{}</LastName>'.format(last_name)
        output += '<AffiliationInfo><Affiliation></Affiliation></AffiliationInfo>'
        output += '</Author>'
    output += '</AuthorList>'
    
    output += '<ArticleIdList><ArticleId IdType="doi">{}</ArticleId></ArticleIdList>'.format(record['DO'])
    
    
    try:
        output += '<Abstract>{}</Abstract>'.format(record['AB'])
    except:
        output += ''
        
    output += '</Article>'
    
output += '</ArticleSet>'

file = open('{}_preprint.xml'.format(preprint_date),mode='w', encoding='utf8')
file.write(output)
file.close()
print('Done! 記得增加作者機構欄位<Affiliation>')