# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 10:39:55 2021

@author: midni
"""

from fastapi.testclient import TestClient

from main import app

import requests
import os



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
            "name": "Permissive",
            "description": "A permissive software license carries only minimal restrictions on how the software can be used, modified, and redistributed, usually including a warranty disclaimer.",
        },
        "description": "A short permissive license, compatible with GPL. Requires altered source versions to be documented as such.",
        "conditions": [
            {
                "id": "CopyrightNoticeCondition",
                "name": "Copyright Notice ",
                "description": "A copy of the license and copyright notice must be included with the licensed material.",
            },
            {
                "id": "LicenseNoticeCondition",
                "name": "License Notice ",
                "description": "A copy of the license and copyright notice must be included with the licensed material in source form, but is not required for binaries.",
            },
            {
                "id": "StateChangesCondition",
                "name": "State Changes ",
                "description": "Changes made to the licensed material must be documented.",
            },
        ],
        "permissions": [
            {
                "id": "CommercialUsePermission",
                "name": "Commercial Use ",
                "description": "  The licensed material and derivatives may be used for commercial purposes.",
            },
            {
                "id": "DistributionPermission",
                "name": "Distribution ",
                "description": "The licensed material may be distributed",
            },
            {
                "id": "ModificationPermission",
                "name": "Modification ",
                "description": "   The licensed material may be modified.",
            },
            {
                "id": "PrivateUsePermission",
                "name": "Private Use ",
                "description": "   The licensed material may be used and modified in private.",
            },
        ],
        "limitations": [
            {
                "id": "LiabilityLimitation",
                "name": "Liability ",
                "description": "This license includes a limitation of liability.",
            },
            {
                "id": "WarrantyLimitation",
                "name": "Warranty ",
                "description": "This license explicitly states that it does NOT provide any warranty.",
            },
        ],
        "compatibility": [],
    }


def test_invalid_input_get_license():
    response = client.get("/licences/0b")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


usedLicenses = ["VIM"]


def test_basic_functionality_check_license():
    response = client.post("/licenses/check/", json=usedLicenses)
    assert response.status_code == 200
    assert response.json() == [
        "AGPL-3.0",
        "GPL-2.0",
        "GPL-3.0",
        "LGPL-2.1",
        "LGPL-3.0",
        "VIM",
    ]
    # licenses = ["lgpl-3.0", "vim"]


licenses = ["MIT", "VIM"]


def test_basic_functionality_twolicenses_check_license():
    response = client.post("/licenses/check/", json=licenses)
    assert response.status_code == 200
    assert response.json() == [
        "AGPL-3.0",
        "GPL-2.0",
        "GPL-3.0",
        "LGPL-2.1",
        "LGPL-3.0",
        "VIM",
    ]


lics = ["AFL-3.0", "VIM", "MIT"]


def test_basic_functionality_morelicenses_check_license():
    response = client.post("/licenses/check/", json=lics)
    assert response.status_code == 200
    assert response.json() == ["VIM"]


unen = [
    {
        "id": "string",
    }
]


def test_validation_error_input_check_license():
    response = client.post("/licenses/check/", json=unen)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {"loc": ["body", 0], "msg": "str type expected", "type": "type_error.str"}
        ]
    }


licen = ["lg"]


def test_validation_error_input_check_license_one_unknown_license():
    response = client.post("/licenses/check/", json=licen)
    assert response.status_code == 422
    assert response.json() == "['lg'] is/are not a part of the Software License API"


lic = ["MIT", "VIM", "0bs", "zli"]


def test_validation_error_input_check_license_more_unknown_licenses():
    response = client.post("/licenses/check/", json=lic)
    assert response.status_code == 422
    assert (
        response.json()
        == "['0bs', 'zli'] is/are not a part of the Software License API"
    )


newlic = {
    "id": "HBD0",
    "name": "HBD-0",
    "url": "https://choosealicense.com/licenses/0hbd/",
    "type": {"id": "Permissive", "name": "Permissive"},
    "conditions": [{"id": "LicenseNoticeCondition", "name": "LicenseNoticeCondition"}],
    "permissions": [
        {"id": "CommercialUsePermission", "name": "CommercialUsePermission"}
    ],
    "limitations": [{"id": "LiabilityLimitation", "name": "LiabilityLimitation"}],
    "compatibility": ["HBD0"],
}


def test_basic_functionality_add_license():
    response = client.post("/licenses/add/", json=newlic)
    assert response.status_code == 200
    assert response.json() == {
        "id": "HBD0",
        "name": "HBD-0",
        "url": "https://choosealicense.com/licenses/0hbd/",
        "type": {"id": "Permissive", "name": "Permissive"},
        "conditions": [
            {"id": "LicenseNoticeCondition", "name": "LicenseNoticeCondition"}
        ],
        "permissions": [
            {"id": "CommercialUsePermission", "name": "CommercialUsePermission"}
        ],
        "limitations": [{"id": "LiabilityLimitation", "name": "LiabilityLimitation"}],
        "compatibility": ["HBD0", "ZLIB"],
    }


newlicens = {
    "id": "HBD0",
    "name": "HBD-0",
    "url": "https://choosealicense.com/licenses/0hbd/",
    "type": {"id": "Permissive", "name": "Permissive"},
    "conditions": ["LicenseNoticeCondition"],
    "permissions": [
        {"id": "CommercialUsePermission", "name": "CommercialUsePermission"}
    ],
    "limitations": [{"id": "LiabilityLimitation", "name": "LiabilityLimitation"}],
    "compatibility": ["HBD0"],
}


def test_validation_error_input_add_license():
    response = client.post("/licenses/add/", json=newlicens)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "conditions", 0],
                "msg": "value is not a valid dict",
                "type": "type_error.dict",
            }
        ]
    }


newlicense = {
    "id": "HBD0",
    "name": "HBD-0",
    "url": "https://choosealicense.com/licenses/0hbd/",
    "type": {"id": "Permissive", "name": "Permissive"},
    "conditions": [{"id": "LicenseNoticeCondition", "name": "LicenseNoticeCondition"}],
    "permissions": [
        {"id": "CommercialUsePermission", "name": "CommercialUsePermission"}
    ],
    "limitations": [{"id": "LiabilityLimitation", "name": "LiabilityLimitation"}],
    "compatibility": ["HBD0", "ZLIB"],
}


def test_basic_functionality_update_new_license():
    response = client.put("/licenses/HBD0", json=newlicense)
    assert response.status_code == 200
    assert response.json() == {
        "id": "HBD0",
        "name": "HBD-0",
        "url": "https://choosealicense.com/licenses/0hbd/",
        "type": {"id": "Permissive", "name": "Permissive"},
        "conditions": [
            {"id": "LicenseNoticeCondition", "name": "LicenseNoticeCondition"}
        ],
        "permissions": [
            {"id": "CommercialUsePermission", "name": "CommercialUsePermission"}
        ],
        "limitations": [{"id": "LiabilityLimitation", "name": "LiabilityLimitation"}],
        "compatibility": ["HBD0", "ZLIB"],
    }


nonvalid = {
    "id": "0hhh",
    "name": "HHH-0",
    "url": "https://choosealicense.com/licenses/0hhd/",
    "type": {"id": "Permissive", "name": "Permissive"},
    "conditions": [{"id": "LicenseNoticeCondition", "name": "LicenseNoticeCondition"}],
    "permissions": [],
    "limitations": [],
    "compatibility": ["HBD0", "ZLIB"],
}


def test_invalid_input_update_new_license():
    response = client.put("/licenses/0hhh", json=nonvalid)
    assert response.status_code == 404
    assert response.json() == "The license id 0hhh does not exist"


def test_403_update_new_license():
    response = client.put("/licenses/0BSD", json=newlicense)
    assert response.status_code == 403
    assert response.json() == "The license id 0BSD cannot be updated"


# def test_invalid_input_delete_new_license():
#    response = client.delete("/licenses/0BHHH")
#    assert response.status_code == 404
#    assert response.json() == 'The license id 0BHHH does not exist'


def test_403_delete_new_license():
    response = client.delete("/licenses/0bsd")
    assert response.status_code == 403
    assert response.json() == "The license id 0bsd cannot be deleted"


cond = [
  {
    "id": "CopyrightNoticeCondition",
    "name": "Copyright Notice ",
    "description": "A copy of the license and copyright notice must be included with the licensed material."
  },
  {
    "id": "LicenseNoticeCondition",
    "name": "License Notice ",
    "description": "A copy of the license and copyright notice must be included with the licensed material in source form, but is not required for binaries."
  },
  {
    "id": "StateChangesCondition",
    "name": "State Changes ",
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
    assert response.json() == "The license id zlb does not exist"


lim = [
  {
    "id": "LiabilityLimitation",
    "name": "Liability ",
    "description": "This license includes a limitation of liability."
  },
  {
    "id": "WarrantyLimitation",
    "name": "Warranty ",
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
    assert response.json() == "The license id zlb does not exist"


perm = [
  {
    "id": "CommercialUsePermission",
    "name": "Commercial Use ",
    "description": "  The licensed material and derivatives may be used for commercial purposes."
  },
  {
    "id": "DistributionPermission",
    "name": "Distribution ",
    "description": "The licensed material may be distributed"
  },
  {
    "id": "ModificationPermission",
    "name": "Modification ",
    "description": "   The licensed material may be modified."
  },
  {
    "id": "PrivateUsePermission",
    "name": "Private Use ",
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
    assert response.json() == "The license id zlb does not exist"


def test_basic_functionality_get_license_type():
    response = client.get("/licenses/VIM/license_type")
    assert response.status_code == 200
    assert response.json() == "Copyleft"


def test_invalid_input_get_license_type():
    response = client.get("/licenses/vm/license_type")
    assert response.status_code == 404
    assert response.json() == "The license id vm does not exist"


def test_basic_functionality_check_osi_popularity():
    response = client.get("/licenses/0bsd/osi_popular")
    assert response.status_code == 200
    assert response.json() == []


def test_invalid_input_check_osi_popularity():
    response = client.get("/licenses/0bs/osi_popular")
    assert response.status_code == 404
    assert response.json() == "The license id 0bs does not exist"


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
    "VIM",
]


def test_basic_functionality_return_licenses_for_type():
    response = client.get("/licenses/types/COPYLEFT")
    assert response.status_code == 200
    assert response.json() == typ


def test_upload_poetry_file():
    absolute_path = os.path.dirname(__file__)
    files = {
        "file": open(absolute_path+"/api_tests/pyproject_test1.toml", "rb")
    }
    response = client.post("/licenses/uploaddependencyfile/", files=files)
    assert response.status_code == 200
    assert response.json()=={
  "filename": "pyproject_test1.toml",
  "Content": {
    "toml": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "Tool Poetry Dependency"
    },
    "poetry-semver": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "Tool Poetry Dependency"
    }
  }
}
    
def test_upload_build_system_file():
    absolute_path = os.path.dirname(__file__)
    files = {
        "file": open(absolute_path+"/api_tests/pyproject_test2.toml", "rb")
    }
    response = client.post("/licenses/uploaddependencyfile/", files=files)
    assert response.status_code == 200
    assert response.json()=={
  "filename": "pyproject_test2.toml",
  "Content": {
    "hatchling": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "build-system requires"
    },
    "hatch-vcs": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "build-system requires"
    },
    "hatch-fancy-pypi-readme": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "build-system requires"
    }
  }
}
def test_upload_project_dependencies_file():
    absolute_path = os.path.dirname(__file__)
    files = {
        "file": open(absolute_path+"/api_tests/pyproject_test3.toml", "rb")
    }
    response = client.post("/licenses/uploaddependencyfile/", files=files)
    assert response.status_code == 200
    assert response.json()=={
  "filename": "pyproject_test3.toml",
  "Content": {
    "SQLAlchemy": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "Project Dependencies"
    },
    "lxml": {
      "license_name": "BSD",
      "license_id": [
        "0BSD"
      ],
      "source": "Project Dependencies"
    },
    "python-dateutil": {
      "license_name": "Apache",
      "license_id": [
        "APACHE-2.0"
      ],
      "source": "Project Dependencies"
    },
    "requests": {
      "license_name": "Apache",
      "license_id": [
        "APACHE-2.0"
      ],
      "source": "Project Dependencies"
    },
    "sqlalchemy-utils": {
      "license_name": "BSD",
      "license_id": [
        "0BSD"
      ],
      "source": "Project Dependencies"
    }
  }
}
def test_upload_poetry_second_file():
    absolute_path = os.path.dirname(__file__)
    files = {
        "file": open(absolute_path+"/api_tests/pyproject_test4.toml", "rb")
    }
    response = client.post("/licenses/uploaddependencyfile/", files=files)
    assert response.status_code == 200
    assert response.json()=={
  "filename": "pyproject_test4.toml",
  "Content": {
    "imageio": {
      "license_name": "BSD",
      "license_id": [
        "0BSD"
      ],
      "source": "Tool Poetry Dependency"
    },
    "numpy": {
      "license_name": "BSD",
      "license_id": [
        "0BSD"
      ],
      "source": "Tool Poetry Dependency"
    },
    "scipy": {
      "license_name": "BSD",
      "license_id": [
        "0BSD"
      ],
      "source": "Tool Poetry Dependency"
    },
    "typing-extensions": {
      "license_name": "Python",
      "license_id": [
        "CC-BY-4.0"
      ],
      "source": "Tool Poetry Dependency"
    }
  }
}
def test_upload_requirements_file():
    absolute_path = os.path.dirname(__file__)
    files = {
        "file": open(absolute_path+"/api_tests/requirements_test1.txt", "rb")
    }
    response = client.post("/licenses/uploaddependencyfile/", files=files)
    assert response.status_code == 200
    assert response.json()=={
  "filename": "requirements_test1.txt",
  "Content": {
    "calar": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "requirements"
    },
    "lix": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "requirements"
    },
    "flowa": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "requirements"
    },
    "maddy5": {
      "license_id": [
        "No License found"
      ],
      "source": "requirements"
    },
    "clygon": {
      "license_id": [
        "No License found"
      ],
      "source": "requirements"
    },
    "simple-interpolator": {
      "license_id": [
        "No License found"
      ],
      "source": "requirements"
    },
    "zenfilter": {
      "license_name": "3-clause",
      "license_id": [
        "BSD-3-CLAUSE-CLEAR"
      ],
      "source": "requirements"
    },
    "herbal": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "requirements"
    },
    "ER3": {
      "license_id": [
        "No License found"
      ],
      "source": "requirements"
    },
    "streamlit-otp-auth": {
      "license_id": [
        "No License found"
      ],
      "source": "requirements"
    },
    "ranni": {
      "license_name": "The",
      "license_id": [
        "UNLICENSE"
      ],
      "source": "requirements"
    },
    "scriptgen": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "requirements"
    },
    "anonknight": {
      "license_id": [
        "No License found"
      ],
      "source": "requirements"
    },
    "numpy": {
      "license_name": "BSD",
      "license_id": [
        "0BSD"
      ],
      "source": "requirements"
    }
  }
}
def test_upload_requirements_second_file():
    absolute_path = os.path.dirname(__file__)
    files = {
        "file": open(absolute_path+"/api_tests/requirements_test2.txt", "rb")
    }
    response = client.post("/licenses/uploaddependencyfile/", files=files)
    assert response.status_code == 200
    assert response.json()=={
  "filename": "requirements_test2.txt",
  "Content": {
    "owlready2": {
      "license_name": "GNU",
      "license_id": [
        "GPL-2.0"
      ],
      "source": "requirements"
    },
    "bcrypt": {
      "license_name": "Apache",
      "license_id": [
        "APACHE-2.0"
      ],
      "source": "requirements"
    },
    "passlib": {
      "license_name": "BSD",
      "license_id": [
        "0BSD"
      ],
      "source": "requirements"
    },
    "tortoise-orm": {
      "license_name": "Apache",
      "license_id": [
        "APACHE-2.0"
      ],
      "source": "requirements"
    },
    "python-multipart": {
      "license_name": "Apache",
      "license_id": [
        "APACHE-2.0"
      ],
      "source": "requirements"
    },
    "fastapi": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "requirements"
    },
    "uvicorn": {
      "license_name": "BSD",
      "license_id": [
        "0BSD"
      ],
      "source": "requirements"
    },
    "PyJWT": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "requirements"
    },
    "pydantic": {
      "license_name": "MIT",
      "license_id": [
        "MIT"
      ],
      "source": "requirements"
    }
  }
}
def test_upload_package_json_file():
    absolute_path = os.path.dirname(__file__)
    files = {
        "file": open(absolute_path+"/api_tests/package.json", "rb")
    }
    params={'choice':'JS'}
    response = client.post("/licenses/uploaddependencyfile/", files=files,params=params)
    assert response.status_code == 200
    assert response.json()=={
  "filename": "package.json",
  "Content": {
    "@fortawesome/fontawesome-free": {
      "license_name": "(CC-BY-4.0 AND OFL-1.1 AND MIT)",
      "license_id": "(CC-BY-4.0 AND OFL-1.1 AND MIT)",
      "source": "Package.Json"
    },
    "@quasar/extras": {
      "license_name": "MIT",
      "license_id": "MIT",
      "source": "Package.Json"
    },
    "@vue/cli-service": {
      "license_name": "MIT",
      "license_id": "MIT",
      "source": "Package.Json"
    },
    "axios": {
      "license_name": "MIT",
      "license_id": "MIT",
      "source": "Package.Json"
    },
    "core-js": {
      "license_name": "MIT",
      "license_id": "MIT",
      "source": "Package.Json"
    },
    "element-plus": {
      "license_name": "MIT",
      "license_id": "MIT",
      "source": "Package.Json"
    },
    "pinia": {
      "license_name": "MIT",
      "license_id": "MIT",
      "source": "Package.Json"
    },
    "quasar": {
      "license_name": "MIT",
      "license_id": "MIT",
      "source": "Package.Json"
    },
    "vue-router": {
      "license_name": "MIT",
      "license_id": "MIT",
      "source": "Package.Json"
    }
  }
}