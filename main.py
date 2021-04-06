#import urllib.request
from urllib import request
from discord.ext.commands.core import command
import requests as req
from bs4 import BeautifulSoup
from time import sleep as wait
from emailer import main as send_email

import discord
from discord.ext import commands
import asyncio

bot = commands.Bot(command_prefix='dl!')


#links organizados
notices = {'titles':'', 'contents':'', 'links':'', 'imgs':''}

def send_notice():
    #seta a msg
    global msg
    msg = ''

    #prepara ela com o conteudo
    msg += f'{notices["titles"]}\n\n'
    msg += f'{notices["contents"]}\n'

    
    #faz o envio dos emails e posta no discord
    
    #email = input('Informe seu e-mail: ')
    #send_email(email, msg, types[type_notice])

    return msg

def get_notice():
    #faz a request ao g1 para coletar a ultima notícia
    res = req.get('https://g1.globo.com/economia/tecnologia/')
    content = res.content



    site = BeautifulSoup(content, 'html.parser')
    cards = site.find('a', 'feed-post-link')
    
    title = cards.text
    notices['titles'] = title


    content_link = cards.get('href')
    res_ntc = req.get(content_link)

    content_ntc = res_ntc.content
    site_ntc = BeautifulSoup(content_ntc, 'html.parser')
    
    img_1 = site.find('img', 'bstn-fd-picture-image')
    notices['imgs'] = str(img_1.get('src'))

    
    card_ntc = site_ntc.find_all('p', 'content-text__container')
    ntc = ''
    for i in range(0, len(card_ntc) - 1):
        p = card_ntc[i].text
        ntc += (f'{p}\n')
        notices['links'] = content_link
        notices['cotents'] = ''
        notices['contents'] = ntc


@bot.event
async def on_ready():
    canal = bot.get_channel(792882239734022145)
    while True:

        get_notice()

        em = discord.Embed(title = f'{notices["titles"].upper()}', description = f'{notices["contents"]}\n\n**fonte: **{notices["links"]}', color = 0x33348B)
        em.set_thumbnail(url=notices['imgs'])

        await canal.send(embed = em)
        await asyncio.sleep(7200)


with open('token', 'r') as txt:
    tk = txt.read()
bot.run(tk)