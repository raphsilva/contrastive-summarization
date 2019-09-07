sudo python3.6 -m pip install nltk
sudo python3.6 -m pip install nlpnet
sudo python3.6 -m pip install h5py
sudo python3.6 -m pip install sklearn


python3.6  - << EOF

import nltk

nltk.download('rslp')
nltk.download('punkt')
nltk.download('stopwords')

exit()

EOF
