import re

def replacePicterFormatTexToHtml(fileName):
    f = open(fileName, "r", encoding="utf-8")
    data = f.read()
    f.close()

    texPictures = re.findall(r"\\includegraphics\[[\s\S]*?]\{\{[\s\S]*?}}", data)
    print(texPictures)

    for texPic in texPictures:
        print(texPic)
        params = re.findall(r"\[([\s\S]*?)]", texPic)[0].replace(" ", "").split(",")
        params = {param.split("=")[0]:param.split("=")[1] for param in params if param != ""}
        width = "auto"
        height = "auto"
        for param in params:
            if (param == "width"):
                width = params[param]
                break
            elif (param == "height"):
                height = params[param]
                break
        picName = re.findall(r"\{\{([\s\S]*?)}}", texPic)[0]
        htmlImage = f"<img src='../../signature/{picName}.png' width='{width}' height='{height}'>"

        data = data.replace(texPic, htmlImage)

    f = open(fileName, "w", encoding="utf-8")
    f.write(data)
    f.close()

replacePicterFormatTexToHtml("all.html")

