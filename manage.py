import click

from argraph.models import RefSequence, Reference

from neomodel import db, clear_neo4j_database
from neomodel import config



@click.group()
@click.pass_context
def cli(ctx):
    pass


@cli.command()
def build_database():
    """ IN DEVELOPMENT: builds base neo4j ARG database """
    click.echo('Building database')
    config.DATABASE_URL = 'bolt://neo4j:neo4j@localhost:7687'
    #clear_neo4j_database(db)
    #db.set_connection('bolt://neo4j:neo4j@localhost:7687')
    RefSequence(sequence='ACGT', antibiotic_molecule='None').save()
    Reference(name='CARD2017').save()
    print(RefSequence.nodes.get())


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
