from neomodel import (config, StructuredNode, StringProperty, IntegerProperty)
from neomodel import (DateProperty, UniqueIdProperty, RelationshipTo, RelationshipFrom)


""" Reference Data """
class RefSequence(StructuredNode):
    """ Sequence found in ARG reference database w/ attributes
    """
    sequence = StringProperty(unique_index=True, required=True)
    antibiotic_molecule = StringProperty() # molecule resistant to
    #reference = RelationshipFrom('Reference', 'Found_In')


class Reference(StructuredNode):
    name = StringProperty(unique_index=True)
    release = DateProperty()


""" Study Data """
#class SequenceClassification(StructuredNode):
#    sequence = StringProperty(unique_index=True, required=True)
#    refseq = RelationshipTo('RefSequence', 'REFSEQ')
    #study = RelationshipFrom('Study', 'IS_FROM')
    #sample = RelationshipFrom('Sample', 'IS_FROM')


#class Study(StructuredNode):
#    name = StringProperty(unique_index=True, required=True)


#class Sample(StructuredNode):
#    sample_id = StringProperty(unique_index=True, required=True) # lab designated
#    illumina_id = StringProperty() # biocore designated sample identifier
