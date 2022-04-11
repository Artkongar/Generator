with open("../tex/packages.tex") as f:
    lines = f.readlines()
    r = '+'.join(["`"+ line+"`" for line in lines])[1:-1]
    print(r.replace("\\", "\\\\"))