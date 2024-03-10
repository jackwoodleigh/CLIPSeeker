from simple_salesforce import Salesforce, SalesforceLogin
import json
import pandas

username='woodleighj@cunning-wolf-1a2vra.com'
pwd='jack2002'
security_token='e65yTgEDlcv8q5s5rxgDzPGD'

session_id, instance = SalesforceLogin(username=username, password=pwd, security_token=security_token)
sf = Salesforce(instance=instance, session_id=session_id)
print(sf)

account = sf.account
account_metadata = account.describe()
print(account_metadata.keys())