FROM python:3.6

COPY . .
RUN pip3 install -r requirements.txt && python3 setup.py build_ext --inplace

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]