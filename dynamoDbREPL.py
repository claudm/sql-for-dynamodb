from dynamodb import dynamoDbConnect
import sys, os, logging

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)


def setup():
    print('## Enter values or simply press enter to use default values ##')
    region_name = {'region_name': input('Enter region_name ')}
    aws_access_key_id = {'aws_access_key_id': input('Enter aws_access_key_id ')}
    aws_secret_access_key = {'aws_secret_access_key': input('Enter aws_secret_access_key ')}
    endpoint_url = {'endpoint_url': input('Enter endpoint_url ')}
    dict_kwargs = {**region_name, **aws_access_key_id, **aws_access_key_id, **endpoint_url}
    dict_nonEmpty_kwargs = {k:v for k,v in dict_kwargs.items() if v != ''}
    dynamoDbConnect.dyanamoOps.setup(**dict_nonEmpty_kwargs)
    os.system('cls')
    #os.system('clear')


def runCommand():
    user_input = input('Type command [or help or exit] here \n')
    if user_input != 'exit':
        dynamoDbConnect.run(user_input.split(' '))
    return user_input


def runSqlHelp():
    print("""
        - to list tables
                'show tables;' to list tables
        - to select all items from tables
                'select * from <table>;'
                'select * from <table> where k1=1 and k2 = 2'
        - to exit
                'exit;' 
        - to view help
                'help;'
    """)


def runSqlAPI(sql_api_input):
    """
    Used to take input from the API and call runSql
    """
    l_sql_api_input = sql_api_input.split(' ')
    runSql(l_sql_api_input)


def runSqlREPL():
    """
    Used to take input from the user on the sql> prompt and call runSql
    """
    sql_user_input = input('sql> ').replace(';', '')
    l_sql_user_input = sql_user_input.split(' ')
    runSql(l_sql_user_input)
    return (sql_user_input)


def runSql(l_sql_user_input=[]):
    if l_sql_user_input.__contains__('help'):   # help
        runSqlHelp()
    elif l_sql_user_input[0] == 'show' and l_sql_user_input[1] == 'tables': # show tables
        dynamoDbConnect.run(['list'])
    elif l_sql_user_input[0] == 'select' and l_sql_user_input[2] == 'from':
        l_parsed_text = []
        if len(l_sql_user_input) == 4 and l_sql_user_input[1] == '*':   # select * from table1
            l_parsed_text = [l_sql_user_input[3], 'select']
        else:                                                           # select * from table1 where a=1 and b=2
            predicates = ''.join(l_sql_user_input[5:]).replace(' ','')               # a=1andb=2
            parsed_predicates = predicates.replace('=', ',').replace('and', ',')            # a,1,b,2
            l_parsed_text = [l_sql_user_input[3], 'select', parsed_predicates]
        try:
            #print (parsed_text.split(' '))
            #dynamoDbConnect.run(parsed_text.split(' '))
            dynamoDbConnect.run(l_parsed_text)
        except:
            logger.exception(" Unable to understand input. Type help if unsure.")
    else:
        print('Unable to understand the input. Type help if unsure.')


def run(argv):
    #setup()                                !!!!!!!!!!!!!!!!!!! uncomment before going live!
    dynamoDbConnect.dyanamoOps.setup()  #   !!!!!!!!!!!!    comment this
    user_input = ''
    if argv == '':
        user_input = input("""
            Enter 1 for command based input
            Enter 2 for sql based input    
        """)
    else:
        user_input = '2'
    if user_input == '1':
        # command based api
        while user_input != 'exit':
            user_input = runCommand()
    elif user_input == '2':
        # sql based api
        while user_input != 'exit':
            user_input = runSqlREPL()
    else:
        print('No suitable input received. Exiting.')


if __name__ == '__main__':
    run(sys.argv[1:])