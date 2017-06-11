from flask import Flask, render_template, url_for, redirect, request, flash, jsonify
app = Flask(__name__)



from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurants import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()






#REST API 

@app.route('/restaurants/JSON/')
def restaurantsJSON():
    restaurants = session.query(Restaurant).all()
    return jsonify(Restaurants=[i.serialize for i in restaurants])
 
@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])
    
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    print "did we find the restaurant? %s" % restaurant.name
   
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    for i in items:
       print "found an item %s %s" % (i.name, i.id)
   
       if i.id == menu_id:
           return jsonify(MenuItems=[i.serialize])
           
    
@app.route('/')
@app.route('/restaurants/')
def showRestaurants():

    restaurants = session.query(Restaurant).all()

    return render_template('restaurants.html', restaurants=restaurants)

                
@app.route('/restaurant/new/', methods=['GET', 'POST'])              
def newRestaurant():

    if request.method == 'POST':
        newRestaurant = Restaurant(
            name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        flash("New Restaurant Created")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')    
    

    

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id, methods=['GET', 'POST']):
    
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    
    if editedRestaurant==None:
        return "could not find this restaurant"
    
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        flash("Restaurant Successfully Edited")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editrestaurant.html', restaurant_id=restaurant_id, restaurant=editedRestaurant)
    
    
    return render_template(
        'editrestaurant.html', restaurant=restaurant)
    

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):


    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash("Restaurant Successfully Deleted")
        return redirect(url_for('showRestaurants'))
    else:
        return render_template(
            'deleterestaurant.html', restaurant=restaurant)
    

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):

    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if items == None:
        return "could not find the menu for this restaurant"
        
    return render_template(
        'menu.html', restaurant = restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])              
def newMenuItem(restaurant_id):

    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Menu Item Created!")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)    
    
    
@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])              
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    
    
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash("Menu Item Successfully Edited")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)
            

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])              
def deleteMenuItem(restaurant_id, menu_id):

    item = session.query(MenuItem).filter_by(id=menu_id).one()
    print "did we find the item? %s" % item.name
    if request.method == 'POST':
        print "method is POST"
        session.delete(item)
        session.commit()
        flash("Menu Item Successfully Deleted")
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'deletemenuitem.html', item=item)
    
    return render_template(
        'deletemenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=item)
    
if __name__ == '__main__':
    app.secret_key='todo_put_good_secret_key_here'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)