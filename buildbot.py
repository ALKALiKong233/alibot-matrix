from distutils.command.config import config
from lib2to3.refactor import MultiprocessRefactoringTool
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
            sync = os.system(str(buildinfo['proxy']) + ' repo sync --force-sync -j$(nproc --all) --no-tags --no-clone-bundle --current-branch | tee sync.log ')
        else:
            sync = os.system(str(buildinfo['proxy']) + ' repo sync --force-sync -j$(nproc --all) --no-tags --no-clone-bundle --current-branch ' + " ".join(match.args()) + ' | tee sync.log ')
        if sync ==0:
            await alibuildbot.api.send_text_message(room.room_id, 'Sync Status: Succeed')
        else:
            await alibuildbot.api.send_text_message(room.room_id, 'Sync Status: Failed')
        url = PB.create_paste_from_file('sync.log', 0, None, None, None)
        await alibuildbot.api.send_text_message(room.room_id, 'Sync log:' + url)

@alibuildbot.listener.on_message_event
async def build(room, message):
    match = botlib.MessageMatch(room, message, alibuildbot, PREFIX)
    if match.is_not_from_this_bot() and match.prefix() and match.command("build"):
        os.chdir(buildinfo['dir'])
        if '-c' in match.args():
            await alibuildbot.api.send_text_message(room.room_id, 'Starting installclean')
            os.system('bash build/envsetup.sh && lunch ' + str(match.args()[0]) + ' && mka installclean')
            await alibuildbot.api.send_text_message(room.room_id, 'Installclean finished')
        await alibuildbot.api.send_text_message(room.room_id, 'Starting Build')
        if '-gapps' in match.args():
            os.environ['YAAP_BUILDTYPE']="GAPPS"
            await alibuildbot.api.send_text_message(room.room_id, 'Option -g found, building GAPPS Variant')
        else:
            os.environ['YAAP_BUILDTYPE']="VANILLA"
            await alibuildbot.api.send_text_message(room.room_id, 'Option -g not found, building VANILLA Variant')
        build = os.system('bash build/envsetup.sh && lunch '+ str(match.args()[0]) + ' && mka yaap -j$(nproc --all) | tee build.log')
        if build ==0:
            await alibuildbot.api.send_text_message(room.room_id, 'Build succeed')
            url = PB.create_paste_from_file('build.log', 0, None, None, None)
            await alibuildbot.api.send_text_message(room.room_id, 'Build log:' + url)
        else:
            await alibuildbot.api.send_text_message(room.room_id, 'Build Failed')
            url = PB.create_paste_from_file('build.log', 0, None, None, None)
            await alibuildbot.api.send_text_message(room.room_id, 'Build log:' + url)

@alibuildbot.listener.on_message_event
async def ava(room, message):
    match = botlib.MessageMatch(room, message, alibuildbot, PREFIX)
    if match.is_not_from_this_bot() and match.prefix() and match.command("getava"):
        os.chdir(buildinfo['dir'])
        ava = os.popen('find out/target/product/lisa -maxdepth 1 -type f -name "YAAP*lisa*.zip" | sed -n -e "1{p;q}"').read()
        await alibuildbot.api.send_text_message(room.room_id, 'Available ZIPs: ' + ava)

@alibuildbot.listener.on_message_event
async def upload(room, message):
    match = botlib.MessageMatch(room, message, alibuildbot, PREFIX)
    if match.is_not_from_this_bot() and match.prefix() and match.command("upload"):
        os.chdir(buildinfo['dir'])
        upload = os.popen('./transfer cow --cookie=' + str(match.args()[0]) + ' -a ' + str(match.args()[1]) + ' ' + str(match.args()[2])).read()
        await alibuildbot.api.send_text_message(room.room_id, 'Download link:' + upload)

alibuildbot.run()