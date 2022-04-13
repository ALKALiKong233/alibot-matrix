from distutils.command.config import config
from os import system
import os
from pbwrap import Pastebin
import simplematrixbotlib as botlib
from configparser import ConfigParser
import psutil

cp = ConfigParser()
cp.read('buildbot.config', encoding='UTF-8')
logininfo = cp['login']
buildinfo = cp['build']
pastebininfo  = cp['pastebin']
PB = Pastebin(pastebininfo['key'])
Creds = botlib.Creds(logininfo['homeserver'], logininfo['user'], logininfo['password'])
alibuildbot = botlib.Bot(Creds)
PREFIX = '!'

@alibuildbot.listener.on_message_event
async def sysInfo(room, message):
    match = botlib.MessageMatch(room, message, alibuildbot, PREFIX)
    if match.is_not_from_this_bot() and match.prefix() and match.command("getinfo"):
        systemInfo = 'CPU Count:' + str(psutil.cpu_count()) + ' RAM Status:' + str(psutil.virtual_memory())
        await alibuildbot.api.send_text_message(room.room_id, systemInfo)
    

@alibuildbot.listener.on_message_event
async def repo(room, message):
    match = botlib.MessageMatch(room, message, alibuildbot, PREFIX)
    if match.is_not_from_this_bot() and match.prefix() and match.command("sync"):
        os.chdir(buildinfo['dir'])
        if not match.args():
            sync = os.system(buildinfo['proxy'] + 'repo sync --force-sync -j$(nproc --all) --no-tags --no-clone-bundle --current-branch | tee sync.log ')
        else:
            sync = os.system(buildinfo['proxy'] + 'repo sync --force-sync -j$(nproc --all) --no-tags --no-clone-bundle --current-branch' + match.args() + '| tee sync.log ')
        await alibuildbot.api.send_text_message(room.room_id, 'Sync Status:' + str(sync))
        url = PB.create_paste_from_file('sync.log', 0, None, None, None)
        await alibuildbot.api.send_text_message(room.room_id, 'Sync log:' + str(url))

alibuildbot.run()