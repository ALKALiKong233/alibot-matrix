# ALKALiKong's Personal Matrix Bots

## Now Including
* Android ROM Buildbot for Matrix
* Status Bot

## Me noob in Python so don't laungh at my code

## Thanks:
* [SiHua](https://github.com/zxc135781)

## Usage:
### Android ROM Buildbot for Matrix:
1. Copy `buildbot.config.example` to `buildbot.config` and fill it. Note: leave blank for proxy if you don't use proxy
2. Edit `build.sh` and `buildbot.py` to fit your ROM
3. Run `buildbot.py` and enjoy!
```
    !build <target-variant> <making-target> [options]
    <target-variant>: The variant you gonna to lunch, such as yaap_lisa-eng
    <making-target>: The target you gonna to make (make <making-target> )
    [options]: -c: Run mka installclean before building
               -g: Build GAPPS variant of your ROM
```
```
    !getava: Get a list of avaliable ZIPs you've built
```
```
    !upload <cookies:remember-mev2=> <cow-auth-token> <file-path>
    Description: Upload files to CowTransfer using https://github.com/Mikubill/transfer
```
### Status Bot
```
    !getsysinfo: Get some system info
```