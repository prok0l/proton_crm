FROM python:3.11
EXPOSE 8000
WORKDIR /proton_crm
COPY . /proton_crm
RUN pip install -r requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1