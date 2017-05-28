from flask import Flask, render_template, url_for, redirect, request
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurants import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)    
    
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, MenuID):
    editedItem = session.query(MenuItem).filter_by(id=MenuID).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, MenuID=MenuID, item=editedItem)

    
@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/delete',
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, MenuID):
    print "hit delete menu item for restaurant id=%s menuID=%s" % (restaurant_id, MenuID)
    item = session.query(MenuItem).filter_by(id=MenuID).one()
    print "did we find the item? %s" % item.name
    if request.method == 'POST':
        print "method is POST"
        session.delete(item)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'deletemenuitem.html', item=item)
    

    
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    print "got restaurant %s" % restaurant.name
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    return render_template('menu.html', restaurant = restaurant, items = items)
    
    
if __name__ == '__main__':
    print "hit main"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)