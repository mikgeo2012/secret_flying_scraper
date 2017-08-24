# Scrape secretflying.com for all flights from location to destination

from bs4 import BeautifulSoup
import urllib
import requests
import re
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

masterList = {}

DEPARTURE = ["Chicago", "Detroit"]

ARRIVAL = ["Seoul", "Hong Kong", "Singapore", "Tokyo", "Shanghai", "Bangkok", "Beijing", "Osaka", "Manila"]

def parsePage(lim):
    i = 1

    while i <= lim:
        req = requests.get('http://www.secretflying.com/usa-deals/page/' + str(i), headers={'User-Agent': 'Mozilla/5.0'})

        soup = BeautifulSoup(req.text, "html.parser")


        a = soup.find_all('div', class_='snews-loop-wrap')


        articles = []

        for elm in a[0].find_all('article'):
            if "post-37933" not in elm["class"]:
                articles.append(elm)



        for article in articles:
            text = article.div.h2.a.get_text()
            if (any(s in text for s in DEPARTURE) and any(s in text for s in ARRIVAL)) and (text not in masterList):
                masterList[text] = article.div.h2.a["href"]


        i += 1


def sendEmail(sender, receiver):
    gmail_user = 'mkyeong1309@gmail.com'
    gmail_password = 'Prabhu1110'

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
    except:
        print 'Something went wrong...'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Flight Deals of the Day"
    msg['From'] = sender
    msg['To'] = receiver

    text = ""
    html = "<html><head></head><body><p>"

    for k, v in masterList.iteritems():
        text += k + " | " + v + "\n"
        html += "<a href='{0}'>{1}</a>".format(v, k) + "<br>"

    html +="</p></body></html>"



    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)


    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sender, receiver, msg.as_string())
        server.close()

        print 'Email sent!'
    except:
        print 'Something went wrong when sending...'

if __name__ == "__main__":
    parsePage(5)
    sendEmail("mkyeong1309@gmail.com", "mikgeo2012@gmail.com")



