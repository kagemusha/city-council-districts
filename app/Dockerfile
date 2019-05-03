FROM thinkwhere/gdal-python:3.6-shippable
RUN curl -L http://download.osgeo.org/libspatialindex/spatialindex-src-1.8.5.tar.gz | tar xz
RUN cd spatialindex-src-1.8.5 && ./configure && make && make install && ldconfig
WORKDIR /app
COPY requirements.txt /app
RUN  pip install -r /app/requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["app.py"]

