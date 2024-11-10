#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os 
#import torch
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.neighbors import KNeighborsClassifier, NearestNeighbors  # K-Nearest Neighbors
from sklearn.linear_model import LogisticRegression  # Logistic Regression
from sklearn.tree import DecisionTreeClassifier  # Decision Tree
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
# from scraping import get_ingredients
#from SMILES import CIRconvert
import pubchempy as pcp
import cirpy
import ast
import time
import csv
from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
# import faiss


# In[2]:


import cirpy

def get_smiles(identifiers):
    # Retrieve SMILES for each identifier in the list
    smiles_list = []
    for identifier in identifiers:
        smiles = cirpy.resolve(identifier, "smiles")
        if smiles:
            smiles_list.append(smiles)
        else:
            smiles_list.append("SMILES not found")  # Handle cases where SMILES isn't found
    return smiles_list


# In[3]:


import pandas as pd
from transformers import AutoTokenizer, AutoModel, AutoModelForMaskedLM
import torch
from sklearn.metrics.pairwise import cosine_similarity
# Load model directly


tokenizer = AutoTokenizer.from_pretrained("seyonec/ChemBERTa-zinc-base-v1")
model = AutoModelForMaskedLM.from_pretrained("seyonec/ChemBERTa-zinc-base-v1")


# In[17]:


file_path = r"./Copy of with null - Smiles.csv"
dfFR = pd.read_csv(file_path, header=0)


# In[18]:


def get_embedding(smiles):
    print("hi")
    inputs = tokenizer(smiles, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
        # Get the last hidden state, average over token embeddings
        embedding = outputs.hidden_states[-1].mean(dim=1).squeeze()
        print("embedding", embedding)
    return embedding.numpy()

# Precompute embeddings for each product
#dfFR["embedding"] = dfFR["SMILES"].apply(lambda x: get_embedding(x))


# In[ ]:


# import pandas as pd

# # Load the DataFrame from the pickle file
# dfFR = pd.read_pickle("chemBerta.pkl")


# In[19]:


dfFR


# In[6]:


dfFR


# In[21]:


dfFR.to_pickle("tryAgain.pkl")


# In[22]:


testing = pd.read_pickle("tryAgain.pkl")


# In[23]:


testing


# In[24]:


from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def find_similar_products(user_smiles, df, top_n=5):
    # Calculate embedding for user-inputted product
    user_embedding = get_embedding(user_smiles)
    
    # Ensure user_embedding is 2D
    if len(user_embedding.shape) == 1:
        user_embedding = user_embedding.reshape(1, -1)
    
    # Calculate cosine similarity
    similarities = []
    for idx, product_embedding in enumerate(df['embedding']):
        # Ensure product_embedding is 2D
        print(type(product_embedding))
        print(product_embedding)
        if len(product_embedding.shape) == 1:
            product_embedding = product_embedding.reshape(1, -1)
        
        # Pad only for the current comparison
        padded_user_embedding = user_embedding
        padded_product_embedding = product_embedding
        
        if padded_user_embedding.shape[1] != padded_product_embedding.shape[1]:
            if padded_user_embedding.shape[1] > padded_product_embedding.shape[1]:
                padding_size = padded_user_embedding.shape[1] - padded_product_embedding.shape[1]
                padded_product_embedding = np.pad(padded_product_embedding, ((0, 0), (0, padding_size)), 'constant')
            else:
                padding_size = padded_product_embedding.shape[1] - padded_user_embedding.shape[1]
                padded_user_embedding = np.pad(padded_user_embedding, ((0, 0), (0, padding_size)), 'constant')
        
        # Calculate cosine similarity with locally padded embeddings
        similarity = cosine_similarity(padded_user_embedding, padded_product_embedding)
        similarities.append((idx, similarity[0][0]))  # Store index and similarity score

    # Sort by similarity score and retrieve top_n most similar
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)
    top_indices = [idx for idx, _ in similarities[:top_n]]
    top_similarities = [score for _, score in similarities[:top_n]]

    top_products = df.iloc[top_indices].copy()
    top_products['Similarity Score'] = top_similarities

    return top_products

# User input (example SMILES list)
user_smiles = ["OCC(O)CO", "CCCCCCCCCCCCCCCCO"]

# Find top 5 similar products
top_similar_products = find_similar_products(user_smiles, testing)
print(top_similar_products[['product_name', 'clean_ingreds', 'price', 'Similarity Score']])


# In[24]:


def predict(ingreList):
    testing = pd.read_pickle("tryAgain.pkl")
    # Find top 5 similar products
    b = get_smiles(ingreList)
    top_similar_products = find_similar_products(b, testing)
    return top_similar_products[['product_name', 'clean_ingreds']]


# In[25]:


import pandas as pd

# Load the CSV file
csv_file_path = 'embeddings.csv'  # Replace with your CSV file path
dfFR = pd.read_csv(csv_file_path)

# Save the DataFrame to a pickle file
pickle_file_path = 'chemBerta.pkl'  # Specify your desired pickle file path
dfFR.to_pickle(pickle_file_path)


# In[43]:


merged_df = pd.read_csv("fingerprints_and_smiles.csv")


# In[49]:


merged_df.shape


# In[46]:


def calculate_top_5_similar_products(user_fingerprint_list, df):
    # Calculate Tanimoto similarity of each of the fingerprints of the user's product against every product's fingerprints
    tanimoto = {}
    i=0
    curr_row_index = 0
    curr_product_list_len = 0
    for product_fp_row in df['Fingerprints']: # product_fp_row is of type 2d list
        total_similarity = [0]*len(user_fingerprint_list) # Calculate the total sum of Tanimoto similarities between user's and product's fingerprints.
        for user_fp in user_fingerprint_list: # user_fp is of type list (fingerprint of one of the user's ingredients)
            for product_fp in product_fp_row: # product_fp is of tyoe list (fingerprint of one of our products' ingredients)
                curr_product_list_len = len(product_fp_row)
                similarity = DataStructs.TanimotoSimilarity(user_fp, product_fp)
                total_similarity[i] += similarity # total_similarity[i] is the sum of the similarity of each ingredient from the each of the user's ingredients against the product
                num_product_ingredients = len(product_fp_row)
            i += 1
        for j in range(len(total_similarity)):
            total_similarity[j] = total_similarity[j] / curr_product_list_len
        avg_tanimoto = sum(total_similarity) / len(total_similarity) # normalization
        key = df.iloc[curr_row_index, 1] # gets name of the current product being compared to and stores it as a key
        tanimoto[key] = avg_tanimoto
        # prevent out of bounds error
        i = 0
        curr_row_index += 1
    return dict(sorted(tanimoto.items(), key=lambda item: item[1], reverse=True)[:5])


# In[48]:


user_smiles = ["OCC(O)CO", "CCCCCCCCCCCCCCCCO"]
# turn into fingerprints
user_fingerprint_list = []
for r in user_smiles:
        mol = Chem.MolFromSmiles(r)
        try:
            # Generate Morgan Fingerprints
            user_fingerprint_list.append(AllChem.GetMorganFingerprintAsBitVect(mol, radius=2, nBits=2048))
        except:
            continue
total_similarity = calculate_top_5_similar_products(user_fingerprint_list, merged_df) # this returns correct normalized similarities
total_similarity

