from fastapi import FastAPI, Query
from .task_queue.connection import queue
from .task_queue.worker import process_query

app = FastAPI()


@app.get("/")
def root():
    return {"status": "Server is up and running!"}


@app.post("/chat")
def chat(query: str = Query(..., description="The user query to be processed")):
    job = queue.enqueue(process_query, query)
    return {"status": "Query enqueued for processing", "job_id": job.id}


@app.get("/result/{job_id}")
def get_result(job_id: str):
    job = queue.fetch_job(job_id=job_id)
    if job is None:
        return {"status": "Job not found"}
    if job.is_finished:
        result = job.return_value()
        return {"status": "Query processed", "result": result}
    return {"status": "Job is still processing"}
