# Contrastive Summarization of Opinative Texts

This repository contains algorithms used to perform contrastive opinion summarization, which is a task that aims to build summaries that help find differences about two entities given opinions about them. 

Scientific text explaining the methods and their implementations will be coming soon. The methods available in this repository are:
* **Statistic**: Builds summaries that are more statistically similar to the source, considering the means and standard deviations of polarities of each aspect. Described by _Lerman and McDonald (2009)_.  
* **Clustering**: Performs a similarity clustering of sentences, them matches clusters as to form pairs and selects the best sentence of each cluster to be added to the summary. Described by _Kim and Zhai (2009)_.
* **Similarity**: Uses similarities of sentences (by looking at the topics approached in each sentence) to estimate which sentences add more value to the summary considering representativity, contrastivity and diversity. Described by _Jin et al. (2016)_.
* **Ranking**: Makes a ranking of pairs of contrasting opinions based on their frequency in the source, then selects sentences that contain the top-ranked opinions to enter the summary. Novel method, not published yet.


## Implementations

The software of this repository is intended to run on Linux with **Python 3.6** and the use of a terminal for commands execution. The software provided is meant to be used for research by people with experience in programming.

The implementation is made to allow tests in batch: a single execution can perform tests over all input files and repeat the tests an adjustable amount of times (for each input) as to find the average performance of the methods (since they are non deterministic).


### Input

The input data is supposed to be in the directory `input` in the root of the repository. This directory will be made during the installation procedures. 

The input data of each entity is a JSON file with a list of sentences with IDs and their opinions identified. Opinions are a list of form `[aspect, polarity]`. Positive polarity is represented as `100` and negative polarity is represented as `-100`. Below there's an example of an excerpt of an input data file. 

```json
{
  "data": [
    { "sentence": "Bom custo/benefício.",
      "opinions": [["PREÇO",100]],
      "id": 1            
    },
    { "sentence": "Boa velocidade na reprodução de vídeos e bom de espaço de memória.",
      "opinions": [["DESEMPENHO",100], ["ARMAZENAMENTO",100]],
      "id": 3            
    }
  ]
}
```

### Output

After tests are done, the outputs will be in two folders: `OUTPUT` will contain the summaries generated and `RESULTS` will contain the summaries characteristics, including evaluation. 

#### Summaries 

After a method of summarization has been executed multiple times for a given input, the summary that best reflects the average performance of the method is chosen and saved at `[method]/OUTPUT/[n]_[dataset].txt`, where `n` is an identifier attributed to each execution. Summaries are saved in simple text format and are divided in two parts, separated by a long line break, one for each entity.

#### Evaluation

The evaluation results are saved in the directory `RESULTS` of each method. They are files named `[method]/OUTPUT/[n]_[dataset].txt`,  where `n` is an identifier attributed to each execution. The files are JSONs organized as follows: 
* Information about the **input**, such as **number of words**, **number of sentences**, **file names**.
* The **options** used in the tests, such as **method parameters**, **limits of words**, etc;
* Statistics of execution, such as **time consumed** and **number of distinct summaries** gotten;
* The **evaluation** information, with the metrics of **representativity**, **contrastivity** and **diversity** (indicated by their first letters) calculated for the summaries and the **harmonic mean** of the three (indicated by H):
    * The **scores** for all tests made on the dataset;
    * The **means** of the scores;
    * The **standard deviation** of the scores. 
* The **quantitative** information of summaries, with the **average of words** and **average of sentences**.
* Information of **each summary** generated for that input, showing the **parameters** used, the **size** of the summary, the **evaluation** scores and the **indexes of sentences** that were chosen for the summary.



## Instructions

### Installation

#### Download repository

Download the repository with `git clone https://github.com/raphsilva/contrastive-summarization.git`. 

#### Get dependencies

Some dependencies need to be installed before the first execution. On a terminal, go to the repository main directory and follow the instructions below.

#### Dataset

A dataset is needed to be used as input by the methods. To download the dataset and place it properly, run the file `get_dataset.sh` in the root of this repository. 

The dataset used is available at https://github.com/raphsilva/corpus-4p, where you can find more information about it. You can use other dataset as long as they have the same format as this one.

#### Language data

If you intend to run the Clustering method, additional data is needed for language processing. Download them with the script in `get_dependencies.sh`.

#### Python modules

THe python modules needed to execute the files are listed in `requirements.txt`. To install them, run `pip install -r requirements.txt`. Depending on how Python and pip were installed in you computer, you may need to specify the pip version: `pip3 install -r requirements.txt`.


### Execution

The execution of each method is done inside the method's directory. Choose the method you want to execute, go to its directory and follow the instructions below.

#### Set options

Each method has a file `setup.py` which allows you to choose the options for execution. The values you may want to change are: 
* `LIM_WORDS`: Maximum number of words in the summary (for each entity).
* `LIM_SENTENCES`: Maximum number of sentences in the summary (for each entity).
* `REPEAT_TESTS`: Number of tests performed with each dataset (which are shuffled before each repetition)
* `DISCARD_TESTS`: Amount of outliers tests that will be discarded for overall evaluation (the total number of discarded tests is twice this value, because this amount of best summaries and of worst summaries are discarded).
* `DATASETS_TO_TEST`: Choose which files of data will be tested.

#### Run

To run a method, go to its directory and run the `main.py` file with Python 3.6. 

#### See results

Output files and evaluation results will be inside each method's directory.


### Summary

Below are all the commands from the steps detailed above. 

To install:
```
git clone https://github.com/raphsilva/contrastive-summarization.git
cd contrastive-summarization
./get_dataset.sh
./get_dependencies.sh
pip install -r requirements.txt
```

To execute all methods:
```
cd Similarity
python main.py
cd ../Ranking
python main.py
cd ../Statistic
python main.py
cd ../Clustering
python main.py
cd ..
```