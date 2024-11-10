# Dewy

Submission for HackUMassXII \
Team members: Larissa Zhu, Tiffany Nguyen, Aditi Ravindra, Rachel Jee

## Inspiration
All the members of our team have an interest in skincare and are invested in having good products that have clean ingredients so we wanted to make a system to make it easier to find other products with similar ingredients!

## What it does
This website takes in a user's product that they already like and returns the 5 most similar products that we had based on the similarity of the ingredients between the user's product and the ingredients of the products in our dataset using ChemBERTa, a large pre-trained model for molecular property prediction. 

## How we built it

Front End: HTML, CSS, JavaScript
Back End: Flask, Selenium, SQL (almost)

First, we take the user's input (the url to their favorite product on either Ulta or IncideDecoder) and use Selenium to scrape the ingredients list of the product. We then feed this ingredients list into the ChemBERTa model and the model uses the ingredients list to calculate the similarity between the ingredients of the user's product and the similarity between the products in our dataset (https://www.kaggle.com/datasets/eward96/skincare-products-clean-dataset).  The model takes in a list of compounds of SMILES (Simplified Molecular Input Line Entry System) notation, which is a standard notation for chemical compounds in chemoinformatics and returns the top 5 most similar products. Then, we take the output of the model and display the names of the products on the webpage.

Given more time, we would finished connecting our SQL database to our front end to display the images of the top 5 most similar products. We filled this database with the name of the product and its corresponding image, which was scraped from Google Images search using Playwright.
