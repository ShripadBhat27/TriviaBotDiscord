import discord
# import os
# import requests
# import json
import berserk
import asyncio
import requests
from keep_alive import keep_alive

from replit import db
from threading import Timer

import datetime as dt
from time import sleep

client = discord.Client()

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)



userpoints = dict()

def modify_dict( userid ):
    # print(userid)
    if userid not in userpoints:
        userpoints[userid] = 5
    else :
        userpoints[userid] += 5

def print_dict():
    finalresult = ""
    for x in userpoints:
        res = str(x) + ":" + str(userpoints[x])
        finalresult += res
    return finalresult

def ret_dict():
    return userpoints 

msgid = ""
shunya = 0 


       
def timerfun(lastmessage):
    print("helloworld ")
    print(lastmessage.reactions)



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    name=message.author
    


    if msg.startswith("!start_trivia"):
        res = " PLese EnTeR NuMbEr Of QeStIoNs as if you want 1 question !n 1 if you want 2 enter !n 2"
        print(res)
        await message.channel.send(res) # simple command asking number of questions before starting the quiz 
        takeN = True
    
    if msg.startswith("!n"):    
        db["shunya"] = 0;  
        number = msg.split("!n ",1)[1]
        res = " The QuIz will start in next 1 min be ready !!! \n Instructions : \n Once trivia is started and the number of questions is set, trivia begins for all online users in that particular text channel.\n Each question will be asked to participants at an interval of one minute. Within one minute window of two questions, the participants have to react to the question with certain emojis.\n Each option is associated with certain emoji.\n Each participant must react only once to questions and within 1 min. At end of trivia, a leaderboard will be displayed."
        print(res)
        await message.channel.send(res)
        # simple command asking number of questions before starting the quiz
        print(number)
        num=number
        diff="medium"
        URL="https://opentdb.com/api.php?amount="+num+"&category=14&difficulty="+diff+"&type=multiple"
        r=requests.get(url=URL)
        data=r.json()
        # print(data)
        # await message.channel.send(data)
        t = dt.datetime.now()
        minute_count = 0
        tot_no_question=int(number)
        cnt=0
        
        while True:
            global shunya
            
            if(cnt==tot_no_question):
                break 
            delta_minutes = (dt.datetime.now() -t).seconds/30
            if delta_minutes and delta_minutes !=  minute_count:
                global shunya
                minute_count = delta_minutes 
                que=data["results"][cnt]["question"]
                que =que.replace("&#039;", "'")
                que = que.replace("&quot;","\"")
                # for k in ["results"][cnt+1]["incorrect_answers"] :
                # #     res.append(k) 
                option1 = data["results"][cnt]["incorrect_answers"][0]
                option1 = option1.replace("&#039;", "'")
                option1 = option1.replace("&quot;","\"")
                option2 = data["results"][cnt]["incorrect_answers"][1]
                option2 = option2.replace("&#039;", "'")
                option2 = option2.replace("&quot;","\"")
                option3 = data["results"][cnt]["incorrect_answers"][2]
                option3 = option3.replace("&#039;", "'")
                option3 = option3.replace("&quot;","\"")
                correctans  = data["results"][cnt]["correct_answer"]
                correctans = correctans.replace("&#039;", "'")
                correctans = correctans.replace("&quot;","\"")
                cnt+=1

                res =  "Q "  + str(cnt) + " ; " +  que + "\n\n" + option1 + "   ❤" + "\n" + option2 + "   💛"+ "\n" + option2 + "   💚" + "\n" + correctans + "   🧡"
                lastmsg = await message.channel.send(res)
                global msgid
                msgid = lastmsg.id 
                for emoji in ('❤', '💛','💚','🧡'):
                    await lastmsg.add_reaction(emoji)
                #shoud be a global variable 
                # await message.channel.send(msgid)
                # print_dict()

            sleep(30)# Stop maxing out CPU
               


            if(cnt==tot_no_question):
                break 
        
        print("loop chya baher ")                      
        print(shunya)
        #loop through the points and show : 
        res = "Its Showtime of the FInal Results of the !\n Lets see who is The Amazing Human/Genius \n GIve us some time to calculate the results type in !scorecard to check the results out in some time  "
        # print(res)
        await message.channel.send(res)
        
        # value = db["shunya"]
        # print(value)
        # await message.channel.send(value)
        # print_dict()
            # res = "Sorry Connot start a quiz as its not asked "
            # print(res)
            # await message.send(res) # simple command asking number of questions before starting the quiz 
    
    if msg.startswith("!scorecard") :
        res = print_dict()
        resdict = ret_dict() 
        resultres = ""
        tagstring = ""
        sort_orders = sorted(resdict.items(), key=lambda x: x[1], reverse=True)
        for x in resdict:
            print(x)
            cuser = client.get_user(x)
            if(cuser != None ) :
                resstr = cuser.mention + " : "+ str(resdict[x]) +"\n"
                resultres += resstr
                print(resstr)
                tagstring += cuser.mention
        # await message.channel.send(resultres)
        resultres = "Excited For the results here we g0 ...........\n"
        tagstring = ""
        for x in sort_orders:
            print(x[0])
            if(x[0] != 826763139021930546) :
                cuser = client.get_user(x[0])
                if(cuser != None ) :
                    resstr = cuser.mention + " : "+ str(x[1]) +"\n"
                    resultres += resstr
                    print(resstr)
                    tagstring += cuser.mention
        await message.channel.send(resultres)

    
      
          
    if msg.startswith("!help") :
        await message.channel.send("Commands \n \n !start_trivia: starts the trivia contest for everyone online in that text channel at that moment\n \n  !n <number_of_questions>: helps to decide the number of questions in the trivia\n \n !scorecard : helps to display the scores of participants at the end of trivia")

        
   
    
   
@client.event
async def on_raw_reaction_add(payload):
    global shunya
    shunya+=5
        
    # this function will be used to give points to the loka 
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    user = client.get_user(payload.user_id)
    
    userid = payload.user_id
    #comapre ( msgid with payload.message_id) and compare (msgid--> emojistring with payload emoji to string )if true add score in score wala map


    if str(payload.emoji) == "🧡":
        print("INside the inner msgid ")
        value = int(db["shunya"])
        db["shunya"] = value+5
        print_dict()
        modify_dict(userid)




        

        
    
keep_alive()
client.run('Should not be shared here ')
