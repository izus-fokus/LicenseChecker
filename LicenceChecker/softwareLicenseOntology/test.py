from owlready2 import *
onto = get_ontology("slo.owl").load()



def get_licenese_constraint(req = "condition"):
    if req == "condition":
        lst = st = list(onto.search(type=onto.Condition))
        conditon = []
        for cond in lst:
            iri = cond.iri
            iri = iri.split("#")[-1]
            conditon.append(iri)
    
        return conditon

def remove_prefix(id: str):
    '''
    removes the prefix "slo." from ids
    '''
    if id[0:4] == "slo.":
        return id[4:]
    return id

def return_correct_case(input):
    correct_case = input.upper()
    return correct_case

def list_all_licenses_as_objects():
    all_licenses_object_list = onto.search(type=onto.SoftwareLicense)
    return all_licenses_object_list
    
def check_compatiblity(license_id):
   
    correct_case_license_id = return_correct_case(license_id)
    lic = onto[correct_case_license_id]
    type_ = remove_prefix(str(lic.hasLicenseType[0]))
    type_compatible_forw = onto[type_].isForwardCompatibleWith
    type_compatible_back = onto[type_].isBackwardCompatibleWith
    all_lice = list_all_licenses_as_objects()
    
    if onto.Permissive in type_compatible_back:
        print("Yes")
    print(type_compatible_forw,type_compatible_back)
    license_ = []
    for lic in all_lice:
        if lic.hasLicenseType[0] in type_compatible_forw or lic.hasLicenseType[0] in  type_compatible_back:
            license_.append(lic.licenseName[0])
    print(license_)

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
    
def remove_prefix(id: str):
    '''
    removes the prefix "slo." from ids
    '''
    if id[0:4] == "slo.":
        return id[4:]
    return id


#print(get_licenese_constraint())

#print(onto.search(isExplicitlyCompatibleWith = "*"))
#print(onto.classes())

out = onto["AFL-3.0"]
#print(out.isExplicitlyCompatibleWith[2].isExplicitlyCompatibleWith)



all_licenses_object_list = onto.search(type=onto.SoftwareLicense)
ids = []
names = []
for ls in all_licenses_object_list:
    ids.append(remove_prefix(str(ls)))
    names.append(ls.licenseName)

lic_2_vec = {}
for id in ids:
    lic_2_vec[id] = word2vec(id)
scores = []
print(lic_2_vec)

inp = input("Enter license to check:")
ipn_word2vec = word2vec(inp)
for key, val in lic_2_vec.items():
    scores.append((key, cosdis(ipn_word2vec,val)))

scores.sort(key=lambda tup: tup[1],reverse=True)
print(scores)
    #print(ls.licenseName)
#print(all_licenses_object_list)
""""
check_compatiblity("GPL-2.0")
print(list(onto.classes()))
print("......")
print(list(onto.object_properties()))
print(onto.search(_case_sensitive=False, iri = "*#GPL*"))
step1 = onto["GPL-2.0"].hasLicenseType


print("step1:",step1[0])
type_ = remove_prefix(str(step1[0]))
print("out:",onto[type_].isBackwardCompatibleWith)
print(onto["Permissive"])
print(list(onto.search(type=onto.Permissive)))
#print(onto[step1])
#step2 = onto[step1].isForwardCompatibleWith
#print(step2)

print(onto["GPL-2.0"].hasPermission)
#print(onto.search(type=onto.Condition))
'''
print((onto.Condition.iri))
#for i in onto.Condition.instances(): print(i)
print("----")
print(onto.SoftwareLicense.is_a)
print(onto.search(type=onto.SoftwareLicense))
print(onto.search(_case_sensitive=False, iri = "*#GPL*"))
'''

"""