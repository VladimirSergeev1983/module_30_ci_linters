from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException
from sqlalchemy import update
from sqlalchemy.future import select

from .database_rb import Base, engine
from .database_rb import session as sess
from .models_rb import Recipe
from .schemas_rb import RecipeIn, RecipeOut, RecipeOutResponse, RecipeOutSingle


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("База готова")
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    print("База очищена")


app = FastAPI(lifespan=lifespan)


@app.post("/recipes/", response_model=RecipeOut)
async def create_recipes(recipe: RecipeIn) -> Recipe:
    new_recipe = Recipe(**recipe.model_dump())
    async with sess.begin():
        sess.add(new_recipe)
    return new_recipe


@app.get("/recipes/", response_model=List[RecipeOutResponse])
async def get_recipes() -> List[Recipe]:
    r = await sess.execute(select(Recipe).order_by(Recipe.views_number.desc()))
    return r.scalars().all()


@app.get("/recipes/{idx}", response_model=RecipeOutSingle)
async def get_recipes_by_id(idx: int) -> Recipe:
    my_view = await sess.execute(select(Recipe.views_number).filter_by(id=idx))
    views_num = my_view.scalar_one_or_none()
    if views_num is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    new_views = views_num + 1
    query = update(Recipe).filter_by(id=idx).values(views_number=new_views)
    await sess.execute(query)
    await sess.commit()
    res = await sess.execute(select(Recipe).filter_by(id=idx))
    return res.scalars().first()
