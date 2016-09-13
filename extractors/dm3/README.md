This package contains 2 extractors for dm3 digital micrograph files. One (dm3_metadata_extractor.py) 
gets all available metadata tags from a dm3 files. The other (dm3_metadata_shortlist_extractor.py) only gets the 
most in demand metadata tags (subject to change based on input from lab users.) 

dm3reader_v072.py was available online and has been modified to work with with our extraction process instead of 
as a stand-alone script. New methods were added. 

In order to run the extractor, make sure that correct values are in the config file. 
 
Rabbitmq (or other event bus) and clowder should be started first. To run either extractor, do 
'sudo python *name-of-extractor* from the command line. 