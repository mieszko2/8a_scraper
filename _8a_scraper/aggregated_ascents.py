import json
import pandas as pd
from slugify import slugify
from _8a_scraper.utils import get_route_ascents_from_link, get_links_to_routes_from_a_crag,\
    get_sector_name_from_route_link, get_route_name_from_route_link


def get_route_ascents(driver, category, country, crag, sector, route):
    """
    Get ascents of a given route.
    :param driver: driver logged into 8a
    :type driver: selenium driver
    :param category: sport climbing or bouldering
    :type category: string
    :param country: Name of the country
    :type country: string
    :param crag: Name of the crag
    :type crag: string
    :param sector: Name of the sector
    :type sector: string
    :param route: Name of the route
    :type route: string
    :return: pandas dataframe with ascents and their details
    """
    country_slug = slugify(country)
    crag_slug = slugify(crag)
    sector_slug = slugify(sector)
    route_slug = slugify(route)

    ascents = []
    page_index = 0
    while True:
        driver.get(
            f'https://www.8a.nu/api/crags/{category}/{country_slug}/{crag_slug}/sectors/'
            f'{sector_slug}/routes/{route_slug}/ascents?pageIndex={page_index}')
        element = driver.find_element_by_tag_name('pre').text
        page_data = json.loads(element)
        ascents.extend(page_data['items'])
        page_index += 1
        if not page_data['pagination']['hasNext']:
            break
    return pd.DataFrame(ascents)


def get_crag_ascents(driver, category, country, crag, min_number_of_ascents,
                     min_date='1950-01-01T12:00:00+00:00'):
    """
    Get all ascents of routes in a crag.
    :param driver: selenium driver: driver logged into 8a.nu
    :param category: string: sportclimbing or bouldering
    :param country: string: name of the country
    :param crag: string: name of the crag
    :param min_number_of_ascents: int: minimal ascents the route should have to count it
    :param min_date: string: date since when ascents should be downloaded
    :return: pandas.DataFrame: list of crag ascents: route, sector, date
    """

    routes_links = get_links_to_routes_from_a_crag(driver, category, country, crag, min_number_of_ascents)
    crag_ascents = pd.DataFrame()
    for link in routes_links:
        route_ascents = get_route_ascents_from_link(driver, link, min_date)[['date']]
        route_ascents['route_name'] = get_route_name_from_route_link(driver, link)
        route_ascents['sector_name'] = get_sector_name_from_route_link(driver, link)
        crag_ascents = pd.concat([crag_ascents, route_ascents])
    crag_ascents.reset_index(drop=True, inplace=True)
    return crag_ascents
