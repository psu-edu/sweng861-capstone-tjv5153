from prometheus_client import Counter, start_http_server, Summary
from fastapi import Request
import time
import logging
from datetime import datetime

date_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

REQUEST_DURATION = Summary('request_duration_seconds', 'Time spent processing request')
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "http_status"])
RESPONSE_500_COUNT = Counter("http_response_500_total", "Total HTTP 500 responses", ["method", "endpoint"])
RESPONSE_200_COUNT = Counter("http_response_200_total", "Total HTTP 200 responses", ["method", "endpoint"])

def start_metrics_server():
    start_http_server(8000)
    logger.info("Prometheus metrics server started on port 8000")

async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    REQUEST_DURATION.observe(duration)
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path, http_status=response.status_code).inc()
    if response.status_code == 500:
        RESPONSE_500_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    elif response.status_code == 200:
        RESPONSE_200_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    logger.info(f"Request to {request.url.path} took {duration:.4f} seconds")

    return response