import discord
import asyncio
import re # needed for regex

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def findWholeWord(w): # uses regular expressions to prevent finding words within other words, e.g. 'here' in the word 'there'
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

#Open the text file containing the banned words and split them into a list
fobj = open("swearWords.txt")
txtFile = fobj.read().strip().split()
fobj.close()

@client.event
async def on_message(message): # every time a message is posted, mod-bot will check to see if it contains any banned words
##    if message.content.startswith('!test'):
##        counter = 0
##        tmp = await client.send_message(message.channel, 'Calculating messages...')
##        async for log in client.logs_from(message.channel, limit=100):
##            if log.author == message.author:
##                counter += 1
##
##        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
##    elif message.content.startswith('!sleep'):
##        await asyncio.sleep(5)
##        await client.send_message(message.channel, 'Done sleeping')
    #print("Message author id is ", message.author.id)

    # we do not want the bot to reply to itself - this stops it flagging its own messages
    if message.author == client.user:
        return
    
    # making use of the text file from http://www.bannedwordlist.com/
    # todo each of which has a response appropriate to- whatever is appropriate.  Don't forget to use the toxic role. 
    if message.channel.name != "adult-only-chat": # this isolates 'adult-only-chat' from this bot's influence
        if findWholeWord("hello")(message.content.lower()):
            await client.send_message(message.channel, 'Hi there')
        elif findWholeWord("gay")(message.content.lower()):
            await client.send_message(message.channel, "Homophobia is not welcome here - think carefully about how you're using that word Jacko.")
        for each in txtFile: # loop through the list of banned words
            if findWholeWord(each)(message.content.lower()):
                await client.send_message(message.channel, "Found the word '" + each + "' ") # if a word is found, post a message to the channel stating which banned word was found
                print("Recognised that a member called " + message.author.name + " used the banned word '" + each + "'")
                # check if the message.author already has the 'warned' role
                newRoleAwarded = ""
                bannedBefore = False
                for r in message.author.roles:
                    if r.name == "warned": # if they have already been warned then ban them or mute them immediately (toxic role)
                        bannedBefore = True
                if bannedBefore:
#use replace_roles maybe? it replaces all old roles with whatever new roles are specified
                    role = discord.utils.get(message.server.roles, name="toxic")
                    await client.add_roles(message.author, role)
                    print("Toxic role awarded for second offence...")
                    await client.send_message(message.channel, "Successfully added role {0}".format(role.name))
                    oldRole = discord.utils.get(message.server.roles, name="warned")
                    await client.remove_roles(message.author, oldRole)
                    print("... and removed warning role")
                    newRoleAwarded = "toxic"
                else: # warn the user and record that warning somewhere for checking in future (warned role) 
                    role = discord.utils.get(message.server.roles, name="warned")
                    await client.add_roles(message.author, role)
                    await client.send_message(message.channel, "Successfully added role {0}".format(role.name))
                    newRoleAwarded = "warned"
                        
                # record the warning by sending me a private message
                #scruffyUser = server.get_member(305284540887334923)
                server=message.author.server
                await client.send_message(server.owner, "The user named '" + message.author.name + "' has been awarded the '" + newRoleAwarded + "' role for using the banned word '" + each + "'")
                print("Sent message to " + server.owner.name)

                
                
                # Reasons and words used must be recorded 
                

client.run('token-goes-here')
