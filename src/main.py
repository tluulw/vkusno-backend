from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.categories.router import router as categories_router
from src.items.router import router as items_router
from src.items_sizes.router import router as items_sizes_router
from src.items_types.router import router as items_types_router
from src.types.router import router as types_router
from src.invoice.router import router as invoice_router

app = FastAPI(
    title='Vkusno'
)

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(items_router)
app.include_router(types_router)
app.include_router(categories_router)
app.include_router(items_types_router)
app.include_router(items_sizes_router)
app.include_router(invoice_router)
