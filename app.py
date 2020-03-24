import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv("MONGO_URI")
app.config["MONGO_DBNAME"] = 'myCookbook'


mongo = PyMongo(app)


@app.route('/')
@app.route('/get_shopping')
def get_shopping():
    return render_template("shoppinglist.html", shoppinglist=mongo.db.shoppinglist.find())
    
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", recipe=mongo.db.recipes.find())
    
@app.route('/add_item')
def add_item():
    return render_template("additem.html")
    
@app.route('/add_recipe')
def add_recipe():
    return render_template("addrecipe.html")
    
@app.route('/insert_item', methods=['POST'])
def insert_item():
    items = mongo.db.shoppinglist
    items.insert_one(request.form.to_dict())
    return redirect(url_for('get_shopping'))
    
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))
    
@app.route('/edit_item/<item_id>')
def edit_item(item_id):
    the_item = mongo.db.shoppinglist.find_one({"_id": ObjectId(item_id)})
    return render_template("edititem.html", item=the_item)
    
@app.route('/delete_item/<item_id>')
def delete_item(item_id):
    mongo.db.shoppinglist.remove({'_id':ObjectId(item_id)})
    return redirect(url_for('get_shopping'))
    
@app.route('/update_item/<item_id>', methods=["POST"])
def update_item(item_id):
    items = mongo.db.shoppinglist
    items.update( {'_id': ObjectId(item_id)},
    {
        'item_name':request.form.get('item_name'),
        'item_quantity':request.form.get('item_quantity'),
        'item_info': request.form.get('item_info')
    })
    return redirect(url_for('get_shopping'))


    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)

