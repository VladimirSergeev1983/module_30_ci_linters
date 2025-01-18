import os
from typing import List

from fastapi import FastAPI, HTTPException
from sqlalchemy import update
from sqlalchemy.future import select

import models_rb
import schemas_rb
from database_rb import engine, session

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
    await session.close()
    await engine.dispose()


@app.post("/recipes/", response_model=schemas_rb.RecipeOut)
async def recipes(recipe: schemas_rb.RecipeIn) -> models_rb.Recipe:
    new_recipe = models_rb.Recipe(**recipe.dict())
    async with session.begin():
        session.add(new_recipe)
    return new_recipe


@app.get("/recipes/", response_model=List[schemas_rb.RecipeOutResponse])
async def recipes() -> List[models_rb.Recipe]:
    res = await session.execute(
        select(models_rb.Recipe).order_by(
            models_rb.Recipe.views_number.desc(), models_rb.Recipe.cooking_time.desc()
        )
    )
    return res.scalars().all()


@app.get("/recipes/{idx}", response_model=schemas_rb.RecipeOutSingle)
async def recipes(idx: int) -> models_rb.Recipe:
    cur_views = await session.execute(
        select(models_rb.Recipe.views_number).filter_by(id=idx)
    )
    views_num = cur_views.scalar_one_or_none()
    if views_num is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    new_views = views_num + 1
    await session.execute(
        update(models_rb.Recipe).filter_by(id=idx).values(views_number=new_views)
    )
    await session.commit()
    res = await session.execute(select(models_rb.Recipe).filter_by(id=idx))
    return res.scalars().first()
