from fastapi import FastAPI, Query
from .worker import process_query
from .connection import redis_queue as queue

app = FastAPI()


@app.post("/query")
def query_policy_bot(
    query: str = Query(..., description="The user query to be processed")
):
    job = queue.enqueue(process_query, query)
    print(f"Received query: {query}")
    return {"status": "Query received", "Job ID": job.id}


@app.get("/status/{job_id}")
def check_status(job_id: str):
    job = queue.fetch_job(job_id)
    if job is None:
        return {"status": "Job not found"}
    return {"status": job.get_status(), "result": job.result}
