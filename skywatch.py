import requests
import fnmatch
import time
import csv

# Enter in your Bot Token and the Chat ID of the chat you want the alerts sent to.
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""

# Add or remove these as needed
SQUAWK_MEANINGS = {
    "7500": "Aircraft Hijacking",
    "7600": "Radio Failure",
    "7700": "Emergency",
    "5000": "NORAD",
    "5400": "NORAD",
    "6100": "NORAD",
    "6400": "NORAD",
    "1277": "Search & Rescue"
}


def load_watchlist():
    watchlist = []
    with open("watchlist.txt", "r") as file:
        for line in file:
            watchlist.append(line.strip().upper())
    return watchlist


def send_telegram_alert(message):
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    params = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
    }
    response = requests.get(telegram_url, params=params)
    return response.status_code


def get_aircraft_data():
    url = "http://adsbexchange.local/tar1090/data/aircraft.json"
    response = requests.get(url)
    data = response.json()
    return data['aircraft']


def load_csv_data(filename):
    csv_data = {}
    with open(filename, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            hex_code = row['$ICAO']
            csv_data[hex_code] = row
    return csv_data


def main():
    squawk_alert_history = {}
    watchlist_alert_history = {}
    csv_files = ["plane-alert-civ-images.csv", "plane-alert-mil-images.csv", "plane-alert-gov-images.csv"]
    csv_data = {}

    for filename in csv_files:
        csv_data.update(load_csv_data(filename))

    watchlist = load_watchlist()

    while True:
        aircraft_data = get_aircraft_data()

        for aircraft in aircraft_data:
            hex_code = aircraft['hex'].upper()
            flight = aircraft.get('flight', '').strip().upper()
            squawk = aircraft.get('squawk', '')

            # Alert on specific squawk codes
            if squawk in SQUAWK_MEANINGS and (
                    hex_code not in squawk_alert_history or time.time() - squawk_alert_history[hex_code] >= 3600):
                squawk_alert_history[hex_code] = time.time()
                squawk_meaning = SQUAWK_MEANINGS[squawk]

                if hex_code in csv_data:
                    context = csv_data[hex_code]
                    message = (
                        f"Squawk Alert!\nHex: {hex_code}\nSquawk: {squawk} ({squawk_meaning})\n"
                        f"Flight: {aircraft.get('flight', 'N/A')}\nAltitude: {aircraft.get('alt_geom', 'N/A')} ft\n"
                        f"Ground Speed: {aircraft.get('gs', 'N/A')} knots\nTrack: {aircraft.get('track', 'N/A')}\n"
                        f"Operator: {context.get('$Operator', 'N/A')}\nType: {context.get('$Type', 'N/A')}\n"
                        f"Image: {context.get('#ImageLink', 'N/A')}"
                    )
                else:
                    message = (
                        f"Squawk Alert!\nHex: {hex_code}\nSquawk: {squawk} ({squawk_meaning})\n"
                        f"Flight: {aircraft.get('flight', 'N/A')}\nAltitude: {aircraft.get('alt_geom', 'N/A')} ft\n"
                        f"Ground Speed: {aircraft.get('gs', 'N/A')} knots\nTrack: {aircraft.get('track', 'N/A')}"
                    )

                status_code = send_telegram_alert(message)
                if status_code == 200:
                    message_lines = message.split('\n')[:3]
                    for line in message_lines:
                        print(line)
                else:
                    print(f"Failed to send squawk alert. Status Code: {status_code}")

            # Alert on items in the watchlist
            for entry in watchlist:
                if entry.endswith('*'):
                    if fnmatch.fnmatch(flight, entry):
                        if (hex_code not in watchlist_alert_history or
                                time.time() - watchlist_alert_history[hex_code] >= 3600):
                            watchlist_alert_history[hex_code] = time.time()
                            if hex_code in csv_data:
                                context = csv_data[hex_code]
                                message = (
                                    f"Watchlist Alert!\n"
                                    f"Hex: {hex_code}\n"
                                    f"Flight: {aircraft.get('flight', 'N/A')}\n"
                                    f"Altitude: {aircraft.get('alt_geom', 'N/A')} ft\n"
                                    f"Ground Speed: {aircraft.get('gs', 'N/A')} knots\n"
                                    f"Track: {aircraft.get('track', 'N/A')}\n"
                                    f"Operator: {context.get('$Operator', 'N/A')}\n"
                                    f"Type: {context.get('$Type', 'N/A')}\n"
                                    f"Image: {context.get('#ImageLink', 'N/A')}"
                                )
                            else:
                                message = (
                                    f"Watchlist Alert!\n"
                                    f"Hex: {hex_code}\n"
                                    f"Flight: {aircraft.get('flight', 'N/A')}\n"
                                    f"Altitude: {aircraft.get('alt_geom', 'N/A')} ft\n"
                                    f"Ground Speed: {aircraft.get('gs', 'N/A')} knots\n"
                                    f"Track: {aircraft.get('track', 'N/A')}"
                                )

                            status_code = send_telegram_alert(message)
                            if status_code == 200:
                                message_lines = message.split('\n')[:3]
                                for line in message_lines:
                                    print(line)
                            else:
                                print(f"Failed to send watchlist alert. Status Code: {status_code}")
                elif hex_code == entry or flight == entry:
                    if hex_code not in watchlist_alert_history or time.time() - watchlist_alert_history[hex_code] >= 3600:
                        watchlist_alert_history[hex_code] = time.time()
                        if hex_code in csv_data:
                            context = csv_data[hex_code]
                            message = (
                                f"Watchlist Alert!\n"
                                f"Hex: {hex_code}\n"
                                f"Flight: {aircraft.get('flight', 'N/A')}\n"
                                f"Altitude: {aircraft.get('alt_geom', 'N/A')} ft\n"
                                f"Ground Speed: {aircraft.get('gs', 'N/A')} knots\n"
                                f"Track: {aircraft.get('track', 'N/A')}\n"
                                f"Operator: {context.get('$Operator', 'N/A')}\n"
                                f"Type: {context.get('$Type', 'N/A')}\n"
                                f"Image: {context.get('#ImageLink', 'N/A')}"
                            )
                        else:
                            message = (
                                f"Watchlist Alert!\nHex: {hex_code}\n"
                                f"Flight: {aircraft.get('flight', 'N/A')}\n"
                                f"Altitude: {aircraft.get('alt_geom', 'N/A')} ft\n"
                                f"Ground Speed: {aircraft.get('gs', 'N/A')} knots\n"
                                f"Track: {aircraft.get('track', 'N/A')}"
                            )

                        status_code = send_telegram_alert(message)
                        if status_code == 200:
                            message_lines = message.split('\n')[:3]
                            for line in message_lines:
                                print(line)
                        else:
                            print(f"Failed to send watchlist alert. Status Code: {status_code}")

        time.sleep(30)


if __name__ == "__main__":
    main()
