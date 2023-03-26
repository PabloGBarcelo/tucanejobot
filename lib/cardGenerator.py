import os, random
from pyquery import PyQuery as pq
from html2image import Html2Image
from datetime import datetime
import cv2

hti = Html2Image(
    browser_executable="./chrome/App/Chrome-bin/chrome.exe",
    custom_flags=["--hide-scrollbars", "--window-size=800,1150"],
)


def createFileName():
    now = datetime.now()
    nameFile = "photo" + str(now.strftime("%Y-%m-%d-%H%M%S")) + ".png"
    return nameFile  # name of photo to upload


def generateCard(data, name, rootDir):
    # Select font color
    fontColor = random.choice(["white", "black"])

    # load random image
    imagePath = (
        str(rootDir)
        + f"\\templates\\cards\\{fontColor}\\"
        + random.choice(os.listdir(f".\\templates\\cards\\{fontColor}\\"))
    )

    flagPath = (
        str(rootDir)
        + f"\\templates\\flags\\"
        + random.choice(os.listdir(f".\\templates\\flags\\"))
    )
    # calculate average
    dataForAverage = {
        k: v
        for k, v in data.items()
        if k in ["puta", "calvo", "autonomo", "pene", "facha", "fairy"]
    }
    average = str(int(sum(dataForAverage.values()) / len(dataForAverage)))
    # load html
    htmlString = pq(open("./templates/baseCard.html").read())
    # set font color
    htmlString("#container").attr("class", fontColor)
    # Fill name
    htmlString(".cardContent")(".name")(".din-font").append(name)
    # Fill average
    htmlString(".cardContent")(".average")(".din-font").append(average)
    # Fill image path
    htmlString("#cardModel").attr("src", imagePath)
    # Fill flag path
    htmlString("#flag").attr("src", flagPath)
    data["auton"] = data["autonomo"]

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
    nameFile = createFileName(str(htmlString))
    # transform to jpg
    image = cv2.imread(nameFile)
    nameFileJPG = nameFile.replace(".png", ".jpg")
    cv2.imwrite(nameFileJPG, image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    return nameFileJPG