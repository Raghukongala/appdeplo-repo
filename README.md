# Calculator App

A simple REST API calculator built with Flask.

## Endpoints

- `POST /calculate` — performs calculation
- `GET /health` — health check

## Request Body

```json
{
  "a": 10,
  "b": 5,
  "operator": "+"
}
```

Supported operators: `+`, `-`, `*`, `/`

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

## Run with Docker

```bash
docker build -t calculator-app .
docker run -p 5000:5000 calculator-app
```
