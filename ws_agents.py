import requests
from bs4 import BeautifulSoup
import random
import connections.dbConnect as db

def scrape_data(url : str):
    """
    'name' | 'rank' | 'attribute' | 'speciality' | 'type' | 'birthday' | 
    'gender' | 'species' | 'faction' | 'w_engine' | 'image' 
    """
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    # DONE : Get agets content container & info board
    content_container = soup.find('div', id = 'content').find('div', id = 'mw-content-text').find('div', class_ = 'mw-parser-output')
    info_board = content_container.find('aside', role = 'region')

    # DONE : get data-source
    def get_name():
        res = info_board.find('h2', attrs = {'data-source' : 'name'}).decode_contents()
        if res == None:
            return 'N/A'
        else:
            return res
    
    
    # TODO : get line
    def get_line():
        res = content_container.find('div', class_ = 'description standard-border')
        if res == None:
            return 'N/A'
        else:
            res = res.find('div').decode_contents().replace('<br/>', " ")
            return res
    
    # DONE : get rank
    def get_rank():
        res = info_board.find('td', attrs = {'data-source' : 'rank'}).find('span', title = True)['title']
        if res == None:
            return 'N/A'
        else:
            return f'{res[-1]}'
        
    # DONE : get attribute
    def get_attribute():
        res = info_board.find('td', attrs = {'data-source' : 'attribute'}).find('img', alt = True)['alt']
        if res == None:
            return 'N/A'
        else:
            return f'{res}'
        
    # DONE : get speciality
    def get_speciality():
        res = info_board.find('td', attrs = {'data-source' : 'specialty'}).find('img', alt = True)['alt']
        if res == None:
            return 'N/A'
        else:
            return f'{res}'
        
    # DONE : get type (attack type)
    def get_type():
        res = info_board.find('td', attrs = {'data-source' : 'attackType'}).find('img', alt = True)['alt']
        if res == None:
            return 'N/A'
        else:
            return f'{res}'
        
    # DONE : get birthday
    def get_birthday():
        res = info_board.find('div', attrs = {'data-source' : 'birthday'}).find('div').decode_contents()
        if res == None:
            return 'N/A'
        else:
            return res
        
    # DONE : get gender
    def get_gender():
        res = info_board.find('div', attrs = {'data-source' : 'gender'}).find('div').decode_contents()
        if res == None:
            return 'N/A'
        else:
            return res
        
    # DONE : get species
    def get_species():
        res = info_board.find('div', attrs = {'data-source' : 'species'}).find('a', title = True)['title']
        if res == None:
            return 'N/A'
        else:
            return f'{res}'
        
    # DONE : get faction
    def get_faction():
        res = info_board.find('div', attrs = {'data-source' : 'faction'}).find('a', title = True)['title']
        if res == None:
            return 'N/A'
        else:
            return f'{res}'
        
    # DONE : get w-engine
    def get_signature_w_engine():
        res = info_board.find('div', attrs = {'data-source' : 'signature'}).find('div').find('a', title = True)['title']
        if res == None:
            return 'N/A'
        else:
            return f'{res}'
        
    # DONE : get image 
    def get_image():
        # image options : 
        #   > (priority) new eridu archives
        #   > (if priority nonexcist) agent record 3
        
        media_link = content_container.find('div', class_ = 'custom-tabs-default custom-tabs').find('a', title = f'{get_name()}/Media', href = True)['href']
        media_req = requests.get(f'https://zenless-zone-zero.fandom.com{media_link}')
        media_soup = BeautifulSoup(media_req.content, 'html.parser')
        
        gallery2 = media_soup.find('div', id = 'gallery-2')
        if gallery2 == None:
            gallery2 = media_soup.find('div', id = 'gallery-1')
        
        IMG = gallery2.find('div', id = f'New_Eridu_Archives_-_{get_name().replace(" ", "_")}-png')
        if IMG == None:
            IMG = gallery2.find('div', id = f'Agent_{get_name().replace(" ", "_")}_Agent_Record_3-png')
        
        url = IMG.find('img', src = True)['src']
        url = url.replace('/scale-to-width-down/185', '')
        
        return f'{url}'
    
    
    # TODO : set id
    def set_id():
        """
        format :
            > 1 digit based on rank (S = 1, A = 2)
            > 1 digit based on gender (Male = 1, Female = 2)
            > 1 digit based on species (Human = 1, Non Human = 2)
            > 3 random digit from 100 - 999
            > 2 random digit from 10 - 99
            > 1 random digit from 0 - 9
        
        """
        
        if rank.lower() == "s":
            rankid = 1
        elif rank.lower() == "a":
            rankid = 2
        
        if gender == "Male":
            gendid = 1
        elif gender == "Female":
            gendid = 2

        if species == "Human":
            specid = 1
        else:
            specid = 2
        
        rand1 = random.randint(100, 999)
        rand2 = random.randint(10, 99)
        rand3 = random.randint(0, 9)
        
        res = f'{rankid}{gendid}{specid}{rand1}{rand2}{rand3}'

        return res
    
    name = get_name()
    line = get_line()
    rank = get_rank()
    attribute = get_attribute()
    speciality = get_speciality()
    type = get_type()
    birthday = get_birthday()
    gender = get_gender()
    species = get_species()
    faction = get_faction()
    signature = get_signature_w_engine()
    image = get_image()
    id = set_id()
    
    data = {
        'id' : id,
        'name' : name,
        'line' : line,
        'rank' : rank,
        'attribute' : attribute,
        'speciality' : speciality,
        'type' : type,
        'birthday' : birthday,
        'gender' : gender,
        'species' : species,
        'faction' : faction,
        'w_engine' : signature,
        'image' : image
    }
    
    return data

# TODO : Add data to database
def add_to_db(data : dict):
    mycursor = db.mycursor
    
    sql = 'INSERT INTO agents (id, name, line, rank, attribute, speciality, type, birthday, gender, species, faction, signature_w_engine, image) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
    entry = (data['id'], data['name'], data['line'], data['rank'], data['attribute'], data['speciality'], data['type'], data['birthday'], data['gender'], data['species'], data['faction'], data['w_engine'], data['image'])
    mycursor.execute(sql, entry)

    db.mydb.commit()
    
    
#data = scrape_data('https://zenless-zone-zero.fandom.com/wiki/Billy_Kid')
#entry = (data['id'], data['name'], data['line'], data['rank'], data['attribute'], data['speciality'], data['type'], data['birthday'], data['gender'], data['species'], data['faction'], data['w_engine'], data['image'])
#print(entry)
#add_to_db(data)

def start_scraping(lists : list):
    print(f'begin scrapping agents, Remaining : {len(lists)} of {len(lists)}')
    i = 1
    for link in lists:
        if link != ' ':
            data = scrape_data(link)
            add_to_db(data)
            lists_count = len(lists)
            print(f'{data["name"]} Added to Database, Remaining : {lists_count - i} of {lists_count}')
            i += 1
        else:
            print('the link contained blacklisted agents. Skipping!')
            i += 1
    print("All agents Has Been Added To Database")

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
   
    table = mwpu.find_all('table').pop(1)
    tbody = table.find('tbody')
    
    if limit == 0:
        tr = tbody.find_all('tr')[1:]
    else:
        tr = tbody.find_all('tr', limit = limit+1)[1:]  
    
    for tds in tr:
        td = tds.find('td')
        
        href = td.find('a', href = True)['href']
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