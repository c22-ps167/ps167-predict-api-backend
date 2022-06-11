FROM python:slim-buster as compiler

WORKDIR /app

ENV VIRTUAL_ENV=env
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies:
COPY . .
RUN pip install -Ur requirements.txt

# Run the application:
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]