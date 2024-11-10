from urllib.request import urlopen
from urllib.parse import quote
import time

# Modify CIRconvert to handle retries and delays
# def CIRconvert(identifiers, retries=3, delay=3):
#     smiles_results = []
#     for ids in identifiers:
#         attempt = 0
#         while attempt < retries:
#             try:
#                 # Encode ingredient and request SMILES conversion
#                 url = 'http://cactus.nci.nih.gov/chemical/structure/' + quote(ids) + '/smiles'
#                 ans = urlopen(url, timeout=10).read().decode('utf8')  # Adding timeout for robustness
#                 if ans:
#                     smiles_results.append(ans)
#                 else:
#                     smiles_results.append(None)
#                     print(f"No SMILES found for '{ids}'")
#                 break  # Break the retry loop if successful
#             except Exception as e:
#                 print(f"Error retrieving SMILES for '{ids}': {e}. Retrying...")
#                 attempt += 1
#                 time.sleep(delay)  # Delay before retrying
#                 if attempt == retries:
#                     smiles_results.append(None)  # Append None after final failed attempt
#                     print(f"Failed to retrieve SMILES for '{ids}' after {retries} attempts.")
#     return smiles_results

def CIRconvert(ingredients_list):
    smiles_results = []
    for ingredient in ingredients_list:
        try:
            url = 'http://cactus.nci.nih.gov/chemical/structure/' + quote(ingredient.strip()) + '/smiles'
            ans = urlopen(url).read().decode('utf8')
            if ans:
                smiles_results.append(ans)
        except:
            continue
            smiles_results.append(None)  # Append None if conversion fails
    return smiles_results

# Example array of identifiers
identifiers = ['capric triglyceride', 'cetyl alcohol', 'propanediol', 'Titanium Dioxide (Ci 77891)', 'Hydrogenated Castor Oil', 'Isohexadecane']

# Call CIRconvert with the array
smiles_results = CIRconvert(identifiers)

# Print results
for identifier, smiles in zip(identifiers, smiles_results):
    print(f"{identifier}: {smiles}")


# import requests
# import time

# def pubchem_smiles(ingredient):
#     try:
#         url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{ingredient}/property/IsomericSMILES/JSON"
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()  # Check for HTTP errors
#         data = response.json()
#         # Extract SMILES if available
#         smiles = data["PropertyTable"]["Properties"][0]["IsomericSMILES"]
#         return smiles
#     except Exception as e:
#         #print(f"Error retrieving SMILES for '{ingredient}': {e}")
#         return None

# # Example array of ingredients
# identifiers = ['capric triglyceride', 'cetyl alcohol', 'propanediol', 'Titanium Dioxide', 'Hydrogenated Castor Oil', 'Isohexadecane']


# # Retrieve SMILES, skipping None results
# smiles_results = []
# for ingredient in identifiers:
#     smiles = pubchem_smiles(ingredient)
#     if smiles is not None:
#         smiles_results.append(smiles)
#     time.sleep(1)  # Respect rate limit

# # Print results
# for ingredient, smiles in zip(identifiers, smiles_results):
#     print(f"{ingredient}: {smiles}")
