import requests
from bs4 import BeautifulSoup
import random
import connections.dbConnect as db

def scrape_data(url : str):
    """
    'id' | 'name' | 'rank' | 'attribute' | 'speciality' | 'desc' | 'signature' | 'base atk' | 
    'substat type' | 'substat atr' | 'effect name' | 'effect desc' | 'image'
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # DONE : Get agets content container & info board
    content_container = soup.find('div', id = 'content').find('div', id = 'mw-content-text').find('div', class_ = 'mw-parser-output')
    info_board = content_container.find('aside', role = 'region')
    
    def get_name():
        res = info_board.find('h2', attrs = {'data-source' : 'title'}).decode_contents()
        if res == None:
            return 'N/A'
        else:
            return res
        
    def get_desc():
        res = content_container.find('div', class_ = 'description standard-border')
        if res == None:
            return 'N/A'
        else:
            res = res.find('div').decode_contents().replace('<br/>', " ")
            return res
        
    def get_rank():
        res = info_board.find('td', attrs = {'data-source' : 'rank'}).find('span', title = True)['title']
        if res == None:
            return 'N/A'
        else:
            return f'{res[-1]}'
        
    def get_speciality():
        res = info_board.find('td', attrs = {'data-source' : 'specialty'})
        if res == None:
            return 'N/A'
        else:
            res = res.find('img', alt = True)['alt']
            return f'{res}'
        
    def get_attribute():
        res = info_board.find('td', attrs = {'data-source' : 'attribute'})
        if res == None:
            return 'N/A'
        else:
            res = res.find('img', alt = True)['alt']
            return f'{res}'
        
    def get_signature():
        res = info_board.find('td', attrs = {'data-source' : 'signature'})
        if res == None:
            return 'N/A'
        else:
            res = res.find('a', title = True)['title']
            return f'{res}'
        
    def get_base_atk():
        res = info_board.find('td', attrs = {'data-source' : 'base1'})
        if res == None:
            return 'N/A'
        else:
            res = res.decode_contents()
            return f'{res}'
        
    def get_substat_type():
        res = info_board.find('th', attrs = {'data-source' : 'stat1'})
        if res == None:
            return 'N/A'
        else:
            res = res.decode_contents()
            return f'{res}'
        
    def get_substat_atr():
        res = info_board.find('td', attrs = {'data-source' : 'stat1'})
        if res == None:
            return 'N/A'
        else:
            res = res.decode_contents()
            return f'{res}'
        
    def get_effect_name():
        res = info_board.find('th', attrs = {'data-source' : 'eff_var1_u5'})
        if res == None:
            return 'N/A'
        else:
            res = res.decode_contents()
            return f'{res}'
        
    def get_effect_desc():
        res = info_board.find('td', attrs = {'data-source' : 'eff_var1_u5'})
        if res == None:
            return 'N/A'
        else:
            for i in res.find_all('b'):
                i.unwrap()
            for i in res.find_all('span'):
                i.unwrap()
            for i in res.find_all('a'):
                i.unwrap()
            for i in res.find_all('i'):
                i.unwrap()
            for i in res.find_all('u'):
                i.unwrap()
            for i in res.find_all('p'):
                i.unwrap()
            for i in res.find_all('aside'):
                i.extract()
            for i in res.find_all('sup'):
                i.extract()
            
            res = res.decode_contents()
            res = res.replace('<br/>', '\n')
                
            return f'{res}'
        
    def get_image():
        res = info_board.find('figure', attrs = {'data-source' : 'image'})
        if res == None:
            return 'N/A'
        else:
            res = res.find('a', href = True)['href']
            return f'{res}'
    
    def get_id(rank : str):
        if rank.lower() == 's':
            rankid = 1
        elif rank.lower() == 'a':
            rankid = 2
        else:
            rankid = 3
            
        rand1 = random.randint(1000, 9999)
        rand2 = random.randint(10, 99)
        rand3 = random.randint(0, 9)
        
        #12222334
        
        res = f'{rankid}{rand1}{rand2}{rand3}'
        return res
    
    data = {
        'id' : get_id(get_rank()),
        'name' : get_name(),
        'desc' : get_desc(),
        'rank' : get_rank(),
        'speciality' : get_speciality(),
        'attribute' : get_attribute(),
        'signature' : get_signature(),
        'base atk' : get_base_atk(),
        'substat type' : get_substat_type(),
        'substat atr' : get_substat_atr(),
        'effect name' : get_effect_name(),
        'effect desc' : get_effect_desc(),
        'image' : get_image()
    }
    
    return data

def add_to_db(data : dict):
    mycursor = db.mycursor
    
    sql = 'INSERT INTO w_engines (id, name, description, rank, speciality, attribute, signature, base_atk, substat_type, substat_atr, effect_name, effect_dec, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    entry = (data['id'], data['name'], data['desc'], data['rank'], data['speciality'], data['attribute'], data['signature'], data['base atk'], data['substat type'], data['substat atr'], data['effect name'], data['effect desc'], data['image'])
    mycursor.execute(sql, entry)

    db.mydb.commit()

def start_scraping(lists : list):
    print(f'begin scrapping w-engines, Remaining : {len(lists)} of {len(lists)}')
    i = 1
    for link in lists:
        if link != ' ':
            data = scrape_data(link)
            add_to_db(data)
            lists_count = len(lists)
            print(f'{data["name"]} Added to Database, Remaining : {lists_count - i} of {lists_count}')
            i += 1
        else:
            print('the link contained blacklisted w-engines. Skipping!')
            i += 1
    print("All w-engines Has Been Added To Database")
    
def input_manually():
    link = input("Input Link Here [(n) if enough] > ")
    if link != "n":
        link_list.append(link)
        input_manually()
    else:
        start_scraping(link_list)

def input_automatically(limit : int):
    link = input("Input link here > ")
    
    req = requests.get(link)
    sp = BeautifulSoup(req.content, 'html.parser')
    mwpu = sp.find('div', id = 'content').find('div', id = 'mw-content-text').find('div', class_ = 'mw-parser-output')
   
    table = mwpu.find('table', class_ = 'navbox-border navbox')
    table = table.find('table')
    tbody = table.find('tbody')
    """
    if limit == 0:
        tr = tbody.find_all('tr')[2:]
    else:
        tr = tbody.find_all('tr', limit = limit+1)[2:]  
    
    for tds in tr:
        td = tds.find('td')
        
        href = td.find('a', href = True)['href']
        url = f'https://zenless-zone-zero.fandom.com{href}'
        link_list.append(url)
    """
    if limit == 0:
        cardlink = tbody.find_all('div', class_ = 'card-link')
    else:
        cardlink = tbody.find_all('div', class_ = 'card-link', limit = limit)
        
    for a in cardlink:
        href = a.find('a', href = True)['href']
        url = f'https://zenless-zone-zero.fandom.com{href}'
        link_list.append(url)
        
    start_scraping(link_list)
        
link_list = []

ask = input("scrape data mannualy ? [y/n]")

if ask == "y":
    input_manually()
elif ask == "n":
    ask_lim = input("limit to how much? [0 if no limit]: ")
    input_automatically(int(ask_lim))

#dat = scrape_data('https://zenless-zone-zero.fandom.com/wiki/Deep_Sea_Visitor')
#dat1 = scrape_data('https://zenless-zone-zero.fandom.com/wiki/Electro-Lip_Gloss')
#dat2 = scrape_data('https://zenless-zone-zero.fandom.com/wiki/(Magnetic_Storm)_Bravo')

#print(dat)
#print(dat1)
#print(dat2)



