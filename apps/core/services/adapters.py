def adapt(modelId, data):
    if modelId == 1:
        return cin_adapter(data)
    elif modelId == 2:
        return driving_licence_adapter(data)
    elif modelId == 3:
        return passport_adapter(data)
    else:
        return None

def cin_adapter(data):
    try:
        is_recto = data["data"][0]["recto_verso"] == "face"
        if is_recto:
            key_val = [
                {"key": "N° CIN", "value" : data["data"][0]["ar"]["id"]},
                {"key": "Nom (ar)", "value": data["data"][0]["ar"]["last_name"]},
                {"key": "Prénom (ar)", "value": data["data"][0]["ar"]["first_name"]},
                {"key": "Deuxième nom (ar)", "value": data["data"][0]["ar"]["other_name"]},
                {"key": "Date de naissance", "value": data["data"][0]["ar"]["birthdate"]},
                {"key": "Lieu de naissance (ar)", "value": data["data"][0]["ar"]["birthplace"]},
                {"key": "Sexe", "value": data["data"][0]["extrat_info"]["sexe"]}
            ]
        else:
            key_val = [
                {"key": "Addresse", "value": data["data"][0]["ar"]["address"]},
                {"key": "Date", "value": data["data"][0]["ar"]["date"]},
                {"key": "Profession", "value": data["data"][0]["ar"]["job"]},
                {"key": "Nom de la mère", "value": data["data"][0]["ar"]["mother_name"]},
            ]
    except KeyError as e:
        key_val = {}
    return key_val

def passport_adapter(data):
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

def driving_licence_adapter(data):
    try:
        key_val = [
            {"key": "Addresse", "value": data["permis_recto"]["address"]},
            {"key": "Date de naissance", "value": data["permis_recto"]["birth_date"]},
            {"key": "Lieu de naissance (fr)", "value": data["permis_recto"]["birthplace_fr"]},
            {"key": "N° CIN", "value": data["permis_recto"]["cin_id"]},
            {"key": "Date de délivrance", "value": data["permis_recto"]["date"]},
            {"key": "Prénom (fr)", "value": data["permis_recto"]["first_name_fr"]},
            {"key": "Nom (fr)", "value": data["permis_recto"]["last_name_fr"]},
            {"key": "ID", "value": data["permis_recto"]["id"]}
        ]
    except KeyError as e:
        key_val = []
    return key_val
