#FROM python:3.10-bookworm
#
#WORKDIR /app
#
#COPY . .
#
#RUN apt-get update && apt-get install -y libx11-6 libxext-dev libxrender-dev libxinerama-dev libxi-dev libxrandr-dev libxcursor-dev libxtst-dev tk-dev && pip install rm -rf /var/lib/apt/lists/*
#
#CMD ["python", "Gra.py"]