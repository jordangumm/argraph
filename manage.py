import os, sys
import click
import screed
import configparser

from argraph.models import RefSequence, Reference

from neomodel import db, clear_neo4j_database
from neomodel import config

from urllib.parse import urlparse

from argraph.compression import encode_nuc, decode_nuc


def get_config():
    cfg = configparser.ConfigParser()
    cfg.read('config.ini')
    return cfg


@click.group()
@click.pass_context
def cli(ctx):
    cfg = get_config()
    config.DATABASE_URL = cfg['neo4j']['DATABASE_URL']
    db.set_connection(config.DATABASE_URL)


@cli.command()
def set_argdb_path(path):
    """ Writes path as config ARG_DATABASE_PATH """
    cfg = get_config()

    cfg['neo4j']['ARG_DATABASE_PATH'] = user_input
    with open('config.ini', 'w+') as configfile:
        cfg.write(configfile)
    return None


@cli.command()
def print_multirelational_args():
    """ Print ARGs with multiple relationships """
    #seqs = RefSequence.nodes.filter(sequence=sequence)
    refs = Reference.nodes.filter()
    refs = [x for x in refs]
    seqs = RefSequence.nodes.filter() # print any sequence for testing
    for seq in seqs:
        num_relations = 0
        for ref in refs:
            if seq.reference.relationship(ref):
                num_relations += 1
        if num_relations > 1:
            print('{}: {}'.format(seq.id, num_relations))

@cli.command()
def clear_database():
    """ Print speciric ARG reference sequence attributes by sequence """
    clear_neo4j_database(db)


@cli.command()
def build_database():
    """ IN DEVELOPMENT: builds base neo4j ARG database
    """
    cfg = get_config()
    if cfg['neo4j']['ARG_DATABASE_PATH'] == 'None':
        while True:
            user_input = input('ARG_DATABASE_PATH: ')
            if os.path.exists(user_input):
                set_argdb_path(user_input)
                cfg = get_config()
                break
            print('The path {} does not exist!\n'.format(user_input))

    click.echo('Clearing database')
    clear_neo4j_database(db)
    click.echo('Building database')
    for argdb in os.listdir(cfg['neo4j']['ARG_DATABASE_PATH']):
        if not '.fasta' in argdb and not '.fa' in argdb: continue
        reference_name = argdb.replace('.fasta','')
        click.echo('\nloading {}'.format(reference_name))

        reference_holder = Reference(name=reference_name)
        reference_holder.save()
        with screed.open(os.path.join(cfg['neo4j']['ARG_DATABASE_PATH'], argdb)) as seqfile:
            for read in seqfile:
                if any((c in set('NSRKY')) for c in read.sequence):
                    print('read has illegal character')
                    continue # binary representation doesn't support unknown nucleotides
                card_elements = read.name.split('|')

                card_accession = 'None'
                genbank_accession = 'None'
                antibiotic_molecule = 'None'
                if 'ARO' in card_elements:
                    card_accession = [x for x in card_elements if 'ARO' in x][0]
                    genbank_accession = card_elements[1]
                    antibiotic_molecule = card_elements[-1].split(' ')[0]

                already_existed = False
                for refseq in RefSequence.nodes.filter(sequence=encode_nuc(read.sequence)):
                    if refseq.sequence == encode_nuc(read.sequence):
                        print('duplicate sequence')

                        card_accession = refseq.card_accession
                        genbank_accession = refseq.genbank_accession
                        antibiotic_molecule = refseq.antibiotic_molecule

                        if card_accession == 'None':
                            card_accession = refseq.card_accession # keep the CARD accession if there
                        if refseq.card_accession != card_accession:
                            card_accession = '{}|{}'.format(card_accession, refseq.card_accession)
                        if refseq.genbank_accession != genbank_accession:
                            genbank_accession = '{}|{}'.format(genbank_accession, refseq.genbank_accession)
                        if refseq.antibiotic_molecule != antibiotic_molecule:
                            antibiotic_molecule = '{}|{}'.format(antibiotic_molecule, refseq.antibiotic_molecule)
                        RefSequence.create_or_update({'sequence': encode_nuc(read.sequence),
                                                      'sequence_length': len(read.sequence),
                                                      'card_accession': card_accession,
                                                      'genbank_accession': genbank_accession,
                                                      'antibiotic_molecule': antibiotic_molecule})
                        already_existed = True
                        break

                if not already_existed:
                    refseq = RefSequence(sequence=encode_nuc(read.sequence),
                                sequence_length=len(read.sequence),
                                card_accession=card_accession,
                                genbank_accession=genbank_accession,
                                antibiotic_molecule=antibiotic_molecule)
                    refseq.save()
                    refseq.reference.connect(reference_holder)
    return None


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
