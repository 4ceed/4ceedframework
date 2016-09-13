FROM python:2.7
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install numpy
RUN pip install chardet 
RUN pip install tifffile
RUN pip install git+https://bitbucket.org/todd_n/t2-c2-pyclowder.git
ADD ./src /code
WORKDIR /code
ENV HOSTIP UNKNOWN
CMD python dm3_metadata_extractor.py $HOSTIP
