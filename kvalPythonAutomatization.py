import requests

data = {
    "username": "admin",
    "password": "admin"
}

response = requests.post('http://127.0.0.1:58002/api/v1/ticket', json=data) #HTTP POST metode, lai iegūtu atpakaļ lietotāja atuentifikācijas marķieri

if response.status_code == 201:
    response_json = response.json()
    ServiceTicket = response_json["response"]["serviceTicket"]  #tiek saglabāts autentifikācijas marķieris mainīgajā, lai ar to var darboties arī tālāk
    print("ServiceTicket:", ServiceTicket)
    
    headers = {
        "Content-Type": "application/json",
        "x-Auth-Token": ServiceTicket
    }
    
    post_body = {
        "password": "C1sc0RoutErRIP45S",
        "username": "cisco1",
        "enablePassword": "C1sc0RoutErRIP45S",
        "description": "R1"
    }
    
    post_response = requests.post('http://127.0.0.1:58002/api/v1/global-credential/cli', headers=headers, json=post_body) #HTTP POST metode, lai ievietotu tīklas iekārtas jaunus autentfikācijas datus
    print("POST Request Status Code:", post_response.status_code)
    
    if post_response.status_code in [200, 201]:
        post_response_json = post_response.json()
        print("POST Response:", post_response_json)
        
        globalCredentialId = post_response_json["id"] #tiek saglabāts id, lai ar to var darboties tālāk
        print("Global Credential ID:", globalCredentialId)
        
        post_body_new = {
            "ipAddress": "192.168.10.1",
            "globalCredentialId": globalCredentialId
        }
        
        new_post_response = requests.post('http://127.0.0.1:58002/api/v1/network-device', headers=headers, json=post_body_new) #HTTP POST metode, lai pievienotu jaunu tīkla iekārtu kontrolierī
        print("New POST Request Status Code:", new_post_response.status_code)
        
        if new_post_response.status_code in [200, 201]:
            print("New POST Response:", new_post_response.json())
        else:
            print("Failed to post data. Response text:", new_post_response.text)
        
        put_body = {
            "password": "cisco1",
            "username": "cisco1",
            "enablePassword": "12345",
            "description": "R1",
            "id": globalCredentialId
        }
        
        put_response = requests.put('http://127.0.0.1:58002/api/v1/global-credential/cli', headers=headers, json=put_body) # HTTP PUT metode, lai varētu demonstrēt, ka ir iespēja mainīt lietotāja autentifikācijas datus
        print("PUT Request Status Code:", put_response.status_code)
        
        if put_response.status_code in [200, 201]:
            print("PUT Response:", put_response.json())
        else:
            print("Failed to update global credential. Response text:", put_response.text)
            
        get_response = requests.get('http://127.0.0.1:58002/api/v1/network-device', headers=headers) # HTTP GET metode, kura pretī nosūta visu informāciju par esošajām kontrolierī pievienotajām tīkla iekārtām.
        print("GET Request Status Code:", get_response.status_code)
        
        if get_response.status_code == 200:
            print("GET Response:", get_response.json())
        else:
            print("Failed to retrieve network devices. Response text:", get_response.text)
        
    else:
        print("Failed to create global credential. Response text:", post_response.text)
else:
    print("Failed to get service ticket. Status code:", response.status_code)
    print("Response text:", response.text)