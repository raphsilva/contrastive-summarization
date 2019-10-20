POS_PT='http://nilc.icmc.usp.br/nlpnet/data/pos-pt.tgz'

echo 'Making directories'
mkdir Clustering/language
mkdir Clustering/language/portuguese
cd Clustering/language/portuguese

echo 'Downloading files'
wget $POS_PT

echo 'Extracting files'
tar -xzf pos-pt.tgz --strip-components 1

echo 'Cleaning files'
gio trash pos-pt.tgz
