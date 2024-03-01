# cs224n

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
