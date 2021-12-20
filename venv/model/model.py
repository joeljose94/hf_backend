from peewee import *

# Connect to a Postgres database.
pg_db = PostgresqlDatabase('hf_db', user='postgres',
                           password='letmein123', host='localhost')


class BaseModel(Model):
    class Meta:
        # a base model that will use our Postgresql database
        database = pg_db


class Recipe(BaseModel):
    recipe_id = AutoField()
    name = CharField(max_length=100, index=True)
    prep_time = IntegerField(null=False)
    difficulty = CharField(default='Easy')
    utensils = CharField(null=True)
    instructions = TextField(null=True)
    nutitional_information = TextField(null=True)

    # @property
    # def serialize(self):
    #     data = {
    #         'recipe_id': self.recipe_id,
    #         'name': str(self.name).strip(),
    #         'prep_time': str(self.prep_time).strip(),
    #     }

    #     return data


class Ingredient(BaseModel):
    ingredient_id = AutoField()
    ingredient_name = CharField(max_length=100, null=False)


class RecipeIngredient(BaseModel):
    recipe_ingredient_id = AutoField()
    recipe = ForeignKeyField(Recipe, backref='recipe_ingredients')
    ingredient = ForeignKeyField(Ingredient, backref='ingredients')


class RecipeIngredientQty(BaseModel):
    recipe_ingredient_qty_id = AutoField()
    recipe_ingredient = ForeignKeyField(
        RecipeIngredient, backref='ingredient_qtys')
    qty = FloatField(null=False)
    serving_amt = IntegerField(null=False)

    # class Customer(Model):

    # class WeeklyMenu(Model):


def create_tables():
    with pg_db:
        pg_db.create_tables(
            [Recipe, Ingredient, RecipeIngredient, RecipeIngredientQty], safe=True)


if pg_db.is_closed() == True:
    pg_db.connect()
    # pg_db.close()
