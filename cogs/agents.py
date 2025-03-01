from discord.ext import commands
from discord import app_commands
import controllers.agents as ac
import discord
import typing
import connections.webhook as wb
import random

async def setup(bot : commands.Bot):
    await bot.add_cog(Agents(bot))

class Agents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    async def agents_autocomplete(
        self,
        ctx : commands.Context,
        current : str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        agentlist = await ac.get_agents_list()
        agentlist.append('random')
        for agent in agentlist:
            if current.lower() in agent.lower():
                data.append(app_commands.Choice(name = agent, value = agent))
        return data[:25]
        
    @commands.hybrid_command()
    @app_commands.autocomplete(name = agents_autocomplete)
    async def show_agent(self, ctx : commands.Context, *, name : str):
        """ show an agent based on [name] or [random] to select random agent """
        
        if name == 'random':
            lst = await ac.get_agents_list()
            c = len(lst) - 1
            r = random.randint(0, c)
            name_ = lst[r]
        else:
            name_ = await ac.check_agent(name)
            
        if name_ != None:
            embed = discord.Embed(title=f'Zenless Zone Zero Fandom Wiki | Agents | {name_}')
        else:
            await ctx.send(f'Theres no agents named : {name_} in the database')
            return
        
        id = await ac.get_agent_id(name_)
        line = await ac.get_data('line', id)
        rank = await ac.get_data('rank', id)
        attribute = await ac.get_data('attribute', id)
        speciality = await ac.get_data('speciality', id)
        type = await ac.get_data('type', id)
        birthday = await ac.get_data('birthday', id)
        gender = await ac.get_data('gender', id)
        species = await ac.get_data('species', id)
        faction = await ac.get_data('faction', id)
        signature_w_engine = await ac.get_data('signature_w_engine', id)
        image = await ac.get_data('image', id)
        color = await ac.get_rank_color(rank)
        
        agents_info_field = f'Name : {name_}\nRank : {rank}\nAttribute : {attribute}\n Speciality : {speciality}\nAttack Type : {type}'
        more_info_field = f'Birthday : {birthday}\nGender : {gender}\nSpecies : {species}\nFaction : {faction}'

        embed.color = color
        embed.description = line
        embed.set_thumbnail(url = 'https://static.wikia.nocookie.net/zenless-zone-zero/images/e/e6/Site-logo.png/revision/latest?cb=20240703222351')
        embed.set_image(url = image)
        embed.add_field(name = 'AGENTS INFO', value = agents_info_field, inline = True)
        embed.add_field(name = 'MORE INFO', value = more_info_field, inline = True)
        embed.add_field(name = 'SIGNATURE W-ENGINE', value = signature_w_engine, inline = False)
        embed.set_footer(text = 'Data Collected from Zenless Zone Zero Fanom Wiki', icon_url = 'https://static.wikia.nocookie.net/6a181c72-e8bf-419b-b4db-18fd56a0eb60')
        
        await ctx.send(embed = embed)
        
