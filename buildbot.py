from distutils.command.config import config
from lib2to3.refactor import MultiprocessRefactoringTool
from os import system
import os
from pbwrap import Pastebin
import simplematrixbotlib as botlib
from configparser import ConfigParser
from aligo import Aligo
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
        mkscr = os.popen('readlink -f build.sh').read()
        os.chdir(buildinfo['dir'])
        if '-g' in match.args() and '-c' in match.args():
            await alibuildbot.api.send_text_message(room.room_id, 'Starting Build, clean, GAPPS')
            build = os.system('bash ' + buildinfo['botdir'] + 'build.sh' + ' 1 1 ' + buildinfo['dir'] + ' ' + str(match.args()[0]) + ' ' + str(match.args()[1]))
        elif '-g' in match.args():
            await alibuildbot.api.send_text_message(room.room_id, 'Starting Build, clean, VANILLA')
            build = os.system('bash ' + buildinfo['botdir'] + 'build.sh' + ' 0 1 ' + buildinfo['dir'] + ' ' + str(match.args()[0]) + ' ' + str(match.args()[1]))
        elif '-c' in match.args():
            await alibuildbot.api.send_text_message(room.room_id, 'Starting Build, dirty, GAPPS')
            build = os.system('bash ' + buildinfo['botdir'] + 'build.sh' + ' 1 0 ' + buildinfo['dir'] + ' ' + str(match.args()[0]) + ' ' + str(match.args()[1]))
        if build == 0:
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
    if match.is_not_from_this_bot() and match.prefix() and match.command("cowupload"):
        os.chdir(buildinfo['dir'])
        upload = os.popen('./transfer cow --cookie=' + str(match.args()[0]) + ' -a ' + str(match.args()[1]) + ' ' + str(match.args()[2])).read()
        await alibuildbot.api.send_text_message(room.room_id, 'Download link:' + upload)

@alibuildbot.listener.on_message_event
async def upload(room, message):
    match = botlib.MessageMatch(room, message, alibuildbot, PREFIX)
    if match.is_not_from_this_bot() and match.prefix() and match.command("aliupload"):
        ali = Aligo(refresh_token=str(match.args()[0]))
        ali.get_file_by_path('buildbot')
        ali.upload_file(str(match.args()[1]),'buildbot')

alibuildbot.run()
