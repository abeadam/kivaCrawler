# Kiva Team Crawler
This is going to crawl Kiva.org for the teams a lender belongs to. This information is not avalible through their daily snapshot
The get request for the team is sent to http://api.kivaws.org/v1/lenders/{lender_name}/teams.json 
For more information refer to http://build.kiva.org/docs/data/lenders

## Setting up
This project expects the kiva daily snapshot to be in a folder in the same directory as the folder containing the kiva.js that does the crawling. 
We are expecting the kiva daily snapshot folder to have the default name of kiva_ds_json and the lenders folder inside to have the default name of lenders
To get the kiva daily snapshot use their url http://build.kiva.org/docs/data/snapshots

## Setting up Node

To see if node is installed run
'''
node -v
'''

if that commend is not intalled you will need to install node
can be done with Mac Ports and Home Brew
'''
port install nodejs
'''
'''
brew install node
'''
or you can download it from their main sites http://nodejs.org/#download

## How to run
after cloning the repo, go inside the repo folder and run
''' 
node kiva.js 
'''

as currently it only reads first json first leaders and you also need to go to localhost:5000 in the browser to trigger it to start crawling.
Those short comming will be addressed in the near future
 
