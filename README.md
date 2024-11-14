# Dewy

Submission for HackUMassXII \
Contributers: Larissa Zhu, Aditi Ravindra, Tiffany Nguyen, Rachel Jee

## Our Mission
After a long day of school or work, you likely look forward to going home, freshening up, and feeling good. As lovers of skincare ourselves, we know how much your daily skincare routine probably means to you. We want to help you perfect that routine! If you've been loving a product lately or have been feeling like branching out to explore new ones, we're here for you! With Dewy, you can look for products that contain similar ingredients to those that you've been loving or maybe have just heard good things about. Our ML Model explores the ingredients in each product in depth, right down to its molecular composition, and introduces you to other products that are composed similarly. We can't wait to help you expand your horizons!

## What it does
This website takes in a link to a product and returns the 5 most similar products contained in our database. We evaluate "similarity" based on the similarity of the ingredients between the user's product and the ingredients of the products in our dataset using ChemBERTa, a large pre-trained model for molecular property prediction. This helps us break down the chemical composition for each ingredient and compare them with each other.

## Tech Stack & Explanation

Front End: HTML, CSS, JavaScript
Back End: Flask, Selenium, SQL

First, we take the user's input (the url to their favorite product on either Ulta or IncideDecoder) and use Selenium to scrape the ingredients list of the product. We then feed this ingredients list into the ChemBERTa model and the model uses the ingredients list to calculate the similarity between the ingredients of the user's product and the similarity between the products in our dataset (https://www.kaggle.com/datasets/eward96/skincare-products-clean-dataset).  The model takes in a list of compounds of SMILES (Simplified Molecular Input Line Entry System) notation, which is a standard notation for chemical compounds in chemoinformatics and returns the top 5 most similar products. Then, we take the output of the model and display the names of the products on the webpage.

Given more time, we plan on finishing connecting our SQL database to our front end to display the images of the top 5 most similar products. We filled this database with the name of the product and its corresponding image, which was scraped from Google Images search using Playwright.
