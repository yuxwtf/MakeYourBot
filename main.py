
# don't skid // yux#3039

import shutil
import discord
from discord.ext import commands
from dislash import *
import json
import os
import ascii2text
import time

bot = commands.Bot(command_prefix="!")
inter_client = InteractionClient(bot)
bottoken = ""
botname = ""
botprefix = ""

botbase = """import discord
from discord.ext import commands
from dislash import *
import json

config = json.load(open('./config.json'))
bot = commands.Bot(command_prefix=config['prefix'])
inter_client = InteractionClient(bot)

## BOT CODE / START





## BOT CODE / END


bot.run(config['token'])
"""


async def managebotui(ctx, msg):
    global bottoken, botname, botprefix

    def check(inter):
        return inter.message.id == msg.id

    rib = ActionRow(
        Button(
            style=ButtonStyle.blurple,
            label="Bot Informations",
            custom_id="botinfo"
        ),
        Button(
            style=ButtonStyle.blurple,
            label="Token",
            custom_id="token"
        ),
        Button(
            style=ButtonStyle.blurple,
            label="New Command",
            custom_id="addcommand"
        ),
        Button(
            style=ButtonStyle.blurple,
            label="New Event",
            custom_id="addevent"
        )
    )
    await msg.edit(embed=discord.Embed(title=f"MANAGER", description=f"`You can now manage your bot !`"), components=[rib])
    inter = await ctx.wait_for_button_click(check)
    button_text = inter.clicked_button.custom_id
    if button_text == "token":
        embed=discord.Embed(title="Your BOT Token:", description=f"`{bottoken}`")
        await msg.edit(embed=embed, components=[Button(style=ButtonStyle.blurple,label="Change",custom_id="changetkn")])
        inter = await ctx.wait_for_button_click(check)
        button_text = inter.clicked_button.custom_id
        if button_text == 'changetkn':
            await msg.edit(embed=discord.Embed(title="Your BOT Token:", description="`please send the new token in the chat`"), components=[])
            bottoken = await bot.wait_for("message")
            await bottoken.delete()
            bottoken = bottoken.content
            embed=discord.Embed(title="Your BOT Token Is Now:", description=f"`{bottoken}`")
            await msg.edit(embed=embed, components=[Button(style=ButtonStyle.blurple,label="Change",custom_id="changetkn")])
            await managebotui(ctx, msg)
    if button_text == "addcommand":
        await msg.edit(embed=discord.Embed(title="MYB | New Command", description=f"`Please send the command without prefix in the chat:`"), components=[])
        command = await bot.wait_for("message")
        await command.delete()
        await msg.edit(
            embed=None,
            components=[
                SelectMenu(
                    custom_id="selected",
                    placeholder="Action",
                    max_values=1,
                    options=[
                        SelectOption("Send A Message", "send_msg"),
                        SelectOption("Send A Private Message", "send_pmsg")
                    ]
                )
            ]
        )
        def check(inter):
            return inter.author == ctx.author
        inter = await msg.wait_for_dropdown(check)
        customid = [option.value for option in inter.select_menu.selected_options]
        print(customid)
        if customid[0] == "send_msg":
            await msg.edit(embed=discord.Embed(title="MYB | New Command", description=f"`Please send the message you want to send in the chat:`"), components=[])
            msg1 = await bot.wait_for("message")
            addbotcode(f'''
@bot.command()
async def {command.content}(ctx):
    await ctx.send("""{msg1.content}""")
            ''')
            await managebotui(ctx, msg)
        elif customid[0] == "send_pmsg":
            await msg.edit(embed=discord.Embed(title="MYB | New Command", description=f"`Please send the message you want to send in the chat:`"), components=[])
            msg1 = await bot.wait_for("message")
            addbotcode(f'''
@bot.command()
async def {command.content}(ctx):
    await ctx.author.send("""{msg1.content}""")
            ''')
            await managebotui(ctx, msg)
    await msg.edit(embed=discord.Embed(title="MYB | Command Succesfully Created", description=f"`{botprefix.content}{command.content} >> Has been created !`"), components=[])
    if button_text == "addevent":
        await msg.edit(
            embed=None,
            components=[
                SelectMenu(
                    custom_id="selected",
                    placeholder="Action",
                    max_values=1,
                    options=[
                        SelectOption("On Message", "on_message"),
                        SelectOption("On Ready", "on_ready")
                    ]
                )
            ]
        )
        def check(inter):
            return inter.author == ctx.author
        inter = await msg.wait_for_dropdown(check)
        customid = [option.value for option in inter.select_menu.selected_options]
        if customid[0] == 'on_message':
            await msg.edit(
            embed=None,
            components=[
                SelectMenu(
                    custom_id="selected",
                    placeholder="Action",
                    max_values=1,
                    options=[
                        SelectOption("Send A Message", "send_msg"),
                        SelectOption("Send A Private Message", "send_pmsg")
                    ]
                )
            ]
            )
            def check(inter):
                return inter.author == ctx.author
            inter = await msg.wait_for_dropdown(check)
            customid = [option.value for option in inter.select_menu.selected_options]
            if customid[0] == "send_msg":
                await msg.edit(embed=discord.Embed(title="MYB | New Command", description=f"`Please send the message you want to send in the chat:`"), components=[])
                msg1 = await bot.wait_for("message")
                addbotcode(f'''
@bot.event
async def on_message(message):
    await message.channel.send("""{msg1.content}""")                 
                
                ''')
                await managebotui(ctx, msg)
            elif customid[0] == "send_pmsg":
                await msg.edit(embed=discord.Embed(title="MYB | New Command", description=f"`Please send the message you want to send in the chat:`"), components=[])
                msg1 = await bot.wait_for("message")
                addbotcode(f'''
@bot.event
async def on_message(message):
    await message.author.send("""{msg1.content}""")                 
                
                ''')
                await managebotui(ctx, msg)
        if customid[0] == 'on_ready':
            await managebotui(ctx, msg)


def loadbot(botname):
    global bottoken
    foldername = str(botname).replace(' ', '')
    configdata = json.load(open(f'./Bots/{foldername}/config.json'))
    bottoken = configdata['token']
    botname = configdata['name']

def addbotcode(code):
    foldername = str(botname.content).replace(' ', '')
    with open(f'./Bots/{foldername}/main.py', 'r') as f:
        data = f.readlines()
    data[12] = f'\n\n\n{code}\n\n\n'
    with open(f'./Bots/{foldername}/main.py', 'w') as f:
        f.writelines(data)

def getbotscount():
    list = os.listdir('./Bots/')
    number_files = len(list)
    return number_files

def getbots():
    list = os.listdir('./Bots/')
    return list

def setupbotmainfile(token, name, prefix):
    try:
        foldername = name.replace(' ', '')
        os.mkdir(os.path.join("./Bots/", foldername))
        with open(f'./Bots/{foldername}/config.json', 'w') as f:
            f.write('''
{
    "token": "'''+token+'''",
    "name": "'''+name+'''",
    "prefix": "'''+prefix+'''"
}
            ''')
        with open(f'./Bots/{foldername}/main.py', 'w') as f:
            f.write(botbase)
    except Exception as e:
        print(e)



async def mainmenu(ctx, msg):
    global bottoken, botname, bot
    # Make a row of buttons
    basebuttons = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="New Bot",
            custom_id="create"
        ),
        Button(
            style=ButtonStyle.blurple,
            label="My Bots",
            custom_id="bots"
        ),
        Button(
            style=ButtonStyle.green,
            label="Load A Bot",
            custom_id="load"
        ),
        Button(
            style=ButtonStyle.red,
            label="Delete A Bot",
            custom_id="delete"
        )
    )

    okbtn = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="Ok",
            custom_id="ok"
        )
    )

    await msg.edit(
        embed=discord.Embed(title=f"MYB | {getbotscount()} Bots Loaded", description="`Please select a choice:`", ),
        components=[basebuttons]
    )
    # Wait for someone to click on them
    def check(inter):
        return inter.message.id == msg.id
    inter = await ctx.wait_for_button_click(check)
    button_text = inter.clicked_button.custom_id

    if button_text == "delete":
        await msg.edit(embed=discord.Embed(title="MYB | Delete A Bot", description="`please send the name of your bot you want to delete!`"), components=[])
        db = await bot.wait_for("message")
        await db.delete()
        try:
            shutil.rmtree(f'./Bots/{db.content}/')
            await msg.edit(embed=discord.Embed(title="MYB | Delete A Bot", description="`The bot has been deleted !`"), components=[])
            time.sleep(2)
            await mainmenu(ctx, msg)
        except Exception as e:
            await msg.edit(embed=discord.Embed(title="MYB | Delete A Bot", description="`Failed to delete the bot !`"), components=[])
            print(e)
            time.sleep(2)
            await mainmenu(ctx, msg)


    if button_text == "load":
        await msg.edit(embed=discord.Embed(title="MYB | Load A Bot", description="`please send the name of your bot you want to load!`"), components=[])
        bottoload = await bot.wait_for("message")
        await bottoload.delete()
        try:
            loadbot(bottoload.content)
            await msg.edit(embed=discord.Embed(title="MYB | Load A Bot", description=f"`{bottoload.content} Has been loaded !`"), components=[])
        except Exception as e:
            await msg.edit(embed=discord.Embed(title="MYB | Load A Bot", description=f"`Failed to load bot : {bottoload.content}`"), components=[okbtn])
            print(e)
            def check(inter):
                return inter.message.id == msg.id
            inter = await ctx.wait_for_button_click(check)
            button_text = inter.clicked_button.custom_id
            await mainmenu(ctx, msg)
        time.sleep(1)
        await managebotui(ctx, msg)

    if button_text == "create":

        await msg.edit(embed=discord.Embed(title="MYB | Bot Setup (1/4)", description="`please send the BOT TOKEN in the chat`"), components=[])
        bottoken1 = await bot.wait_for("message")
        await bottoken1.delete()
        await msg.edit(embed=discord.Embed(title="MYB | Bot Setup (2/4)", description="`please send the BOT NAME in the chat`"), components=[])
        botname1 = await bot.wait_for("message")
        await botname1.delete()
        await msg.edit(embed=discord.Embed(title="MYB | Bot Setup (3/4)", description="`please send the BOT PREFIX in the chat`"), components=[])
        botprefix1 = await bot.wait_for("message")
        await botprefix1.delete()
        await msg.edit(embed=discord.Embed(title="MYB | Setting Up Your Bot... (4/4)", description="`please wait ...`"), components=[])
        setupbotmainfile(bottoken1.content, botname1.content, botprefix1.content)
        loadbot(botname1.content)
        time.sleep(2)
        await managebotui(ctx, msg)          
    
    elif button_text == "bots":
        embed=discord.Embed(title="MYB | Your Bots", description="There is your bots loaded:")
        okbtn = ActionRow(
            Button(
                style=ButtonStyle.green,
                label="Ok",
                custom_id="ok"
            )
        )
        for bot in getbots():
            embed.add_field(name=f"```{bot}```", value=f"` `", inline=True)
        await msg.edit(embed=embed, components=[okbtn])
        def check(inter):
            return inter.message.id == msg.id
        inter = await ctx.wait_for_button_click(check)
        button_text = inter.clicked_button.custom_id
        await mainmenu(ctx, msg)


@bot.command()
async def start(ctx):
    basebuttons = ActionRow(
        Button(
            style=ButtonStyle.green,
            label="New Bot",
            custom_id="create"
        ),
        Button(
            style=ButtonStyle.blurple,
            label="My Bots",
            custom_id="bots"
        ),
        Button(
            style=ButtonStyle.green,
            label="Load A Bot",
            custom_id="load"
        ),
        Button(
            style=ButtonStyle.red,
            label="Delete A Bot",
            custom_id="delete"
        )
    )
    msg = await ctx.send(
        embed=discord.Embed(title=f"MYB | {getbotscount()} Bots Loaded", description="`Please select a choice:`", ),
        components=[basebuttons]
    )
    while True:
        try:
            await mainmenu(ctx, msg)
        except:
            global bottoken, botname, botprefix
            bottoken = ""
            botname = ""
            botprefix = ""
            time.sleep(5)
            await msg.edit(
                embed=discord.Embed(title=f"MYB | Bot Crashed", description="`this is a beta made by yux then sorry for crashs, enjoy`", ),
                components=[]
            )
            bot.logout()
            exit('bot crashed')
            return

        


bot.run("YOUR_BOT_TOKEN")
