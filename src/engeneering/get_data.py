#%%

import os
import dotenv

dotenv.load_dotenv('../../.env')

print(os.environ['KAGGLE_USERNAME'])
print(os.environ['KAGGLE_KEY'])
#%%

#%%
from kaggle import api

api = api.KaggleApi()