from prisma.client import Prisma
from prisma.partials import VerticalLifeRoute
from enum import Enum


class RouteType(Enum):
    NEW = 1
    UPDATED = 2
    EXISTING = 3
    REMOVED = 4

def upsert_route(db: Prisma, route: VerticalLifeRoute) -> RouteType:
    existing_route = db.route.find_first(where={'id': route.id})
    if existing_route is None:
        db.route.create(data={'id': route.id, 'name': route.name, 'difficulty': route.difficulty, 'url': route.url})
        return RouteType.NEW
    elif existing_route.name != route.name or existing_route.difficulty != route.difficulty or existing_route.url != route.url:
      db.route.update(where={'id': route.id}, data={'name': route.name, 'difficulty': route.difficulty, 'url': route.url})
      return RouteType.UPDATED
    return RouteType.EXISTING
