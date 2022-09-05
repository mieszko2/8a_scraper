import unittest
#import yaml
#import sys, os
#sys.path.append("..")
#fetch config
#with open('../config/CONFIG.yaml') as stream:
#    config = yaml.safe_load(stream)
#update environ
#for item in config:
#    os.environ[item]=config[item]
from _8a_scraper.utils import login
from _8a_scraper.aggregated_ascents import get_route_ascents, get_crag_ascents


class TestSectors(unittest.TestCase):
    def test_get_route_ascents(self):
        driver = login()
        route_ascents = get_route_ascents(driver, 'sportclimbing', 'Poland', 'Dolina Szklarki',
                                          'sloneczne-skaly-df811', 'panel-sloneczny')
        driver.close()
        self.assertGreater(route_ascents.shape[0], 200)

    def test_get_crag_ascents_number_of_ascents(self):
        driver = login()
        crag_ascents = get_crag_ascents(driver, 'sportclimbing', 'Poland', 'Dolina Szklarki',
                                        400, '2020-01-01T12:00:00+00:00')
        driver.close()
        self.assertGreater(crag_ascents.shape[0], 100)
        self.assertEqual(list(crag_ascents.columns), ['date', 'route_name', 'sector_name'])

    def test_get_crag_ascents_columns(self):
        driver = login()
        crag_ascents = get_crag_ascents(driver, 'sportclimbing', 'Poland', 'Dolina Szklarki',
                                        400, '2022-01-01T12:00:00+00:00')
        driver.close()
        self.assertEqual(list(crag_ascents.columns), ['date', 'route_name', 'sector_name'])

    def test_get_crag_ascents_no_ascents(self):
        driver = login()
        crag_ascents = get_crag_ascents(driver, 'sportclimbing', 'Poland', 'Dolina Szklarki',
                                        400, '2093-10-09T12:00:00+00:00')
        driver.close()
        self.assertEqual(crag_ascents.empty, True)


if __name__ == '__main__':
    unittest.main()
