# This code meant to be run in Jupyter Notebook.
# Please follow the steps in the report

# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import random


# In[ ]:


# File creation
with open('smalldata20.txt', 'w') as f:

    # Generate the data
    rows = set()
    while len(rows) < 20:
        row_number = random.randint(1, 10)
        column_number = random.randint(1, 10)
        while (row_number, column_number) in rows:
            # Avoid duplicates
            row_number = random.randint(1, 10)
            column_number = random.randint(1, 10)
        cell_value = round(random.uniform(-10, 10), 2)

        # Write the data to the file
        f.write('{} {} {}\n'.format(row_number, column_number, cell_value))
        rows.add((row_number, column_number))

