from prisma.models import Route

Route.create_partial('VerticalLifeRoute', include={'id', 'name', 'difficulty', 'url'})
