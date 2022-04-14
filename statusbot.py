import simplematrixbotlib as botlib
from configparser import ConfigParser
import psutil

cp = ConfigParser()
cp.read('buildbot.config', encoding='UTF-8')
logininfo = cp['login']
buildinfo = cp['build']
Creds = botlib.Creds(logininfo['homeserver'], logininfo['user'], logininfo['password'])
statusbot = botlib.Bot(Creds)
PREFIX = '!'

@statusbot.listener.on_message_event
async def sysInfo(room, message):
    match = botlib.MessageMatch(room, message, statusbot, PREFIX)
    if match.is_not_from_this_bot() and match.prefix() and match.command("getsysinfo"):
        mem = psutil.virtual_memory()
        RAMTOTAL = float(mem.total) / 1024 / 1024 / 1024
        RAMUSED = float(mem.used) / 1024 / 1024 / 1024
        RAMFREE = float(mem.free) / 1024 / 1024 / 1024
        RAMUSEDPERCENT = mem.percent
        CPUTHREAD = psutil.cpu_count()
        CPUUSEDPERCENT = psutil.cpu_percent()
        systemInfo = f"""RAM Total: {round(RAMTOTAL,3)} GB
RAM Used: {round(RAMUSED,3)} GB
RAM Free: {round(RAMFREE,3)} GB
RAM Used Percent: {RAMUSEDPERCENT}%
CPU Thread: {CPUTHREAD}
CPU Used Percent: {CPUUSEDPERCENT}%
        """
        await statusbot.api.send_text_message(room.room_id, systemInfo)

statusbot.run()
