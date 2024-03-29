from flask.cli import AppGroup
from app.seeders.user_seeds import add_user_seeds, remove_user_seeds
from app.seeders.game_seeds import add_game_seeds, remove_game_seeds
from app.seeders.trade_seeds import add_trade_seeds, remove_trade_seeds
from app.seeders.review_seeds import add_review_seeds, remove_review_seeds

from app import db, environment, SCHEMA

seeder_command = AppGroup('seed')


@seeder_command.command('all')
def seed_all():
    if environment == 'production':
        db.session.execute(f"TRUNCATE table {SCHEMA}.trades RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE table {SCHEMA}.reviews RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE table {SCHEMA}.games RESTART IDENTITY CASCADE;")
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
        db.session.commit()
    add_user_seeds()
    add_game_seeds()
    add_trade_seeds()
    add_review_seeds()


@seeder_command.command('undo')
def unseed_all():
    remove_trade_seeds()
    remove_review_seeds()
    remove_game_seeds()
    remove_user_seeds()
