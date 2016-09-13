This extractor was extended from the ncsa.image.preview extractor. It provides an image preview
for files, including the .dm3 digital micrograph files. 

In order to run this extractor, do the following:

1. Install pyclowder using : 

pip install git+https://opensource.ncsa.illinois.edu/stash/scm/cats/pyclowder.git

2. Install imagemagickconvert and make sure that the correct path is listed in imageBinary in the config files.

3. The extractor script t2c2.image.preview.py requires no arguments. All necessary values are in the config file. 

4. To run - make sure rabbitmq (or other event bus) is running as well as clowder. Run extractor from command line 
using 'sudo python t2c2.image.preview.py' . 