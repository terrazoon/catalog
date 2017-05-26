from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi


import sys

from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from datetime import datetime, date, timedelta

from sqlalchemy.orm import sessionmaker
Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    
    
engine = create_engine('sqlite:///restaurantmenu.db')
Session = sessionmaker(bind=engine)
session = Session()

currentRestaurant = ""
                
class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
				
                output = ""
                output += "<html><body>Hello!"
                output += "<form method='post' enctype='multipart/form-data' action='/hello'>"
                output += "<h2>What would you like me to say?</h2><input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form></body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, "File not found")
        try:
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()
				
                output = ""
                output += "<html><body>&#161Hola  <a href='/hello'>Back to Hello</a>"
                output += "<form method='post' enctype='multipart/form-data' action='/hello'>"
                output += "<h2>What would you like me to say?</h2><input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form></body></html>"
                
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, "File not found")
        
        try:
            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text-html')
                    self.end_headers()
                    output = "<html><body><h1>"
                    output += myRestaurantQuery.name
                    output += "</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
                    output += "<input name='newRestaurantName' type='text' placeholder='%s'>" % myRestaurantQuery.name
                    output += "<input type='submit' value='Rename'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    
                    print "<BR><BR><BR> created rename form, etc"
                    return
            
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-Type', 'text-html')
                    self.end_headers()
                    output = "<html><body><h1> Are you sure you want to delete "
                    output += myRestaurantQuery.name
                    output += "?</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
                    output += "<input name='newRestaurantName' type='text' placeholder='%s'>" % myRestaurantQuery.name
                    output += "<input type='submit' value='Delete'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    
                    print "<BR><BR><BR> created rename form, etc"
                    return
                        
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = "<html><body><a href='/restaurants/new'>Add a Restaurant</a>"
                
                output += "<h2>Restaurants</h2><BR><BR>"
                
                for restaurant in session.query(Restaurant):
                    output += "<BR><BR>"
                    output += restaurant.name
                    output += "<BR>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a><BR>" % restaurant.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a><BR>" % restaurant.id 
                output += "</body></html>"
                
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, "File not found")
                
        
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1> Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new' >"
                output += "<input name='newRestaurantName' type='text' placeholder = 'New Restaurant Name' >"
                output += "<input type='submit' value='Create'>"
                output += "</body></html>"

                
                
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, "File not found")
            
    def do_POST(self):
        
        try:
        
            if self.path.endswith("/edit"):
                print "<BR><BR>Hit do_POST"
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-Type'))
                if ctype=='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    print "<BR><BR>found new restaurant name %s" % messagecontent[0]
                    restaurantIDPath = self.path.split("/")[2]
                    print "<BR><BR>found restaurant id %s" % restaurantIDPath
                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()
                        print "<BR><BR>should have committed to the db here"
                        self.send_response(301)
                        print "send response 301"
                    
                        self.send_header('Content-Type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
            
            
            if self.path.endswith("/delete"):
                print "<BR><BR>Hit do_POST"
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-Type'))
                if ctype=='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    print "<BR><BR>found new restaurant name %s" % messagecontent[0]
                    restaurantIDPath = self.path.split("/")[2]
                    print "<BR><BR>found restaurant id %s" % restaurantIDPath
                    myRestaurantQuery = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                    if myRestaurantQuery != []:
                        session.delete(myRestaurantQuery)
                        session.commit()
                        print "<BR><BR>should have committed to the db here"
                        self.send_response(301)
                        print "send response 301"
                    
                        self.send_header('Content-Type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
        
            if self.path.endswith("/restaurants/new"):
                print "self.path=%s" % self.path
                ctype, pdict = cgi.parse_header(self.headers.getheader('Content-Type'))
                if ctype=='multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    print "got the new restaurant name %s" % messagecontent[0]
                    newRestaurant = Restaurant(name = messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()
                    print "committed to db"
                    
                    self.send_response(301)
                    print "send response 301"
                    
                    self.send_header('Content-Type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    print "should be returning here to /restaurants"
                    return
            
            """
            ctype, pdict = cgi.parse_header(self.headers.getheader('Content-Type'))
            if ctype=='multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                output = "<html><body>"
                output += "<h2>Okay, how about this?</h2>"
                output += "<h1>%s</h1" % messagecontent[0]
                output += "<form method='post' enctype='multipart/form-data' action='/hello'>"
                output += "<h2>What would you like me to say?</h2><input name='message' type='text'>"
                output += "<input type='submit' value='Submit'></form></body></html>"
                self.wfile.write(output)
                print output
                return
            """    
        except:        
			pass
	
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Webserver running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, shutting down server ..."
        server.socket.close()
	



if __name__ == '__main__':
    main()