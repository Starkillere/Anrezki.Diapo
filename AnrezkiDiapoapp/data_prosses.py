import os

def acceuil_data_print():
    templates = os.listdir("./AnrezkiDiapoapp/templates/")
    data_templates = [''.join(data_template[5:].split(".")[:len(data_template[5:].split("."))-1]) for data_template in templates if os.path.isfile(os.path.join("./AnrezkiDiapoapp/templates/", data_template)) and data_template[:len("data-")] == "data-"]
    diapos = [diapo for diapo in templates if not os.path.isfile(os.path.join("./AnrezkiDiapoapp/templates/", diapo)) and diapo[:len("Diaporama-")] == "Diaporama-"]
    return (len(diapos), data_templates)

def presentation_reterner():
    templates = os.listdir("./AnrezkiDiapoapp/templates/")
    diapos = [diapo[len("Diaporama-"):].split("-")[0] for diapo in templates if not os.path.isfile(os.path.join("./AnrezkiDiapoapp/templates/", diapo)) and diapo[:len("Diaporama-")] == "Diaporama-"]
    return diapos
