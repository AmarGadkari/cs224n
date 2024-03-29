# cs224n

Project Setup:
Folder Id:

1. Make sure to upload the 224n Project folder into your home Google Drive
2. To get folder_id, right click the 224n folder and click "share".
3. Click "copy link".
4. Example of link: https://drive.google.com/drive/folders/1FwqVD1UvjaoSC8IksUBhVkPzPQy75iTg?usp=drive_link 5. The folder id is the series of characters between "folders/" and "?usp=drive_link". Copy this id and paste it into the folder_id for and edit the file_folder path to your corresponding path.

Overall progress:

Added support for -

1. Introduce major error in all 3 input fileds - description, vendor, and comment.
2. Model is failing to learn when vendor and comment doesn't have error, but description has errors.
3. Trying to understand and experiment with techniques to fix issue (#2) above
4. We also ability to do basic carbon emission calculations e.g. cost_usd \* emission factor per given NAICS Title that is matched based on description+vendor+comment

Business activity data generation prompts:

You are the sustainability related business activity data expert. You maintain that data for the large hospital. Generate domain specific business activity description, cost, vendor, comment, 2017 NAICS Title. All this data is used for carbon emission calculations for this large hospital. You are responsible for this entire operation.

The goal of this data generation is to train a model. Later that model is used to predict correct '2017 NAICS Title' for particular business activity details including business activity description, cost, vendor, and comment. Then from EPA database based on '2017 NAICS Title' right emission factor is picked up to compute co2e emitted by particular business activity.

Here are some of the specifics for this data:

1. description of business activity itself. This is what sourcing team would use if they proceure various material for hospital, just as an example. There may be lot of business activities that are possible for a given '2017 NAICS Title'. My ask is to generate 10 unique business activity descriptions for each of the title.
2. vendor name - there is some part of vendor name that will help identify correct '2017 NAICS Title'. There is some part of the name that is going to be irrelevent. E.g. vendor name 'Nirvana Software Corporation' tells us Nirvana is just a name and irrelevent for mapping, but 'software corporation' tells they are the software vendor. Same thing for 'delightful dental chair maker' where delightful is irrelevant part of the vendor name and they are dental chair maker is a clue LLM would eventually pick up on. I want you to seed these clues in the data now, so we can educate LLM on these details later.
3. Comments - are comments from real world business systems would have. Similar to first two, in comments you should add clues for LLM to pick up on for picking the correct '2017 NAICS Title'.

I want you to generate script to generate this high quality business activity data for following '2027 NAICS Title's:
Support Activities for Metal Mining
Support Activities for Nonmetallic Minerals (except Fuels) Mining
Natural Gas Distribution
Water Supply and Irrigation Systems
Sewage Treatment Facilities
Steam and Air-Conditioning Supply
New Single-Family Housing Construction (except For-Sale Builders)

generate above datastructure naics_info for following NAICS Titles. It should have 10 business activities, 5 vendors for each activity, and 3 comments for each activity.

- Timber Tract Operations
