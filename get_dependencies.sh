POS_PT='http://nilc.icmc.usp.br/nlpnet/data/pos-pt.tgz'
LEMMAS='http://www.nilc.icmc.usp.br/nilc/projects/unitex-pb/web/files/DELAF_PB_v2.zip'

echo 'Making directories'
mkdir Clustering/language
mkdir Clustering/language/portuguese
cd Clustering/language/portuguese

echo 'Downloading files'
wget $POS_PT
wget $LEMMAS

echo 'Extracting files'
tar -xzf pos-pt.tgz --strip-components 1
unzip DELAF_PB_v2.zip

echo 'Cleaning files'
gio trash pos-pt.tgz
gio trash DELAF_PB_v2
