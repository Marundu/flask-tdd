import json
import os
import unittest

from app import app, db


TEST_DB='test.db'


class BasicTestCase(unittest.TestCase):
    
    def test_index(self):
        '''Initial test: ensure flask was set up correctly.'''
        tester=app.test_client(self)
        response=tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
    
    def test_database(self):
        '''Initial test: ensure the database exists.'''
        tester=os.path.exists('flaskr.db')
        self.assertTrue(tester)


class FlaskrTestCase(unittest.TestCase):
    
    def setUp(self):
        '''Set up a blank test database before each test.'''
        basedir=os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING']=True
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app=app.test_client()
        db.create_all()
    
    def tearDown(self):
        '''Destroy blank temp database after each test.'''
        db.drop_all()
    
    def login(self, username, password):
        '''Login helper function.'''
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)
    
    def logout(self):
        '''Logout helper function.'''
        return self.app.get('/logout', follow_redirects=True)
    
    
    # assert functions 
    
    def test_empty_db(self):
        '''Ensure the database is blank.'''
        rv=self.app.get('/')
        self.assertIn(b'No entries so far 0_o', rv.data)
    
    
    def test_login_logout(self):
        '''Test login and logout using helper functions.'''
        rv=self.login(app.config['USERNAME'], app.config['PASSWORD'])
        self.assertIn(b'You were logged in', rv.data)
        rv=self.logout()
        self.assertIn(b'You were logged out', rv.data)
        rv=self.login(app.config['USERNAME'] + 'x', app.config['PASSWORD'])
        self.assertIn(b'Invalid username or password :(', rv.data)
        rv=self.login(app.config['USERNAME'], app.config['PASSWORD'] + 'x')
        self.assertIn(b'Invalid username or password :(', rv.data)
    
    
    def test_messages(self):
        '''Ensure that a user can post messages.'''
        self.login(app.config['USERNAME'], app.config['PASSWORD'])
        rv=self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here!'
        ), follow_redirects=True)
        self.assertNotIn(b'No entries so far 0_o', rv.data)
        self.assertIn(b'&lt;Hello&gt;', rv.data)
        self.assertIn(b'<strong>HTML</strong> allowed here!', rv.data)
    
    
    def test_delete_message(self):
        '''Ensure the messages are being deleted.'''
        rv=self.app.get('/delete/1')
        data=json.loads((rv.data)
        self.assertEqual(data['status'], 0)
        self.login(app.config['USERNAME'], app.config['PASSWORD'])
        rv=self.app.get('/delete/1')
        data=json.loads(rv.data)
        self.assertEqual(data['status'], 1)

    
if __name__=='__main__':
    unittest.main()
