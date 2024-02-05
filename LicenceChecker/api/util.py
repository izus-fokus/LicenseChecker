from conf import *
import conf
import sqlite3

def create_connection():

    con = sqlite3.connect('owl-db.db',check_same_thread=False)
    return con

def create_table(client):
    cur = client.cursor()

    try:
        cur.execute('''CREATE TABLE comp
               (id INTEGER PRIMARY KEY, entityA text, entityB text, isCompatible text,reason text, caveat text DEFAULT "None")''')
    except Exception as exp:
        print(exp)

def add_data(client, entityA, entityB,isCompatible,reason, caveat=None):
# Create table
        cur = client.cursor()


        if caveat is None:
            params = ( entityA, entityB,isCompatible,reason)
            cur.execute("INSERT INTO comp(entityA, entityB,isCompatible, reason) VALUES (?,?,?,?)",params)
        else:
            params = ( entityA, entityB,isCompatible,reason,caveat)
            cur.execute("INSERT INTO comp(entityA, entityB,isCompatible, reason,caveat) VALUES (?,?,?,?,?)",params)

        client.commit()

def get_output_all(client):
    cur = client.cursor()

    cur.execute('SELECT * FROM comp')
    rows = cur.fetchall()
    return rows


def query(client, licenA, licenB):
    cur = client.cursor()
    cur.execute("select reason, caveat from comp where (entityA=? and  entityB=?) and isCompatible='Yes'",(licenA,licenB))
    rows = cur.fetchall()
    return rows

def intersection(list1, list2):
    '''
    creates an intersection of two lists of licence objects
    '''
    result = []
    for elem in list1:
        for elem2 in list2:
            if elem == elem2:
                result.append(elem)
    return result


def remove_prefix(id: str):
    '''
    removes the prefix "slo." from ids
    '''
    if id[0:4] == "slo.":
        return id[4:]
    return id


def lic_list():
    license_object_list = list(conf.slo.search(hasPermission="*"))
    license_name_list = []
    for x in license_object_list:
        license_name_list.append(x.name)
    return license_name_list


def return_correct_case(input):
    correct_case = input.upper()
    return correct_case

def list_all_licenses_as_objects():
    all_licenses_object_list = slo.search(type=slo.SoftwareLicense)
    return all_licenses_object_list


def list_all_licenses_as_strings():
    all_licenses_string_list = []
    for x in list_all_licenses_as_objects():
        all_licenses_string_list.append(x.name)
    return all_licenses_string_list


def list_all_licenses_spdx_ids():
    """this function is not necessary if we decide to use the License name as identifier which is the identifier in
     our ontology as well
    """
    all_licenses_spdx_id_list = []
    for x in list_all_licenses_as_objects():
        all_licenses_spdx_id_list.append(x.spdxID[0])
    return all_licenses_spdx_id_list


def create_license_dictionary():
    """not sure, if we should use the name or the spdx-ID as an identifier.
    spdx ID could have the advantage of being more prevalent. (advantage if being accessed from the outside)
    Question might be, if we want to access our ontology via name or spdx ID.
    There might be licenses without spdx id in the future (although it seems unlikely for our purposes)
    Difference might not be grave though as it is a simple matter of uppercase / lowercase.
    Could also consider changing the name to be identical to the spdx ID.
    """
    keys = list_all_licenses_as_objects()
    values = list_all_licenses_as_strings()
    license_dictionary = dict(zip(keys, values))
    return license_dictionary

# print(create_license_dictionary())
# print(list_all_licenses_as_strings())

def create_property_dict():
    keys = list(slo.properties())
    values = []
    for x in keys:
        values.append(x.name)
    return dict(zip(keys, values))


def find_weakest_compatible_license_type(usedLicenses):
    '''
    Currently not in use, might be useful later. If not, can be deleted.
    '''
    license_type_list = [slo.Copyleft, slo.Permissive, slo.PublicDomain]
    typenamelist = []
    for x in usedLicenses:
        license = slo.search(_case_sensitive=False, iri="*{}".format(x))
        type = license[0].hasLicenseType
        typenamelist.append(type[0])

    for x in license_type_list:
        if x in typenamelist:
            return x

def find_incompatible_licenses_cond(license: str):
    '''
    Returns a set of incompatible licenses according to license conditions.
    Can be enhanced for more conditions.
    Work in progress.
    '''
    incomp_licenses = set()
    if slo.CopyrightNoticeCondition in slo["{}".format(license)].hasCondition:
        for x in list_all_licenses_as_objects():
            if slo.CopyrightNoticeCondition not in x.hasCondition:
                incomp_licenses.add(x)
    if slo.DiscloseSourceCondition in slo["{}".format(license)].hasCondition:
        for x in list_all_licenses_as_objects():
            if slo.DiscloseSourceCondition not in x.hasCondition:
                incomp_licenses.add(x)
    return incomp_licenses



def find_incompatible_licenses_type(license: str):
    '''
    Returns a set of incompatible licenses according to license type.
    '''
    incomp_licenses = set()
    type = slo["{}".format(license)].hasLicenseType
    incompatible_types = slo.search(_case_sensitive=False, isLessRestrictiveThan=type)
    incompatible_types = list(incompatible_types)
    for x in list_all_licenses_as_objects():
        # print(x.hasLicenseType)
        if x.hasLicenseType[0] in incompatible_types:
            incomp_licenses.add(x)
    return incomp_licenses


def find_incompatible_licenses_all(licenses):
    '''
    Combines all functions that collect incompatible licenses.
    Work in progress.
    '''
    incomp_licenses_all = set()
    for license in licenses:
        '''
        More functions can be added here.
        '''
        find_incompatible_licenses_cond(license)
        find_incompatible_licenses_type(license)
        incomp_licenses_all = set.union(incomp_licenses_all, find_incompatible_licenses_cond(license))
    return incomp_licenses_all



def clean_iri(iris):
    """
    return after # part of iri
    """
    
    data = []
    for cond in iris:
        iri = cond.iri
        iri = iri.split("#")[-1]
        data.append(iri)
    return data
    

def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]
    
