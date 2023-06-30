import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlsplit
from typing import Generator, Union
from prisma.partials import VerticalLifeRoute


def get_current_routes(gym_url: str) -> Generator[VerticalLifeRoute, None, None]:
  url = urlsplit(gym_url)
  response = requests.get(gym_url)
  soup = BeautifulSoup(response.text, 'html.parser')
  route_stats = soup.find(id='route_stats')
  if route_stats is None or isinstance(route_stats, str):
    raise Exception('Could not find route_stats')
  a_tags = route_stats.find_all('a')
  if not a_tags:
    raise Exception('Could not find any routs - that\'s weird')
  pattern = re.compile(f'{url.path}/climbs/[a-z0-9]+$')
  route_urls = [
      f'{url.scheme}://{url.netloc}{a["href"]}' for a in a_tags if pattern.match(a.get('href', ''))]

  for route_url in route_urls:
    route_info = get_route_info(route_url)
    if route_info is None:
      continue
    yield route_info


def get_route_info(route_url: str) -> Union[VerticalLifeRoute, None]:
  response = requests.get(route_url)
  soup = BeautifulSoup(response.text, 'html.parser')
  route_info = soup.find('h1')
  if route_info is None or isinstance(route_info, str):
    return None
  route_id = route_url.split('/')[-1]
  route_difficulty = route_info.get('data-difficulty')
  if route_difficulty is None:
    return None
  route_name = route_info.text.replace(f'{route_difficulty}', '').strip()
  if not route_name:
    return None
  return VerticalLifeRoute(id=route_id, name=route_name, difficulty=str(route_difficulty), url=route_url)
