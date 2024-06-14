from fastapi import FastAPI, File, UploadFile, Request, HTTPException
from fastapi.responses import FileResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from generator_api.generation_services import read_file, create_word_array, generate_combinations, write_to_file
from generator_api.quote_of_a_day import get_the_quote, translate, find_author_in_wikipedia

templates = Jinja2Templates('templates/html')
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# Разрешаем доступ из всех источников для разработки
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def index(request: Request):
    quote, author = await get_the_quote()
    translated_quote = translate(quote)
    context = {
        "quote": translated_quote,  # Цитата, переведённая на русский язык
        "author": translate(author),  # Автор цитаты, переведённый на русский язык
        "author_wiki": translate(await find_author_in_wikipedia(author))  # Информация об авторе из википедии
    }
    return templates.TemplateResponse("index.html", {"request": request, **context})

@app.post("/api/create_kernel/")
async def create_kernel(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = read_file(content, file.filename)
        word_array = create_word_array(df)
        combinations = generate_combinations(word_array)
        result_path = write_to_file(combinations)
        return FileResponse(result_path,
                            media_type='application/octet-stream',
                            filename=result_path.split('/')[-1],
                            status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "detail": exc.detail}, status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return templates.TemplateResponse("error.html", {"request": request, "detail": str(exc)}, status_code=400)

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("error.html", {"request": request, "detail": str(exc)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
