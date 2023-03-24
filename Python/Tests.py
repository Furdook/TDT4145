import unittest as u
from Queries import *

class test_methods(u.TestCase):
            
    def test_get_all_routes(self):
        self.assertEqual(get_all_routes('Trondheim', 'Mandag'), [(1,), (2,), (3,)])
        self.assertEqual(get_all_routes('Mo i Rana', 'Lørdag'), [(2,)])
        self.assertEqual(get_all_routes('Trondheim', 'Søndag'), [(2,)])
        self.assertEqual(get_all_routes('Mosjøen', 'Fredag'), [(1,), (2,), (3,)])
        self.assertEqual(get_all_routes('Bodø', 'Mandag'), [(1,), (2,)])
    
    
    def test_get_all_routes_between(self):
        self.assertEqual(get_all_routes_between('Trondheim', 'Mosjøen', '2023-04-04'), [[(1, 'Trondheim', '07:49', 'Mosjøen', '13:20', 'Tirsdag'),(2, 'Trondheim', '23:05', 'Mosjøen', '04:41', 'Tirsdag')],[(1, 'Trondheim', '07:49', 'Mosjøen', '13:20', 'Onsdag'),(2, 'Trondheim', '23:05', 'Mosjøen', '04:41', 'Onsdag')]])
        self.assertEqual(get_all_routes_between('Steinkjer', 'Bodø'), [(1,), (2,)])
        self.assertEqual(get_all_routes_between('Mosjøen', 'Fauske'), [(1,), (2,)])
        self.assertEqual(get_all_routes_between('Trondheim', 'Bodø'), [(1,), (2,)])
        self.assertEqual(get_all_routes_between('Mo i Rana', 'Trondheim'), [(3,)])


    def test_get_customer(self):
        self.assertEqual(get_customer('viktort@ntnu.no'),  ('viktort@ntnu.no', 'Viktor', 'Tingstad', '004702800'))
        self.assertIsNone(get_customer('ikkeEnBruker'))



    def test_get_stations_between(self):
        self.assertEqual(get_stations_between('Trondheim', 'Mosjøen'), ['Steinkjer'])
        self.assertEqual(get_stations_between('Bodø', 'Steinkjer'), ['Mosjøen', 'Mo i Rana', 'Fauske'])
        self.assertEqual(get_stations_between('Fauske', 'Mosjøen'), ['Mo i Rana'])
        self.assertEqual(get_stations_between('Trondheim', 'Bodø'), ['Steinkjer', 'Mosjøen', 'Mo i Rana', 'Fauske'])
        self.assertEqual(get_stations_between('Mo i Rana', 'Trondheim'), ['Mosjøen', 'Steinkjer'])


def test(): 
    u.main()
