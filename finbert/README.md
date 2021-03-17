## Setup

Install the dependencies and activate it
```
conda env create -f environment.yml
conda activate finbert
export PYTHONPATH=$PYTHONPATH:<root module path>
```

Create a directory to store the model
```
mkdir -p models/classifier_model/finbert-sentiment
cd models/classifier_model/finbert-sentiment
wget https://prosus-public.s3-eu-west-1.amazonaws.com/finbert/finbert-sentiment/pytorch_model.bin
```

## Predict
This will write the output `predictions.csv` to `output_dir`. 

Each sentences in `text_path` is assumed to be separated by '\n\n'. 

```bash
python predict.py --text_path daily_mail_first_sentence.txt --output_dir output/ --model_path models/classifier_model/finbert-sentiment
```
