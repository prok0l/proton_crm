FROM python:3.11
EXPOSE 80
WORKDIR /protom_crm
COPY requirements.txt /proton_crm
COPY . /proton_crm
CMD ["venv/Scripts/activate"]
