import re

import networkx
import obonet
import pandas as pd
import screed


graph = obonet.read_obo('card/ontology/aro.obo')
info  = pd.read_csv('card/data/aro_index.tsv', sep='\t')


def get_relationship(aro, relation):
    node = graph.node[aro]
    if 'relationship' in node:
        for rel in node['relationship']:
            if relation in rel:
                rel_aro = rel.split(' ')[-1]
                yield graph.node[rel_aro]['name']
    if 'is_a' in node:
        for new_aro in node['is_a']:
            yield from get_relationship(new_aro, relation)


def get_mechanism(aro):
    node = graph.node[aro]
    if 'is_a' in node:
        for new_aro in node['is_a']:
            if new_aro == 'ARO:1000002':  # mechanism of antibiotic resistance
                yield node['name']
            else:
                yield from get_mechanism(new_aro)


with screed.open('card/data/nucleotide_fasta_protein_homolog_model.fasta') as seqfile:
    output = []
    for seq in seqfile:
        aro = seq.name.split('|')[4]
        output.append({
            'target':     seq.name,
            'aro':        aro,
            'gc_content': len(re.findall('[GC]', seq.sequence)) / len(seq.sequence),
            'drug_class': '|'.join(set([d for d in get_relationship(aro, 'confers_resistance_to_drug_class')])),
            'mechanism':  '|'.join(set([m for m in get_mechanism(aro)])),
        })

df = pd.DataFrame(output)
df.to_csv('gene_info.tsv', sep='\t')
