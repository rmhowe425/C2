import unittest
from Src.Route import Route
from stem.control import Controller
'''
    Tests the functionality of the Route class.
'''
class MyTestCase(unittest.TestCase):

    '''
        Tests the functionality of the constructor for Route()
    '''
    def test_something(self):
        inst = Route()
        self.assertIsNotNone(inst.log)
        self.assertEqual(inst.c_PORT, 9051)
        self.assertEqual(inst.r_PORT, 80)
        self.assertEqual(inst.h_PORT, 8081)

    '''
        Tests the functionality of the createController method in the Route() class.
    '''
    def testCreateController(self):
        inst = Route()
        val = inst.createController()

        self.assertIsNotNone(val)
        self.assertEqual(type(val), Controller)

    '''
        Tests the functionality of the setUpService method in the Route() class.
    '''
    def SetUpService(self):
        inst = Route()
        controller = inst.createController()
        inst.setUpService(controller)





if __name__ == '__main__':
    unittest.main()
