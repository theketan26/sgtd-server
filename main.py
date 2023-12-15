from fastapi import FastAPI

from modules.setup.setup import App


app = FastAPI()
end = App()


@app.get('/')
async def root():
    return {
        'message': 'This is working'
    }
