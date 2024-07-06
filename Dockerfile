FROM continuumio/anaconda3:4.4.0
COPY . /usr/app/
EXPOSE 8080
WORKDIR /usr/app/
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "app.py"]


