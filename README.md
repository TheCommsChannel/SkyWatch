[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/B0B1OZ22Z)

SkyWatch

This script is to be used in conjunction with an readsb/tar1090 setup to alert on specific aircraft via their Hex code, N-Number, or Flight Name. This has only been tested with the image from adsbexchange.com, but it should work with readsb/tar1090 setup.

The **watchlist.txt** file can contain a list of aircraft by Hex code, N-Number, Flight ID. You can also use * as a wildcard for picking up any flight starting with whatever you want. (e.g. AAL* will pick up all aircraft with a flight ID starting with AAL) One aircraft per line. These should be followed by a colon and then a label which can be whatever you like. 
**Example:** `"a88bde: Dept of Commerce (hurricane hunters)"`

There is a section in the code with squawk codes to alert on that can be edited to fit your needs.

### Telegram Bot

Open up Telegram and search for "BotFather" and send the command `/newbot` and then follow the prompts for the bot name and username. You'll then be provided with the bot's token to be entered in the `TELEGRAM_BOT_TOKEN` section of the code.
Next click on the link provided by BotFather, usually `t.me/thebotnamehere`. This will take you to the bot and you can hit start.

Then you can go to the following link for checking the Telegram Chat ID.

```
https://api.telegram.org/botYOURBOTTOKENHERE/getUpdates
```

### Systemd Service

If you would like to set this script up as a systemd service that will start the script at boot time and restart it if the script stops, take the following steps to do so:

From the SkyWatch directory, run the following commands:

```bash
sudo cp skywatch.service /etc/systemd/system/
```

```bash
sudo systemctl enable skywatch.service
```

```bash
sudo systemctl start skywatch.service
```

The service should be started now and should start anytime your device is powered on or rebooted. You can check the status ofk the service by running the following command:

```bash
sudo systemctl status skywatch.service
```

If you need to stop the service, you can run the following:

```bash
sudo systemctl stop skywatch.service
```

###

### Plane Data Source:

https://github.com/sdr-enthusiasts/plane-alert-db/tree/main
