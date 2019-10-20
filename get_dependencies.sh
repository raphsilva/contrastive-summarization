POS_PT='http://nilc.icmc.usp.br/nlpnet/data/pos-pt.tgz'
LEMMAS='http://www.nilc.icmc.usp.br/nilc/projects/unitex-pb/web/files/DELAF_PB_v2.zip'
STOPWORDS='https://gist.github.com/alopes/5358189/raw/2107d809cca6b83ce3d8e04dbd9463283025284f/stopwords.txt'

echo 'Making directories'
mkdir Clustering/language
mkdir Clustering/language/portuguese
cd Clustering/language/portuguese

echo 'Downloading files'
wget $POS_PT
wget $LEMMAS
wget $STOPWORDS

echo 'Extracting files'
tar -xzf pos-pt.tgz --strip-components 1
unzip DELAF_PB_v2.zip
mv Delaf2015v04.dic lemmas.dic

echo 'Cleaning files'
gio trash pos-pt.tgz
gio trash DELAF_PB_v2.zip
