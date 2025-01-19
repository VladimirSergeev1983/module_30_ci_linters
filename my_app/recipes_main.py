import os
from typing import List

import schemas_rb
from models_rb import Recipe
from database_rb import engine, session as sess
from fastapi import FastAPI, HTTPException
from sqlalchemy import update
from sqlalchemy.future import select

app = FastAPI()


@app.on_event("startup")
async def startup():
    print("Starting system.")
    if not os.path.exists("recipe_book.db"):
        async with engine.begin() as conn:
            print("Creating DB tables.")
            await conn.run_sync(models_rb.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    print("Closing DB sessions")
    await sess.close()
    await engine.dispose()


@app.post("/recipes/", response_model=schemas_rb.RecipeOut)
async def create_recipes(recipe: schemas_rb.RecipeIn) -> models_rb.Recipe:
    new_recipe = Recipe(**recipe.dict())
    async with sess.begin():
        sess.add(new_recipe)
    return new_recipe


@app.get("/recipes/", response_model=List[schemas_rb.RecipeOutResponse])
async def get_recipes() -> List[Recipe]:
    r = await sess.execute(select(Recipe).order_by(Recipe.views_number.desc()))
    return r.scalars().all()


@app.get("/recipes/{idx}", response_model=schemas_rb.RecipeOutSingle)
async def get_recipes_by_id(idx: int) -> Recipe:
    cur_views = await sess.execute(select(Recipe.views_number).where(id=idx))
    views_num = cur_views.scalar_one_or_none()
    if views_num is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    new_views = views_num + 1
    await sess.execute(
        update(Recipe).filter_by(id=idx).values(views_number=new_views)
    )
    await session.commit()
    res = await sess.execute(select(Recipe).filter_by(id=idx))
    return res.scalars().first()
