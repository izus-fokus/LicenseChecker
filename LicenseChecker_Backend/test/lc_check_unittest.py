import unittest
import requests
import pytest 
class TestLicenseComp(unittest.TestCase):


	def depracated_test_check_brief(self):
		result = {
  "compatible": [
    "AGPL-3.0",
    "APACHE-2.0",
    "BSD-3-CLAUSE",
    "GPL-2.0",
    "GPL-3.0",
    "LGPL-2.1",
    "LGPL-3.0",
    "MIT"
  ],
  "reasons": [],
  "possible compatible": [
    "AFL-3.0",
    "AGPL-3.0",
    "GPL-3.0",
    "MPL-2.0",
    "APACHE-2.0",
    "ARTISTIC-2.0",
    "BSD-3-CLAUSE",
    "BSD-3-CLAUSE-CLEAR",
    "BSL-1.0",
    "CC-BY-4.0",
    "CECILL-2.1",
    "ECL-2.0",
    "ISC",
    "NCSA",
    "ZLIB",
    "GPL-2.0",
    "LGPL-3.0",
    "BSD-2-CLAUSE",
    "LGPL-2.1",
    "BSD-4-CLAUSE",
    "CC-BY-SA-4.0",
    "MIT",
    "EUPL-1.1",
    "EPL-1.0",
    "LPPL-1.3c",
    "MS-PL",
    "MS-RL",
    "OFL-1.1",
    "POSTGRESQL",
    "EPL-2.0",
    "EUPL-1.2",
    "ODBL-1.0",
    "OSL-3.0",
    "UPL-1.0",
    "VIM"
  ]
}

		headers = {
         'accept': 'application/json',
    # Already added when you pass json= but not when you pass data=
    # 'Content-Type': 'application/json',
             }
		json_data = [
                'MIT']
		response = requests.post('http://127.0.0.1:8000/licenses/check/detail', headers=headers, json=json_data)
		output = response.json()
        
        #self.assertEqual(result, output)
		assert result == output
	def test_check2(self):
		result = [
	          "BSD-3-CLAUSE-CLEAR",
	          "APACHE-2.0",
	          "LGPL-2.1",
	          "EPL-2.0",
	          "LGPL-3.0",
	          "UPL-1.0",
	          "CC-BY-4.0",
	          "ZLIB",
	          "BSD-2-CLAUSE",
	          "EPL-1.0",
	          "GPL-3.0",
	          "AFL-3.0",
	          "MS-RL",
	          "AGPL-3.0",
	          "EUPL-1.1",
	          "LPPL-1.3c",
	          "OFL-1.1",
	          "MPL-2.0",
	          "ARTISTIC-2.0",
	          "POSTGRESQL",
	          "NCSA",
	          "VIM",
	          "BSD-3-CLAUSE",
	          "CECILL-2.1",
	          "ISC",
	          "BSD-4-CLAUSE",
	          "MIT",
	          "MS-PL",
	          "GPL-2.0",
	          "ODBL-1.0",
	          "BSL-1.0",
	          "EUPL-1.2",
	          "CC-BY-SA-4.0",
	          "ECL-2.0",
	          "OSL-3.0"
	        ]
		headers = {
	                 'accept': 'application/json',
	            # Already added when you pass json= but not when you pass data=
	            # 'Content-Type': 'application/json',
	                     }
		json_data = [
	                        'BSD-3-CLAUSE']
		response = requests.post('http://127.0.0.1:8000/licenses/check/', headers=headers, json=json_data)
		output = response.json()
		assert output == result
	        #if __name__ == '__main__':
	        #    unittest.main()`