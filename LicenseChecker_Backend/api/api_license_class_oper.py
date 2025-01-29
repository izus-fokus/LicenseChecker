from ast import Mod
from pydantic import BaseModel, AnyUrl
from tortoise.models import Model
from tortoise import fields
from passlib.hash import bcrypt
import re
from typing import List, Optional
from owl_class import *
from util import *
from conf import *
import requests
import json
import tomllib

# from license_oper import *
"""
class CompLic(BaseModel):
    response: str
    license: List[str]
"""


class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    role = fields.CharField(30)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

    def verify_role(self, role_):
        if self.role == role:
            return True
        else:
            return False

    def get_role(self) -> str:
        return self.role


class Conditions(BaseModel):
    id: str
    name: str
    description: str


class Permissions(BaseModel):
    id: str
    name: str
    description: str


class Limitations(BaseModel):
    id: str
    name: str
    description: str


class LicenseTypes(BaseModel):
    id: str
    name: str
    description: str

    def get_compatible_types(self):
        # hier alle kompatiblen Typen abrufen
        types = [
            "Public Domain",
            "Permissive",
            "Copyleft",
            "Network Protective",
            "Weakly Protective",
            "Strongly Protective",
        ]
        if self.id == "Public Domain" or self.id == "Permissive":
            return types
        else:
            return types[2:6]


class License(BaseModel):
    id: str
    name: str
    url: Optional[AnyUrl]
    type: Optional[LicenseTypes]
    description: str

    conditions: List[Conditions] = []
    permissions: List[Permissions] = []
    limitations: List[Limitations] = []
    compatibility: List[str] = []

    def __hash__(self):
        return hash((self.id))

    def get_compatible_licenses(self):
        # hier alle explizit kompatiblen Lizenzen abrufen
        licen = slo[self.id]
        compatible_licenses = licen.isExplicitlyCompatibleWith
        info = []
        for lic in compatible_licenses:
            licens = remove_prefix(str(lic))
            info.append(licens)
        return info


def get_description(desc):
    description = "".join((desc.description.en))
    return description


def remove_suffix(input_string, suffix):
    if suffix and input_string.endswith(suffix):
        return input_string[: -len(suffix)]
    return input_string


def add_space(space):
    space = re.sub(r"(\w)([A-Z])", r"\1 \2", space)
    return space


def check_compatiblity(license_id):
    """
    1. first type (forward)
    2. Add explicit compatible
    3. remove not compatible
    """
    print(str(license_id))
    correct_case_license_id = return_correct_case(license_id)
    lic = slo[correct_case_license_id]
    print("lic", lic)
    type_ = remove_prefix(str(lic.hasLicenseType[0]))
    print("Type_", type_)
    type_compatible_forw = slo[
        type_
    ].isForwardCompatibleWith  # permissive is not compatible with any other license
    print("forward Compatible With", type_compatible_forw)
    log.debug(type_compatible_forw)
    # explicit compatible logic
    exp_comp = (
        slo[license_id].isExplicitlyCompatibleWith
    )  # only those license objects which have this property will return value
    print("Explicitly Compatible With", exp_comp)

    log.debug(exp_comp)
    # not compatible
    not_comp = slo[license_id].isNotCompatibleWith
    print("Not Compatible With", not_comp)

    log.debug(not_comp)
    # type_compatible_back = slo[type_].isBackwardCompatibleWith
    all_lice = list_all_licenses_as_objects()

    # print(type_compatible_forw,type_compatible_back)
    license_ = []
    license_.append(license_id)
    for lic in all_lice:
        if (
            lic.hasLicenseType[0] in type_compatible_forw
        ):  # or lic.hasLicenseType[0] in  explicit_comp:
            license_.append(remove_prefix(str(lic)))
            # print(lic.licenseName)

    # adding explicit license to the list
    for lic in exp_comp:
        license_.append(remove_prefix(str(lic)))

    # remove duplicates from the list because it might be that type compatible and explicit compatible will end up same license
    license_ = list(set(license_))

    for lic in not_comp:
        lc = remove_prefix(str(lic))
        if lc in license_:
            index_ = license_.index(lc)
            license_.pop(index_)
    license_.sort()
    print("Sorted Licenses", license_)

    return license_


def get_license_object(license_id: str):
    correct_case_license_id = return_correct_case(license_id)
    lic = slo[correct_case_license_id]

    # get_ids()

    # print(lic.LicenseName[0])
    if lic is None:
        return lic
    cond_list = []
    perm_list = []
    lim_list = []
    comp_list = []

    typ = add_space(remove_prefix(str(lic.hasLicenseType[0])))
    typ_description = "".join(remove_prefix(lic.hasLicenseType[0].description.en))
    # print(lic.licenseName[0].spdxID[0])

    for condition in lic.hasCondition:
        description = get_description(condition)
        condit = remove_prefix(str(condition))
        conditname = add_space(condit)
        conditname = remove_suffix(conditname, "Condition")
        cond_list.append(
            Conditions(id=condit, name=conditname, description=description)
        )
    for permission in lic.hasPermission:
        description = get_description(permission)
        permis = remove_prefix(str(permission))
        permisname = add_space(permis)
        permisname = remove_suffix(permisname, "Permission")
        perm_list.append(
            Permissions(id=permis, name=permisname, description=description)
        )
    for limitation in lic.hasLimitation:
        description = get_description(limitation)
        limit = remove_prefix(str(limitation))
        limitname = add_space(limit)
        limitname = remove_suffix(limitname, "Limitation")
        lim_list.append(Limitations(id=limit, name=limitname, description=description))
    for comp_license in lic.isExplicitlyCompatibleWith:
        comp_lic = remove_prefix(str(comp_license))
        comp_list.append(comp_lic)
    # print(type(lic.hasPermission))
    retrieved_license = License(
        id=correct_case_license_id,
        name=lic.licenseName[0],
        url=lic.url[0] if len(lic.url) >= 1 else None,
        description="".join(lic.hasChoosealicenseDescription),
        type=LicenseTypes(id=typ, name=typ, description=typ_description),
        permissions=perm_list,
        conditions=cond_list,
        limitations=lim_list,
        compatibility=comp_list,
    )

    return retrieved_license


def create_new_license_object(newlic: License):
    """
    In progress
    """
    newlics = SoftwareLicense(newlic.id)
    newlics.url.clear()
    url = str(newlic.url)
    newlics.url.append(url)
    newlics.licenseName.clear()
    name = str(newlic.name)
    newlics.licenseName.append(name)
    lictype = newlic.type
    lictypes = LicenseType(lictype.id)
    newlics.hasLicenseType.append(lictypes)
    for condition in newlic.conditions:
        cond = condition.id
        if Condition(cond) not in newlics.hasCondition:
            newlics.hasCondition.append(Condition(cond))
    for permission in newlic.permissions:
        perm = permission.id
        if Permission(perm) not in newlics.hasPermission:
            newlics.hasPermission.append(Permission(perm))
    for limitation in newlic.limitations:
        lim = limitation.id
        if Limitation(lim) not in newlics.hasLimitation:
            newlics.hasLimitation.append(Limitation(lim))
    for comp_license in newlic.compatibility:
        if SoftwareLicense(comp_license) not in newlics.isExplicitlyCompatibleWith:
            newlics.isExplicitlyCompatibleWith.append(SoftwareLicense(comp_license))
    idd = newlic.id
    print(slo.idd)
    slo.save()
    print(slo.idd)
    return None


def check_python_dependency(my_file):
    # t = prettytable.PrettyTable(['Package', 'License'])
    data = {}
    packages = my_file.decode("utf-8").splitlines()
    # print(packages)
    line = 0
    for package in packages:
        line += 1
        # print(line)
        #   print(package)
        check_lic_remove_char = re.match(
            "([\w-]*)(\[.*\])?[ ]*([=~<>]{0,2})[ ]*(.*)", package
        )
        lic = check_lic_remove_char.group(1)
        # print(lic)
        response = requests.get("https://pypi.org/pypi/{}/json".format(lic))
        json = response.json()
        if "info" in json:
            # if(len(json['info']['classifiers'])!=0  ):
            # if('classifiers' in json['info'] and len(json['info']['classifiers'])!=0 ):

            if (
                len(list(filter(lambda x: "License" in x, json["info"]["classifiers"])))
                != 0
            ):
                # print(len(list(filter(lambda x: 'License' in x, json['info']['classifiers']))))
                res = list(
                    filter(lambda x: "License" in x, json["info"]["classifiers"])
                )
                # print(res)
                lic_name = re.match("([\w\s]*)(::)([\w\s]*)(:: )([\w]*)", res[0])
                if lic_name is not None:
                    #  print(lic_name)
                    data[lic] = {
                        "license_name": lic_name.group(5),
                        "license_id": rank(str(lic_name.group(5)), 1),
                        "source": "requirements",
                    }
            elif (
                "license" in json["info"]
                and json["info"]["license"] is not None
                and len(json["info"]["license"]) != 0
            ):
                lic_name = json["info"]["license"].split()
                data[lic] = {
                    "license_name": lic_name[0],
                    "license_id": rank(lic_name[0], 1),
                    "source": "requirements",
                }
            else:
                lic_name = "No License found"
                data[lic] = {"license_id": [lic_name], "source": "requirements"}
                # t.add_row((lic, lic_name))

    return data


def check_python_toml_dependency(my_file):
    decode_contents = my_file.decode("utf-8")
    data_toml = tomllib.loads(decode_contents)
    print(data_toml["build-system"].get("requires"))
    data = {}

    if data_toml["tool"].get("poetry") is not None:
        for lic in data_toml["tool"]["poetry"]["dependencies"]:
            response = requests.get("https://pypi.org/pypi/{}/json".format(lic))
            json = response.json()

            if "info" in json:
                # if(len(json['info']['classifiers'])!=0  ):
                # if('classifiers' in json['info'] and len(json['info']['classifiers'])!=0 ):

                if (
                    len(
                        list(
                            filter(
                                lambda x: "License" in x, json["info"]["classifiers"]
                            )
                        )
                    )
                    != 0
                ):
                    # print(len(list(filter(lambda x: 'License' in x, json['info']['classifiers']))))
                    res = list(
                        filter(lambda x: "License" in x, json["info"]["classifiers"])
                    )
                    # print(res)
                    lic_name = re.match("([\w\s]*)(::)([\w\s]*)(:: )([\w]*)", res[0])
                    if lic_name is not None:
                        #  print(lic_name)
                        data[lic] = {
                            "license_name": lic_name.group(5),
                            "license_id": rank(str(lic_name.group(5)), 1),
                            "source": "Tool Poetry Dependency",
                        }
                elif (
                    "license" in json["info"]
                    and json["info"]["license"] is not None
                    and len(json["info"]["license"]) != 0
                ):
                    lic_name = json["info"]["license"].split()
                    data[lic] = {
                        "license_name": lic_name[0],
                        "license_id": rank(lic_name[0], 1),
                        "source": "Tool Poetry Dependency",
                    }
                else:
                    lic_name = "No License found"
                    data[lic] = {
                        "license_id": [lic_name],
                        "source": "Tool Poetry Dependency",
                    }
                # t.add_row((lic, lic_name))
    elif data_toml["project"].get("dependencies") is not None:
        for lic in data_toml["project"]["dependencies"]:
            response = requests.get("https://pypi.org/pypi/{}/json".format(lic))
            json = response.json()

            if "info" in json:
                # if(len(json['info']['classifiers'])!=0  ):
                # if('classifiers' in json['info'] and len(json['info']['classifiers'])!=0 ):

                if (
                    len(
                        list(
                            filter(
                                lambda x: "License" in x, json["info"]["classifiers"]
                            )
                        )
                    )
                    != 0
                ):
                    # print(len(list(filter(lambda x: 'License' in x, json['info']['classifiers']))))
                    res = list(
                        filter(lambda x: "License" in x, json["info"]["classifiers"])
                    )
                    print(res)
                    lic_name = re.match("([\w\s]*)(::)([\w\s]*)(:: )([\w]*)", res[0])
                    if lic_name is not None:
                        #  print(lic_name)
                        data[lic] = {
                            "license_name": lic_name.group(5),
                            "license_id": rank(str(lic_name.group(5)), 1),
                            "source": "Project Dependencies",
                        }
                elif (
                    "license" in json["info"]
                    and json["info"]["license"] is not None
                    and len(json["info"]["license"]) != 0
                ):
                    lic_name = json["info"]["license"].split()
                    data[lic] = {
                        "license_name": lic_name[0],
                        "license_id": rank(lic_name[0], 1),
                        "source": "Project Dependencies",
                    }
                else:
                    lic_name = "No License found"
                    data[lic] = {
                        "license_id": [lic_name],
                        "source": "Project Dependencies",
                    }
    elif data_toml["build-system"].get("requires") is not None:
        for package in data_toml["build-system"]["requires"]:
            check_lic_remove_char = re.match(
                "([\w-]*)(\[.*\])?[ ]*([=~<>]{0,2})[ ]*(.*)", package
            )
            lic = check_lic_remove_char.group(1)
            # print(lic)
            response = requests.get("https://pypi.org/pypi/{}/json".format(lic))
            json = response.json()

            if "info" in json:
                # if(len(json['info']['classifiers'])!=0  ):
                # if('classifiers' in json['info'] and len(json['info']['classifiers'])!=0 ):

                if (
                    len(
                        list(
                            filter(
                                lambda x: "License" in x, json["info"]["classifiers"]
                            )
                        )
                    )
                    != 0
                ):
                    # print(len(list(filter(lambda x: 'License' in x, json['info']['classifiers']))))
                    res = list(
                        filter(lambda x: "License" in x, json["info"]["classifiers"])
                    )
                    print(res)
                    lic_name = re.match("([\w\s]*)(::)([\w\s]*)(:: )([\w]*)", res[0])
                    if lic_name is not None:
                        #  print(lic_name)
                        data[lic] = {
                            "license_name": lic_name.group(5),
                            "license_id": rank(str(lic_name.group(5)), 1),
                            "source": "build-system requires",
                        }
                elif (
                    "license" in json["info"]
                    and json["info"]["license"] is not None
                    and len(json["info"]["license"]) != 0
                ):
                    lic_name = json["info"]["license"].split()
                    data[lic] = {
                        "license_name": lic_name[0],
                        "license_id": rank(lic_name[0], 1),
                        "source": "build-system requires",
                    }
                else:
                    lic_name = "No License found"
                    data[lic] = {
                        "license_id": [lic_name],
                        "source": "build-system requires",
                    }
    # else:
    #         return "No Dependency Available"
    return data


def check_js_dependency(my_file):
    # print(my_file)
    data = {}
    packages = my_file.decode("utf-8")
    print(type(packages))
    packages_json = json.loads(packages)
    print(packages_json["dependencies"])
    for k, v in packages_json["dependencies"].items():
        # print(k,v)
        version = v[1 : len(v)]
        # print(version)
        response = requests.get(" https://registry.npmjs.org/{}/{}".format(k, version))
        response_json = response.json()
        lic = response_json["name"]
        print(type(response_json["license"]))
        data[lic] = {
            "license_name": response_json["license"],
            "license_id": response_json["license"],
            "source": "Package.Json",
        }

    return data
