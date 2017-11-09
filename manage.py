import click
import configparser

from argraph.models import RefSequence, Reference

from neomodel import db, clear_neo4j_database
from neomodel import config

from urllib.parse import urlparse


def get_config():
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')

    if config['neo4j']['ARG_DATABASE_PATH'] == 'None':
        while True:
            user_input = raw_input('ARG_DATABASE_PATH.  Set now?: [Y/n]')
            if 'n' in user_input or 'N' in user_input:
                break
            elif 'y' in user_input or 'Y' in user_input:
                user_input = raw_input('ARG_DATABASE_PATH')

    return cfg


@click.group()
@click.pass_context
def cli(ctx):
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    config.DATABASE_URL = cfg['neo4j']['DATABASE_URL']
    db.set_connection(config.DATABASE_URL)


@cli.command()
def build_database():
    """ IN DEVELOPMENT: builds base neo4j ARG database """
    #user_input = raw_input('[WARNING] ')
    click.echo('Clearing database')
    clear_neo4j_database(db)
    click.echo('Building database')
    RefSequence(sequence='ACGT', antibiotic_molecule='None').save()
    RefSequence(sequence='ACGTCT', antibiotic_molecule='None').save()
    Reference(name='CARD2017').save()
    for refseq in RefSequence.nodes.filter():
        print(refseq)


@cli.command()
def add_reads(sample_name, r1_fp, r2_fp=None):
    """ TODO: classifies and adds reads to database """
    click.echo('reads successfully added to database')


@cli.command()
def add_contigs(sample_name, contigs_fp):
    """ TODO: classifies and adds contigs to database """
    click.echo('still in development')


@cli.command()
def add_orfs(sample_name, orfs_fp):
    """ TODO: classifies and adds orfs to database """
    click.echo('still in development')


if __name__ == "__main__":
    cli()
