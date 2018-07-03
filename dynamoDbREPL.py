import dynamoDbConnect
import sys, os


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
        - 'show tables;' to list tables
        - 'select * from <table>;' to select all items from tables
        - 'exit;' to exit
    """)

def runSql():
    sql_user_input = input('sql> ').replace(';','')
    l_sql_user_input = sql_user_input.split(' ')
    #
    if sql_user_input == 'help':
        runSqlHelp()
    elif sql_user_input == 'show tables':
        dynamoDbConnect.run(['list'])
    elif l_sql_user_input[0] == 'select' and l_sql_user_input[2] == 'from':
        parsed_text = l_sql_user_input[3] + ' select'
        dynamoDbConnect.run(parsed_text.split(' '))
    else:
        print('Unable to understand the input. Type help if unsure.')
    return sql_user_input

def run(argv):
    #setup()                                !!!!!!!!!!!!!!!!!!! uncomment before going live!
    dynamoDbConnect.dyanamoOps.setup()  #   !!!!!!!!!!!!    comment this
    user_input = ''
    if (argv == ''):
        user_input = input("""
            Enter 1 for command based input
            Enter 2 for sql based input    
        """)
    else:
        user_input =
    if user_input == '1':
        # command based api
        while(user_input != 'exit'):
            user_input = runCommand()
            #print('\n')
    elif user_input == '2':
        # sql based api
        while(user_input != 'exit'):
            user_input = runSql()
            #print('\n')
    else:
        print('No suitable input received. Exiting.')

if __name__ == '__main__':
    run(sys.argv[1:])