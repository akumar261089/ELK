FROM node:19-bullseye
ADD https://artifacts.elastic.co/downloads/kibana/kibana-7.17.0-linux-x86_64.tar.gz /tmp/kibana.tar.gz
USER root
RUN tar -zxvf /tmp/kibana.tar.gz -C /tmp/  && rm -rf /tmp/kibana.tar.gz
RUN  adduser  kibana 


RUN mv /tmp/kibana-*  /usr/share/kibana &&  chown -R kibana:kibana /usr/share/kibana
USER kibana
ADD kibana.yml /usr/share/kibana/config/kibana.yml
CMD [ "/usr/share/kibana/bin/kibana"]