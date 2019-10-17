from app import app

import unittest

class BasicTestCase(unittest.TestCase):
    
    def test_index(self):
        tester=app.test_client(self)
        response=tester.get('/', content_type='text/html')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, Master Flasker!')
    
    if __name__=='__main__':
        unittest.main()
