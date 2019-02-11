import random
from sqlalchemy import *

from collections import Counter

db = create_engine('mysql+mysqlconnector://discord:7T4vVtjC9VF41Sil@78.46.212.179/discord')


db.echo = False  # Try changing this to True and see what happens
connection = db.connect()
metadata = MetaData(db)


tbl = Table('users', metadata,
               Column('user_id', Integer, primary_key=True),
               Column('discord_user_id', String(255)),
               Column('discord_name', String(255)),
               Column('karma', Integer),
               Column('retardnis', Integer),
               Column('vote_true', Integer),
               Column('vote_false', Integer),
               Column('messages', Integer),
               Column('time_online', Integer),
               Column('time_mute', Integer),
               Column('time_def', Integer),
               Column('stoned', Integer))

rr = Table('retard_reasons', metadata,
               Column('discord_user_id', String(255), primary_key=True),
               Column('message', String(255)),
               Column('accepted', String(255)),
               Column('requested_by', String(255)))
########################################stoned####################################################################

def getJunkie(discord_user_id):
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row.stoned

def addJunkie(discord_user_id,add_junk_stat):
    smt = tbl.update().values(stoned=(tbl.c.stoned + add_junk_stat)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)


########################################Online_Stuff####################################################################



def getTime_Mute(discord_user_id):
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row.time_mute

def getOnlineStats(discord_user_id):
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row.time_online,row.time_mute,row.time_def

def addTime_Mute(discord_user_id,time_mute_to_add):
    smt = tbl.update().values(time_mute=(tbl.c.time_mute + time_mute_to_add)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)


def getTime_Online(discord_user_id):
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row.time_online



def addTime_Online(discord_user_id,time_online_to_add):
    smt = tbl.update().values(time_online=(tbl.c.time_online + time_online_to_add)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)



def getTime_def(discord_user_id):
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row.time_def


def addTime_def(discord_user_id, time_def_to_add):
    smt = tbl.update().values(time_def=(tbl.c.time_online + time_def_to_add)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)


############################################Top_Stuff###################################################################


def getTopUser():
    userdict = {}
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        userdict[row.discord_name] = row.karma
    userdict = Counter(userdict)
    return userdict


def getTopUserRetard():
    userdict = {}
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        userdict[row.discord_name] = row.retardnis
    userdict = Counter(userdict)
    return userdict

def getTopUserMessages():
    userdict = {}
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        userdict[row.discord_name] = row.messages
    userdict = Counter(userdict)
    return userdict

def getTopUserSecessVotes():
    userdict = {}
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        userdict[row.discord_name] = row.vote_true
    userdict = Counter(userdict)
    return userdict

def getTopUserOnline():
    userdict = {}
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        userdict[row.discord_name] = row.time_online
    userdict = Counter(userdict)
    return userdict

def getTopUserMute():
    userdict = {}
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        userdict[row.discord_name] = row.time_mute
    userdict = Counter(userdict)
    return userdict

def getTopUserDef():
    userdict = {}
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        userdict[row.discord_name] = row.time_def
    userdict = Counter(userdict)
    return userdict


def getTopUserStoned():
    userdict = {}
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        userdict[row.discord_name] = row.stoned
    userdict = Counter(userdict)
    return userdict


####################################################USER################################################################

def addUser(discord_user_id,discord_name):
    i = tbl.insert()
    i.execute(discord_user_id=discord_user_id, discord_name=discord_name)

def getUser(discord_user_id,discord_name):
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row
    addUser(discord_user_id,discord_name)
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row


#######################################################Karma#########################################

def getKarma(discord_user_id):
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row.karma

def addKarma(discord_user_id,karma_to_add):
    smt = tbl.update().values(karma=(tbl.c.karma + karma_to_add)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)

def remKarma(discord_user_id,karma_to_remove):
    smt = tbl.update().values(karma=(tbl.c.karma - karma_to_remove)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)

#######################################################Retard#########################################

def getRetard(discord_user_id):
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row.retardnis

def addRetard(discord_user_id,retardnis_to_add):
    smt = tbl.update().values(retardnis=(tbl.c.retardnis + retardnis_to_add)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)

def remRetard(discord_user_id,retardnis_to_remove):
    smt = tbl.update().values(retardnis=(tbl.c.retardnis - retardnis_to_remove)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)

#######################################################Vote_True#########################################

def getVote_True(discord_user_id):
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row.vote_true

def addVote_True(discord_user_id,vote_true_to_add):
    smt = tbl.update().values(vote_true=(tbl.c.vote_true + vote_true_to_add)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)

def remVote_True(discord_user_id,vote_true_to_remove):
    smt = tbl.update().values(vote_true=(tbl.c.vote_true - vote_true_to_remove)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)

#######################################################Vote_False#########################################

def getVote_False(discord_user_id):
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row.vote_false

def addVote_False(discord_user_id,vote_false_to_add):
    smt = tbl.update().values(vote_false=(tbl.c.vote_false + vote_false_to_add)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)

def remVote_False(discord_user_id,vote_false_to_remove):
    smt = tbl.update().values(vote_false=(tbl.c.vote_false - vote_false_to_remove)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)

#######################################################messages#########################################

def getMessages(discord_user_id):
    s = tbl.select()
    rs = s.execute()
    for row in rs:
        if row.discord_user_id == discord_user_id:
            return row.messages

def addMessages(discord_user_id,messages_to_add):
    smt = tbl.update().values(messages=(tbl.c.messages + messages_to_add)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)

def remMessages(discord_user_id,messages_to_remove):
    smt = tbl.update().values(messages=(tbl.c.messages - messages_to_remove)). \
        where(tbl.c.discord_user_id == discord_user_id)
    connection.execute(smt)

#######################################################retard_reason#########################################

def addRetardReason(discord_user_id,message,accepted,requested_by):
    try:
        i = rr.insert()
        i.execute(discord_user_id=discord_user_id, message=message, accepted=accepted,requested_by=requested_by)
    except:
        None
def getRetardReason():
    userdict = {}
    s = rr.select()
    rs = s.execute()
    for row in rs:
        userdict[row.discord_user_id] = row.message
    userdict = Counter(userdict)
    return userdict








