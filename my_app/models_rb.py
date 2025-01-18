from database_rb import Base
from sqlalchemy import Column, String, Integer


class Recipe(Base):
    __tablename__ = "Recipes"
    id = Column(Integer, primary_key=True, index=True)
    recipe_name = Column(String, index=True)
    cooking_time = Column(Integer, index=True)
    views_number = Column(Integer, index=True)
    ingredients = Column(String, nullable=False)
    description = Column(String, nullable=True)
