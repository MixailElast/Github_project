from pydantic import BaseModel, ConfigDict


class RecipeBase(BaseModel):
    title: str
    views: int = 0
    cooking_time: int
    ingredients: str
    description: str


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
