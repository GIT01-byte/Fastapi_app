from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import uvicorn

from pydantic import BaseModel

from demo_auth.views import demo_auth_router

app = FastAPI()

app.include_router(demo_auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
)


class BookAddScheme(BaseModel):
    title: str
    author: str


books = [
    {
        'id': 1,
        'title': 'Ассинхронность в Python',
        'author': 'Мэттью'
    },
    {
        'id': 2,
        'title': 'Ассинхронность в Java',
        'author': 'Мэттью Скарлетт'
    },
]


@app.get('/books/get_all',
        summary='Получить все книги',
        tags=['Книги📚'])
def get_books():
    return books


@app.post('/books/add_book',
        summary='Добавить книгу',
        tags=['Книги📚'])
def add_book(book: BookAddScheme):
    new_book = {
        'id': len(books) + 1,
        'title': book.title,  
        'author': book.author
    }
    for existing_book in books:
        if existing_book['title'] == new_book['title'] and existing_book['author'] == new_book['author']:
            raise HTTPException(status_code=400, detail='Книга с таким названием и автором уже существует')

    books.append(new_book)
    return {'success': True, 'message': 'Книга успешно добавлена!'}


@app.put('/books/update/{book_id}',
        summary='Обновить информацию о книге',
        tags=['Книги📚'])
def update_book(updated_book: BookAddScheme, book_id: int):
    for i, book in enumerate(books):
        if book['id'] == book_id:
            books[i]['title'] = updated_book.title
            books[i]['author'] = updated_book.author
            return {'success': True, 'message': 'Книга успешно обновлена!'}
    raise HTTPException(status_code=404, detail='Книга не найдена')


@app.delete('/books/delete_all',
            summary='Удалить все книги',
            tags=['Книги📚'])
def books_cleare():
    books.clear()
    return {'success': True, 'message': 'Книги успешно удаленны!'}

if __name__ == '__main__':
    uvicorn.run(f'{__name__}:app', reload=True, host='0.0.0.0', port=8000)
