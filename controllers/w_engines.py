import connections.dbConnect as db
import discord

mycursor = db.mycursor

async def get_engine_list():
    sql = "SELECT name FROM w_engines"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    agentlist = []
    for agent in myresult:
        agentlist += agent
    agentlist.sort()
    
    return agentlist

async def check_engines(engine_name : str):
    wildcard = f'%{engine_name}%'

    sql = "SELECT name FROM w_engines WHERE name LIKE %s"
    name = (wildcard, )

    mycursor.execute(sql, name)
    myresult = mycursor.fetchone()

    if myresult != None:
        res = ""
        for agent in myresult:
            res += agent
        return res
    else:
        return None
    
async def get_engine_id(name : str):
    sql = "SELECT id FROM w_engines WHERE name = %s"
    enginename = (name, )
    
    mycursor.execute(sql, enginename)
    myresult = mycursor.fetchone()

    id = 0
    for result in myresult:
        id += result
    return id

async def get_data(data_source : str, id : int):
    """
    name' | 'rank' | 'attribute' | 'speciality' | 'desc' | 'signature' | 'base atk' | 
    'substat type' | 'substat atr' | 'effect name' | 'effect desc' | 'image'
    """
    sql = f"SELECT {data_source} FROM w_engines WHERE id = {id}"

    mycursor.execute(sql)
    myresult = mycursor.fetchone()

    result = ""
    for i in myresult:
        result += i
    
    return result

async def get_engine_list_based_on_rank(rank : str):
    sql = 'SELECT name FROM w_engines WHERE rank = %s'
    _rank = (rank, )

    mycursor.execute(sql, _rank)
    myresult = mycursor.fetchall()

    enginelist = []
    for engine in myresult:
        enginelist += engine
    enginelist.sort()
    
    return enginelist

async def get_rank_color(rank : str):
    if rank == "A":
        return discord.Color.purple()
    elif rank == "S":
        return discord.Color.gold()
    elif rank == "B":
        return discord.Color.brand_green()
