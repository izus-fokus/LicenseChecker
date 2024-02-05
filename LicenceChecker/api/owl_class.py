import conf
from owlready2.namespace import Thing


with conf.slo:
    class SoftwareLicense(Thing):
        pass


    class LicenseType(Thing):
        pass


    class Condition(Thing):
        pass


    class Permission(Thing):
        pass


    class Limitation(Thing):
        pass