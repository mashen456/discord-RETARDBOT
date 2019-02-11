import discord
from discord.ext import commands
import random
import time
import cfg
import var
from sql import *
from charts import *

description = 'retardchart.com'
bot = commands.Bot(command_prefix='$', description=description)








@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    member = bot.get_all_members()
    for row in member:
        name = str(row)
        aname = name.encode('ascii',errors='ignore')
        getUser(str(row.id),aname)



@bot.command()
async def add(left: int, right: int):
    """Adds two numbers together."""
    await bot.say(left + right)


@bot.command()
async def roll(dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices: str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))


@bot.command()
async def repeat(times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)


@bot.command()
async def joined(member: discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))


@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """

    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))


@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')


# @bot.event
# async def on_message(message):
#     if message.content.startswith('!deleteme'):
#         msg = await bot.send_message(message.channel, 'I will delete myself now...')
#         time.sleep(5)
#
#         await bot.send_message(message.channel, message.author)
#         await bot.delete_message(msg)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    try:
        addMessages(str(message.author.id).strip("!"),1)
    except:
        None

    if message.content.startswith('$karma'):
        if message.author == bot.user:
            return
        await bot.delete_message(message)
        await bot.send_message(message.author, "Du hast " + str(getKarma(str(message.author.id).strip("!"))) + " Karma")

    if message.content.startswith('$retard'):
        if message.author == bot.user:
            return
        await bot.delete_message(message)
        await bot.send_message(message.author, "Du hast " + str(getRetard(str(message.author.id).strip("!"))) + " Retard Punkt/e")

    if message.content.startswith('$startvote'):
        await bot.delete_message(message)
        var.VOTED.clear()
        var.RETARD_COUNT_TEMP_TRUE = 4
        var.RETARD_COUNT_TEMP_FALSE = 0
        retard = str(message.content).split(' ')[1]
        retardplain = retard.replace('<@', '')
        retardplain = retardplain.replace('>','')
        retardplain = retardplain.replace('!', '')
        author = "<@" + message.author.id + ">"

        grund = str(message.content)
        grund = grund.replace('$startvote ', '')
        grund = grund.replace(retard, '')
        grund = grund.lstrip(' ')

        if message.author == bot.user:
            return

        if message.content == '$startvote':
            await bot.send_message(message.author, "Um ein Retard Vote zu starten, schreibe $startvote @Name grund")
            return

        try:


            msg = await bot.send_message(message.channel,
                                         "Ein Retard Votum wurde von: " + author + " gestartet. "
                                                                                   "\nEs wird abgestimmt, ob " + retard + " retardet ist."
                                                                                                                          "\nIhr habt " + str(
                                             cfg.RETARD_VOTE_TIME) + " Sekunden, um zu entscheiden, ob dies wahr ist.")

            for i in range(cfg.RETARD_VOTE_TIME):
                await bot.edit_message(msg,
                                       "Ein Retard Votum wurde von: " + author + " gestartet. "
                                                                                 "\nEs wird abgestimmt, ob " + retard + " retardet ist."
                                                                                                                        "\n\n\nBegründung: " + grund + "\n\n"+
                                                                                                                        "\nIhr habt " + str(
                                           cfg.RETARD_VOTE_TIME - i) + " Sekunden, um zu entscheiden, ob dies wahr ist.")
                time.sleep(1)


            await bot.edit_message(msg,
                                   "Ein Retard Votum wurde von: " + author + " gestartet. "
                                                                             "\nEs wird abgestimmt, ob " + retard + " retardet ist. \n"
            
                                                                      "\nDas Vote Ist zuende !!!\n\n" + str(var.RETARD_COUNT_TEMP_TRUE) + " x Ja |  " + str(var.RETARD_COUNT_TEMP_FALSE) + " x Nein")

            if var.RETARD_COUNT_TEMP_TRUE + var.RETARD_COUNT_TEMP_FALSE <2:
                await bot.edit_message(msg,"Es haben nicht genug Leute abgestimmt.\nEs müssen mindestens 3 Votes fallen, für eine erfolgreiche Abstimmung!\n"
                                           "Um zu Voten schreibt einfach $vote ja oder $vote nein, in den chat.\n"
                                            + str(var.RETARD_COUNT_TEMP_TRUE + var.RETARD_COUNT_TEMP_FALSE) + "/3 votes")
                return

            accepted= "false"
            if var.RETARD_COUNT_TEMP_TRUE > var.RETARD_COUNT_TEMP_FALSE:
                await bot.edit_message(msg,
                                       "Ein Retard Votum wurde von: " + author + " gestartet. "
                                                                                 "\nEs wird abgestimmt, ob " + retard + " retardet ist. "
                                                                                                                        "\n\n\nBegründung: " + grund + "\n\n"+
                                                                                                                        "\nDas Votum Ist zuende !!!\n\n" + str(
                                           var.RETARD_COUNT_TEMP_TRUE) + " x Ja |" + str(
                                           var.RETARD_COUNT_TEMP_FALSE) + " x Nein\n\nSomit ist " + retard + " ein RETARD\nDamit steigt sein Retardstatus um einen Punkt an.\n"
                                                                                                             " "+ author +" hat außerdem 50 Karma für die erfolgreiche Abstimmung erhalten.")
                addRetard(retardplain,1)
                addVote_True(str(message.author.id).strip('!'),1)
                addKarma(str(message.author.id).strip('!'),50)
                accepted = "true"
            else:
                await bot.delete_message(msg)
                msg = await bot.send_message(message.channel,
                                       "Ein Retard Votum wurde von: " + author + " gestartet. "
                                                                                 "\nEs wird abgestimmt, ob " + retard + " retardet ist. \n"
                                                                                                                        "\nDas Vote Ist Zuende !!!\n\n" + str(
                                           var.RETARD_COUNT_TEMP_TRUE) + " x Ja |" + str(
                                           var.RETARD_COUNT_TEMP_FALSE) + " x Nein\n\nSomit ist " + retard + " Kein RETARD " + author + " verliert dadurch 100 Karma")
                remKarma(str(message.author.id).strip('!'),100)
                addVote_False(str(message.author.id).strip('!'),1)
                accepted = "false"

            try:



                addRetardReason(retardplain,grund,accepted,str(message.author.id).strip('!'))
            except:
                None







        except:
            await bot.send_message(message.channel, "Bist du retardet ? ")
            await bot.send_message(message.channel, "Um ein Retard Vote zu starten, schreibe $startvote @Name ")
            return

    if message.content.startswith('$vote'):
        try:
            ergebnis = str(message.content).split('$vote ')[1]
        except:
            await bot.delete_message(message)
            await bot.send_message(message.author, "Probiere lieber mal $vote ja oder $vote nein")
            return

        for item in var.VOTED:
            if item == message.author.id:
                await bot.delete_message(message)
                await bot.send_message(message.author, "Du hast bereits gevotet, oder es ist keine Abstimmung in gange!")
                return
        var.VOTED.append(message.author.id)

        if message.author == bot.user:
            return

        if ergebnis == "ja":
            var.RETARD_COUNT_TEMP_TRUE = var.RETARD_COUNT_TEMP_TRUE + 1
        if ergebnis == "nein":
            var.RETARD_COUNT_TEMP_FALSE = var.RETARD_COUNT_TEMP_FALSE + 1
        await bot.delete_message(message)

    if message.content.startswith('$chartkama'):
        await bot.delete_message(message)
        msg = await bot.send_message(message.channel, 'chart is getting generated!!\nThis can Take up to 60sec!')
        try:
            getPieChart()
            await bot.delete_message(msg)
            await bot.send_file(message.channel, 'snapshot.png')
        except:
            await bot.delete_message(message)
            await bot.send_message(message.channel, 'Failed to generate chart')

    if message.content.startswith('$chartretard'):
        await bot.delete_message(message)
        msg = await bot.send_message(message.channel, 'chart is getting generated!!\nThis can Take up to 60sec!')
        try:
            getPieChartRetard()
            await bot.delete_message(msg)
            await bot.send_file(message.channel, 'snapshotRetard.png')
        except:
            await bot.delete_message(message)
            await bot.send_message(message.channel, 'Failed to generate chart')

    if message.content.startswith('$chartvote'):
        await bot.delete_message(message)
        msg = await bot.send_message(message.channel, 'chart is getting generated!!\nThis can Take up to 60sec!')
        try:
            getPieChartSucessVotes()
            await bot.delete_message(msg)
            await bot.send_file(message.channel, 'snapshotSucessVotes.png')
        except:
            await bot.delete_message(message)
            await bot.send_message(message.channel, 'Failed to generate chart')

    if message.content.startswith('$chartmessage'):
        await bot.delete_message(message)
        msg = await bot.send_message(message.channel, 'chart is getting generated!!\nThis can Take up to 60sec!')
        try:
            getPieChartMessages()
            await bot.delete_message(msg)
            await bot.send_file(message.channel, 'snapshotMessages.png')
        except:
            await bot.delete_message(message)
            await bot.send_message(message.channel, 'Failed to generate chart')

    if message.content.startswith('$help'):
        await bot.delete_message(message)
        await bot.send_message(message.channel,'Der Bot bietet folgende Funktionen:\n\n'
                                              '$karma --> Zeigt dir dein aktuelles Kama an.\n'
                                              '$retard --> Zeigt deinen Retardstatus an.\n'
                                              '$startvote --> Hiermit kannst du Retard Abstimmungen starten.\n'
                                              'Es werden immen mindestens 3 Leute benötigt, um eine Mehrheitsabstimmung durch zu bekommen.\n'
                                              'Benutzt wird er folgendermaßen: \n'
                                              '$startvote @Retard Grund\n'
                                              '$vote --> Hiermit kannst du immer einmal per Abstimmung Voten.\n'
                                              '$vote ja um dafür zu stimmen.\n'
                                              '$vote nein dagegen\n'
                                              '$help --> Diese Übersicht.\n'
                                              '--------------------------------------------------------------------------------------------\n'
                                              '                                 Wer Liebt sie nicht ? Diagramme!! \n\n'
                                              '$chartkama für das aktuelle Kama Chart\n'
                                              '$chartmessage hier siehst du, wie viele Nachrichten die anderen und du so schreiben.\n'
                                              '$chartretard das Beste von allen!! Wie Retardet bist du? Finde es heraus!\n'
                                              '$chartvote Wer schafft die meist erfolgreichen Abstimmungen?\n\n'
                                              '--------------------------------------------------------------------------------------------\n'
                                              '                                  Wie bekomme ich welch Punkte?\n\n'
                                              'Für jede Erfolgreiche Abstimmung bekommst du Kama. Für eine Erfolglose das Gegentil.\n'
                                              'Chatmessages werden 24/7 mitgezählt. Keine Angst wir speichern auch den Inhalt!')



       # bot.join_voice_channel(bo)

    # if message.content.startswith('$onlinetime'):
    #     message.author.
    #     print(test.created_at)





bot.run('NDYxMjgzNzA1OTQwMzQ0ODUz.DhRHAQ.mozqQwiYgpOTDS0RFshApAdCIi0')
