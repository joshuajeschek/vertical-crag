DEV_ENV = $(shell cat .env.development)
PROD_ENV = $(shell cat .env.production)


default: dev

dev:
	env $(DEV_ENV) python3 src/main.py

prod:
	env $(PROD_ENV) python3 src/main.py

tunnel:
	cloudflared access tcp --hostname postgres.jeschek.eu --url localhost:5432

prisma: prisma-dev

prisma-prod:
	prisma $(run)
prisma-dev:
	env $(DEV_ENV) prisma $(run)
