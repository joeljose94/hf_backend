from flask import Flask, jsonify, request
from model.model import Ingredient, RecipeIngredient, RecipeIngredientQty, create_tables, Recipe
from flask_cors import CORS
from playhouse.shortcuts import model_to_dict, dict_to_model

app = Flask(__name__)
CORS(app)
create_tables()

# error handling
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


# send 200 status ok response
def send_success(msg):
    message = {
        'status': 200,
        'message': msg
    }
    resp = jsonify(message)
    resp.status_code = 200
    return resp


# testing

@app.route("/test", methods=['GET', 'POST'])
def test_api():
    message = {
        'status': 200,
        'message': ''
    }
    if request.method == "GET":
        message['message'] = 'GET Request for ' + request.url
        resp = jsonify(message)
        resp.status_code = 200
        return resp
    elif request.method == "POST":
        message['message'] = 'Hi ' + request.json['name']
        resp = jsonify(message)
        resp.status_code = 200
        return resp


# Routes for Recipes

@app.route("/recipes", methods=['GET'])
def display_recipes():
    per_page = 10
    query = Recipe.select().paginate(1, per_page)
    data = [model_to_dict(i, backrefs=True, recurse=True) for i in query]
    return jsonify({'recipe': data, 'page': 1, 'per_page': per_page})

# returns recipe 
@app.route("/recipe/<int:r_id>", methods=['GET'])
def get_recipe(r_id):
    recipeQuery = Recipe.select().where(Recipe.recipe_id == r_id)

    if recipeQuery.exists():
        data = {'recipe': model_to_dict(
            recipeQuery.get(), backrefs=True, recurse=True)}
    else:
        return not_found()

    return jsonify(data)

@app.route("/recipe/<int:r_id>", methods=['PUT'])
def update_recipe(r_id):
    recipe = request.json
    new_recipe = dict_to_model(Recipe, recipe)
    new_recipe.save()
    # recipe_details.save()

    # remove all existing ingredients (it should be based on the old entries )
    recipeQuery = Recipe.select().where(Recipe.recipe_id == r_id)

    # cannot be based on the newly created new_recipe as it will never have the removed
    # recipies after doing dict_to_model of the new payload
    if recipeQuery.exists():
        old_recipe =  recipeQuery.get()    
    
        for recipe_ingredient in old_recipe.recipe_ingredients:
            # if recipe_ingredient.exists():
            for servingQty in recipe_ingredient.ingredient_qtys:
                # if servingQty.exists():
                servingQty.delete_instance()
            recipe_ingredient.delete_instance()

    # add new
    for recipe_ingredient in new_recipe.recipe_ingredients:
        print(recipe_ingredient.ingredient_id)
        recipeIngredient = RecipeIngredient.create(
            recipe=new_recipe, ingredient=recipe_ingredient.ingredient_id)
        for servingQty in recipe_ingredient.ingredient_qtys:
            RecipeIngredientQty.create(
                recipe_ingredient=recipeIngredient, qty=servingQty.qty, serving_amt=servingQty.serving_amt)

    msg = 'Updated Successfully'
    return send_success(msg)


@app.route("/recipe/<int:r_id>", methods=['DELETE'])
def remove_recipe(r_id):
    check_query = Recipe.select().where(Recipe.recipe_id == r_id)

    if check_query.exists():
        recipe = check_query.get()
        recipe.delete_instance()
        msg = 'Deleted Successfully'
        return send_success(msg)
    else:
        return not_found()


@app.route("/recipe/create", methods=['POST'])
def create_recipe():
    recipe = request.json
    new_recipe = dict_to_model(Recipe, recipe)
    new_recipe.save()

    for ingredient in new_recipe.recipe_ingredients:
        print(ingredient)
        ingredientUsed = Ingredient.select().where(
            Ingredient.ingredient_id == ingredient.ingredient_id).get()
        # save relation for recipe ingredient
        recipeIngredient = RecipeIngredient.create(
            recipe=new_recipe, ingredient=ingredientUsed)
        print(recipeIngredient)
        for servingQty in ingredient.ingredient_qtys:
            print(servingQty)
            RecipeIngredientQty.create(
                recipe_ingredient=recipeIngredient, qty=servingQty.qty, serving_amt=servingQty.serving_amt)

    msg = 'Inserted Successfully'
    return send_success(msg)


# Routes for Ingredients

@app.route("/ingredients", methods=['GET'])
def get_all_ingredients():
    query = Ingredient.select()
    data = [model_to_dict(i) for i in query]
    return jsonify({'ingredients': data})


if __name__ == '__main__':
    app.run(debug=False)
