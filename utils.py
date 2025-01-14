import requests
import praw
import random as rd

def getMsgAttributes(bot, update):
    myself = str(update.message.from_user.username)
    myselfID = str(update.message.from_user.id)
    text = str(update.message.text)
    
    isGroup = str(update.message.chat.type) == "group"
    chatID = str(update.message.chat_id)
    chatName = str(update.message.chat.title if isGroup else update.message.chat.username)

    cm = bot.getChatMember(chatID, int(myselfID))
    isAdmin = cm.status == "creator" or cm.status == "administrator"
    canRunAdmin = not isGroup or update.message.chat.all_members_are_administrators or isAdmin

    return (myself, text, isGroup, chatID, chatName, canRunAdmin)

def printCommandExecution(bot, update):
    myself, text, isGroup, chatID, chatName, canRunAdmin = getMsgAttributes(bot, update)

    print("{{{}}}@{} in {}[{}]: \"{}\"".format("A" if canRunAdmin else "U", myself, chatName, chatID, text))

def loadFile(filename):
    with open(filename, encoding="UTF-8") as f:
        content = [l.strip() for l in f]

    return content

def parseGender(filme, gender):
    words = filme.split()

    if gender == "male":
        for i in range(len(words)):
            if words[i].startswith("["):
                s = words[i].index("[")+1
                e = words[i].index("|")
                words[i] = words[i][s:e]
    else: # female
        for i in range(len(words)):
            if words[i].startswith("["):
                s = words[i].index("|")+1
                e = words[i].index("]")
                words[i] = words[i][s:e]

    return " ".join(words)

def getRandomImageReddit(reddit, subreddit, user=None, l=50):
    if not user:
        sub = reddit.subreddit(subreddit)
    else:
        sub = reddit.multireddit(user, subreddit)
    
    posts = [post for post in sub.hot(limit=l)]

    randomPost = None
    isImage = False
    while not isImage and posts:
        randomPost = rd.choice(posts)
        isImage = randomPost.url.endswith(".jpg") or randomPost.url.endswith(".png") or randomPost.url.endswith(".jpeg")
        if not isImage: posts.remove(randomPost)

    if randomPost:
        return randomPost.title, randomPost.url
    else:
        return None, None