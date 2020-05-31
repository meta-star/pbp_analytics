# Phishing Blocker Project - Analytics
# (c)2020 Star Inc.(https://starinc.xyz).

### Select the browser you prefer
# Google Chrome
# FROM selenium/standalone-chrome:latest
# Mozilla Firefox
FROM selenium/standalone-firefox:latest
###

# PB Project Maintainer
LABEL maintainer="SuperSonic<supersonic@livemail.tw>"

# Set working directory
WORKDIR /app
COPY . /app

# Initialize working environment
RUN sudo chown -R seluser:seluser ../app
RUN sudo apt-get update
RUN sudo apt-get upgrade -y
RUN sudo apt-get install -y python3.7 python3-pip libqt5core5a qt5dxcb-plugin
RUN sudo apt-get autoremove -y
RUN python3.7 -m pip install --upgrade pip
RUN python3.7 -m pip install --trusted-host pypi.python.org -r requirements.txt --no-warn-script-location

# Expose port
EXPOSE 2020

# Disable python buffered for display
ENV PYTHONUNBUFFERED true
# Set User PATH
ENV PATH $HOME/.local/bin:$PATH

# Execute Analytics
CMD ["python3.7", "main.py"]
