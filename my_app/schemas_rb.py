from typing import Optional

from pydantic import BaseModel, Field


class BaseRecipe(BaseModel):
    recipe_name: str = Field(
        ...,
        title="Title of the recipe",
        min_length=2,
        max_length=50,
        description="Recipe name should be from 2 to 50 chars",
    )
    cooking_time: int = Field(
        ...,
        title="Cooking time",
        gt=0,
        description="The cooking time should be greater than 0",
    )
    ingredients: str = Field(..., title="List of ingredients")
    description: Optional[str] = Field(..., title="Recipe desc")


class RecipeIn(BaseRecipe):
    views_number: int = Field(default=0, title="Recipe view count")


class RecipeOut(BaseRecipe):
    # id: int

    class Config:
        from_attributes = True


class RecipeOutSingle(BaseRecipe):
    ...

    class Config:
        from_attributes = True


class RecipeOutResponse(BaseRecipe):
    views_number: int
    ingredients: str = Field(exclude=True)
    description: Optional[str] = Field(..., exclude=True)

    class Config:
        from_attributes = True
