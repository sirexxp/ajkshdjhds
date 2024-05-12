import time
import requests
import urllib.parse
import random
from tqdm import tqdm

def simulate_loading_screen():
    print("Loading...", end="")
    for _ in range(10):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print("\nLoaded!")

def get_single_sms_details():
    sender_id = input("Enter Sender ID: ")
    destination = input("Enter the recipient number (To): ")
    message = input("Enter the message: ")
    return sender_id, destination, message

def get_mass_sms_details():
    companies = ["WhatsApp", "Tinder", "Facebook", "Starbucks", "Apple", "Samsung", "Google", "Microsoft", "Nike", "Adidas", "Sony", "Netflix", "Amazon", "eBay", "McDonald's", "Burger King", "Visa", "MasterCard", "Intel", "AMD", "Cisco"]
    messages = {
        "WhatsApp": "Verify your phone number. Your code: 456123.",
        "Tinder": "Swipe Right to see who likes you!",
        "Facebook": "Your security code is 543218.",
        "Starbucks": "Enjoy 20% off your next order with code COFFEE20!",
        "Apple": "Your Apple ID verification code is 123456.",
        "Samsung": "Your Samsung account needs verification.",
        "Google": "Your Google verification code is 654321.",
        "Microsoft": "Update your password. Your code: 987654.",
        "Nike": "Explore new styles! Get 15% off on your next purchase.",
        "Adidas": "Adidas: Your exclusive offer awaits! Click to unlock.",
        "Sony": "Thank you for registering your product with Sony.",
        "Netflix": "Add a new device to continue streaming.",
        "Amazon": "Amazon security alert: verify login attempt.",
        "eBay": "Your eBay purchase has been confirmed!",
        "McDonald's": "McDelivery: Get your food delivered for free today.",
        "Burger King": "Whooper Wednesday! Get 2 for 1 this week only.",
        "Visa": "Visa Fraud Alert: Verify transaction for $500.",
        "MasterCard": "MasterCard notice: Please confirm your card details.",
        "Intel": "Intel: Your warranty period has been extended.",
        "AMD": "AMD Ryzen: Optimize your gaming experience now.",
        "Cisco": "Cisco WebEx: Schedule your meeting today."
    }

    destination = input("Enter the recipient numbers (comma-separated if multiple): ").split(',')
    amount = min(int(input("Enter the amount of SMS to send (max 20): ")), 20)
    print("Available speeds: slow (1 SMS per minute), medium (1 SMS per 30 seconds), fast (all SMS instantly)")
    speed_choice = input("Choose the speed of sending SMS (slow, medium, fast): ")
    delays = {"slow": 60, "medium": 30, "fast": 0}
    delay = delays[speed_choice]

    return companies, messages, destination, amount, delay

def check_account_balance():
    url = "https://smsmobile.cc/account?username=kekd&password=rifdoV-xejki6-hanryz"
    response = requests.get(url)
    if response.status_code == 200:
        balance_info = response.text.split(',')  # Assuming the API returns comma-separated values
        return "Account Balance Information:\n" + "\n".join(balance_info)
    else:
        return "Failed to retrieve account balance."

def create_sms_url(sender_id, destination, message):
    base_url = "https://smsmobile.cc/sendsms"
    params = {
        "username": "kekd",
        "password": "rifdoV-xejki6-hanryz",
        "type": "2",
        "source": sender_id,
        "destinations": destination,
        "message": urllib.parse.quote(message)
    }
    url_params = urllib.parse.urlencode(params)
    return f"{base_url}?{url_params}"

def send_sms(url):
    response = requests.get(url)
    return response.status_code, response.text

def send_mass_sms(companies, messages, destinations, amount, delay):
    print(f"Sending {amount} SMS at {['slow', 'medium', 'fast'][delay == 60 and 0 or delay == 30 and 1 or 2]} speed.")
    for destination in destinations:
        for i in tqdm(range(amount), desc=f"Sending SMS to {destination}"):
            sender_id = random.choice(companies)
            message = messages[sender_id]
            sms_url = create_sms_url(sender_id, destination, message)
            response = requests.get(sms_url)
            if response.status_code != 200:
                print(f"Failed to send SMS to {destination}. HTTP status code: {response.status_code}")
            if delay > 0:
                time.sleep(delay)

def main():
    while True:
        print("\nChoose an option:")
        print("1. Send SMS")
        print("2. Mass SMS")
        print("3. Check Account Balance")
        print("99. Exit")
        choice = input("Enter choice: ")
        
        if choice == "1":
            sender_id, destination, message = get_single_sms_details()
            sms_url = create_sms_url(sender_id, destination, message)
            status_code, response_text = send_sms(sms_url)
            if status_code == 200:
                print("\nSMS successfully sent!")
            else:
                print(f"\nFailed to send SMS. HTTP status code: {status_code}\nResponse: {response_text}")
        elif choice == "2":
            companies, messages, destinations, amount, delay = get_mass_sms_details()
            send_mass_sms(companies, messages, destinations, amount, delay)
        elif choice == "3":
            balance_info = check_account_balance()
            print(balance_info)
        elif choice == "99":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 99.")

if __name__ == "__main__":
    main()
