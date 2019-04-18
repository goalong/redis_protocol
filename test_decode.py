# encoding: utf8

from unittest import TestCase

from decode import decode_resp

class TestDecode(TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_simple_str(self):
		assert decode_resp("+OK\r\n") == "OK"
		assert decode_resp("+Test\r\n") == "Test"


	def test_error(self):
		assert decode_resp("-Error message\r\n") == "Error message"
		assert decode_resp("-ERR unknown command 'foobar'\r\n") == "ERR unknown command 'foobar'"


	def test_int(self):
		assert decode_resp(":0\r\n") == 0
		assert decode_resp(":100\r\n") == 100



	def test_bulk_str(self):
		assert decode_resp("$6\r\nfoobar\r\n") == "foobar"
		assert decode_resp("$0\r\n\r\n") == ""
		assert decode_resp("$-1\r\n") == None


	def test_array(self):
		assert decode_resp("*0\r\n") == []
		assert decode_resp("*2\r\n$3\r\nfoo\r\n$3\r\nbar\r\n") == ["foo", "bar"]
		assert decode_resp("*3\r\n$3\r\nfoo\r\n$0\r\n$3\r\nbar\r\n") == ['foo', '', 'bar']
		assert decode_resp("*-1\r\n") == None
		assert decode_resp("*2\r\n*3\r\n:1\r\n:2\r\n:3\r\n*2\r\n+Foo\r\n-Bar\r\n") == [[1,2,3], ["Foo", "Bar"]]
		assert decode_resp("*3\r\n$3\r\nfoo\r\n$-1\r\n$3\r\nbar\r\n") == ['foo', None, 'bar']
		assert decode_resp("*3\r\n$3\r\nfoo\r\n*-1\r\n$3\r\nbar\r\n") == ['foo', None, 'bar']

if __name__ == "__main__":
	TestDecode()