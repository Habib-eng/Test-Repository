def adapt(modelId, data):
    if modelId == 1:
        return cin_adapter(data)
    elif modelId == 3:
        return driving_licence_adapter(data)
    elif modelId == 2:
        return passport_adapter(data)
    elif modelId == 4:
        return caret_grise_adapter(data)
    elif modelId == 5:
        return visite_technique_adapter(data)
    elif modelId == 6:
        return quittance_adapter(data)
    elif modelId == 7:
        return rne_adapter(data)
    elif modelId == 8:
        return bs_adapter(data)
    else:
        return None 

def cin_adapter(data):
    recto = [e for e in data["data"] if e["recto_verso"] == "face"][0]
    verso = [e for e in data["data"] if e["recto_verso"] == "back"][0]
    try:
        key_val = [
            {"key": "N° CIN", "value": recto["fr"]["id"]},
            {"key": "Nom (fr)", "value": recto["fr"]["last_name"]},
            {"key": "Prénom (fr)", "value": recto["fr"]["first_name"]},
            {
                "key": "Deuxième nom (fr)",
                "value": recto["fr"]["other_name"],
            },
            {
                "key": "Date de naissance",
                "value": recto["fr"]["birthdate"],
            },
            {
                "key": "Lieu de naissance (fr)",
                "value": recto["fr"]["birthplace"],
            },
            {"key": "Sexe", "value": recto["extrat_info"]["sexe"]},
            {"key": "Addresse", "value": verso["fr"]["address"]},
            {"key": "Date", "value": verso["fr"]["date"]},
            {"key": "Profession", "value": verso["fr"]["job"]},
            {"key": "Nom de la mère", "value": verso["fr"]["mother_name"]},
        ]
    except KeyError as e:
        key_val = []
    return key_val

def passport_adapter(raw_data):
    data = raw_data["results"][0]
    try:
        key_val = [
            {"key": "Date de naissance", "value": data["birth_date"]},
            {"key": "N° CIN", "value": data["cin_id"]},
            {"key": "Pays", "value": data["country"]},
            {"key": "Prénom", "value": data["first_name"]},
            {"key": "Nom", "value": data["last_name"]},
            {"key": "Sexe", "value": data["gender"]},
            {"key": "Gouvernorat", "value": data["governorate"]},
            {"key": "Profession", "value": data["job"]},
        ]
    except KeyError as e:
        key_val = []
    return key_val
def driving_licence_adapter(raw_data):
    data = raw_data["results"][0]
    try:
        key_val = [
            {"key": "Addresse", "value": data["permis_recto"]["address"]},
            {"key": "Date de naissance", "value": data["permis_recto"]["birth_date"]},
            {
                "key": "Lieu de naissance (fr)",
                "value": data["permis_recto"]["birthplace_fr"],
            },
            {"key": "N° CIN", "value": data["permis_recto"]["cin_id"]},
            {"key": "Date de délivrance", "value": data["permis_recto"]["date"]},
            {"key": "Prénom (fr)", "value": data["permis_recto"]["first_name_fr"]},
            {"key": "Nom (fr)", "value": data["permis_recto"]["last_name_fr"]},
            {"key": "ID", "value": data["permis_recto"]["id"]},
        ]
    except KeyError as e:
        print(e)
        key_val = []
    return key_val
def caret_grise_adapter(raw_data):
    data = raw_data["results"][0]
    result = []
    try:
        recto = data["carte_grise_recto"]
    except KeyError:
        recto = None
    try:
        verso = data["carte_grise_verso"]
    except KeyError:
        verso = None
    if (recto):
        for k,v in recto.items():
            result.append({"key": k, "value": v})
    if (verso):
        for k,v in verso.items():
            result.append({"key": k, "value": v})
    print(result)
    return result
def visite_technique_adapter(raw_data):
    try:
        result = []
        data = raw_data["results"][0]["visit_recto"]
        for k,v in data.items():
            result.append({'key': k, 'value': v})
    except Exception as e:
        result = [] 
    return result
def rne_adapter(raw_data):
    try:
        result = []
        data = raw_data["results"][0]["rne"]
        for k,v in data.items():
            result.append({'key': k, 'value': v})
    except Exception as e:
        result = []
    return result
def quittance_adapter(raw_data):
    try:
        result = []
        data = raw_data["results"][0]["quittance"]
        for k,v in data.items():
            if (k == "image"):
                continue
            result.append({'key': k, 'value': v})
    except Exception as e:
        result = []
    return result
def bs_adapter(raw_data):
    try:
        data = [{"key": " ", "value": line } for line in raw_data["processed_text"] ]
        return data
    except Exception as e :
        data = []
    return data
