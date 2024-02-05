# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 10:39:55 2021

@author: midni
"""

from fastapi.testclient import TestClient

from main import app

import requests


client = TestClient(app)


def test_basic_functionality_get_license():
    response = client.get("/licenses/zlib")
    assert response.status_code == 200
    assert response.json() == {
  "id": "ZLIB",
  "name": "zlib License",
  "url": "https://choosealicense.com/licenses/zlib/",
  "type": {
    "id": "Permissive",
    "name": "Permissive"
  },
  "description": "",
  "conditions": [
    {
      "id": "Copyright Notice",
      "name": "Copyright Notice",
      "description": "A copy of the license and copyright notice must be included with the licensed material."
    },
    {
      "id": "License Notice",
      "name": "License Notice",
      "description": "A copy of the license and copyright notice must be included with the licensed material in source form, but is not required for binaries."
    },
    {
      "id": "State Changes",
      "name": "State Changes",
      "description": "Changes made to the licensed material must be documented."
    }
  ],
  "permissions": [
    {
      "id": "Commercial Use",
      "name": "Commercial Use",
      "description": "  The licensed material and derivatives may be used for commercial purposes."
    },
    {
      "id": "Distribution",
      "name": "Distribution",
      "description": "The licensed material may be distributed"
    },
    {
      "id": "Modification",
      "name": "Modification",
      "description": "   The licensed material may be modified."
    },
    {
      "id": "Private Use",
      "name": "Private Use",
      "description": "   The licensed material may be used and modified in private."
    }
  ],
  "limitations": [
    {
      "id": "Liability",
      "name": "Liability",
      "description": "This license includes a limitation of liability."
    },
    {
      "id": "Warranty",
      "name": "Warranty",
      "description": "This license explicitly states that it does NOT provide any warranty."
    }
  ],
  "compatibility": []
}
def test_invalid_input_get_license():
    response = client.get("/licences/0b")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Not Found'}
    
usedLicenses = ["VIM"]

def test_basic_functionality_check_license(): 
    response = client.post("/licenses/check/", json = usedLicenses)
    assert response.status_code == 200
    assert response.json() ==[
  "AGPL-3.0",
  "GPL-2.0",
  "GPL-3.0",
  "LGPL-2.1",
  "LGPL-3.0",
  "VIM"
]
    #licenses = ["lgpl-3.0", "vim"]
licenses=["MIT","VIM"]
def test_basic_functionality_twolicenses_check_license(): 
    response = client.post("/licenses/check/", json = licenses)
    assert response.status_code == 200
    assert response.json() == [
  "AGPL-3.0",
  "GPL-2.0",
  "GPL-3.0",
  "LGPL-2.1",
  "LGPL-3.0",
  "VIM"
]
        
lics = ["AFL-3.0","VIM","MIT"]
def test_basic_functionality_morelicenses_check_license(): 
    response = client.post("/licenses/check/", json = lics)
    assert response.status_code == 200
    assert response.json() == [
  "VIM"
]
unen = [{"id": "string",}]
    
def test_validation_error_input_check_license():
    response = client.post("/licenses/check/", json = unen)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 0], 'msg': 'str type expected', 'type': 'type_error.str'}]}

licen = ["lg"]    
    
def test_validation_error_input_check_license_one_unknown_license():
    response = client.post("/licenses/check/", json = licen)
    assert response.status_code == 422
    assert response.json() ==  "['lg'] is/are not a part of the Software License API"
    
lic = ["MIT", "VIM", "0bs", "zli"]

def test_validation_error_input_check_license_more_unknown_licenses():
    response = client.post("/licenses/check/", json = lic)
    assert response.status_code == 422
    assert response.json() ==  "['0bs', 'zli'] is/are not a part of the Software License API"
    
newlic = {
    "id": "HBD0",
    "name": "HBD-0",
    "url": "https://choosealicense.com/licenses/0hbd/",
    "type": {
        "id": "Permissive",
        "name": "Permissive"
    },
    "conditions": [{"id": "LicenseNoticeCondition", "name": "LicenseNoticeCondition"}],
    "permissions": [{"id": "CommercialUsePermission", "name": "CommercialUsePermission"}],
    "limitations": [{"id": "LiabilityLimitation", "name": "LiabilityLimitation"}],
    "compatibility": ["HBD0"]
}
  
def test_basic_functionality_add_license():
    response = client.post("/licenses/add/", json = newlic)
    assert response.status_code == 200
    assert response.json() == {
      "id": "HBD0",
      "name": "HBD-0",
      "url": "https://choosealicense.com/licenses/0hbd/",
      "type": {
        "id": "Permissive",
        "name": "Permissive"
      },
      "conditions": [
        {
          "id": "LicenseNoticeCondition",
          "name": "LicenseNoticeCondition"
        }
      ],
      "permissions": [
        {
          "id": "CommercialUsePermission",
          "name": "CommercialUsePermission"
        }
      ],
      "limitations": [
        {
          "id": "LiabilityLimitation",
          "name": "LiabilityLimitation"
        }
      ],
      "compatibility": [
        "HBD0", "ZLIB"
      ]
    }
           
newlicens = {
    "id": "HBD0",
    "name": "HBD-0",
    "url": "https://choosealicense.com/licenses/0hbd/",
    "type": {
        "id": "Permissive",
        "name": "Permissive"
    },
    "conditions": ["LicenseNoticeCondition"],
    "permissions": [{"id": "CommercialUsePermission", "name": "CommercialUsePermission"}],
    "limitations": [{"id": "LiabilityLimitation", "name": "LiabilityLimitation"}],
    "compatibility": ["HBD0"]
}

def test_validation_error_input_add_license():
    response = client.post("/licenses/add/", json = newlicens)
    assert response.status_code == 422
    assert response.json() ==  {
      "detail": [
        {
          "loc": [
            "body",
            "conditions",
            0
          ],
          "msg": "value is not a valid dict",
          "type": "type_error.dict"
        }
      ]
    }
    
newlicense = {
    "id": "HBD0",
    "name": "HBD-0",
    "url": "https://choosealicense.com/licenses/0hbd/",
    "type": {
        "id": "Permissive",
        "name": "Permissive"
    },
    "conditions": [{"id": "LicenseNoticeCondition", "name": "LicenseNoticeCondition"}],
    "permissions": [{"id": "CommercialUsePermission", "name": "CommercialUsePermission"}],
    "limitations": [{"id": "LiabilityLimitation", "name": "LiabilityLimitation"}],
    "compatibility": ["HBD0", "ZLIB"]
}
    
def test_basic_functionality_update_new_license():
    response = client.put("/licenses/HBD0", json = newlicense)
    assert response.status_code == 200
    assert response.json() == {
      "id": "HBD0",
      "name": "HBD-0",
      "url": "https://choosealicense.com/licenses/0hbd/",
      "type": {
        "id": "Permissive",
        "name": "Permissive"
      },
      "conditions": [
        {
          "id": "LicenseNoticeCondition",
          "name": "LicenseNoticeCondition"
        }
      ],
      "permissions": [
        {
          "id": "CommercialUsePermission",
          "name": "CommercialUsePermission"
        }
      ],
      "limitations": [
        {
          "id": "LiabilityLimitation",
          "name": "LiabilityLimitation"
        }
      ],
      "compatibility": [
        "HBD0",
        "ZLIB"
      ]
    }
            
            
nonvalid = {
  "id": "0hhh",
  "name": "HHH-0",
  "url": "https://choosealicense.com/licenses/0hhd/",
  "type": {
    "id": "Permissive",
    "name": "Permissive"
  },
  "conditions": [{"id":"LicenseNoticeCondition", "name":"LicenseNoticeCondition"}],
  "permissions": [],
  "limitations": [],
  "compatibility": ["HBD0", "ZLIB"]
}    
    
def test_invalid_input_update_new_license():
    response = client.put("/licenses/0hhh", json = nonvalid)
    assert response.status_code == 404
    assert response.json() == 'The license id 0hhh does not exist'
      
def test_403_update_new_license():
    response = client.put("/licenses/0BSD", json = newlicense)
    assert response.status_code == 403
    assert response.json() == "The license id 0BSD cannot be updated"
    
#def test_invalid_input_delete_new_license():
#    response = client.delete("/licenses/0BHHH")
#    assert response.status_code == 404
#    assert response.json() == 'The license id 0BHHH does not exist'

def test_403_delete_new_license():
    response = client.delete("/licenses/0bsd")
    assert response.status_code == 403
    assert response.json() == "The license id 0bsd cannot be deleted"

cond = [
  {
    "id": "Copyright Notice",
    "name": "Copyright Notice",
    "description": "A copy of the license and copyright notice must be included with the licensed material."
  },
  {
    "id": "License Notice",
    "name": "License Notice",
    "description": "A copy of the license and copyright notice must be included with the licensed material in source form, but is not required for binaries."
  },
  {
    "id": "State Changes",
    "name": "State Changes",
    "description": "Changes made to the licensed material must be documented."
  }
]
def test_basic_functionality_get_license_conditions():
    response = client.get("/licenses/ZLIB/conditions")
    assert response.status_code == 200
    assert response.json() == cond
    
def test_invalid_input_get_license_conditions():
    response = client.get("/licenses/zlb/conditions")
    assert response.status_code == 404
    assert response.json() == 'The license id zlb does not exist'
    
lim = [
  {
    "id": "Liability",
    "name": "Liability",
    "description": "This license includes a limitation of liability."
  },
  {
    "id": "Warranty",
    "name": "Warranty",
    "description": "This license explicitly states that it does NOT provide any warranty."
  }
]
def test_basic_functionality_get_license_limitations():
    response = client.get("/licenses/ZLIB/limitations")
    assert response.status_code == 200
    assert response.json() == lim
    
def test_invalid_input_get_license_limitations():
    response = client.get("/licenses/zlb/limitations")
    assert response.status_code == 404
    assert response.json() == 'The license id zlb does not exist'
    
perm = [
  {
    "id": "Commercial Use",
    "name": "Commercial Use",
    "description": "  The licensed material and derivatives may be used for commercial purposes."
  },
  {
    "id": "Distribution",
    "name": "Distribution",
    "description": "The licensed material may be distributed"
  },
  {
    "id": "Modification",
    "name": "Modification",
    "description": "   The licensed material may be modified."
  },
  {
    "id": "Private Use",
    "name": "Private Use",
    "description": "   The licensed material may be used and modified in private."
  }
]
def test_basic_functionality_get_license_permissions():
    response = client.get("/licenses/ZLIB/permissions")
    assert response.status_code == 200
    assert response.json() == perm
    
def test_invalid_input_get_license_permissions():
    response = client.get("/licenses/zlb/permissions")
    assert response.status_code == 404
    assert response.json() == 'The license id zlb does not exist'

def test_basic_functionality_get_license_type():
    response = client.get("/licenses/VIM/license_type")
    assert response.status_code == 200
    assert response.json() == "Copyleft"
    
def test_invalid_input_get_license_type():
    response = client.get("/licenses/vm/license_type")
    assert response.status_code == 404
    assert response.json() == 'The license id vm does not exist'
    
def test_basic_functionality_check_osi_popularity():
    response = client.get("/licenses/0bsd/osi_popular")
    assert response.status_code == 200
    assert response.json() == []
    
def test_invalid_input_check_osi_popularity():
    response = client.get("/licenses/0bs/osi_popular")
    assert response.status_code == 404
    assert response.json() == 'The license id 0bs does not exist'

typ = [
  "AGPL-3.0",
  "GPL-2.0",
  "GPL-3.0",
  "LGPL-2.1",
  "LGPL-3.0",
  "CECILL-2.1",
  "EUPL-1.1",
  "EUPL-1.2",
  "EPL-1.0",
  "EPL-2.0",
  "MS-PL",
  "MS-RL",
  "OFL-1.1",
  "MPL-2.0",
  "OSL-3.0",
  "ODBL-1.0",
  "VIM"
]
def test_basic_functionality_return_licenses_for_type():
    response = client.get("/types/COPYLEFT")
    assert response.status_code == 200
    assert response.json() == typ
    



    



