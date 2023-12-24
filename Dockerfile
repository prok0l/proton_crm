FROM python:3.11

COPY . /proton_crm
WORKDIR /proton_crm
EXPOSE 8000
RUN pip install -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1