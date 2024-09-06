FROM fabric8/java-centos-openjdk11-jre
ADD https://artifacts.elastic.co/downloads/logstash/logstash-7.17.13-linux-x86_64.tar.gz /tmp/logstash.tar.gz
#ADD logstash.tar.gz /tmp/
USER root
RUN tar -zxvf /tmp/logstash.tar.gz -C /tmp/ && rm -rf  /tmp/logstash.tar.gz
RUN  adduser  logstash 
RUN mv /tmp/logstash-*  /usr/share/logstash
#ADD pipelines.yml /usr/share/logstash/config/pipelines.yml
RUN chown -R logstash:logstash /usr/share/logstash
USER logstash
#RUN tar zxvf /tmp/elasticsearch.tar.gz -C /opt && mv /opt/elasticsearch* /opt/elasticsearch && rm -rf /tmp/elasticsearch.tar.gz
CMD [ "/usr/share/logstash/bin/logstash"]