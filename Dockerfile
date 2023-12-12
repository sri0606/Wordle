FROM ubuntu:20.04
LABEL maintainer "Sriram Seelamneni"
LABEL description="This is a custom Docker Image inspired from Dr. Ghassemi's Web Application Course (MSU)"

ENV TZ="America/New_York"

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt update && \
    apt-get update -qq && \
    apt-get install -y mysql-server=5.7 python3-pip=20.0.2 vim=2:8.1.2269-1ubuntu5.3 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN service mysql start && \
    mysql -e "CREATE USER 'master'@'localhost' IDENTIFIED BY 'master'; \
              CREATE DATABASE db; \
              GRANT ALL PRIVILEGES ON db.* TO 'master'@'localhost';"

RUN mkdir /app
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
ENV PORT=8080
ENV FLASK_ENV=production

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
