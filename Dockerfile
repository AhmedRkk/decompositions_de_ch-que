FROM jjanzic/docker-python3-opencv

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get -y install tesseract-ocr
RUN apt-get update && apt-get install -y python3-opencv

COPY . /app
WORKDIR /app
RUN pip install opencv-python
RUN pip install pytesseract


RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
COPY app.py /app
CMD ["app.py"]