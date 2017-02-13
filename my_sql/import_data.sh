#Kyile LeBlanc

#CIS 322 HW #2

#import_data.sh


#This is hard coded for the sample files that osnap gave

#Get bash inputs
database_name = $1
database_port = $2


#Get legacy data
curl https://classes.cs.uoregon.edu//17W/cis322/files/osnap_legacy.tar.gz > osnap_legacy.tar.gz
tar -xzf osnap_legacy.tar.gz
#cd osnap_legacy


## Run the python script to insert the roles and output the role maping
python3 import_data.py $database_name $database_port
