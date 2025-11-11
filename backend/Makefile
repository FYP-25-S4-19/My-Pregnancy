# Make sure that the module path matches those of the seeding scripts
db_seed_base:
	python -m app.db.seeding.seed_db_base

db_seed_dev:
	python -m app.db.seeding.seed_db_dev

db_seed_tests:
	python -m app.db.seeding.seed_db_tests

nuke_db: # I think this goes without saying but BE.VERY.CAREFUL!
	python -m app.db.seeding.nuke_db