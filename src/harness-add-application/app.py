import requests
import json
import os
import logging
import ast
# import boto3
sqs = boto3.client('sqs')

url = os.environ['stagingUrl']
api_token = os.environ['api_token']
header = {"x-api-key": api_token}



def postencryptedtext(encryptedtextName, token):
    
    print("calling from function postencryptedtext ******** print all variables")
    encryptedText_Name = encryptedtextName
    encryptedText_Value = token
    print(encryptedText_Name)
    print(encryptedText_Value)
    print("test ci change")

    query = """
        mutation($secret: 
            CreateSecretInput!){
                createSecret(input : $secret) 
                    {
                         clientMutationId
                    }
            }
        """    

    variables= {
        "secret": 
            { 
                "secretType": "ENCRYPTED_TEXT", 
                "encryptedText": { 
                    "name": encryptedText_Name, 
                    "value": encryptedText_Value
                }
            }
        }

    graphql_api_create_secret = {'query': query, 'variables': variables}
    
    print("inside postencryptedtext function **  making post call")
    create_secret_response = requests.post(url=url, json=graphql_api_create_secret, headers=header)
    print(create_secret_response)
    
    print("inside postencryptedtext function ** secret status code")
    # return create_secret_response.status_code()
    #response response object
    print("return status code inside postencryptedtext *** create_secret_response.json()", create_secret_response.json())
    return create_secret_response.json()


def onboardCluster(payload_list):

    list = payload_list
    cloudProviderName =  list[0]['clusterName']
    masterUrl  =   list[0]['masterUrl']
    encryptedtextName = list[0]['serviceAccountToken']
    token = list[0]['token'] 
   
    print("calling from function onboardCluster ******** print all variables")
    print(cloudProviderName)
    print(masterUrl)
    print(encryptedtextName)
    print(token)

    secretposted = postencryptedtext(encryptedtextName, token)
    print(secretposted)
    
    MANUAL_CLUSTER_DETAILS = "MANUAL_CLUSTER_DETAILS"
    SERVICE_ACCOUNT_TOKEN="SERVICE_ACCOUNT_TOKEN"
    
    serviceAccountTokenSecretId = "hashicorpvault://Vault/harness-staging/" + encryptedtextName + "#value"
    
    query= """
        mutation {
                createSecret(input: {
                    secretType: ENCRYPTED_TEXT,
                    encryptedText: {
                    name: "GraphQL Live Demo",
                    secretManagerId: "zjiAPtICRcu9d1GWRQOHeg",
                    secretReference: "harness-staging/dev-ca-test#value"
                    }
                }) {
                    clientMutationId
                }
                }
        """

    variables = {
        "cloudProvider": {
            "cloudProviderType": "KUBERNETES_CLUSTER",
            "k8sCloudProvider": {
                "name": cloudProviderName, 
                "clusterDetailsType": MANUAL_CLUSTER_DETAILS,
                "skipValidation": 'true', 
                "manualClusterDetails": { 
                    "masterUrl": masterUrl,
                    "type": SERVICE_ACCOUNT_TOKEN, 
                    "serviceAccountToken": { 
                        "serviceAccountTokenSecretId": serviceAccountTokenSecretId
                        }
                     }
                }
            }
        }
    
    print("inside onboardCluster function ** print(variables)")
    print(variables)
    
    graphql_api_create_cloud_provider = {'query': query, 'variables': variables}
    
    print("inside onboardCluster function ** makign post call")
    create_CloudProvider_response = requests.post(url=url, json=graphql_api_create_cloud_provider, headers=header)
   
    print("inside onboardCluster function ** CloudProvider Response status code")
    print(create_CloudProvider_response.status_code)
    
    print("inside onboardCluster function *** CloudProvider Response Json code")
    return (create_CloudProvider_response.json())



def lambda_handler(event, context):
    
         for record in event['Records']: 
            
            print("Print raw record body")
            print(record["body"])
            
            rawRecordBody = record["body"]
            
            print("Print raw record body inside VAR rawRecordBody")
            print(rawRecordBody)
            print(type(rawRecordBody))
            
            record["body"] = ast.literal_eval(record["body"])
            
            recordBody = record["body"]
            
            
            print("******print ast.literal_eval converetd raw single record body *****")
            print(recordBody)
           
            print("******print TYPE of ast.literal_eval converetd raw record body******") 
            print(type(recordBody))
            
            message = recordBody["Message"]
            
            
            print("*****message******") 
            print( message)
            
            print("******message type******") 
            print(type(message))
            
            
            dictTypeMessage =  ast.literal_eval(message)
            print("SQS message")
            print(type(dictTypeMessage))
            
            print("Print message of type ")
            print(dictTypeMessage)
        
            # res = str(dictPayloadData)
            print("Pay ------load ----data")
            payload_list = dictTypeMessage["payload"]
            
            print("printing the payload data **********")
            print (payload_list)
            
            print("type of ---Payload")
            print(type(payload_list))
            
            print(payload_list[0]['clusterName'])
            print(payload_list[0]['masterUrl'])
            print(payload_list[0]['serviceAccountToken'])
            print(payload_list[0]['test'])
            
            
            onboardCluster(payload_list)
            

            print("standard queue delivers the message and we need to clean the queue after reading the message")

            sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
            )