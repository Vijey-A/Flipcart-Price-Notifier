import os
import bs4
import requests
import yagmail
from dotenv import load_dotenv

load_dotenv()
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("PASSWORD")
receiver_email = os.getenv("RECIEVER_EMAIL")

# use ToFloat to converts ₹1000,000 to 100000
def toFloat(string):
    s = string.replace('₹', '')
    s = s.replace(',', '')
    f = float(s)
    formatted_price = '{:.2f}'.format(f)
    return formatted_price

# sends price drop mail to user
def sendMail(msg):
    yag = yagmail.SMTP(sender_email, sender_password)
    yag.send(
        to=receiver_email,
        subject="Price drop alert !",
        contents=msg,
    )
    return f"Mailed price drop alert to {receiver_email} successfully"

# To check whether price dropped or not
def checkPrice(target_price, current_price, productURL):
    if (current_price <= target_price):
        mail_msg = f"⚠ Price dropped for {productURL} below the target price! Current price: {current_price}"
        message = f"{mail_msg}. Sent mail to {receiver_email}"
        sendMail(mail_msg)
    else:
        message = f"⚠ Price is still above the target price. Current price: {current_price}"
    return message

# gets the price of the product using its pdp URL
def getFlipCartPrice(productUrl):
    res = requests.get(productUrl)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    price_element = soup.select_one(
        '#container > div > div._2c7YLP.UtUXW0._6t1WkM._3HqJxg > div._1YokD2._2GoDe3 > div._1YokD2._3Mn1Gg.col-8-12 > div:nth-child(2) > div > div.dyC4hf > div.CEmiEU > div > div._30jeq3._16Jk6d').text
    return toFloat(price_element)


userInput = input("➡ Enter the Flipcart PDP URL 🔗 : ")
target_price = float(input("➡ Enter the target price 🎯: "))
current_price = float(getFlipCartPrice(userInput))
checked_price = checkPrice(target_price, current_price, userInput)
print(checked_price)
