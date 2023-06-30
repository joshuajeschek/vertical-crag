import os
from prisma import Prisma
from db import upsert_route
from scraper import get_current_routes


def main(gym_url: str) -> None:
  db = Prisma()
  db.connect()

  routes = get_current_routes(gym_url)
  for route in routes:
    route_type = upsert_route(db, route)
    print(f'Upserted {route_type.name} route: {route.name} ({route.difficulty})')

  db.disconnect()


if __name__ == '__main__':
  gym_url = os.environ.get('GYM_URL')
  if gym_url is None:
    raise Exception('GYM_URL environment variable not set')
  main(gym_url)
