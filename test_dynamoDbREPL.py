import unittest
from dynamodb import dynamoDbREPL

class TestMethods(unittest.TestCase):
    dynamoDbREPL.dynamoDbConnect.dyanamoOps.setup()
    def test_runSqlAPI_help(self):
        try:
            dynamoDbREPL.runSqlAPI('help')
        except:
            self.fail("exception occured")

    def test_runSqlAPI_showtables(self):
        try:
            dynamoDbREPL.runSqlAPI('show tables')
        except:
            self.fail("exception occured")

    def test_runSqlAPI_select(self):
        try:
            dynamoDbREPL.runSqlAPI('select * from table1')
        except:
            self.fail("exception occured")

    def test_runSqlAPI_selectwhere(self):
        try:
            dynamoDbREPL.runSqlAPI('select * from table1 where pkcol =2')
        except:
            self.fail("exception occured")