FROM postgres 
ENV POSTGRES_PASSWORD mydwh
ENV POSTGRES_DB dwhdb
COPY init.sql /docker-entrypoint-initdb.d/
