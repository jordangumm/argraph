from neomodel import (config, StructuredNode, StringProperty, IntegerProperty)
from neomodel import (DateProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom)


""" Reference Data """
class RefSequence(StructuredNode):
    """ Sequence found in ARG reference database w/ attributes
    """
    sequence = StringProperty(required=True) # encoded to 4x shorter length
    sequence_length = IntegerProperty() # unencoded sequence length, for use by encode/decode algorithm
    card_accession = StringProperty() # antibiotic resistance ontology identifier
    genbank_accession = StringProperty()
    antibiotic_molecule = StringProperty() # molecule resistant to
    reference = RelationshipTo('Reference', 'Found_In')


class Reference(StructuredNode):
    name = StringProperty()
    release = DateProperty()


""" Study Data """
#class SequenceClassification(StructuredNode):
#    sequence = StringProperty(unique_index=True, required=True)
#    refseq = RelationshipTo('RefSequence', 'REFSEQ')
    #study = RelationshipFrom('Study', 'IS_FROM')
    #sample = RelationshipFrom('Sample', 'IS_FROM')


#class Sample(StructuredNode):
#    sample_id = StringProperty(unique_index=True, required=True) # lab designated
#    illumina_id = StringProperty() # biocore designated sample identifier
