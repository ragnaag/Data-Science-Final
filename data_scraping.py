from bs4 import BeautifulSoup
import requests
import sqlite3
date=['2010', '2012', '2014', '2016', '2018', '2020']
data={}
affliates={}
for d in date:
    url='https://www.opensecrets.org/pacs/industry.php?txt=B13&cycle='
    url=url+d
    html_doc = requests.get(url)
    html_dump = BeautifulSoup(html_doc.text, 'html.parser')
    rows = html_dump.find_all('td')
    count=0
    for row in rows[9:]:
        if count==5:
            count=0
        if count==0:
            name=row.a.string
            if name not in data:
                data[name]=[]
                link=row.a.get("href").split("=")
                id=link[1].split("&")[0]
                data[name].append(id)
            count+=1
        elif count==1:
            affiliate=row.a.string
            data[name].append(affiliate)
            count+=1
        else:
            amount=row.text.strip('()$')
            amount=amount.replace(",", "")
            amountToAdd=d+"-"+amount
            data[name].append(amountToAdd)
            count+=1
        #print(row)
    #print(count)
for d in date:
    url='https://www.opensecrets.org/pacs/industry.php?txt=B12&cycle='
    url=url+d
    html_doc = requests.get(url)
    html_dump = BeautifulSoup(html_doc.text, 'html.parser')
    rows = html_dump.find_all('td')
    count=0
    for row in rows[9:]:
        if count==5:
            count=0
        if count==0:
            name=row.a.string
            if name not in data:
                data[name]=[]
                link=row.a.get("href").split("=")
                id=link[1].split("&")[0]
                data[name].append(id)
            count+=1
        elif count==1:
            affiliate=row.a.string
            data[name].append(affiliate)
            count+=1
        else:
            amount=row.text.strip('()$')
            amount=amount.replace(",", "")
            amountToAdd=d+"-"+amount
            data[name].append(amountToAdd)
            count+=1


for key in data:
    values=data[key]
    for i in range(1, len(values)):
        if i%4==2:
            total=values[i]
            total=total.split('-')
            date=total[0]
            total=total[1]
            total=int(total)
        if i%4==3:
            dem=values[i]
            dem=dem.split('-')[1]
            dem=int(dem)
        if i%4==0:
            rep=values[i]
            rep=rep.split('-')[1]
            rep=int(rep)
            if total<dem+rep:
                newTotal=dem+rep
                stringTotal=str(newTotal)
                data[key][i-2]=date+'-'+stringTotal


conn = sqlite3.connect('tmb_data.db')
c = conn.cursor()

# Delete tables if they exist
c.execute('DROP TABLE IF EXISTS "pac_donations";')
c.execute('DROP TABLE IF EXISTS "candidate_donations";')


c.execute('CREATE TABLE pac_donations(pacid varchar(255), pacname varchar(255) PRIMARY KEY, "2010-affiliate" varchar(255), "2010-total" INTEGER, "2010-dems" INTEGER, "2010-repubs" INTEGER, "2012-affiliate" varchar(255), "2012-total" INTEGER, "2012-dems" INTEGER, "2012-repubs" INTEGER, "2014-affiliate" varchar(255), "2014-total" INTEGER, "2014-dems" INTEGER, "2014-repubs" INTEGER, "2016-affiliate" varchar(255), "2016-total" INTEGER, "2016-dems" INTEGER, "2016-repubs" INTEGER, "2018-affiliate" varchar(255), "2018-total" INTEGER, "2018-dems" INTEGER, "2018-repubs" INTEGER, "2020-affiliate" varchar(255), "2020-total" INTEGER, "2020-dems" INTEGER, "2020-repubs" INTEGER)')
for key in data:
    values=data[key]
    all_data=[0]*26
    #print(all_data)
    all_data[0]=values[0]
    all_data[1]=key
    for i in range(1, len(values),4):
        year=values[i+1].split("-")[0]
        if year=='2010':
            all_data[2]=values[i]
            total=values[i+1]
            total=total.split('-')[1]
            total=int(total)
            all_data[3]=total
            dem=values[i+2]
            dem=dem.split('-')[1]
            dem=int(dem)
            all_data[4]=dem
            rep=values[i+3]
            rep=rep.split('-')[1]
            rep=int(rep)
            all_data[5]=rep
        if year=='2012':
            all_data[6]=values[i]
            total=values[i+1]
            total=total.split('-')[1]
            total=int(total)
            all_data[7]=total
            dem=values[i+2]
            dem=dem.split('-')[1]
            dem=int(dem)
            all_data[8]=dem
            rep=values[i+3]
            rep=rep.split('-')[1]
            rep=int(rep)
            all_data[9]=rep
        if year=='2014':
            all_data[10]=values[i]
            total=values[i+1]
            total=total.split('-')[1]
            total=int(total)
            all_data[11]=total
            dem=values[i+2]
            dem=dem.split('-')[1]
            dem=int(dem)
            all_data[12]=dem
            rep=values[i+3]
            rep=rep.split('-')[1]
            rep=int(rep)
            all_data[13]=rep
        if year=='2016':
            all_data[14]=values[i]
            total=values[i+1]
            total=total.split('-')[1]
            total=int(total)
            all_data[15]=total
            dem=values[i+2]
            dem=dem.split('-')[1]
            dem=int(dem)
            all_data[16]=dem
            rep=values[i+3]
            rep=rep.split('-')[1]
            rep=int(rep)
            all_data[17]=rep
        if year=='2018':
            all_data[18]=values[i]
            total=values[i+1]
            total=total.split('-')[1]
            total=int(total)
            all_data[19]=total
            dem=values[i+2]
            dem=dem.split('-')[1]
            dem=int(dem)
            all_data[20]=dem
            rep=values[i+3]
            rep=rep.split('-')[1]
            rep=int(rep)
            all_data[21]=rep
        if year=='2020':
            all_data[22]=values[i]
            total=values[i+1]
            total=total.split('-')[1]
            total=int(total)
            all_data[23]=total
            dem=values[i+2]
            dem=dem.split('-')[1]
            dem=int(dem)
            all_data[24]=dem
            rep=values[i+3]
            rep=rep.split('-')[1]
            rep=int(rep)
            all_data[25]=rep
    for i in range(2, len(all_data),4):
        if all_data[i]==0:
            all_data[i]=None
    c.execute('INSERT INTO pac_donations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (all_data[0], all_data[1], all_data[2], all_data[3], all_data[4], all_data[5], all_data[6], all_data[7], all_data[8], all_data[9], all_data[10], all_data[11], all_data[12], all_data[13], all_data[14], all_data[15], all_data[16], all_data[17], all_data[18], all_data[19], all_data[20], all_data[21], all_data[22], all_data[23], all_data[24], all_data[25]))


c.execute('CREATE TABLE candidate_donations(donation_id INTEGER PRIMARY KEY AUTOINCREMENT, company_id varchar(255), company_name varchar(255), candidate_name varchar(255), race varchar(255), party varchar(255), state varchar(255), amount INTEGER, year varchar(255), FOREIGN KEY(company_name) REFERENCES pac_donations(pacname) )')


dates=['2010', '2012', '2014', '2016', '2018', '2020']
for key in data:
    id=data[key][0]
#id='C00502906'
    for d in dates:
        url='https://www.opensecrets.org/pacs/pacgot.php?cycle='
        url=url+d
        url=url+'&cmte='
        url=url+id
        html_doc = requests.get(url)
        html_dump = BeautifulSoup(html_doc.text, 'html.parser')
        tables = html_dump.find_all('table')
        if len(tables)>1:
            for i in range(1, len(tables)):
                table=tables[i]
                rows = table.find_all('tr')
                for row in rows[1:]:
                    print(key)
                    print(d)
                    candidate_info=[]
                    candidate_info.append(id)
                    #key='Facebook Inc'
                    candidate_info.append(key)
                    cols=row.find_all('td')
                    for j in range(len(cols)):
                        if j==0:
                            splitVal=cols[j].text.split('(')
                            name=splitVal[0].strip()
                            candidate_info.append(name)
                            race=table.caption.span.text
                            candidate_info.append(race)
                            if(race != 'Presidential'):
                                extraSplit=splitVal[1].split('-')
                                print(extraSplit)
                                party=extraSplit[0]
                                candidate_info.append(party)
                                state=extraSplit[1].strip(")")
                                candidate_info.append(state)
                            else:
                                party = splitVal[1].strip(')')
                                candidate_info.append(party)
                                state = None
                                candidate_info.append(state)
                        if j==1:
                            amount=cols[j].text.strip('()$')
                            amount=amount.replace(",", "")
                            amount=int(amount)
                            candidate_info.append(amount)
                    candidate_info.append(d)
                    c.execute('INSERT INTO candidate_donations (company_id, company_name, candidate_name, race, party, state, amount, year) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (candidate_info[0], candidate_info[1], candidate_info[2], candidate_info[3], candidate_info[4], candidate_info[5], candidate_info[6], candidate_info[7]))




"""
dates=['2010', '2012', '2014', '2016', '2018', '2020']
#for key in data:
    #id=data[key][0]
id='C00502906'
#for d in dates:
url='https://www.opensecrets.org/pacs/pacgot.php?cycle='
url=url+'2012'
url=url+'&cmte='
url=url+id
html_doc = requests.get(url)
html_dump = BeautifulSoup(html_doc.text, 'html.parser')
tables = html_dump.find_all('table')
for table in tables:

print(table.caption.span.text)
"""
conn.commit()
