import json
import os
import unittest
import tempfile

from app import app, init_db


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
        self.db_fd, app.config['DATABASE']=tempfile.mkstemp()
        app.config['TESTING']=True
        self.app=app.test_client()
        # app.init_db()
        init_db()
    
    def tearDown(self):
        '''Destroy blank temp database after each test.'''
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])
    
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
        assert b'No entries so far 0_o' in rv.data
    
    
    def test_login_logout(self):
        '''Test login and logout using helper functions.'''
        rv=self.login(
            app.config['USERNAME'],
            app.config['PASSWORD'],
        )
        assert b'You were logged in' in rv.data
        rv=self.logout()
        assert b'You were logged out' in rv.data
        rv=self.login(
            app.config['USERNAME'] + 'x',
            app.config['PASSWORD']
        )
        assert b'Invalid username or password :(' in rv.data
        rv=self.login(
            app.config['USERNAME'],
            app.config['PASSWORD'] + 'x'
        )
        assert b'Invalid username or password :(' in rv.data
    
    
    def test_messages(self):
        '''Ensure that a user can post messages.'''
        self.login(
            app.config['USERNAME'],
            app.config['PASSWORD']
        )
        rv=self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here!'
        ), follow_redirects=True)
        assert b'No entries so far 0_o' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here!' in rv.data
    
    
    def test_delete_message(self):
        '''Ensure the messages are being deleted.'''
        rv=self.app.get('/delete/1')
        data=json.loads((rv.data).decode('utf-8'))
        self.assertEqual(data['status'], 1)

    
if __name__=='__main__':
    unittest.main()
