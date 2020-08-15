FROM python:3.8
WORKDIR /app
RUN git clone https://github.com/lastlegion/StarWars.git
WORKDIR /app/StarWars
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python", "main.py"]

