from owlready2 import onto_path, get_ontology, destroy_entity, DataProperty
import logging
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
log = logging.getLogger('ML-SERVICE-Inference-Training')
log.setLevel(logging.DEBUG)
JWT_SECRET = 'myjwtsecret'

onto_path.append("../softwareLicenseOntology/")
slo = get_ontology("../softwareLicenseOntology/slo.owl").load()
with open("license_list.txt", 'r', encoding='utf-8') as licenses:
    license_list = [line.rstrip() for line in licenses]
    first_license = license_list[0][-4:]
    license_list[0] = first_license
    license_list_upper = []
    for i in license_list:
        license_list_upper.append(i.upper())




