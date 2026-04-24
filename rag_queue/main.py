import uvicorn
from .server import app

from dotenv import load_dotenv

load_dotenv()


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


main()
