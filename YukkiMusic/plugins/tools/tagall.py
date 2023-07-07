import os, logging, asyncio, random
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

from config import BOT_TOKEN as bot_token, API_ID as api_id, API_HASH as api_hash

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)


spam_chats = []


@client.on(events.NewMessage(pattern="^/tagall|@all|/all ?(.*)"))
async def mentionall(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("__This command can be use in groups and channels!__")

    is_admin = False
    try:
        partici_ = await client(GetParticipantRequest(
            event.chat_id,
            event.sender_id
        ))
    except UserNotParticipantError:
        is_admin = False
    else:
        if ("1843616228", bot_token.split(":")[1],
                isinstance(
                    partici_.participant,
                    (
                            ChannelParticipantAdmin,
                            ChannelParticipantCreator
                    )
                )
        ):
            is_admin = True
    if not is_admin:
        return await event.reply("__Only admins can mention all!__")

    if event.pattern_match.group(1) and event.is_reply:
        return await event.reply("__Give me one argument!__")
    elif event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.is_reply:
        mode = "text_on_reply"
        msg = await event.get_reply_message()
        if msg == None:
            return await event.respond(
                "__I can't mention members for older messages! (messages which are sent before I'm added to group)__")
    else:
        return await event.reply("__Reply to a message or give me some text to mention others!__")

    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    emoji = [ 
         "👍", 
         "👎", 
         "❤", 
         "🔥", 
         "🥰", 
         "😁", 
         "👏", 
         "🤔", 
         "🤯", 
         "😱", 
         "🤬", 
         "😢", 
         "🎉", 
         "🤩", 
         "🤮", 
         "💩", 
         "🙏", 
         "👌", 
         "🕊", 
         "🤡", 
         "🥱", 
         "🥴", 
         "😍", 
         "🐳", 
         "🌚", 
         "💯", 
         "🌭", 
         "🤣", 
         "⚡", 
         "🍌", 
         "🏆", 
         "💔", 
         "🤨", 
         "😐", 
         "🍓", 
         "🍾", 
         "😡", 
         "👾", 
         "🤷", 
         "😎", 
         "🙊", 
         "💊", 
         "😘", 
         "🦄", 
         "🙉", 
         "💘", 
         "🆒", 
         "🗿", 
         "🤪", 
         "💅", 
         "☃", 
         "🎄", 
         "🎅", 
         "🤗", 
         "✍", 
         "🤝", 
         "😨", 
         "😇", 
         "🙈", 
         "🎃", 
         "👀", 
         "👻", 
         "🤓", 
         "😭", 
         "😴", 
         "😈", 
         "🖕", 
         "💋", 
     ]
    async for usr in client.iter_participants(chat_id):
        if not chat_id in spam_chats:
            break
        usrnum += 1
        em = random.choice(emoji)
        usrtxt += f"[{em}](tg://user?id={usr.id}) "
        if usrnum == 8:
            if mode == "text_on_cmd":
                txt = f"{msg}\n\n{usrtxt}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ''
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
    is_admin = False
    try:
        partici_ = await client(GetParticipantRequest(
            event.chat_id,
            event.sender_id
        ))
    except UserNotParticipantError:
        is_admin = False
    else:
      if ("1843616228", bot_token.split(":")[1],
      isinstance(
      partici_.participant,
                  (
                    ChannelParticipantAdmin,
                    ChannelParticipantCreator
                  )
                )
         ):
            is_admin = True
    if not is_admin:
        return await event.reply("__Only admins can execute this command!__")
    if not event.chat_id in spam_chats:
        return await event.reply("__There is no proccess on going...__")
    else:
        try:
            spam_chats.remove(event.chat_id)
        except:
            pass
        return await event.respond("__Stopped Mention.__")


#print(">>BOT START DEXX<<")
#client.run_until_disconnected()
