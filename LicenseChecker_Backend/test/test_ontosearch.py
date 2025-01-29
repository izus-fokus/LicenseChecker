# to test the ontology, independently from the API

from owlready2 import onto_path, get_ontology
import unittest
slo = get_ontology("../softwareLicenseOntology/slo.owl").load()
class TestOwl(unittest.TestCase):


#    def setUp(self):
#        self.slo = get_ontology("../softwareLicenseOntology/slo.owl").load()

    
    def test_search_stronger_license_type(self):
        assert str(slo.search(isMoreRestrictiveTypeThan = slo.PublicDomain)) == "[slo.Permissive, slo.Copyleft]"
    
    def test_search_all_license_types(self):
        assert str(slo.search(type = slo.LicenseType)) == "[slo.Permissive, slo.PublicDomain, slo.Copyleft]"
    
    def test_search_all_conditions(self):
        assert str(slo.search(type = slo.Condition)) == ("[slo.CopyrightNoticeCondition, "
            "slo.LicenseNoticeCondition, slo.StateChangesCondition, slo.DiscloseSourceCondition, "
            "slo.NetworkUseIsDistributionCondition, slo.SameLicenseCondition, slo.SameLicenseLibraryCondition]")
    
    def test_search_all_licenses(self):
        assert str(slo.search(type = slo.SoftwareLicense)) == ("[slo.AFL-3.0, slo.AGPL-3.0, slo.GPL-3.0, slo.MPL-2.0, "
                                                                 "slo.APACHE-2.0, slo.ARTISTIC-2.0, slo.BSD-3-CLAUSE, "
                                                                 "slo.BSD-3-CLAUSE-CLEAR, slo.BSL-1.0, slo.CC-BY-4.0, "
                                                                 "slo.CC0-1.0, slo.CECILL-2.1, slo.ECL-2.0, slo.ISC, "
                                                                 "slo.NCSA, slo.UNLICENSE, slo.ZLIB, slo.GPL-2.0, "
                                                                 "slo.LGPL-3.0, slo.BSD-2-CLAUSE, slo.LGPL-2.1, "
                                                                 "slo.BSD-4-CLAUSE, slo.CC-BY-SA-4.0, slo.MIT, "
                                                                 "slo.EUPL-1.1, slo.EPL-1.0, slo.LPPL-1.3c, slo.MS-PL, "
                                                                 "slo.MS-RL, slo.OFL-1.1, slo.POSTGRESQL, slo.EPL-2.0, "
                                                                 "slo.EUPL-1.2, slo.ODBL-1.0, slo.OSL-3.0, slo.UPL-1.0, "
                                                                 "slo.VIM, slo.WTFPL, slo.0BSD]")
    
    def test_search_copyleft_licenses(self):
        assert str(slo.search(hasLicenseType = slo.Copyleft)) == ("[slo.AGPL-3.0, slo.GPL-3.0, slo.MPL-2.0, "
                "slo.CECILL-2.1, slo.GPL-2.0, slo.LGPL-3.0, slo.LGPL-2.1, slo.EUPL-1.1, slo.EPL-1.0, slo.MS-RL, "
                "slo.OFL-1.1, slo.EPL-2.0, slo.EUPL-1.2, slo.ODBL-1.0, slo.OSL-3.0]")
    
    def test_mit_conditon(self):
        assert str(slo.MIT.hasCondition) == "[slo.CopyrightNoticeCondition, slo.LicenseNoticeCondition]"
    

#if __name__ == '__main__':
#    unittest.main()