wget https://card.mcmaster.ca/download/5/ontology-v3.0.5.tar.gz
mkdir -p card/ontology
tar -zxvf ontology-v3.0.5.tar.gz -C card/ontology
rm ontology-v3.0.5.tar.gz

wget https://card.mcmaster.ca/download/0/broadstreet-v3.0.5.tar.gz
mkdir -p card/data
tar -zxvf broadstreet-v3.0.5.tar.gz -C card/data
rm broadstreet-v3.0.5.tar.gz
