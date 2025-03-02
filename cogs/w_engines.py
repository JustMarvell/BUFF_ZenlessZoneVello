from discord.ext import commands
from discord import app_commands
import controllers.w_engines as ac
import discord
import typing
import connections.webhook as wb
import random

async def setup(bot : commands.Bot):
    await bot.add_cog(Engines(bot))

class Engines(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def engine_autocomplete(
        self,
        ctx : commands.Context,
        current : str
    ) -> typing.List[app_commands.Choice[str]]:
        data = []
        enginelist = await ac.get_engine_list()
        enginelist.append('random')
        for engine in enginelist:
            if current.lower() in engine.lower():
                data.append(app_commands.Choice(name = engine, value = engine))
        return data[:25]
        
    @commands.hybrid_command()
    @app_commands.autocomplete(name = engine_autocomplete)
    async def show_engine(self, ctx : commands.Context, *, name : str):
        """ show an w-engine based on [name] or [random] to select random w-engine """
        
        if name == 'random':
            lst = await ac.get_engine_list()
            c = len(lst) - 1
            r = random.randint(0, c)
            name_ = lst[r]
        else:
            name_ = await ac.check_engines(name)
            
        if name_ != None:
            embed = discord.Embed(title=f'Zenless Zone Zero Fandom Wiki | W-Engines | {name_}')
        else:
            await ctx.send(f'Theres no w-engine named : {name_} in the database')
            return
        
        id = await ac.get_engine_id(name_)
        rank = await ac.get_data('rank', id)
        attribute = await ac.get_data('attribute', id)
        speciality = await ac.get_data('speciality', id)
        desc = await ac.get_data('description', id)
        signature = await ac.get_data('signature', id)
        base_atk = await ac.get_data('base_atk', id)
        substat_type = await ac.get_data('substat_type', id)
        substat_atr = await ac.get_data('substat_atr', id)
        effect_name = await ac.get_data('effect_name', id)
        effect_desc = await ac.get_data('effect_dec', id)
        image = await ac.get_data('image', id)
        color = await ac.get_rank_color(rank)
        
        w_engines_info_field = f'Name : {name_}\nRank : {rank}\nSpeciality : {speciality}\nAttribute : {attribute}\nSignature : {signature}'
        w_engine_stats_field = f'Base ATK : {base_atk}\nSubstat : {substat_atr} {substat_type}'

        embed.color = color
        embed.description = desc
        embed.set_thumbnail(url = 'https://static.wikia.nocookie.net/zenless-zone-zero/images/e/e6/Site-logo.png/revision/latest?cb=20240703222351')
        embed.set_image(url = image)
        embed.add_field(name = 'AGENTS INFO', value = w_engines_info_field, inline = True)
        embed.add_field(name = 'MORE INFO', value = w_engine_stats_field, inline = True)
        embed.add_field(name = f'ENGINE EFFECT : {effect_name}', value = effect_desc, inline = False)
        embed.set_footer(text = 'Data Collected from Zenless Zone Zero Fandom Wiki', icon_url = 'https://static.wikia.nocookie.net/6a181c72-e8bf-419b-b4db-18fd56a0eb60')
        
        await ctx.send(embed = embed)
        
