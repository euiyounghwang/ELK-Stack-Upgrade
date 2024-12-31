
import requests
from requests.auth import HTTPBasicAuth
import json
from elasticsearch import Elasticsearch, exceptions
import os 
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")


''' pip install python-dotenv'''
load_dotenv() # will search for .env file in local folder and load variables 

INDEX = "my-index-000001"

def elasticsearch_es():
    '''
    $ python ./request-test.py
    {
    "name": "test-es8-node#1",
    "cluster_name": "test-es8-node#1-es8-dev",
    "cluster_uuid": "Rs0Ec26mQSK83RIo52il5g",
    "version": {
        "number": "8.12.2",
        "build_flavor": "default",
        "build_type": "tar",
        "build_hash": "48a287ab9497e852de30327444b0809e55d46466",
        "build_date": "2024-02-19T10:04:32.774273190Z",
        "build_snapshot": false,
        "lucene_version": "9.9.2",
        "minimum_wire_compatibility_version": "7.17.0",
        "minimum_index_compatibility_version": "7.0.0"
    },
    "tagline": "You Know, for Search"
    }
    '''
    header =  {
            'Content-type': 'application/json', 
            'Authorization' : '{}'.format(os.getenv('BASIC_AUTH')),
            'Connection': 'close'
    }
    es_client = Elasticsearch(hosts=os.getenv("ES_HOST"),
                              headers=header,
                            #   http_auth=('test', 'test'),
                              verify_certs=False,
                              max_retries=0,
                              timeout=5)
    print(json.dumps(es_client.cluster.health(), indent=2))
    


def request_es():
    '''
    $ python ./request-test.py
    {
    "name": "test-es8-node#1",
    "cluster_name": "test-es8-node#1-es8-dev",
    "cluster_uuid": "Rs0Ec26mQSK83RIo52il5g",
    "version": {
        "number": "8.12.2",
        "build_flavor": "default",
        "build_type": "tar",
        "build_hash": "48a287ab9497e852de30327444b0809e55d46466",
        "build_date": "2024-02-19T10:04:32.774273190Z",
        "build_snapshot": false,
        "lucene_version": "9.9.2",
        "minimum_wire_compatibility_version": "7.17.0",
        "minimum_index_compatibility_version": "7.0.0"
    },
    "tagline": "You Know, for Search"
    }

    '''
    header =  {
            'Content-type': 'application/json', 
            'Authorization' : '{}'.format(os.getenv('BASIC_AUTH')),
            'Connection': 'close'
    }
    # res = requests.get(url=host, auth=HTTPBasicAuth("test", "test"), verify=False)
    res = requests.get(url=os.getenv("ES_HOST"), headers=header, verify=False)
    print(json.dumps(res.json(), indent=2))

    res = requests.get(url="{}/{}/_search".format(os.getenv("ES_HOST"), INDEX), verify=False, headers=header)
    print(json.dumps(res.json(), indent=2))


def es_certificates():
    '''
    $ python ./request-test.py
    {
    "name": "test-es8-node#1",
    "cluster_name": "test-es8-node#1-es8-dev",
    "cluster_uuid": "Rs0Ec26mQSK83RIo52il5g",
    "version": {
        "number": "8.12.2",
        "build_flavor": "default",
        "build_type": "tar",
        "build_hash": "48a287ab9497e852de30327444b0809e55d46466",
        "build_date": "2024-02-19T10:04:32.774273190Z",
        "build_snapshot": false,
        "lucene_version": "9.9.2",
        "minimum_wire_compatibility_version": "7.17.0",
        "minimum_index_compatibility_version": "7.0.0"
    },
    "tagline": "You Know, for Search"
    }

    '''
    header =  {
            'Content-type': 'application/json', 
            'Authorization' : '{}'.format(os.getenv('BASIC_AUTH')),
            'Connection': 'close'
    }

 
    ''' The verify_certs=False disables the underlying Python SSL modules from verifying the self-signed certs, '''
    ''' You can configure the client to use SSL for connecting to your elasticsearch cluster,'''
    ''' root-ca.pem - the root certificate
        root-ca-key.pem - the private key for the root certificate
        node.pem - the node certificate
        node-key.pem - the private key for the node certificate
        admin.pem - the admin certificate
        admin-key.pem - the private key for the admin certificate
    '''
    ''' We are using Elasticsearch 8.12.0 with self-signed certs in SG'''
    ''' https://stackoverflow.com/questions/61961725/how-to-connect-to-elasticsearch-with-python-using-ssl'''

    """ raise HTTP_EXCEPTIONS.get(status_code, TransportError)(elasticsearch.exceptions.AuthenticationException: AuthenticationException(401, 'Unauthorized') without header"""
    es_client = Elasticsearch(hosts=os.getenv("ES_HOST"),
                              headers=header,
                              use_ssl=True, # Useful if the connection is using SSL. If no, SSL certificates will not be validated
                              ca_certs="upgrade-script/cert_files/dev/root-ca.pem",
                              client_cert="upgrade-script/cert_files/dev/kirk.pem",
                              client_key="upgrade-script/cert_files/dev/kirk-key.pem",
                              verify_certs=True,
                              max_retries=0,
                              timeout=5)
    print(json.dumps(es_client.cluster.health(), indent=2))
    print('\n\n')

    query_all = {
        "query" : {
            "match_all" : {}
        }
    }
    resp = es_client.search(index=INDEX, body=query_all)
    print("Got {} hits:".format(resp["hits"]["total"]["value"]))
    print(json.dumps(resp['hits']['hits'], indent=2))
    '''
    for hit in resp["hits"]["hits"]:
        print("{}".format(hit["_source"]))
    '''
    resp = es_client.get(index=INDEX, id=1)
    print(json.dumps(resp['_source'], indent=2))
    


def request_es_certificates():
    '''
    $ python ./request-test.py
    {
    "name": "test-es8-node#1",
    "cluster_name": "test-es8-node#1-es8-dev",
    "cluster_uuid": "Rs0Ec26mQSK83RIo52il5g",
    "version": {
        "number": "8.12.2",
        "build_flavor": "default",
        "build_type": "tar",
        "build_hash": "48a287ab9497e852de30327444b0809e55d46466",
        "build_date": "2024-02-19T10:04:32.774273190Z",
        "build_snapshot": false,
        "lucene_version": "9.9.2",
        "minimum_wire_compatibility_version": "7.17.0",
        "minimum_index_compatibility_version": "7.0.0"
    },
    "tagline": "You Know, for Search"
    }

    '''
    header =  {
            'Content-type': 'application/json', 
            'Authorization' : '{}'.format(os.getenv('BASIC_AUTH')),
            'Connection': 'close'
    }
    res = requests.get(url=os.getenv("ES_HOST"), verify=False, cert=(r'C:\Users\euiyoung.hwang\Git_Workspace\ELK-Stack-Upgrade\upgrade-script\cert_files\dev\kirk.pem', r'C:\Users\euiyoung.hwang\Git_Workspace\ELK-Stack-Upgrade\upgrade-script\cert_files\dev\kirk-key.pem'))
    print(json.dumps(res.json(), indent=2))
    print('\n\n')
    res = requests.get(url="{}/{}/_search".format(os.getenv("ES_HOST"), INDEX), verify=False, cert=(r'C:\Users\euiyoung.hwang\Git_Workspace\ELK-Stack-Upgrade\upgrade-script\cert_files\dev\kirk.pem', r'C:\Users\euiyoung.hwang\Git_Workspace\ELK-Stack-Upgrade\upgrade-script\cert_files\dev\kirk-key.pem'))
    print(json.dumps(res.json(), indent=2))
    

if __name__ == '__main__':
    ''' Adding certificate verification is strongly advised. See: https://urllib3.readthedocs.io/en/latest/advanced-usage.html#tls-warnings '''
    ''' Validating the http request with Search Guard Authentication '''
    """
    https://docs.search-guard.com/latest/tls-in-production
    https://groups.google.com/g/search-guard/c/e1gCz_RU_wQ/m/ZsYHp4mlBAAJ
    https://www.elastic.co/guide/en/elasticsearch/reference/current/setting-up-authentication.html 
    --> When security features are enabled, depending on the realms you’ve configured, you must attach your user credentials to the requests sent to Elasticsearch. For example, when using realms that support usernames and passwords you can simply attach basic auth header to the requests.
    https://stackoverflow.com/questions/23172137/understanding-the-purpose-of-realm-in-basic-www-authentication
    
    - Node certificates are used to identify and secure traffic between Elasticsearch nodes on the transport layer (inter-node traffic). 
    - Client certificates are regular TLS certificates without any special requirements. They are used to identify Elasticsearch clients on the REST and transport layer. 
    They can be used for HTTP client certificate authentication or when using a Java Transport Client on transport layer.
    - Admin certificates are client certificates that have elevated rights to perform administrative tasks.
    - verfy_certs=True -> TLS error caused by: SSLError([SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: self signed certificate in certificate chain (_ssl.c:1131))

    Basic authentication is a very simple authentication scheme that is built into the HTTP protocol. 
    The client sends HTTP requests with the Authorization header that contains the Basic word followed by a space and a base64-encoded username:password string

    """
    '''
    # ------------------------------------------------------------------------
    The TLS Tool has created the following files:
    root-ca.pem - the root certificate
    root-ca-key.pem - the private key for the root certificate
    node.pem - the node certificate
    node-key.pem - the private key for the node certificate
    admin.pem - the admin certificate
    admin-key.pem - the private key for the admin certificate
    '''
    '''
    (.venv) ➜  python ./upgrade-script/request-SG-script.py
    '''
    # print('\n-----')
    # request_es()
    # print('\n-----')
    
    # print('\n-----')
    # request_es_certificates()
    # print('\n-----')
    
    print('\n-----')
    es_certificates()
    print('\n-----')