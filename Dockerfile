FROM kbase/kbase:sdkbase.latest
MAINTAINER KBase Developer
# -----------------------------------------

# Insert apt-get instructions here to install
# any required dependencies for your module.

RUN sudo apt-get install python-dev libffi-dev libssl-dev
RUN pip install cffi --upgrade
RUN pip install pyopenssl --upgrade
RUN pip install ndg-httpsclient --upgrade
RUN pip install pyasn1 --upgrade
RUN pip install requests --upgrade && \
    pip install 'requests[security]' --upgrade
RUN apt-get install -y python-coverage
RUN pip install ndg-httpsclient==0.4.2
# -----------------------------------------

COPY ./ /kb/module
RUN mkdir -p /kb/module/work
RUN chmod -R a+rw /kb/module

WORKDIR /kb/module

RUN make all

ENTRYPOINT [ "./scripts/entrypoint.sh" ]

CMD [ ]
