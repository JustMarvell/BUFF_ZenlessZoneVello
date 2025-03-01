import connections.dbConnect as db
import discord

mycursor = db.mycursor

async def get_agents_list():
    sql = "SELECT name FROM agents"

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    agentlist = []
    for agent in myresult:
        agentlist += agent
    agentlist.sort()
    
    return agentlist

async def check_agent(agent_name : str):
    wildcard = f'%{agent_name}%'

    sql = "SELECT name FROM agents WHERE name LIKE %s"
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
    
async def get_agent_id(name : str):
    sql = "SELECT id FROM agents WHERE name = %s"
    agentname = (name, )
    
    mycursor.execute(sql, agentname)
    myresult = mycursor.fetchone()

    id = 0
    for result in myresult:
        id += result
    return id

async def get_data(data_source : str, id : int):
    """
    name | line | rank | attribute | speciality | type | birthday | gender |
    species | faction | signature_w_engine | image
    """
    sql = f"SELECT {data_source} FROM agents WHERE id = {id}"

    mycursor.execute(sql)
    myresult = mycursor.fetchone()

    result = ""
    for i in myresult:
        result += i
    
    return result

async def get_agents_list_based_on_rank(rank : str):
    sql = 'SELECT name FROM agents WHERE rank = %s'
    _rank = (rank, )

    mycursor.execute(sql, _rank)
    myresult = mycursor.fetchall()

    agentlist = []
    for agent in myresult:
        agentlist += agent
    agentlist.sort()
    
    return agentlist

async def get_rank_color(rank : str):
    if rank == "A":
        return discord.Color.purple()
    elif rank == "S":
        return discord.Color.gold()
