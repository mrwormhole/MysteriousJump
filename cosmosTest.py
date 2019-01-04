import azure.cosmos.cosmos_client as cosmos_client

class AzureIsTheBest:
    def __init__(self):
        self.config = {
            'ENDPOINT': 'WHAT-ARE-YOU-LOOKING-AT???MY CREDIT CARD??',
            'PRIMARYKEY': 'WHAT-ARE-YOU-LOOKING-AT???MY CREDIT CARD??',
            'DATABASE': 'HighScoreDatabase',
            'CONTAINER': 'HighScoreContainer'
        }
        options = {
            'offerThroughput': 400 #must be between 400[INCLUSIVE] and 10000[INCLUSIVE]
        }
        container_definition = {
            'id': self.config['CONTAINER']
        }

        # Initialize the Cosmos client
        self.client = cosmos_client.CosmosClient(url_connection=self.config['ENDPOINT'], auth={
            'masterKey': self.config['PRIMARYKEY']})

        # !! CONFLICTS MIGHT OCCUR WITH DB AND CON !! BE WARNED THIS IS A CURSED REALM OF WINDOWS

        #self.db = self.client.CreateDatabase({ 'id': self.config['DATABASE'] })
        # print("db: " + str(self.db))
        self.db = {'id': 'HighScoreDatabase', '_rid': '3WcMAA==', '_self': 'dbs/3WcMAA==/', '_etag': '"00008701-0000-0000-0000-5c17324f0000"', '_colls': 'colls/', '_users': 'users/', '_ts': 1545024079}

        #self.container = self.client.CreateContainer(self.db['_self'], container_definition, options)
        #print("con: " + str(self.container))
        self.container = {'id': 'HighScoreContainer', 'indexingPolicy': {'indexingMode': 'consistent', 'automatic': True, 'includedPaths': [{'path': '/*', 'indexes': [{'kind': 'Range', 'dataType': 'Number', 'precision': -1}, {'kind': 'Hash', 'dataType': 'String', 'precision': 3}]}], 'excludedPaths': []}, '_rid': '3WcMALwdAY4=', '_ts': 1545024080, '_self': 'dbs/3WcMAA==/colls/3WcMALwdAY4=/', '_etag': '"00008901-0000-0000-0000-5c1732500000"', '_docs': 'docs/', '_sprocs': 'sprocs/', '_triggers': 'triggers/', '_udfs': 'udfs/', '_conflicts': 'conflicts/'}

    def getTop100(self):
        options = {}
        options['enableCrossPartitionQuery'] = False
        options['maxItemCount'] = 100
        query = {'query': 'SELECT * FROM server s'}

        results = self.client.QueryItems(self.container['_self'], query, options)

        for result in results:
            print(result['message'])


    def pushData(self,username,highscore):
        # ITEM ID PLAY AN IMPORTANT ROLE TO GET RID OF ERRORS.
        data = self.client.CreateItem(self.container['_self'], {
            "username": str(username),
            "highscore": str(highscore),
            "message" : str(username) + " got " + str(highscore)
        })

        # self.removeDuplicates(username) CANCELLED DUE TO SECURITY

        self.getTop100()

    '''def removeDuplicates(self,username):
        #https://stackoverflow.com/questions/46878227/cosmos-db-delete-document-with-python?noredirect=1&lq=1 AT LEAST WE TRIED FRIEND
        #https: // docs.microsoft.com / en - us / rest / api / cosmos - db / delete - a - document
        #CURSED REALM OF WINDOWS doesn't support deleting on cosmos db

        noDupQuery = {'query': 'SELECT * FROM server s WHERE s.username = \'' + username + '\' '}
        res = self.client.QueryItems(self.container['_self'], noDupQuery)
      
        for item in iter(res):
            #print(item['message'])
            self.client.DeleteItem("https://test1611.documents.azure.com/dbs/HighScoreDatabase/colls/HighScoreContainer/docs/" + str(item['id'],options={})

        self.client.DeleteItem(
            "https://test1611.documents.azure.com/dbs/HighScoreDatabase/colls/HighScoreContainer/docs/'Joker'")
    '''
    '''def quickTestQuery(self):
            options = {}
            options['enableCrossPartitionQuery'] = True
            options['maxItemCount'] = 10
            query = {'query': 'SELECT * FROM server s'}
            result_iterable = self.client.QueryItems(self.container['_self'], query, options)
            for item in iter(result_iterable):
                #print(item['id'])
                print("https://test1611.documents.azure.com/dbs/HighScoreDatabase/colls/HighScoreContainer/docs/" + "\"" + item['id'] + "\"")
                #self.client.DeleteItem("https://test1611.documents.azure.com/dbs/HighScoreDatabase/colls/HighScoreContainer/docs/" + "\"" + item['id'] + "\"",options )
    '''



