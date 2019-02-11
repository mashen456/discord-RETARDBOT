from pyecharts import Bar
from pyecharts import Funnel
from sql import *
from collections import Counter
from pyecharts import Line, Pie, Grid, Gauge, Style, WordCloud
from pyecharts import Page
from helper import *


from pyecharts.engine import create_default_environment

page = Page()

def helper(data,amount):
    i = 0
    temp1 = []
    while i <= amount:
        temp1.append(str(data.most_common()[i][0]).split('#')[0].split('|')[0])
        i += 1
    return temp1

def helper2(data,amount,time):
    i = 0
    temp1 = []
    while i <= amount:
        if time == True:
            temp1.append(zeitRechner(data.most_common()[i][1])[2])
        else:
            temp1.append(data.most_common()[i][1])
        i += 1
    return temp1


def getPieChart():
        data = getTopUser()

        attr = [data.most_common()[0][0], data.most_common()[1][0], data.most_common()[2][0], data.most_common()[3][0],
                data.most_common()[4][0], data.most_common()[5][0]]
        v1 = [data.most_common()[0][1], data.most_common()[1][1], data.most_common()[2][1], data.most_common()[3][1],
              data.most_common()[4][1], data.most_common()[5][1]]
        pie = Pie("Karma Chart", title_pos="42%")
        pie.add("", attr, v1, radius=[30, 55],
                legend_pos="65%", legend_orient='vertical')

        pie.render(path='snapshot.png')


def getPieChartRetard():
        data = getTopUserRetard()

        attr = [data.most_common()[0][0], data.most_common()[1][0], data.most_common()[2][0], data.most_common()[3][0],
                data.most_common()[4][0], data.most_common()[5][0]]
        v1 = [data.most_common()[0][1], data.most_common()[1][1], data.most_common()[2][1], data.most_common()[3][1],
              data.most_common()[4][1], data.most_common()[5][1]]
        pie = Pie("Retard Chart", title_pos="42%")
        pie.add("", attr, v1, radius=[30, 55],
                legend_pos="65%", legend_orient='vertical')

        pie.render(path='snapshotRetard.png')


def getPieChartSucessVotes():
        data = getTopUserSecessVotes()

        attr = [data.most_common()[0][0], data.most_common()[1][0], data.most_common()[2][0], data.most_common()[3][0],
                data.most_common()[4][0], data.most_common()[5][0]]
        v1 = [data.most_common()[0][1], data.most_common()[1][1], data.most_common()[2][1], data.most_common()[3][1],
              data.most_common()[4][1], data.most_common()[5][1]]
        pie = Pie("Votes mit erfolg", title_pos="42%")
        pie.add("", attr, v1, radius=[30, 55],
                legend_pos="65%", legend_orient='vertical')

        pie.render(path='snapshotSucessVotes.png')


def getPieChartMessages():
        data = getTopUserMessages()
        attr = [data.most_common()[0][0], data.most_common()[1][0], data.most_common()[2][0], data.most_common()[3][0],
                data.most_common()[4][0], data.most_common()[5][0]]
        v1 = [data.most_common()[0][1], data.most_common()[1][1], data.most_common()[2][1], data.most_common()[3][1],
              data.most_common()[4][1], data.most_common()[5][1]]
        pie = Pie("Discord Nachrichten", title_pos="37%")
        pie.add("", attr, v1, radius=[30, 55],
                legend_pos="65%", legend_orient='vertical')
        pie.render(path='snapshotMessages.png')

def getUserStatsChart(discord_user_id, username):
        user = getOnlineStats(discord_user_id)
        attr = ['Aktiv','Stummgeschaltet','Lautsprecher deaktiviert']
        v1 = [user[0] / 60, user[1] / 60, user[2] / 60]
        bar =Bar("Onlinezeit in Minuten von " + username,title_pos="37%")
        bar.add("", attr, v1, radius=[30, 55],
                legend_pos="65%", legend_orient='vertical')
        bar.render(path='onlineTime.png')

def highscoreChart():
        karma = getTopUser()
        retard  = getTopUserRetard()
        votes =  getTopUserSecessVotes()
        message = getTopUserMessages()
        online = getTopUserOnline()
        mute = getTopUserMute()
        deft = getTopUserDef()
        stoned = getTopUserStoned()


        dOnline = Bar("Online Chart in h")
        dOnline.use_theme('dark')
        dOnline.add("Online", helper(online,10), helper2(online,10,True),xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30,is_stack=True)
        dOnline.add("Mic Muted",helper(mute,10), helper2(mute,10,True),xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30,is_stack=True)
        dOnline.add("Sound Muted", helper(deft, 10), helper2(deft, 10,True), xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30,
                is_stack=True)


        dKarma = Pie("Karma Verteilung",title_pos='center')
        dKarma.use_theme('dark')
        dKarma.add("", helper(karma,10), helper2(karma,10,False),label_text_color=None,
        is_label_show=True, legend_orient='vertical',
        legend_pos='left',center=[45, 60])

        count = 0
        for item in retard.most_common():
            count = count + int(item[1])


        dgauge = Gauge("Retard Domination")
        dgauge.use_theme('dark')
        dgauge.add(retard.most_common()[0][0].split('#')[0].split('|')[0], '', (retard.most_common()[0][1])/count *100, angle_range=[180, 0],
                  scale_range=[0, 100], is_legend_show=True)

        jcount = 0
        for item in stoned.most_common():
            jcount = jcount + int(item[1])


        dstoned = Gauge("Junkie Domination")
        dstoned.use_theme('dark')
        dstoned.add(stoned.most_common()[0][0].split('#')[0].split('|')[0], '', int((stoned.most_common()[0][1])/jcount *100), angle_range=[180, 0],
                  scale_range=[0, 100], is_legend_show=True)


        vcount = 0
        for iitem in votes.most_common():
            vcount = vcount + int(iitem[1])


        dvotes = Gauge("Vote Domination")
        dvotes.use_theme('dark')
        dvotes.add(votes.most_common()[0][0].split('#')[0].split('|')[0], '', int((votes.most_common()[0][1])/vcount *100), angle_range=[180, 0],
                  scale_range=[0, 100], is_legend_show=True)

        mcount = 0
        for item in message.most_common():
            mcount = mcount + int(item[1])

        dmessage = Gauge("Message Domination")
        dmessage.use_theme('dark')
        style = Style()

        for counter in range(1):
            dmessage.add(message.most_common()[counter][0].split('#')[0].split('|')[0], '',
                         int((message.most_common()[counter][1]) / mcount * 100), angle_range=[180, 0],
                         scale_range=[0, 100], is_legend_show=True)
        # retardr = []
        # retard = getRetardReason()
        # for item in retard.most_common():
        #     str(retardr.append(item[1]))
        #     str(retardr.append(item[1]))
        #     str(retardr.append(item[1]))
        #     str(retardr.append(item[1]))
        #
        # name = [
        #     retardr[0], 'saaaaaaaaaadssddddddddd', retardr[0], 'Jurassic World', retardr[0],
        #     'Chick Fil A', retardr[0], retardr[0], 'Express', 'Home', retardr[0],
        #     'Lena Dunham', 'saaaaaaaaaadssddddddddd Hamilton', 'saaaaaaaaaadssddddddddd', 'Mary Ellen Mark',
        #     'Farrah Abraham',
        #     'Rita Ora', retardr[0], 'NCAA baseball saaaaaaaaaadssddddddddd', 'Point Break']
        # value = [100, 1000, 100, 1000]
        #
        # wordcloud = WordCloud(width=1300, height=620)
        # wordcloud.add("", retardr, value, word_size_range=[20, 100])



        #wordcloud.render(path='retardr.gif')
        dvotes.render(path='dvotes.gif')
        dmessage.render(path='dmessages.gif')
        dstoned.render(path='dstoned.gif')
        dgauge.render(path='gRetard.gif')
        dOnline.render(path='dOnline.gif')
        dKarma.render(path='dPie.gif')


