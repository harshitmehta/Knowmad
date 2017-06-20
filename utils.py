from wit import Wit

access_token = "6HQAJFBASQKVJDE7AP5PX2KAAO7ZSAIZ"

client = Wit(access_token = access_token)

#message_text = "I have a private car"

def wit_response(message_text):
    resp = client.message(message_text)
    entity = None
    value = []
    

    try:
        entity = list(resp['entities'])[0]
        value = resp['entities'][entity][0]['value']
        #entity = list(resp['entities'])
        #for i in entity:
            #value.append(resp['entities'][i][0]['value'])
            #print(value)
    except:
        pass
    return (entity, value)

#resp = client.message(message_text)
#print(wit_response("I own a private car"))
