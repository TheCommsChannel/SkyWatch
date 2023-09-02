# SkyWatch

This script is to be used in conjunction with an readsb/tar1090 setup to alert on specific aircraft via their Hex code, N-Number, or Flight Name. This has only been tested with the image from adsbexchange.com, but it should work with readsb/tar1090 setup.

The **watchlist.txt** file can contain a list of aircraft by Hex code, N-Number, Flight ID. You can also use * as a wildcard for picking up any flight starting with whatever you want. (e.g. AAL* will pick up all aircraft with a flight ID starting with AAL)

There is a section in the code with squawk codes to alert on that can be edited to fit your needs.

## Plane Data Source:
https://github.com/sdr-enthusiasts/plane-alert-db/tree/main
