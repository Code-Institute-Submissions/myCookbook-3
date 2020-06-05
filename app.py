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
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/get_shopping')
def get_shopping():
    return render_template("shoppinglist.html", shoppinglist=mongo.db.shoppinglist.find())
    
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipe_type.html", recipe=mongo.db.recipes.find())

@app.route('/breakfast')
def breakfast():
    return render_template("breakfast.html", recipe=mongo.db.recipes.find())

@app.route('/mainmeals')
def mainmeals():
    return render_template("mainmeals.html", recipe=mongo.db.recipes.find())

@app.route('/desserts')
def desserts():
    return render_template("desserts.html", recipe=mongo.db.recipes.find())

@app.route('/snacks')
def snacks():
    return render_template("snacks.html", recipe=mongo.db.recipes.find())
    
@app.route('/get_full_recipe/<recipe_id>')
def get_full_recipe(recipe_id):
    return render_template("full_recipe.html", recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)}), categories=mongo.db.categories.find())
    
@app.route('/add_item')
def add_item():
    return render_template("additem.html")
    
@app.route('/add_recipe')
def add_recipe():
    return render_template("add_recipe.html", categories=mongo.db.categories.find())
    
@app.route('/insert_item', methods=['POST'])
def insert_item():
    items = mongo.db.shoppinglist
    items.insert_one(request.form.to_dict())
    return render_template("shoppinglist.html", shoppinglist=mongo.db.shoppinglist.find())
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))
    
@app.route('/edit_item/<item_id>')
def edit_item(item_id):
    the_item = mongo.db.shoppinglist.find_one({"_id": ObjectId(item_id)})
    return render_template("edititem.html", item=the_item)
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    return render_template("edit_recipe.html", recipe=the_recipe, categories=all_categories)
    
@app.route('/delete_item/<item_id>')
def delete_item(item_id):
    mongo.db.shoppinglist.remove({'_id':ObjectId(item_id)})
    return render_template("shoppinglist.html", shoppinglist=mongo.db.shoppinglist.find())

@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    return render_template("recipe_type.html", recipe=mongo.db.recipes.find())
    
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
        'category':request.form.get('category'),
        'prep_time':request.form.get('prep_time'),
        'cook_time': request.form.get('cook_time'),
        'recipe_desc': request.form.get('recipe_desc'),
        'ingredients': request.form.get('ingredients'),
        'method': request.form.get('method'),
        'image': request.form.get('image'),
        'is_vegetarian': request.form.get('is_vegetarian')
        
    })
    return redirect(url_for('get_recipes'))
    

if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=(os.environ.get('PORT')),
            debug=True)

