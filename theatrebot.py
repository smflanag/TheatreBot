import requests
from bs4 import BeautifulSoup
from datetime import datetime


months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def theatre_bot():
    now_full = str(datetime.now())
    now_date = now_full.split(" ")
    now_month = int(now_date[0].split("-")[1])
    now_year = int(now_date[0].split("-")[0])

    theatre_sites = [
        "https://www.abbeytheatre.ie/whats-on/",
        "https://www.gatetheatre.ie/whats-on/",
        "https://www.olympia.ie/whats-on/",
    ]

    play_data = []
    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

    for site in theatre_sites:
        r = requests.get(site, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")

        if "gate" in site:
            play_info_list = soup.find_all(class_="text-content")

            for play in play_info_list:
                theatre = "The Gate Theatre"
                name_of_play = play.h5.a.string.replace("\t","").replace("\r","").replace("\n","")
                date_of_play = play.p.string
                link = play.h5.a.get("href")

                play_dict = {
                            "theatre": theatre,
                            "name_of_play":name_of_play,
                            "date_of_play":date_of_play,
                            "link":link
                        }

                play_data.append(play_dict)

        elif "abbey" in site:
            play_info_list = soup.find_all(class_="event-card-title")

            for play in play_info_list:
                theatre = "The Abbey Theatre"
                name_of_play = play.string
                date_of_play_p = play.find_next("p")
                date_of_play = date_of_play_p.string.replace("\t","").replace("\r\n","")
                link = play.find_next("a").get("href")

                play_dict = {
                    "theatre": theatre,
                    "name_of_play":name_of_play,
                    "date_of_play":date_of_play,
                    "link":link
                }

                play_data.append(play_dict)

        elif "olympia" in site:
            play_info_list = soup.find_all(class_="title")

            for play in play_info_list:
                theatre = "The Abbey Theatre"
                too_far_away = True
                date_of_play = play.find_next("div").find_next("p",class_="first-date").string
                if "-" in date_of_play:
                    first_date = date_of_play.split("-")[0]
                    first_month = (months.index(first_date.split()[0]))+1
                    second_date = date_of_play.split("-")[1]
                    year = int(second_date.split()[2])

                    if first_month > (now_month + 1) or year > now_year:
                        print(first_month,year)
                        pass
                    else:
                        too_far_away = False
                else:
                    month = (months.index(date_of_play.split()[0]))+1
                    year = int(date_of_play.split()[2])
                    if month > (now_month + 1) or year > now_year:
                        pass
                    else:
                        too_far_away = False

                if not too_far_away:
                    name_of_play = play.find_next("a").string
                    link = play.p.a.get("href")

                    play_dict = {
                        "theatre": theatre,
                        "name_of_play":name_of_play,
                        "date_of_play":date_of_play,
                        "link":link
                    }

                    play_data.append(play_dict)



    template = """<html>
    <head></head>
    <body>
    <h1>TheatreBot update</h1>
    <p>Hi Sarah,
    I've just checked the upcoming shows in your favourite theatres for this week. See any you like?</p>   
        """
    for play_index in range(len(play_data)):
        play = play_data[play_index]
        play_details = "%s is playing in %s on %s. Here's the link: %s" % (play["name_of_play"],play["theatre"],play["date_of_play"],play["link"])
        template+="<p>"+play_details+"<p>"
        template+="\r\n"
    template+="</body></html>"

    return template

