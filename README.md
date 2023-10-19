# mega-monke
This repository pulls the wallet addresses of MonkeDAO members who qualify for the Mega Monke role daily at 0:00 UTC. A MonkeDAO member qualifies for Mega Monke status by holding either 5 gen2 monkes or 50 gen3 monkes. 

## Files Included
Main.py contains the logic that grabs the wallet addresses. Each day, new addresses are added to the mega_monke_stats.csv file as a new row. 

The mega_monke_stats.csv includes the following columns: 

date: The date & time the API call was made in UTC\
gen_2_mega_monkes: An array containing all wallet addresses that hold 5 or more gen2 monkes.\
gen_3_mega_monkes: An array containing all wallet addresses that hold 50 or more gen3 monkes.\
all_mega_monkes: An array that contains all wallet addresses that qualify for the mega monke role, regardless if they hold 5 gen2 or 50 gen3 monkes. This array has duplicate addresses removed.\
double_mega_monkes: An array that contains all wallet addresses that hold both 5 gen2 monkes and 50 gen3 monkes. Absolute legends.\
total_mega_monkes: A count of the wallet addresses contained within all_mega_monkes.

## Dependencies
The job is dependent on the Solscan API. While the pro version is not publicly available, it can be easily accessed via devtools by looking at the fetch/XHR tab.  
