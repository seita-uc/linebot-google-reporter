import unittest
from googleAnalyticsReport import return_analytics_report
from googleAdSenseReport import return_adsense_report
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except ValueError as e:
    return False
  return True

class TestGettingReport(unittest.TestCase):

    def test_return_analytics_report(self):
        expected = True
        response = return_analytics_report()
        json_data = response.data
        pp.pprint(json_data)
        actual = is_json(json_data)
        self.assertEqual(expected, actual)

    def test_return_adsense_report(self):
        expected = True
        response = return_adsense_report()
        json_data = response.data
        pp.pprint(json_data)
        actual = is_json(json_data)
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()
