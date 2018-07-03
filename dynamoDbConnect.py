import boto3
import os
import logging
import sys

os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''

# NOTE: a bug in dateutil package that boto3 uses was fixed by using:        https://stackoverflow.com/a/43688152/5992714

class dyanamoOps:
    logging.basicConfig(level=logging.WARN)  # class variables
    logger = logging.getLogger(__name__)

    def __init__(self, tableName='table1'):
        self.tableName = tableName  # instance variables

    @classmethod
    def setup(cls, **kwargs):
        cls.session = boto3.session.Session(region_name=kwargs.get('region_name', 'us-west-2'),
                                            aws_access_key_id=kwargs.get('aws_access_key_id', ' '),
                                            aws_secret_access_key=kwargs.get('aws_secret_access_key', ' '))
        cls.resource = cls.session.resource('dynamodb',
                                            endpoint_url=kwargs.get('endpoint_url', 'http://localhost:8000'))
        cls.client = cls.resource.meta.client
        # other ways of creating client:
        # client = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-west-2', aws_access_key_id=' ', aws_secret_access_key=' ')
        # client = session.client('dynamodb', endpoint_url='http://localhost:8000')

    @staticmethod
    def help():
        print("""
            usage: 
                1. python dynamoDbConnect.py help|list|<tableName> [create [1|2,pk,[S|N|BOOL...],sk,[S|N|BOOL...]] | truncate | insert <pk,1,sk,1,col1,val1,col2,val2> | select [pk,<val1>[,sk,<val2>] | ]]
                2. import dynamoDbConnect
                   dynamoDbConnect.run([ 'help|list|<tableName>',[create,[1|2,pk,sk] | truncate | insert,<pk,1,sk,1,col1,val1,col2,val2> | select,[pk,<val1>[,sk,<val2>] | ]])
        """
              )

    @classmethod
    def listTables(cls):
        l_tables = cls.client.list_tables()
        cls.logger.info(" List of tables= " + " ".join(l_tables['TableNames']))
        return (l_tables['TableNames'])

    @classmethod
    def describeTables(cls, tableName=''):
        if tableName == '':
            l_tables = cls.client.list_tables()
        else:
            l_tables = {'TableNames': [tableName]}
        #
        l_dict_tables_attrName = list(
            map(lambda y: {y['Table']['TableName']: list(map(lambda z: z['AttributeName'], y['Table']['KeySchema']))},
                list(map(lambda x: cls.client.describe_table(TableName=x), l_tables['TableNames']))))
        l_dict_tables_keyType = list(
            map(lambda y: {y['Table']['TableName']: list(
                map(lambda z: z['KeyType'], y['Table']['KeySchema']))},
                list(map(lambda x: cls.client.describe_table(TableName=x), l_tables['TableNames']))))
        l_dict_tables_attrType = list(
            map(lambda y: {
                y['Table']['TableName']: list(map(lambda z: z['AttributeType'], y['Table']['AttributeDefinitions']))},
                list(map(lambda x: cls.client.describe_table(TableName=x), l_tables['TableNames']))))

        dict_tables_attrName = {}
        dict_tables_keyType = {}
        dict_tables_attrType = {}
        cls.logger.info(" List of tables with keys= " + str(l_dict_tables_attrName))
        cls.logger.info(" List of tables with keyTypes= " + str(l_dict_tables_keyType))
        cls.logger.info(" List of tables with attr= " + str(l_dict_tables_attrType))

        for subdict in l_dict_tables_attrName:
            for k, v in subdict.items():
                dict_tables_attrName[k] = v

        for subdict in l_dict_tables_keyType:
            for k, v in subdict.items():
                dict_tables_keyType[k] = v

        for subdict in l_dict_tables_attrType:
            for k, v in subdict.items():
                dict_tables_attrType[k] = v

        d_tables_describe = {}
        for k, v in dict_tables_attrName.items():
            d_tables_describe[k] = [v, dict_tables_attrType.get(k, None), dict_tables_keyType.get(k, None)]

        print(str(d_tables_describe))
        return (d_tables_describe)

    @staticmethod
    def printTables():
        # print("List of tables= " + str(dyanamoOps.listTables()))
        print("List of tables= \n" + "\n".join(dyanamoOps.listTables()))

    def createTable(self, type='2', pkName='pk', pkType='S', skName='sk', skType='S'):
        if not dyanamoOps.listTables().__contains__(self.tableName):
            try:
                self.logger.info(" Table {} creation in progress".format(self.tableName))
                if type == '1':
                    res = self.client.create_table(
                        AttributeDefinitions=[
                            {
                                'AttributeName': pkName,
                                'AttributeType': pkType
                            },
                        ],
                        TableName=self.tableName,
                        KeySchema=[
                            {
                                'AttributeName': pkName,
                                'KeyType': 'HASH'
                            },
                        ],
                        ProvisionedThroughput={
                            'ReadCapacityUnits': 123,
                            'WriteCapacityUnits': 123
                        }
                    )
                    #res.meta.client.get_waiter('table_exists').wait(TableName=self.tableName)
                elif type == '2':
                    res = self.client.create_table(
                        AttributeDefinitions=[
                            {
                                'AttributeName': pkName,
                                'AttributeType': pkType
                            },
                            {
                                'AttributeName': skName,
                                'AttributeType': skType
                            },
                        ],
                        TableName=self.tableName,
                        KeySchema=[
                            {
                                'AttributeName': pkName,
                                'KeyType': 'HASH'
                            },
                            {
                                'AttributeName': skName,
                                'KeyType': 'RANGE'
                            },
                        ],
                        ProvisionedThroughput={
                            'ReadCapacityUnits': 123,
                            'WriteCapacityUnits': 123
                        }
                    )
                    #res.meta.client.get_waiter('table_exists').wait(TableName=self.tableName)
            except:
                #self.logger.warning(" Table {} created, with dateutil error".format(self.tableName))
                self.logger.exception(" Table {} creating failed".format(self.tableName))
            finally:
                dyanamoOps.listTables()
                return
        else:
            self.logger.warn(" Table \"{}\" already exists".format(self.tableName))

    def truncateTable(self):
        if dyanamoOps.listTables().__contains__(self.tableName):
            try:
                self.logger.info(" Table {} deletion in progress".format(self.tableName))
                res = self.client.delete_table(
                    TableName=self.tableName,
                )
            except:
                #self.logger.warn(" Table {} deleted, with dateutil error".format(self.tableName))
                self.logger.exception(" Table {} deletion failed".format(self.tableName))
            finally:
                dyanamoOps.listTables()
                return
        else:
            self.logger.warn(" Table \"{}\" does not exist".format(self.tableName))

    def insertTable(self, l_data):
        table = self.resource.Table(self.tableName)
        iter_data = iter(l_data)
        kv_data = dict(zip(iter_data, iter_data))
        try:
            table.put_item(
                Item=kv_data
            )
        except:
            self.logger.exception(" Table \"{}\" exception occured while inserting data".format(self.tableName))
            exit()
        self.logger.info(" Table \"{}\" inserted".format(self.tableName))
        return

    def selectTable(self, data=''):
        table = self.resource.Table(self.tableName)
        if dyanamoOps.listTables().__contains__(self.tableName):
            if data == '':
                try:
                    res = self.client.scan(TableName=self.tableName)
                except:
                    self.logger.exception(" Table \"{}\" exception occured while selecting data".format(self.tableName))
                    sys.exit()
                #
                self.logger.info(" Table \"{}\" data selected".format(self.tableName))
                print(res['Items'])
                return res['Items']
            else:
                try:
                    iter_data = iter(data.split(','))
                    kv_data = dict(zip(iter_data, iter_data))
                    res = table.get_item(Key=kv_data)
                except:
                    self.logger.exception(" Table \"{}\" exception occured while selecting data".format(self.tableName))
                    sys.exit()
                #
                self.logger.info(" Table \"{}\" data selected".format(self.tableName))
                if (res.keys().__contains__('Item')):
                    print(res['Item'])
                    return res['Item']
                else:
                    print({})
                    return
        else:
            self.logger.exception(" Table \"{}\" does not exist".format(self.tableName))


def run(argv):
    if len(argv) >= 1:
        if len(argv) == 1:
            if argv[0] == 'list':
                dyanamoOps.printTables()
            elif argv[0] == 'help':
                dyanamoOps.help()
            else:
                dyanamoOps.logger.warning(" Incorrect paramters. Type help for usage")
        else:
            tbl = dyanamoOps(str(argv[0]))
            if len(argv) >= 2:
                if argv[1] == 'describe':
                    tbl.logger.info(" Table {} will be described now".format(tbl.tableName))
                    dyanamoOps.describeTables(tbl.tableName)
                elif argv[1] == 'create':
                    if len(argv) == 3:
                        tbl.logger.info(" Table {} creation started".format(tbl.tableName))
                        l = list(argv[2].split(','))
                        tbl.createTable(*l)
                    else:
                        tbl.logger.warn(
                            " Table {} creation started. default type selected i.e. with only partition key".format(
                                tbl.tableName))
                        tbl.createTable()
                elif argv[1] == 'truncate':
                    tbl.logger.info(" Table {} deletion started".format(tbl.tableName))
                    tbl.truncateTable()
                elif argv[1] == 'insert':
                    tbl.logger.info(" Table {} inserting data".format(tbl.tableName))
                    if len(argv) == 3:
                        tbl.insertTable((argv[2].split(',')))
                    else:
                        tbl.logger.error(
                            " Table {} cannot be inserted into, no data provided. Type help for usage>".format(
                                tbl.tableName))
                elif argv[1] == 'select':
                    tbl.logger.info(" Table {} selecting data".format(tbl.tableName))
                    if len(argv) == 3:
                        tbl.selectTable(str(argv[2]))
                    else:
                        tbl.selectTable()
                else:
                    tbl.logger.warn(
                        " Incorrect operation given for table. Type help for usage")
            else:
                tbl.logger.warn(" No operation given for table. Type help for usage")
    else:
        dyanamoOps.logger.warn(" Nothin to do. Type help for usage")


if __name__ == '__main__':
    dyanamoOps.setup()
    run(sys.argv[1:])
