# Company-Name-Standardization
Using Natural Language Processing to standardize Company Names

# Introduction
Problem Statement is to standardize a list of similar company names **(JPMC, JPMorgan, J.P.Morgan Chase)** to their standard name **JPMorgan Chase & Co.**
We could have used traditional string matching approaches like ***Levenshtein Distance*** for string matching but they are really slow for large datasets.

# Installation
1. Clone or download this repository.
2. Run pip install -r requirements.txt inside this repo. Consider doing this inside of a Python virtual environment.
3. **data.xlsx** contains the standard list of company names to which you want your current name(s) to be mapped to. I have downloaded the Forbes 2000 list and taken the **name** column for that purpose. **Note: The name of the column in data.xlsx should be "name". Check out that data.xlsx file in the repo for reference.**
4. Use  ```streamlit run app.py``` to start the application.
![image](https://user-images.githubusercontent.com/21261866/128198978-3677bbdb-9945-446b-8279-bdba792fc331.png)
The user has the option to enter the name in the search bar like I did(**JPMC**) and you could see the result below that it correctly maps **JPMC** to **JPMorgan Chase & Co.** If you have multiple items then you can upload a txt/csv file in with the column name as **"name"**. I will add a **test.txt** in the repo for reference. 
![image](https://user-images.githubusercontent.com/21261866/128200110-c1aa0357-d831-4623-a219-3f4cff356182.png)

As you can see it correctly maps JPMC and Deloittee(wrong spelling) to the correct standard name but fails to do in case of Datsum(it was a random name!). This is where, the human in loop would come and the correct standard name for Datsum has to be manually fed into the **data.xlsx** file to improve the model/algorithm. This is how the model will be optimized as you keep feeding more standard names into the list.

**NOTE: If the standard name would be equal to the name that you have mentioned here then it would give no result or blank. Why is this because we are excluding 100% matches because in that case a wrong spelling name was matching to itself and showing up as a match. So if you see a blank/empty space then that means that it is correct and a full match. I'll attach screenshot for more clarity.**
![image](https://user-images.githubusercontent.com/21261866/128202551-1b6b5e19-1c87-4c8e-a0a7-8a6698b9fddd.png)
In this approach, you can see that JPMC is matched to the correct name, for Deloitte ToucheTohmatsu we are using the standard name so it doesn't return anything and for Datsum it's a wrong entry because we don't have it's standard name so that has to be feeded back into the **data.xlsx** file.

# References
1. [Super Fast String Matching](https://bergvca.github.io/2017/10/14/super-fast-string-matching.html)
2. [sparse_dot_topn](https://github.com/ing-bank/sparse_dot_topn)
3. [Boosting the selection of the most similar entities in large scale datasets](https://medium.com/wbaa/https-medium-com-ingwbaa-boosting-selection-of-the-most-similar-entities-in-large-scale-datasets-450b3242e618)


Reach out for any questions [![Gmail](https://img.shields.io/badge/-Gmail-c14438?style=flat&logo=Gmail&logoColor=white)](mailto:sachin93@gmail.com) 
