import unittest
from _8a_scraper.utils import login
from _8a_scraper.aggregated_ascents import get_route_ascents, get_crag_ascents


class TestSectors(unittest.TestCase):
    def test_get_route_ascents(self):
        driver = login()
        route_ascents = get_route_ascents(driver, 'sportclimbing', 'Poland', 'Dolina Szklarki',
                                          'sloneczne-skaly-df811', 'panel-sloneczny')
        driver.close()
        self.assertGreater(route_ascents.shape[0], 200)

    def test_get_crag_ascents(self):
        driver = login()
        crag_ascents = get_crag_ascents(driver, 'sportclimbing', 'Poland', 'Dolina Szklarki', 400)
        driver.close()
        self.assertGreater(crag_ascents.shape[0], 2000)
        self.assertEqual(list(crag_ascents.columns), ['date', 'route_name', 'sector_name'])


if __name__ == '__main__':
    unittest.main()
