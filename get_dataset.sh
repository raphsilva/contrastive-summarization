DATASET='https://github.com/raphsilva/corpus-4p/archive/v1.0.0-beta.tar.gz'

echo 'Cleaning old files'
gio trash input

echo 'Downloading data set'
wget $DATASET -O dataset.tar.gz

echo 'Extracting files'
mkdir downloaded_dataset
tar -xzf dataset.tar.gz --strip-components 1 --directory downloaded_dataset

echo 'Moving files'
mv downloaded_dataset/dataset/skim/ input

echo 'Cleaning unecessary files'
gio trash downloaded_dataset
gio trash dataset.tar.gz

