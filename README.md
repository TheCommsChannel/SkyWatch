[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B1OZ22Z)

# SkyWatch

This script is to be used in conjunction with an readsb/tar1090 setup to alert on specific aircraft via their Hex code, N-Number, or Flight Name. This has only been tested with the image from adsbexchange.com, but it should work with readsb/tar1090 setup.

The **watchlist.txt** file can contain a list of aircraft by Hex code, N-Number, Flight ID. You can also use * as a wildcard for picking up any flight starting with whatever you want. (e.g. AAL* will pick up all aircraft with a flight ID starting with AAL) One aircraft per line.

There is a section in the code with squawk codes to alert on that can be edited to fit your needs.

### Telegram Bot 
Open up Telegram and search for "BotFather" and send the command `/newbot` and then follow the prompts for the bot name and username. You'll then be provided with the bot's token to be entered in the `TELEGRAM_BOT_TOKEN` section of the code.
Next click on the link provided by BotFather, usually `t.me/thebotnamehere`. This will take you to the bot and you can hit start.

Then you can go to the following link for checking the Telegram Chat ID.
```
https://api.telegram.org/botYOURBOTTOKENHERE/getUpdates
```

### Plane Data Source:
https://github.com/sdr-enthusiasts/plane-alert-db/tree/main
