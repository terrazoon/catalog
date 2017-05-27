from flask import Flask
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from restaurants import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/')
def HelloWorld(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    print "got restaurant %s" % restaurant.name
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant.id)
    output = ''
    for i in items:
        print "got an item %s" % i.name
        output += i.name
        output += '<br>'
        output += i.price
        output += '<br>'
        output += i.description
        output += '<br><br>'
    return output
    
if __name__ == '__main__':
    print "hit main"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)