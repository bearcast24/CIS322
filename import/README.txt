Import scripts:
Read .csv into the LOST databse

Usage:
bash import_data.sh <dbname> <input dir>


<dbname> :is name of the database to import the data into. 
<input dir> :is the path for the directory where the data files should be read from.


import_data.sh: Calls a Python script to insert the data into the database, and excutes those statements.
import_data.py: Python script to parse a csv files and make SQL statments to insert and excute in the database