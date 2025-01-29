import json

import yaml, os
from conf import *

# Listed in this file are the functions which can change the ontology manually.
# They are not needed for the api to work.

def delete_second_part():
    """
    deletes from the Choosealicense yaml files the second part containing the license text as this is interpreted as a second yaml file
    """
    path = "../softwareLicenseOntology/ChoosealicenseLicenses_modif/"
    for file in os.listdir(path):
        with open(path + file, "r", encoding='utf-8') as f:
            filestr = str(f.read())
            data = "---".join(filestr.split("---")[:-1])
        with open(path + file, "w", encoding='utf-8') as f:
            f.write(data)
        print("successful!")


def add_description():
    """
    adds the short descriptions from choosealicence.org to the ontology
    """
    license_object_list = list(slo.search(hasPermission="*"))
    path = "../softwareLicenseOntology/ChoosealicenseLicenses_modif/"
    for x in license_object_list:
        license_name = x.name
        license_name_lowercase = license_name.lower()
        filename = license_name_lowercase + ".txt"
        with open(path + filename, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
            description = doc["description"]
            x.hasChoosealicenseDescription = [description]
    slo.save(file = "test_onto.owl", format = "rdfxml")
    return None


def add_ID():
    """
    adds the property "spdx-id" from choosealicense.com to the ontology
    """
    license_object_list = list(slo.search(hasPermission="*"))
    path = "../softwareLicenseOntology/ChoosealicenseLicenses_modif/"
    for x in license_object_list:
        license_name = x.name
        license_name_lowercase = license_name.lower()
        filename = license_name_lowercase + ".txt"
        with open(path + filename, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f)
            ID = doc["spdx-id"]
            x.spdxID = [ID]
    slo.save(file = "../softwareLicenseOntology/test_onto.owl", format = "rdfxml")
    return None


def add_fsf_osi():
    """
    adds the boolean values of isOsiApproved and isFsfLibre properties from the spdx rescources to the ontology
    """
    license_object_list = list(slo.search(hasPermission="*"))
    file = "../softwareLicenseOntology/spdx_json/licenses.json"
    with open(file, "r") as f:
        data = json.load(f)
    for x in license_object_list:
        licenseID = x.spdxID[0]
        for y in data["licenses"]:
            if y["licenseId"] == licenseID:
                if "isFsfLibre" in y:
                    libre = y["isFsfLibre"]
                    x.isFsfLibre = [libre]
                if "isOsiApproved" in y:
                    osi = y["isOsiApproved"]
                    x.isOsiApproved = [osi]
    slo.save(file = "../softwareLicenseOntology/test_onto.owl", format = "rdfxml")
    return None
