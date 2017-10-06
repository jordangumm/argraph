from django.core.management.base import BaseCommand, CommandError
from argraph.models import RefSequence, Reference

from neomodel import db, clear_neo4j_database

class Command(BaseCommand):
    help = '(re)Builds neo4j database using current references'

    def update_references(self):
        """ Update references from web sources """
        print 'updating references'
        pass

    def handle(self, *args, **options):
        #db.set_connection('bolt://neo4j:neo4j@localhost:7687')
        RefSequence(sequence='ACGT', antibiotic_molecule='None').save()

        #print RefSequence.nodes.get()

        #clear_neo4j_database(db)
        self.update_references()
        print 'building database'
        print 'done'
