from telegram import InlineQueryResultPhoto
import os, random
from pyquery import PyQuery as pq
from html2image import Html2Image
from datetime import datetime

hti = Html2Image(
    browser_executable="./chrome/App/Chrome-bin/chrome.exe",
    custom_flags=["--hide-scrollbars", "--window-size=800,1150"],
)


def createCard(html_str):
    now = datetime.now()
    nameFile = "photo" + str(now.strftime("%Y-%m-%d-%H%M%S")) + ".png"
    hti.screenshot(
        html_str=html_str,
        css_file="templates/style.css",
        save_as=nameFile,
    )
    return nameFile # name of photo to upload


def generateCard(data, name, rootDir):
    # load random image
    fontColor = random.choice(os.listdir(".\\templates\\cards\\"))
    print(fontColor)
    imagePath = (
        str(rootDir)
        + f"\\templates\\cards\\{fontColor}\\" 
        + random.choice(os.listdir(f".\\templates\\cards\\{fontColor}\\"))
    )
    
    # calculate average
    average = str(int(sum(data.values()) / len(data)))
    # load html
    htmlString = pq(open("./templates/baseCard.html").read())
    # set font color
    htmlString("#container").attr("class",fontColor)
    # Fill name
    htmlString(".cardContent")(".name")(".din-font").append(name)
    # Fill average
    htmlString(".cardContent")(".average")(".din-font").append(average)
    # Fill image path
    htmlString("#cardModel").attr("src", imagePath)
    data['auton'] = data['autonomo']
    for value in data:
        # Fill text
        htmlString(".cardStaticContent")("." + value.lower())(".din-font").append(
            value.upper()
        )
        # Fill values
        htmlString(".cardContent")("." + value.lower())(".din-font").append(
            str(data[value])
        )

    # create file in temp folder
    nameFile = createCard(str(htmlString))
    return nameFile


def constructResultPhoto(thumb_url, image_url):    
    # return inlinequeryResultPhoto
    return InlineQueryResultPhoto(
        id="Cromo",
        title="Crea una Medalla con tus características",
        description="¡Muestra con orgullo tu mierda de característicasS!",
        photo_url=image_url,
        photo_width=800,
        photo_height=1150,
        thumb_url=thumb_url,
    )
