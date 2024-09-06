FROM fabric8/java-centos-openjdk11-jre
ADD https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.17.0-linux-x86_64.tar.gz /tmp/elasticsearch.tar.gz


USER root
RUN tar -zxvf /tmp/elasticsearch.tar.gz -C /tmp/ && rm -rf /tmp/elasticsearch.tar.gz
RUN  adduser  elasticsearch 
RUN mv /tmp/elasticsearch-*  /opt/elasticsearch
RUN echo "network.host: 0.0.0.0" >> /opt/elasticsearch/config/elasticsearch.yml
RUN echo "discovery.type: single-node" >> /opt/elasticsearch/config/elasticsearch.yml

RUN chown -R elasticsearch:elasticsearch /opt/elasticsearch
USER elasticsearch

CMD [ "/opt/elasticsearch/bin/elasticsearch"]