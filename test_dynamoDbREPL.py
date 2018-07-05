import unittest, time
from dynamodb import dynamoDbREPL

class TestMethods(unittest.TestCase):

    dynamoDbREPL.dynamoDbAPI.dyanamoOps.setup()
    # drop all existing tables

    def test_1_runDynamoAPI_dropTables(self):
        try:
            l_tables = dynamoDbREPL.dynamoDbAPI.run(['list'])
            #l_tables = dynamoDbREPL.dynamoDbConnect.run(['list', 'false'])
            if (l_tables != None ):
                l_tables = [dynamoDbREPL.dynamoDbAPI.run([x, 'drop']) for x in l_tables]
            print (str(l_tables) + ' dropped')
        except:
            self.fail("exception occured")

    def test_2_runDynamoAPI_listTables(self):
        try:
            print( 'list of table = \n' + str(dynamoDbREPL.dynamoDbAPI.run(['list'])))
        except:
            self.fail("exception occured")

    def test_3_runDynamoAPI_createTable(self):
        try:
            print (str(dynamoDbREPL.dynamoDbAPI.run(['table1', 'create', '2,pk,S,sk,S'])) + ' created')
        except:
            self.fail("exception occured")

    def test_4_runDynamoAPI_insertTables(self):
        try:
            print (str(dynamoDbREPL.dynamoDbAPI.run(['table1', 'insert', "pk,'1',sk,'1',col1,'val1'"])) + ' inserted values')
        except:
            self.fail("exception occured")

    def test_5_runSqlAPI_help(self):
        try:
            dynamoDbREPL.runSqlAPI('help')
        except:
            self.fail("exception occured")

    def test_6_runSqlAPI_showtables(self):
        try:
            print (dynamoDbREPL.runSqlAPI('show tables'))
        except:
            self.fail("exception occured")

    def test_7_runSqlAPI_select(self):
        try:
            print (dynamoDbREPL.runSqlAPI('select * from table1'))
        except:
            self.fail("exception occured")

    def test_8_runSqlAPI_selectwhere(self):
        try:
            print (dynamoDbREPL.runSqlAPI("select * from table1 where pk='1' and sk='1'"))
        except:
            self.fail("exception occured")

    def test_9_runSqlAPI_list(self):
        try:
            print (dynamoDbREPL.runSqlAPI('show tables'))
        except:
            self.fail("exception occured")

    def test_9_runDynamoAPI_describe(self):
        try:
            print (dynamoDbREPL.dynamoDbAPI.run(['table1' ,'describe']))
        except:
            self.fail("exception occured")

    def test_9_runSqlAPI_insert_with_keys(self):
        try:
            print (str(dynamoDbREPL.runSqlAPI("insert into table1 (pk,sk) values ('1','11')")) + ' inserted data' )
        except:
            self.fail("exception occured")
