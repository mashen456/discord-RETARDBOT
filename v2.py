import discord
import asyncio
from discord.ext import commands
from discord import client
from sql import *
from cfg import *
import var
from charts import *
import time

description = 'retardchart.com'
bot = commands.Bot(command_prefix='$', description=description)


async def taskOnline():
    await bot.wait_until_ready()
    counter = 0
    while not bot.is_closed:
        counter += 1
        for user in bot.get_all_members():
            if user.voice.voice_channel != None and user.voice.self_mute == False and user.voice.self_deaf == False:
                addTime_Online(str(user.id), ONLINE_REFRESH_TIME)
            if user.voice.self_mute == True:
                addTime_Mute(str(user.id), ONLINE_REFRESH_TIME)
            if user.voice.self_deaf == True:
                addTime_def(str(user.id), ONLINE_REFRESH_TIME)
        await asyncio.sleep(ONLINE_REFRESH_TIME)  # task runs every 10 seconds


async def taskClientRefresh():
    await bot.wait_until_ready()
    counter = 0
    while not bot.is_closed:
        counter += 1
        member = bot.get_all_members()
        for row in member:
            name = str(row)
            aname = name.encode('ascii', errors='ignore')
            getUser(str(row.id), aname)
        await asyncio.sleep(30)  # task runs every 30 seconds


async def refreshScores():
    await bot.wait_until_ready()
    while not bot.is_closed:
        highscoreChart()
        channel = bot.get_all_channels()
        for c in channel:
            if str(c.name) == 'retard-charts':
                test = c
                async for message in bot.logs_from(c, limit=500):
                    await bot.delete_message(message)
                try:

                    await bot.send_file(c, 'dOnline.gif')
                    await bot.send_file(c, 'dPie.gif')
                    await bot.send_file(c, 'dvotes.gif')
                    await bot.send_file(c, 'dmessages.gif')
                    await bot.send_file(c, 'dstoned.gif')
                    await bot.send_file(c, 'gRetard.gif')

                except:
                    await bot.send_message(c, 'Failed to generate chart')

        await asyncio.sleep(1200)  # task runs every 30 seconds

# await bot.wait_until_ready()
# counter = 0
# while not bot.is_closed:
#     channel= bot.get_all_channels()
#     for c in channel:
#         if str(c.name) == 'retard-charts':
#             async for message in bot.logs_from(c, limit=500):
#                 bot.delete_message(message.id)
#             msg = await bot.send_message(c,
#                                          'chart is getting generated!!\nThis can Take up to 60sec!')
#             try:
#                 highscoreChart()
#                 await bot.send_file(c, 'dvotes.gif')
#                 await bot.send_file(c, 'dmessages.gif')
#                 await bot.send_file(c, 'dstoned.gif')
#                 await bot.send_file(c, 'gRetard.gif')
#                 await bot.send_file(c, 'dOnline.gif')
#                 await bot.send_file(c, 'dPie.gif')
#                 await bot.delete_message(msg)
#             except:
#                 await bot.send_message(c, 'Failed to generate chart')
#
#
#
#
#         print('Channel Name: {} Channel {}'.format(c.name,c.id))
#     await asyncio.sleep(300)  # task runs every 30 seconds


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
    try:
        if message.author == bot.user:
            return
        addMessages(str(message.author.id).strip("!"), 1)
        addKarma(str(message.author.id).strip('!'), 1)
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
        await bot.send_message(message.author,
                               "Du hast " + str(getRetard(str(message.author.id).strip("!"))) + " Retard Punkt/e")

    if message.content.startswith('$startvote'):
        await bot.delete_message(message)
        var.VOTED.clear()
        var.RETARD_COUNT_TEMP_TRUE = 4
        var.RETARD_COUNT_TEMP_FALSE = 0
        retard = str(message.content).split(' ')[1]
        retardplain = retard.replace('<@', '')
        retardplain = retardplain.replace('>', '')
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
                                             RETARD_VOTE_TIME) + " Sekunden, um zu entscheiden, ob dies wahr ist.")

            for i in range(RETARD_VOTE_TIME):
                await bot.edit_message(msg,
                                       "Ein Retard Votum wurde von: " + author + " gestartet. "
                                                                                 "\nEs wird abgestimmt, ob " + retard + " retardet ist."
                                                                                                                        "\n\n\nBegründung: " + grund + "\n\n" +
                                       "\nIhr habt " + str(
                                           RETARD_VOTE_TIME - i) + " Sekunden, um zu entscheiden, ob dies wahr ist.")
                time.sleep(1)

            await bot.edit_message(msg,
                                   "Ein Retard Votum wurde von: " + author + " gestartet. "
                                                                             "\nEs wird abgestimmt, ob " + retard + " retardet ist. \n"

                                                                                                                    "\nDas Vote Ist zuende !!!\n\n" + str(
                                       var.RETARD_COUNT_TEMP_TRUE) + " x Ja |  " + str(
                                       var.RETARD_COUNT_TEMP_FALSE) + " x Nein")

            if var.RETARD_COUNT_TEMP_TRUE + var.RETARD_COUNT_TEMP_FALSE < 2:
                await bot.edit_message(msg,
                                       "Es haben nicht genug Leute abgestimmt.\nEs müssen mindestens 3 Votes fallen, für eine erfolgreiche Abstimmung!\n"
                                       "Um zu Voten schreibt einfach $vote ja oder $vote nein, in den chat.\n"
                                       + str(var.RETARD_COUNT_TEMP_TRUE + var.RETARD_COUNT_TEMP_FALSE) + "/3 votes")
                return

            accepted = "false"
            if var.RETARD_COUNT_TEMP_TRUE > var.RETARD_COUNT_TEMP_FALSE:
                await bot.edit_message(msg,
                                       "Ein Retard Votum wurde von: " + author + " gestartet. "
                                                                                 "\nEs wird abgestimmt, ob " + retard + " retardet ist. "
                                                                                                                        "\n\n\nBegründung: " + grund + "\n\n" +
                                       "\nDas Votum Ist zuende !!!\n\n" + str(
                                           var.RETARD_COUNT_TEMP_TRUE) + " x Ja |" + str(
                                           var.RETARD_COUNT_TEMP_FALSE) + " x Nein\n\nSomit ist " + retard + " ein RETARD\nDamit steigt sein Retardstatus um einen Punkt an.\n"
                                                                                                             " " + author + " hat außerdem 50 Karma für die erfolgreiche Abstimmung erhalten.")
                addRetard(retardplain, 1)
                addVote_True(str(message.author.id).strip('!'), 1)
                addKarma(str(message.author.id).strip('!'), 50)
                accepted = "true"
            else:
                await bot.delete_message(msg)
                msg = await bot.send_message(message.channel,
                                             "Ein Retard Votum wurde von: " + author + " gestartet. "
                                                                                       "\nEs wird abgestimmt, ob " + retard + " retardet ist. \n"
                                                                                                                              "\nDas Vote Ist Zuende !!!\n\n" + str(
                                                 var.RETARD_COUNT_TEMP_TRUE) + " x Ja |" + str(
                                                 var.RETARD_COUNT_TEMP_FALSE) + " x Nein\n\nSomit ist " + retard + " Kein RETARD " + author + " verliert dadurch 100 Karma")
                remKarma(str(message.author.id).strip('!'), 100)
                addVote_False(str(message.author.id).strip('!'), 1)
                accepted = "false"

            try:

                addRetardReason(retardplain, grund, accepted, str(message.author.id).strip('!'))
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
                await bot.send_message(message.author,
                                       "Du hast bereits gevotet, oder es ist keine Abstimmung in gange!")
                return
        var.VOTED.append(message.author.id)

        if message.author == bot.user:
            return

        if ergebnis == "ja":
            var.RETARD_COUNT_TEMP_TRUE = var.RETARD_COUNT_TEMP_TRUE + 1
        if ergebnis == "nein":
            var.RETARD_COUNT_TEMP_FALSE = var.RETARD_COUNT_TEMP_FALSE + 1
        await bot.delete_message(message)

    if message.content.startswith('$chartKarma'):
        await bot.delete_message(message)
        msg = await bot.send_message(message.channel, 'chart is getting generated!!\nThis can Take up to 60sec!')
        try:
            getPieChart()

            await bot.send_file(message.channel, 'snapshot.png')
            await bot.delete_message(msg)
        except:
            await bot.delete_message(message)
            await bot.send_message(message.channel, 'Failed to generate chart')

    if message.content.startswith('$chartretard'):
        await bot.delete_message(message)
        msg = await bot.send_message(message.channel, 'chart is getting generated!!\nThis can Take up to 60sec!')
        try:
            getPieChartRetard()
            await bot.send_file(message.channel, 'snapshotRetard.png')
            await bot.delete_message(msg)
        except:
            await bot.delete_message(message)
            await bot.send_message(message.channel, 'Failed to generate chart')

    if message.content.startswith('$chartvote'):
        await bot.delete_message(message)
        msg = await bot.send_message(message.channel, 'chart is getting generated!!\nThis can Take up to 60sec!')
        try:
            getPieChartSucessVotes()
            await bot.send_file(message.channel, 'snapshotSucessVotes.png')
            await bot.delete_message(msg)
        except:
            await bot.delete_message(message)
            await bot.send_message(message.channel, 'Failed to generate chart')

    if message.content.startswith('$chartmessage'):
        await bot.delete_message(message)
        msg = await bot.send_message(message.channel, 'chart is getting generated!!\nThis can Take up to 60sec!')
        try:
            getPieChartMessages()
            await bot.send_file(message.channel, 'snapshotMessages.png')
            await bot.delete_message(msg)
        except:
            await bot.delete_message(message)
            await bot.send_message(message.channel, 'Failed to generate chart')

    if message.content.startswith('$help'):
        await bot.delete_message(message)
        await bot.send_message(message.channel, 'Der Bot bietet folgende Funktionen:\n\n'
                                                '$karma --> Zeigt dir dein aktuelles Karma an.\n'
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
                                                '$chartKarma für das aktuelle Karma Chart\n'
                                                '$chartmessage hier siehst du, wie viele Nachrichten die anderen und du so schreiben.\n'
                                                '$chartretard das Beste von allen!! Wie Retardet bist du? Finde es heraus!\n'
                                                '$chartvote Wer schafft die meist erfolgreichen Abstimmungen?\n\n'
                                                '--------------------------------------------------------------------------------------------\n'
                                                '                                  Wie bekomme ich welch Punkte?\n\n'
                                                'Für jede Erfolgreiche Abstimmung bekommst du Karma. Für eine Erfolglose das Gegentil.\n'
                                                'Chatmessages werden 24/7 mitgezählt. Keine Angst wir speichern auch den Inhalt!\n\n'
                                                '--------------------------------------------------------------------------------------------\n'
                                                '                                  Onlinezeit?\n\n'
                                                '$chartonlinetime um dein Onlinezeit Chart zu sehen.\n'
                                                '$onlinetime um deine Online Statistiken zu sehen\n\n'
                                                '--------------------------------------------------------------------------------------------\n'
                                                '                                  Junkie?\n\n'
                                                '$junkie @Name, um den Junkiestatus von jemandem anzuheben.\n'
                                                '$statsjunkie um dienen Junkie Status zu sehen.')

    if message.content.startswith('$chartonlinetime'):
        await bot.delete_message(message)
        msg = await bot.send_message(message.channel, 'chart is getting generated!!\nThis can Take up to 60sec!')
        try:
            getUserStatsChart(str(message.author.id).strip("!"), str(message.author))
            await bot.send_file(message.channel, 'onlineTime.png')
            await bot.delete_message(msg)
        except:
            await bot.delete_message(message)
            await bot.send_message(message.channel, 'Failed to generate chart')

    if message.content.startswith('$onlinetime'):
        if message.author == bot.user:
            return
        await bot.delete_message(message)
        tep = getOnlineStats(str(message.author.id).strip("!"))
        await bot.send_message(message.author,
                               'Du warst bisher {}min online, {}min gemuted, {}min stummgeschaltet.'.format(
                                   int(tep[0] / 60), int(tep[1] / 60), int(tep[2] / 60)))

    if message.content.startswith('$junkie'):
        retard = str(message.content).split(' ')[1]
        retardplain = retard.replace('<@', '')
        retardplain = retardplain.replace('>', '')
        retardplain = retardplain.replace('!', '')
        addJunkie(retardplain, 1)
        await bot.delete_message(message)
        addKarma(str(message.author.id).strip('!'), 5)
        await bot.send_message(message.channel,
                               'Der Junkiestatus, von <@{}> ist gestiegen. \n{} hat dafür 5 Karma bekommen!'.format(
                                   retardplain, str(message.author)))

    if message.content.startswith('$statsjunkie'):
        if message.author == bot.user:
            return
        await bot.delete_message(message)
        await bot.send_message(message.author,
                               "Dein Junkie Status ist : " + str(getJunkie(str(message.author.id).strip("!"))))


bot.loop.create_task(refreshScores())
bot.loop.create_task(taskClientRefresh())
bot.loop.create_task(taskOnline())
bot.run('NDYxMjgzNzA1OTQwMzQ0ODUz.DhRHAQ.mozqQwiYgpOTDS0RFshApAdCIi0')
#bot.run('NDY0ODk5MzMxMDgyODEzNDUw.DiFrUQ.Ou4kIeg0mWEs4HKe1KQDjXukcIU')
