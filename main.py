from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from database import database, Recipe
from schemas import RecipeCreate, Recipe as RecipeSchema
from typing import List
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def read_root():
    return {
        "message": "Welcome to the Culinary Book API! Use /recipes to access the recipes."
    }


@app.get("/recipes", response_model=List[RecipeSchema])
async def get_recipes():
    query = Recipe.__table__.select().order_by(Recipe.views.desc(), Recipe.cooking_time)
    return await database.fetch_all(query)


@app.get("/recipes/{recipe_id}", response_model=RecipeSchema)
async def get_recipe(recipe_id: int):
    query = Recipe.__table__.select().where(Recipe.id == recipe_id)
    recipe = await database.fetch_one(query)

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    update_query = (
        Recipe.__table__.update()
        .where(Recipe.id == recipe_id)
        .values(views=recipe["views"] + 1)
    )
    await database.execute(update_query)

    return recipe


@app.post("/recipes", response_model=RecipeSchema)
async def create_recipe(recipe: RecipeCreate):
    query = Recipe.__table__.insert().values(
        title=recipe.title,
        views=recipe.views,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients,
        description=recipe.description,
    )

    recipe_id = await database.execute(query)

    return {**recipe.dict(), "id": recipe_id}
