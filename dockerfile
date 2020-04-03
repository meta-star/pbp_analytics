# Phishing Blocker Project - Analytics
# (c)2019 SuperSonic(https://randychen.tk).

### Select the browser you prefer
# Google Chrome
# FROM selenium/standalone-chrome:latest
# Mozilla Firefox
FROM selenium/standalone-firefox:latest
###

# PB Project Maintainer
MAINTAINER Star Inc.<star_inc@aol.com>

# Set working directory
WORKDIR /app
COPY . /app

# Initialize working environment
RUN sudo chown -R seluser:seluser ../app
RUN sudo apt-get update
RUN sudo apt-get upgrade -y
RUN sudo apt-get install -y python3.7 python3-pip
RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install --trusted-host pypi.python.org -r requirements.txt

# Expose port
EXPOSE 2020

# Disable python buffered for display
ENV PYTHONUNBUFFERED true
# Set User PATH
ENV PATH $HOME/.local/bin:$PATH

# Execute Analytics
CMD ["python3.7", "main.py"]
