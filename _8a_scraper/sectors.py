import json
import time
import pandas as pd
from slugify import slugify


def get_crags(driver, category, country, min_ascents):
    """
    Get list of crags in a given country, with number of ascents at least min_ascents.
    :param driver: driver logged into 8a
    :type driver: selenium driver
    :param category: sport climbing or bouldering
    :type category: string
    :param country: Country
    :type country: string
    :param min_ascents: minimal number of ascents to pull from a sector
    :type min_ascents: int
    :return: list of crag names
    """


def get_crag_coordinates(driver, category, country, crag):
    """
    Get coordinates of a given crag in a given country.
    :param driver: driver logged into 8a
    :type driver: selenium driver
    :param category: sport climbing or bouldering
    :type category: string
    :param country: Name of the country
    :type country: string
    :param crag: Name of the crag
    :type crag: string
    :return: coordinates
    """
    driver.get(f'https://www.8a.nu/crags/{category}/{country}/{crag}/')
    coordinates = driver.find_elements_by_class_name('gps-search-text')[0].text
    return coordinates


def get_sectors(driver, category, country, crag, min_ascents):
    """
    Get sectors from a given crag, with number of ascents at least min_ascents.
    :param driver: driver logged into 8a
    :type driver: selenium driver
    :param category: sport climbing or bouldering
    :type category: string
    :param country: Name of the country
    :type country: string
    :param crag: Name of the crag
    :type crag: string
    :param min_ascents: minimal number of ascents to pull from a sector
    :type min_ascents: int
    :return: list of sectors
    """


def get_routes(driver, category, country, crag, sector, min_ascents):
    """
    Get routes from a given sector with number of ascents at least min_ascents.
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
    :param min_ascents: route has to have at least this number of ascents
    :type min_ascents: int
    :return: List of routes
    """


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
        print(page_index)
        if not page_data['pagination']['hasNext']:
            break
    return pd.DataFrame(ascents)


def get_sector_ascents(driver, category, country, crag, sector):
    """
    Get ascents from  a given sector.
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
    :return: pandas dataframe with ascents and their details
    """


def get_route_ascents_from_link(driver, route_link):
    """ Get list of ascents of a given route from it's 8a.nu link
    :param driver: selenium driver: driver logged into 8a
    :param route_link: string: link to a given route
    :return: route_data: pandas dataframe
    """
    time.sleep(3)
    url = route_link
    url = url.replace('8a.nu/crags', '8a.nu/api/crags')
    url += 'ascents?pageIndex={}&sortfield='

    page_index = 0
    route_ascents = []
    while True:
        driver.get(url.format(page_index))
        time.sleep(1)
        pre = driver.find_element_by_tag_name('pre').text
        data = json.loads(pre)
        # add ascents from a given page
        route_ascents += data['items']
        # break if there is no next page
        if not data['pagination']['hasNext']:
            break
        page_index += 1
    return pd.DataFrame(route_ascents)


def get_links_to_routes_from_a_crag(driver, category, country, crag, min_number_of_ascents):
    """ Get list of links to routes from a given crag, if number of
    their ascents is higher than a threshold.
    :param driver: selenium driver: driver logged into 8a
    :param category: string: sportclimbing or boudlering
    :param country: string: name of the country
    :param crag: string: name of the crag
    :param min_number_of_ascents: int: threshold
    :returns routes_links: list: list of links to routes
    """
    country_slug = slugify(country)
    crag_slug = slugify(crag)
    crag_address = f'https://www.8a.nu/crags/{category}/{country_slug}/{crag_slug}/routes'

    time.sleep(3)
    driver.get(crag_address)
    time.sleep(3)

    #get element with routes in the first page
    table = driver.find_element_by_tag_name("table")
    content = table.find_element_by_tag_name("tbody")
    routes = content.find_elements_by_tag_name("tr")

    #get routes from the first page
    routes_links = []
    for route in routes:
        step1 = route.find_elements_by_tag_name("td")
        if int(step1[2].text) < min_number_of_ascents:
            break
        step2 = step1[1].find_elements_by_class_name('name-link')[0]
        step3 = step2.find_elements_by_tag_name('a')[0]
        link = step3.get_attribute('href')
        routes_links.append(link)

    # if list is empty, return it now
    if not routes_links:
        return routes_links

    # scroll through next pages
    too_low_number = False
    while True:
        uls = driver.find_elements_by_tag_name("ul")
        # pages data
        pages = uls[-2]
        next_page = pages.find_elements_by_tag_name('li')[-1]
        # if next page is not disabled, follow the link to the next page
        if not next_page.get_attribute('class') == 'disabled':
            driver.get(next_page.find_element_by_tag_name('a').get_attribute('href'))
        else:
            break
        time.sleep(3)
        table = driver.find_element_by_tag_name("table")
        content = table.find_element_by_tag_name("tbody")
        routes = content.find_elements_by_tag_name("tr")
        for route in routes:
            step1 = route.find_elements_by_tag_name("td")
            # if the number of ascents is lower than treshold, stop the loop
            if int(step1[2].text) < min_number_of_ascents:
                too_low_number = True
                break
            step2 = step1[1].find_elements_by_class_name('name-link')[0]
            step3 = step2.find_elements_by_tag_name('a')[0]
            link = step3.get_attribute('href')
            routes_links.append(link)
        if too_low_number:
            break

    return routes_links


def get_sector_name_from_route_link(driver, route_link):
    """
    Get sector name from a route link
    :param driver: selenium driver: driver logged into 8a.nu
    :param route_link: string: link to a route
    :return: string: Name of the sector
    """

    time.sleep(2)
    url = route_link.replace('8a.nu/crags', '8a.nu/api/crags')
    driver.get(url)
    pre = driver.find_element_by_tag_name('pre').text
    data = json.loads(pre)
    return data['zlaggable']['sectorName']


def get_route_name_from_route_link(driver, route_link):
    """
    Get route name from a route link
    :param driver: selenium driver: driver logged into 8a.nu
    :param route_link: string: link to a route
    :return: string: Name of the route
    """

    time.sleep(2)
    url = route_link.replace('8a.nu/crags', '8a.nu/api/crags')
    driver.get(url)
    pre = driver.find_element_by_tag_name('pre').text
    data = json.loads(pre)
    return data['zlaggable']['zlaggableName']


def get_crag_ascents(driver, category, country, crag, min_number_of_ascents):
    """
    Get all ascents of routes in a crag.
    :param driver: selenium driver: driver logged into 8a.nu
    :param category: string: sportclimbing or bouldering
    :param country: string: name of the country
    :param crag: string: name of the crag
    :param min_number_of_ascents: int: minimal ascents the route should have to count it
    :return: pandas.DataFrame: list of crag ascents: route, sector, date
    """
    #TODO Raise exception when there is no such crag
    routes_links = get_links_to_routes_from_a_crag(driver, category, country, crag, min_number_of_ascents)

    crag_ascents = pd.DataFrame()
    for link in routes_links:
        print('sciagam dane dla drogi')
        print(link)
        route_ascents = get_route_ascents_from_link(driver, link)[['date']]
        route_ascents['route_name'] = get_route_name_from_route_link(driver, link)
        route_ascents['sector_name'] = get_sector_name_from_route_link(driver, link)
        crag_ascents = pd.concat([crag_ascents, route_ascents])
    return crag_ascents

