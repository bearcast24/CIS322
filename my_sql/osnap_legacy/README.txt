This directory contains the data received from OSNAP for the data migration milestone. The data was complied from several teams within OSNAP and only a small representative sample of records has been given to us. Not all of the data is relevant for LOST, so expect to ignore some of the columns and potentially some of the files.

We need to demonstrate that we can import this data. That may require adding some missing mappings. These mappings can be done statically in your code but must be documented so that we can ask the customer to provide these mappings before they perform the production cut over to LOST in April.

The major output the customer is looking for from the data migration is a report showing all of their assets and which facility the assets are currently located at.


Files:
security_levels.csv - An ordered listing of security levels. 'u' is the lowest security level and 'z' is the highest security level.

security_compartments.csv - A listing of security compartments. The actual descriptions have been redacted but LOST will be expected to allow a comment or description for each compartment.

vendors.csv - A listing of vendors which are on the OSNAP vendor list and have open purchasing agreements.

product_list.csv - A listing of products with their associated vendor.

acquisitions.csv - A listing of items purchased.

transit.csv - Samples from the spreadsheets currently used for tracking transit requests.

convoy.csv - Samples of the current way convoys are tracked for moving assets.

DC_inventory.csv - Inventory from the DC facility

HQ_inventory.csv - Inventory from the HQ facility

MB005_inventory.csv - Inventory from the MB005 facility

NC_inventory.csv - Inventory from the National City facility

SPNV_inventory.csv - Inventory from the Sparks Nevada facility


Notes:
A security tag is composed of both a compartment and level. For example 'moon:ts' indicates that the tagged asset is in the moon compartment at the top secret level.


