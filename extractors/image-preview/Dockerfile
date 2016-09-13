FROM python:2.7
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install numpy
RUN pip install chardet 
RUN pip install tifffile
RUN apt-get -y update && apt-get install -y imagemagick
RUN mv /usr/bin/convert /usr/bin/imagemagickconvert
RUN pip install git+https://bitbucket.org/todd_n/t2-c2-pyclowder.git
ADD ./src /code
WORKDIR /code
ENV HOSTIP UNKNOWN
CMD python t2c2.image.preview.py $HOSTIP
