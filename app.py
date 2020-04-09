import os
from flask import Flask, render_template, redirect, request, url_for
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from os import path
if path.exists("env.py"):
    import env

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")


mongo = PyMongo(app)


@app.route('/')
@app.route('/get_shopping')
def get_shopping():
    return render_template("shoppinglist.html", shoppinglist=mongo.db.shoppinglist.find())
    
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipe=mongo.db.recipes.find())
    
@app.route('/get_full_recipe/<recipe_id>')
def get_full_recipe(recipe_id):
    return render_template("full_recipe.html", recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}))
    
@app.route('/add_item')
def add_item():
    return render_template("additem.html")
    
@app.route('/add_recipe')
def add_recipe():
    return render_template("add_recipe.html")
    
@app.route('/insert_item', methods=['POST'])
def insert_item():
    items = mongo.db.shoppinglist
    items.insert_one(request.form.to_dict())
    return render_template("shoppinglist.html", shoppinglist=mongo.db.shoppinglist.find())
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return render_template("recipes.html", recipes=mongo.db.recipes.find())
    
@app.route('/edit_item/<item_id>')
def edit_item(item_id):
    the_item = mongo.db.shoppinglist.find_one({"_id": ObjectId(item_id)})
    return render_template("edititem.html", item=the_item)
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("edit_recipe.html", recipe=the_recipe)
    
@app.route('/delete_item/<item_id>')
def delete_item(item_id):
    mongo.db.shoppinglist.remove({'_id':ObjectId(item_id)})
    return render_template("shoppinglist.html", shoppinglist=mongo.db.shoppinglist.find())
    
@app.route('/update_item/<item_id>', methods=["POST"])
def update_item(item_id):
    items = mongo.db.shoppinglist
    items.update( {'_id': ObjectId(item_id)},
    {
        'item_name':request.form.get('item_name'),
        'item_quantity':request.form.get('item_quantity'),
        'item_info': request.form.get('item_info')
    })
    return render_template("shoppinglist.html", shoppinglist=mongo.db.shoppinglist.find())

@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),
        'prep_time':request.form.get('prep_time'),
        'cook_time': request.form.get('cook_time'),
        'recipe_desc': request.form.get('recipe_desc'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method'),
        'image': request.form.get('image'),
        'is_vegetarian': request.form.get('is_vegetarian')
        
    })
    return render_template("recipes.html", recipes=mongo.db.recipes.find())
    

if __name__ == '__main__':
    app.run(host=os.environ.get('0.0.0.0'),
            port=os.environ.get('PORT'),
            debug=True)

