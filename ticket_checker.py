import requests
from bs4 import BeautifulSoup
import os

# URL of the ticket booking page
URL = 'https://www.district.in/events/IPL-ticket-booking'

def send_telegram_alert():
    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    chat_id = os.environ.get('TELEGRAM_CHANNEL_ID')
    message = (
        'Tickets for the CSK vs RCB match on March 28, 2025 are now available.\n'
        'Visit: https://www.district.in/events/IPL-ticket-booking'
    )
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    params = {'chat_id': chat_id, 'text': message}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print("Telegram alert sent successfully!")
    else:
        print("Failed to send telegram alert:", response.text)

def check_ticket_availability():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Locate all div elements with a specific class
    divs = soup.find_all('div', class_='css-k20qch')
    for div in divs:
        div_string = str(div).lower()
        # Adjust the text check to match the content structure
        if 'chennai super kings<!-- --> vs <!-- -->royal challengers bengaluru' in div_string:
            print("Found the match div.")
            # Check for indicators of ticket availability
            if 'css-17nyg3h' in div_string or 'book tickets' in div_string:
                print("Tickets are available.")
                return True
            if 'coming soon' in div_string:
                print("Tickets are coming soon.")
                return False
            print("Match div found, but ticket status is unclear.")
            return False
    print("Match div not found.")
    return False

if __name__ == '__main__':
    if check_ticket_availability():
        send_telegram_alert()
        print('Tickets are available. Telegram notification sent.')
    else:
        print('Tickets not available yet.')