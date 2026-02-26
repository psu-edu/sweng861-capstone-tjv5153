FROM python:3.13.9-slim

WORKDIR /backend

# copy the requirements.txt into container COPY <source> <destination>
COPY ./backend/requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY ./backend/ /backend/

WORKDIR /database

COPY ./database/ .

WORKDIR /backend

EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]