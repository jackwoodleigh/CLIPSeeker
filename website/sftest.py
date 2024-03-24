from simple_salesforce import Salesforce, SalesforceLogin
import pandas as pd
from werkzeug.security import generate_password_hash, check_password_hash

username='woodleighj@cunning-wolf-1a2vra.com'
pwd='jack2002'
security_token='e65yTgEDlcv8q5s5rxgDzPGD'

session_id, instance = SalesforceLogin(username=username, password=pwd, security_token=security_token)
sf = Salesforce(instance=instance, session_id=session_id)
print(sf)

account = sf.account
account_metadata = account.describe()

email = 'woodleighj3@wit.edu'
data = sf.query_all("SELECT Email__c FROM CLIPAccount__c WHERE Email__c = '{}'".format(email))

print(data['records'])



'''
#sf.CLIPAccount__c.create({'Email__c': 'woodleighj@wit.edu', 'FirstName__c': 'Jack', 'LastName__c': 'Woodleigh', 'Password__c': '123'})
id=''
data = sf.query_all("SELECT Id, Email__c, FirstName__c, LastName__c, Password__c FROM CLIPAccount__c")
df = pd.DataFrame(data['records']).loc[0]
print(df['Password__c'])

password = "123"
print(df['Password__c'])
print(generate_password_hash("123"))
print(check_password_hash(df['Password__c'], password))

'''





# NOTES

#print(account_metadata.keys())
#data = sf.query("SELECT Id, Email FROM Contact")

#df = pd.DataFrame(data['records']).drop(['attributes'],axis=1)
'''
mdapi = sf.mdapi
custom_object = mdapi.CustomObject(
    fullName = "CustomObjectC__c",
    label = "Custom Object C",
    pluralLabel = "Custom Objects C",
    nameField = mdapi.CustomField(
        label = "Name",
        type = mdapi.FieldType("Text")
    ),
    deploymentStatus = mdapi.DeploymentStatus("Deployed"),
    sharingModel = mdapi.SharingModel("Read")
)


#mdapi.CustomObject.create(custom_object)
describe_response = mdapi.CustomObject.describe()
custom_object = mdapi.CustomObject.read("CustomObject__c")
custom_object.sharingModel = mdapi.SharingModel("ReadWrite")
mdapi.CustomObject.update(custom_object)
mdapi.CustomObject.rename("CustomObject__c", "CustomObject2__c")
mdapi.CustomObject.delete("CustomObject2__c")

query = mdapi.ListMetadataQuery(type='CustomObjectC__c')
query_response = mdapi.list_metadata(query)
print(query_response)

#print(account_metadata.keys())

sf.CustomObjectC__c.create({'Name': 'Test Object'})

data = sf.query("SELECT Name FROM CustomObjectC__c")
df = pd.DataFrame(data['records'])
print(df)
'''

