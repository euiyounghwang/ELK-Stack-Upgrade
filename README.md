# ELK Upgrade with Search Guard
<i>ELK Upgrade with Search Guard


FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.8+ based on standard Python.
This is a repository that provides to deliver the records to the Prometheus-Export application.


Vagrant is a tool for working with virtual environments, and in most circumstances, this means working with virtual machines.

When a node fails, Elasticsearch will rebalance the cluster by moving shards from the failed node to the remaining nodes in the cluster. This ensures that all data is always available even if a node fails

An Elasticsearch index consists of one or more primary shards. As of Elasticsearch version 7, the current default value for the number of primary shards per index is 1. In earlier versions, the default was 5 shards.
- It depends on the query you used and how many documents with the size of each document  that you might have in daily or monthly. 
- We can consider making a dynamic template explicitly to optimize for an index before creating the field. 
- Shard size should not exceed 30-50GB (with a mathematical formula, Core number * The number of Nodes). Also we can consider avoiding ‘wild card query’, ‘script_query to calculate hits’ and retrieve only necessary fields when searching in query_string fields and highlighting.
- Use filter context instead of query context because Elasticsearch does not need to calculate relevance score for filter context. 
- Please note, the replica number should not be zero, otherwise you will have data loss.  In other words, as the number of replica shards increases, search performance should be increased and index performance decreased. Therefore, it is important to find the optimal number of shards according to the data size or the number of requests.
- [Shards] Using the 30-80 GB value, you can calculate how many shards you’ll need. For instance, let’s assume you rotate indices monthly and expect around 600 GB of data per month. In this example, you would allocate 8 to 20 shards.
- ELK : https://scrawled-note.tistory.com/entry/ELK-%EB%AC%B4%EC%9E%91%EC%A0%95-%EC%84%A4%EC%B9%98%ED%95%98%EA%B8%B0


- Typically the heap usage will be a saw tooth pattern, oscillating between around 30% and 70% of the maximum heap being used. This is because the JVM steadily increases heap usage percentage until the garbage collection process frees up memory again (When memory is insufficient, it is executed immediately when additional memory is requested).
- The best practices for managing heap size usage and JVM garbage collection in a large Elasticsearch cluster are to ensure that the heap size is set to a maximum of 50% of the available RAM, and that the JVM garbage collection settings are optimized for the specific use case. It is important to monitor the heap size and garbage collection metrics to ensure that the cluster is running optimall



Search Guard Is An Open Source Security Plugin For Elasticsearch And The Entire ELK stack. Search Guard Encrypts All Data In Transit. 
- Search Guard Versions : https://docs-search--guard-com.webpkgcache.com/doc/-/s/docs.search-guard.com/latest/search-guard-versions
- Account Maintain : Add user to "/plugins/search-guard-flx/sgconfig/sg_internal_user.xml" (Use API : https://docs.search-guard.com/7.x-51/rest-api-internalusers, https://docs.search-guard.com/latest/sgctl, Base64 : https://www.encodebase64.net/, PlainText : <user>:<password>)
- Basic authentication is a very simple authentication scheme that is built into the HTTP protocol. The client sends HTTP requests with the Authorization header that contains the Basic word followed by a space and a base64-encoded username:password string (: -> colon).
- Secure Sockets Layer (SSL) is the technology responsible for data authentication and encryption for internet connections. It encrypts data being sent over the internet between two systems (commonly between a server and a client) so that it remains private. And with the growing importance of online privacy, an SSL port is something you should get familiar with.
- Hypertext transfer protocol secure (HTTPS) is the secure version of HTTP, which is the primary protocol used to send data between a web browser and a website. HTTPS is encrypted in order to increase security of data transfer.  This is particularly important when users transmit sensitive data, such as by logging into a bank account, email service, or health insurance provider.
- What is shield : Shield allows you to easily protect Elasticsearch cluster from unintentional modification or unauthorized access with a username and password. Shield also gives security features like encryption, role-based access control, IP filtering, and auditing are also available when you need them.



How to Choose the Correct Number of Shards per Index in Elasticsearch. (https://opster.com/guides/elasticsearch/capacity-planning/elasticsearch-number-of-shards/)
- Having multiple primary shards when indexing : Shards are basically used to parallelize work on an index. When you send a bulk request to index a list of documents, they will be split and divided among all available primary shards. So, if you have 5 primary shards and send a bulk request with 100 documents, each shard will have to index 20 documents in parallel.
Indexing is usually quicker when you have more shards. For instance, `if you have 3 data nodes, you should have 3, 6 or 9 shards. This is very important. If, instead, you have 3 data nodes and decide to use 4 primary shards, then your indexing process will actually be slower than when using 3 shards`, because 1 node (aka server) will have double the work and the other 2 will sit idle. 
- Having multiple primary shards when searching : When you submit a search request, the node that receives the request acts as the coordinating node, which then looks up which shards belong to that index according to the cluster state. 


#### Test Data using ES API
```bash

GET _cat/indices

POST _bulk
{ "index" : { "_index" : "test", "_id" : "1" } }
{ "field1" : "value1" }
{ "delete" : { "_index" : "test", "_id" : "2" } }
{ "create" : { "_index" : "test", "_id" : "3" } }
{ "field1" : "value3" }
{ "update" : {"_id" : "1", "_index" : "test"} }
{ "doc" : {"field2" : "value2"} }

GET test/search
```

#### Python V3.9 Install
```bash
sudo yum install gcc openssl-devel bzip2-devel libffi-devel zlib-devel git 
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz 
tar –zxvf Python-3.9.0.tgz or tar -xvf Python-3.9.0.tgz 
cd Python-3.9.0 
./configure --libdir=/usr/lib64 
sudo make 
sudo make altinstall 

# python3 -m venv .venv --without-pip
sudo yum install python3-pip

sudo ln -s /usr/lib64/python3.9/lib-dynload/ /usr/local/lib/python3.9/lib-dynload

python3 -m venv .venv
source .venv/bin/activate

# pip install -r ./dev-requirement.txt
pip install poetry
pip install requests
pip install pytz
pip install httpx
pip install python-dotenv
pip install pandas

# when error occur like this
# ImportError: urllib3 v2 only supports OpenSSL 1.1.1+, currently the 'ssl' module is compiled with 'OpenSSL 1.0.2k-fips  26 Jan 2017'. See: https://github.com/urllib3/urllib3/issues/2168
pip install urllib3==1.26.18
pip install pytz
```


### Using Poetry: Create the virtual environment in the same directory as the project and install the dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install poetry

# --
poetry config virtualenvs.in-project true
poetry init
poetry add pytz
poetry add httpx
poetry add python-dotenv
poetry add pytest-cov
peetry add pandas
```
or you can run this shell script `./create_virtual_env.sh` to make an environment. then go to virtual enviroment using `source .venv/bin/activate`


The first time installation procedure on a production cluster is to:

1) Disable shard allocation
- Cluster Reboot

```bash
GET _cat/indices
GET _cluster/stats?human&pretty

# Set shard allocation to stop
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": "none"
  }
}

POST _flush/synced

```
2) Stop all nodes

3) Install the Search Guard plugin on all nodes
- If you install ES at the first time, 
```bash
sudo sysctl -w vm.max_map_count=262144
vi /etc/security/limits.conf

elasticsearch soft memlock unlimited
elasticsearch hard memlock unlimited
elasticsearch soft nofile 65536
elasticsearch hard nofile 65536

#euiyoung soft    nofile  65536
#euiyoung hard    nofile  65536
#euiyoung hard    nproc   65536
#euiyoung soft    nproc   65536
#euiyoung soft    memlock unlimited
#euiyoung hard    memlock unlimited

sudo su -l elasticsearch

```
- Search Guard License : https://search-guard.com/licensing/
- Search Guard : https://docs.search-guard.com/latest/search-guard-versions

```bash
- Elasticsearch Plugin for Search Guard

$ ./bin/elasticsearch-plugin install -b file:////apps/elasticsearch/node1/elasticsearch-8.12.2/search-guard-flx-elasticsearch-plugin-2.0.0-es-8.12.2.zip

[devuser@localhost elasticsearch-8.12.2]$ ./bin/elasticsearch-plugin install -b file:////apps/elasticsearch/node1/elasticsearch-8.12.2/search-guard-flx-elasticsearch-plugin-2.0.0-es-8.12.2.zip
-> Installing file:////apps/elasticsearch/node1/elasticsearch-8.12.2/search-guard-flx-elasticsearch-plugin-2.0.0-es-8.12.2.zip
-> Downloading file:////apps/elasticsearch/node1/elasticsearch-8.12.2/search-guard-flx-elasticsearch-plugin-2.0.0-es-8.12.2.zip
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@     WARNING: plugin requires additional permissions     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
* java.lang.RuntimePermission accessClassInPackage.com.sun.jndi.*
* java.lang.RuntimePermission accessClassInPackage.sun.misc
* java.lang.RuntimePermission accessClassInPackage.sun.nio.ch
* java.lang.RuntimePermission accessClassInPackage.sun.security.x509
* java.lang.RuntimePermission accessDeclaredMembers
* java.lang.RuntimePermission getClassLoader
* java.lang.RuntimePermission loadLibrary.*
* java.lang.RuntimePermission setContextClassLoader
* java.lang.reflect.ReflectPermission suppressAccessChecks
* java.net.NetPermission getProxySelector
* java.net.SocketPermission * connect,accept,resolve
* java.security.SecurityPermission insertProvider
* java.security.SecurityPermission org.apache.xml.security.register
* java.security.SecurityPermission putProviderProperty.BC
* java.util.PropertyPermission * read,write
* java.util.PropertyPermission org.apache.xml.security.ignoreLineBreaks write
* javax.security.auth.AuthPermission doAs
* javax.security.auth.AuthPermission modifyPrivateCredentials
* javax.security.auth.kerberos.ServicePermission * accept
See https://docs.oracle.com/javase/8/docs/technotes/guides/security/permissions.html
for descriptions of what these permissions allow and the associated risks.
-> Installed search-guard-flx
-> Please restart Elasticsearch to activate any plugins installed
[devuser@localhost elasticsearch-8.12.2]$


- Change chmod to run *.sh
[devuser@localhost tools]$ pwd
/apps/elasticsearch/node1/elasticsearch-8.12.2/plugins/search-guard-flx/tools
[devuser@localhost tools]$ ls
install_demo_configuration.sh
[devuser@localhost tools]$ chmod 755 *.sh

devuser@localhost tools]$ ./install_demo_configuration.sh
Search Guard Demo Installer
 ** Warning: Do not use on production or public reachable systems **
Initialize Search Guard? [y/N] y
Cluster mode requires maybe additional setup of:
  - Virtual memory (vm.max_map_count)
    See https://www.elastic.co/guide/en/elasticsearch/reference/current/vm-max-map-count.html

Enable cluster mode? [y/N] n
Basedir: /apps/elasticsearch/node1/elasticsearch-8.12.2
Elasticsearch install type: .tar.gz on NAME="Red Hat Enterprise Linux Server"
Elasticsearch config dir: /apps/elasticsearch/node1/elasticsearch-8.12.2/config
Elasticsearch config file: /apps/elasticsearch/node1/elasticsearch-8.12.2/config/elasticsearch.yml
Elasticsearch bin dir: /apps/elasticsearch/node1/elasticsearch-8.12.2/bin
Elasticsearch plugins dir: /apps/elasticsearch/node1/elasticsearch-8.12.2/plugins
Elasticsearch lib dir: /apps/elasticsearch/node1/elasticsearch-8.12.2/lib
/apps/elasticsearch/node1/elasticsearch-8.12.2/config/elasticsearch.yml seems to be already configured for Search Guard. Quit.
[devuser@localhost tools]$

```

4) Change "elasticsearch.yml" for Search Guard Configuration
```bash

- Created certification automatically
-rw-rw-r--  1 localhost localhost  1704 Jun 21 15:52 esnode-key.pem
-rw-rw-r--  1 localhost localhost  1720 Jun 21 15:52 esnode.pem
..
-rw-rw-r--  1 localhost localhost  1704 Jun 21 15:52 kirk-key.pem
-rw-rw-r--  1 localhost localhost  1610 Jun 21 15:52 kirk.pem
..
-rw-rw-r--  1 localhost localhost  1444 Jun 21 15:52 root-ca.pem


- elasticsearch.yml

path.repo: ["/usr/share/elasticsearch/backup"]

# --------------------------------- Discovery ----------------------------------
#
# Pass an initial list of hosts to perform discovery when this node is started:
# The default list of hosts is ["127.0.0.1", "[::1]"]
#
discovery.seed_hosts: ["192.168.79.107", "192.168.79.108"]
#
# Bootstrap the cluster using an initial set of master-eligible nodes:
#
cluster.initial_master_nodes: ["192.168.79.107"]
#
# For more information, consult the discovery and cluster formation module docum
entation.


######## Start Search Guard Demo Configuration ########
searchguard.enterprise_modules_enabled: true
# WARNING: revise all the lines below before you go into production
searchguard.ssl.transport.pemcert_filepath: esnode.pem
searchguard.ssl.transport.pemkey_filepath: esnode-key.pem
searchguard.ssl.transport.pemtrustedcas_filepath: root-ca.pem
searchguard.ssl.transport.enforce_hostname_verification: false
searchguard.ssl.http.enabled: true
searchguard.ssl.http.pemcert_filepath: esnode.pem
searchguard.ssl.http.pemkey_filepath: esnode-key.pem
searchguard.ssl.http.pemtrustedcas_filepath: root-ca.pem
searchguard.allow_unsafe_democertificates: true
searchguard.allow_default_init_sgindex: true
searchguard.authcz.admin_dn:
  - CN=kirk,OU=client,O=client,L=test, C=de

searchguard.audit.type: internal_elasticsearch
searchguard.enable_snapshot_restore_privilege: true
searchguard.check_snapshot_restore_write_privileges: true
searchguard.restapi.roles_enabled: ["SGS_ALL_ACCESS"]
cluster.routing.allocation.disk.threshold_enabled: false
node.max_local_storage_nodes: 3

xpack.security.enabled: false
searchguard.enterprise_modules_enabled: false
indices.breaker.total.use_real_memory: false

######## End Search Guard Demo Configuration ########

#Max Clause count
indices.query.bool.max_clause_count: 50000

#reindex.remote.whitelist: "otherhost:9200, another:9200, 127.0.10.*:9200, localhost:*
reindex.remote.whitelist: "*:9200"


# ------------------------------------------------------------------------
# The TLS Tool has created the following files:
# root-ca.pem - the root certificate
# root-ca-key.pem - the private key for the root certificate
# node.pem - the node certificate
# node-key.pem - the private key for the node certificate
# admin.pem - the admin certificate
# admin-key.pem - the private key for the admin certificate

```

5) Restart Elasticsearch and check that the nodes come up
- Test connection : https://localhost:9201
- Run : `/apps/elasticsearch/elasticsearch-8.12.2/bin/elasticsearch -d`
- Download sgctl tool script (https://maven.search-guard.com/search-guard-flx-release/com/floragunn/sgctl/)
```bash
- https://docs.search-guard.com/latest/manual-installation
$ ./sgctl.sh
Usage: sgctl [COMMAND]
Remote control tool for Search Guard
Commands:
  connect          Tries to connect to a cluster and persists this connection
                     for subsequent commands
  get-config       Retrieves Search Guard configuration from the server to
                     local files
  update-config    Updates Search Guard configuration on the server from local
                     files
  migrate-config   Converts old-style sg_config.yml and kibana.yml into
                     sg_authc.yml and sg_frontend_authc.yml
  component-state  Retrieves Search Guard component status information
  sgctl-licenses   Displays license information for sgctl
  sgctl-version    Shows the version of this sgctl command
  add-user-local   Adds a new user to a local sg_internal_users.yml file
  add-user         Adds a new user
  update-user      Updates a user
  delete-user      Deletes a user
  add-var          Adds a new configuration variable
  update-var       Updates an existing configuration variable
  delete-var       Deletes an existing configuration variable
  set              Modifies a property in the Search Guard Configuration
  update-license   Updates the SG license
  rest             REST client for administration
  special          Commands for special circumstances
```

- How to use sgctl tool script
```bash
[localhost@localhost sgconfig]$ pwd
/apps/elasticsearch/node1/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig
[localhost@localhost sgconfig]$ ls
elasticsearch.yml.example  sg_action_groups.yml  sg_authc.yml  sg_authz.yml  sg_frontend_authc.yml  sg_frontend_multi_tenancy.yml  sg_internal_users.yml  sg_roles_mapping.yml  sg_roles.yml  sg_tenants.yml
```
- Account Maintain : Add user to "/plugins/search-guard-flx/sgconfig/sg_internal_user.xml" (Use API : https://docs.search-guard.com/7.x-51/rest-api-internalusers, https://docs.search-guard.com/latest/sgctl, Base64 : https://www.encodebase64.net/, PlainText : <user>:<password>)
```bash

- https://docs.search-guard.com/latest/manual-installation
- https://docs.search-guard.com/latest/first-steps-user-configuration

# Add User: 
- if you already have a running cluster, you can also sgctl to directly create users on the cluster without modifying a local sg_internal_users.yml file first.

# monitoring-account for admini permission
sudo /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/tools/sgctl-2.0.0.sh add-user-local monitoring --backend-roles admin --password monitoring1234# -o /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_internal_users.yml


# add for wx-index
sudo /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/tools/sgctl-2.0.0.sh add-user-local wxuser --backend-roles sg_wxreadall --password 1 -o /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_internal_users.yml


sudo /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/tools/sgctl-2.0.0.sh add-user-local jdoe --backend-roles admin --password 1 -o /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_internal_users.yml


[biadmin@localhost ~]$ 
sudo /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/tools/sgctl-2.0.0.sh add-user-local user1 --backend-roles admin --password 1 -o /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_internal_users.yml
Appending to /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_internal_users.yml


sudo /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/tools/sgctl-2.0.0.sh add-user-local user3 --backend-roles sg_guest,kibanauser --password 1 -o /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_internal_users.yml
Appending to /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_internal_users.yml

-- guest
sudo /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/tools/sgctl-2.0.0.sh add-user-local guest --backend-roles sg_guest,readall,kibanauser --password 1 -o /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_internal_users.yml

Appending to /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_internal_users.yml

# Delete User:  (It doesn't need to update configuation using sgctl tool script to ES cluster with Search Guard)
[biadmin@localhost ~]$ 
sudo /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/tools/sgctl-2.0.0.sh delete-user guest --ca-cert /apps/elasticsearch/elasticsearch-8.12.2/config/root-ca.pem --cert /apps/elasticsearch/elasticsearch-8.12.2/config/kirk.pem --key /apps/elasticsearch/elasticsearch-8.12.2/config/kirk-key.pem --host localhost --port 9201 --insecure
--
Successfully connected to cluster supplychain-logging-es8-dev (localhost) as user CN=kirk,OU=client,O=client,L=test,C=de
Internal User user2 has been deleted
--



# Update-Config : 

1) Create a connectin for updating the configuration
[biadmin@localhost ~]$
/apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/tools/sgctl-2.0.0.sh connect --host localhost --port 9201 --ca-cert /apps/elasticsearch/elasticsearch-8.12.2/config/root-ca.pem --cert /apps/elasticsearch/elasticsearch-8.12.2/config/kirk.pem --key /apps/elasticsearch/elasticsearch-8.12.2/config/kirk-key.pem --insecure
--
Successfully connected to cluster supplychain-logging-es8-dev (localhost) as user CN=kirk,OU=client,O=client,L=test,C=de
--

2) Update configuration to add user

[biadmin@localhost ~]$

/apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/tools/sgctl-2.0.0.sh update-config /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_internal_users.yml

/apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/tools/sgctl-2.0.0.sh update-config /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_internal_users.yml /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_roles.yml /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_roles_mapping.yml
--
Successfully connected to cluster supplychain-logging-es8-dev (localhost) as user CN=kirk,OU=client,O=client,L=test,C=de
Configuration has been updated
--

# - ES Logs when run the update configuration
[2024-06-26T17:21:09,643][INFO ][c.f.s.a.PrivilegesEvaluator] [supplychain-logging-es8-node#1] Updated authz config:
[2024-06-26T17:25:05,415][INFO ][c.f.s.c.ConfigurationRepository] [supplychain-logging-es8-node#1] Index update done:
'{"errors":false,"took":25,"items":[{"index":{"_index":".searchguard","_id":"rolesmapping","_version":17,"result":"updated","forced_refresh":true,"_shards":{"total":4,"successful":4,"failed":0},"_seq_no":173,"_primary_term":17,"status":200}},{"index":{"_index":".searchguard","_id":"roles","_version":22,"result":"updated","forced_refresh":true,"_shards":{"total":4,"successful":4,"failed":0},"_seq_no":174,"_primary_term":17,"status":200}},{"index":{"_index":".searchguard","_id":"internalusers","_version":131,"result":"updated","forced_refresh":true,"_shards":{"total":4,"successful":4,"failed":0},"_seq_no":175,"_primary_term":17,"status":200}}]}'
[2024-06-26T17:25:05,422][INFO ][c.f.s.a.AuthorizationService] [supplychain-logging-es8-node#1] Updated authz config:


3) Get configuration
[biadmin@localhost ~]$
/apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/tools/sgctl-2.0.0.sh get-config -0 /apps/elasticsearch/elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/ --output ./



-- Other Instance
1) Create a connectin for updating the configuration
./sgctl-2.0.0.sh connect --host localhost --port 9201 --ca-cert ./search-guard-keys/dev/root-ca.pem --cert  ./search-guard-keys/dev/kirk.pem --key  ./search-guard-keys/dev/kirk-key.pem --insecure

-bash-4.2$ ./sgctl-2.0.0.sh connect --host localhost --port 9201 --ca-cert ./search-guard-keys/dev/root-ca.pem --cert  ./search-guard-keys/dev/kirk.pem --key  ./search-guard-keys/dev/kirk-key.pem --insecure
Successfully connected to cluster supplychain-logging-es8-dev (localhost) as user CN=kirk,OU=client,O=client,L=test,C=de



elastic:
  hash: "$2y$12$ScV8euAglZETM/H1xTuQkOP36raAW7ylOw/pVpF10QKja3RSW2aYu=-="
  reserved: false
  backend_roles:
  - "admin"
  description: "common admin"


# User Test
http://localhost:9200/_searchguard/api/internalusers/admin  (Header : 'Authorization' : 'Basic YWRtaW46YWRtaW4=')


$ curl https://test:test@localhost:9201 --insecure
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   568  100   568    0     0   1192      0 --:--:-- --:--:-- --:--:--  1200{
  "name" : "supplychain-logging-es8-node#1",
  "cluster_name" : "supplychain-logging-es8-dev",
  "cluster_uuid" : "Rs0Ec26mQSK83RIo52il5g",
  "version" : {
    "number" : "8.12.2",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "48a287ab9497e852de30327444b0809e55d46466",
    "build_date" : "2024-02-19T10:04:32.774273190Z",
    "build_snapshot" : false,
    "lucene_version" : "9.9.2",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}

(.venv)

[biadmin@localhost ~]$ curl -XGET --user test:test "https://localhost:9201/_cluster/health?pretty" --insecure
{
  "cluster_name" : "localhost",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 2,
  "number_of_data_nodes" : 2,
  "active_primary_shards" : 43,
  "active_shards" : 86,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}


-bash-4.2$  curl -XGET -u test:test https://localhost:9260 --ca-cert /apps/elasticsearch/elasticsearch-8.12.2/config/root-ca.pem
{
  "name" : "test-node-1",
  "cluster_name" : "test-upgrade",
  "cluster_uuid" : "8Jew6_HCSVa1A7KHL2GOlQ",
  "version" : {
    "number" : "8.12.2",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "48a287ab9497e852de30327444b0809e55d46466",
    "build_date" : "2024-02-19T10:04:32.774273190Z",
    "build_snapshot" : false,
    "lucene_version" : "9.9.2",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
-bash-4.2$


# Get all users from search guard
-bash-4.2$  curl -XGET -u test:test https://localhost:9260/_searchguard/api/internalusers/ | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   582  100   582    0     0   3287      0 --:--:-- --:--:-- --:--:--  3306
{
  "logstash": {
    "backend_roles": [
      "logstash"
    ],
    "description": "Demo logstash user"
  },
  "snapshotrestore": {
    "backend_roles": [
      "snapshotrestore"
    ],
    "description": "Demo snapshotrestore user"
  },
  "admin": {
    "backend_roles": [
      "admin"
    ],
    "description": "Demo admin user"
  },
  "kibanaserver": {
    "description": "Demo kibanaserver user"
  },
  "kibanaro": {
    "backend_roles": [
      "kibanauser",
      "readall"
    ],
    "attributes": {
      "attribute1": "value1",
      "attribute2": "value2",
      "attribute3": "value3"
    },
    "description": "Demo kibanaro user"
  },
  "biadmin": {
    "backend_roles": [
      "admin"
    ]
  },
  "readall": {
    "backend_roles": [
      "readall"
    ],
    "description": "Demo readall user"
  }
}
-bash-4.2$


curl -X 'PATCH' \
  'https://localhost:9260/_searchguard/api/internalusers' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Basic test=' \
  -d '[ 
  { 
    "op": "add", "path": "/test", "value": { "password": "test", "backend_roles": ["admin"] } 
  }
]' | jq

```


6) Re-enable shard allocation by using sgadmin
```bash
PUT _cluster/settings
{
  "persistent": {
    "cluster.routing.allocation.enable": "all"
  }
}
```

7) Configure authentication/authorization, users, roles and permissions by uploading the Search Guard configuration with sgadmin
```bash

- Change the files in ../sgconfig and execute: 
"/home/biadmin/ELK_UPGRADE/search-guard-hash/tools/sgadmin.sh" -cd "/ES/search_guard/elasticsearch-7.9.0/plugins/search-guard-7/sgconfig" -icl -key "/ES/search_guard/elasticsearch-7.9.0/config/kirk-key.pem" -cert "/ES/search_guard/elasticsearch-7.9.0/config/kirk.pem" -cacert "/ES/search_guard/elasticsearch-7.9.0/config/root-ca.pem" -nhnv

- Searchguard 8.12
 /apps/elasticsearch/sgctl-2.0.0.sh update-config ./elasticsearch-8.12.2/plugins/search-guard-flx/sgconfig/sg_roles.yml --ca-cert=./elasticsearch-8.12.2/config/root-ca.pem  --key=./elasticsearch-8.12.2/config/kirk-key.pem

 apps/elasticsearch/sgctl-2.0.0.sh connect localhost --port=9201 --cert=/apps/elasticsearch/elasticsearch-8.12.2/config/root-ca.pem  --key=/apps/elasticsearch/elasticsearch-8.12.2/config/kirk-key.pem


```

8) Install Kibana
```bash
##Kibaba (kibana plugin install 없이 http 기동하게 되면 messaage box for login)
# https://docs.search-guard.com/latest/search-guard-versions

Plugin installation was unsuccessful due to error "No kibana plugins found in archive"
[devuser@gsa02 kibana-7.9.0-linux-x86_64]$ ./bin/kibana-plugin install file:////apps/kibana/kibana-8.12.2/search-guard-flx-kibana-plugin-2.0.0-es-8.12.2.zip
Kibana is currently running with legacy OpenSSL providers enabled! For details and instructions on how to disable see https://www.elastic.co/guide/en/kibana/8.12/production.html#openssl-legacy-provider
Attempting to transfer from file:////apps/kibana/kibana-8.12.2/search-guard-flx-kibana-plugin-2.0.0-es-8.12.2.zip
Transferring 9423509 bytes....................
Transfer complete
Retrieving metadata from plugin archive
Extracting plugin archive
Extraction complete
Plugin installation complete
[devuser@gsa02 kibana-7.9.0-linux-x86_64]$ 


# is proxied through the Kibana server.
elasticsearch.username: "elastic"
elasticsearch.password: "gsaadmin"


elasticsearch.ssl.verificationMode: none
elasticsearch.requestHeadersWhitelist: ["Authorization", "sgtenant"]

# - LOGO (/apps/kibana/kibana-8.12.2/plugins/searchguard/public/assets)


/home/ES/kibana-7.9.0-linux-x86_64/plugins/searchguard/public/apps/loginlogin.html

COPY /apps/kibana/kibana-8.12.2/plugins/searchguard/public/assets/searchguard_logo.svg from /home/biadmin/ELK_UPGRADE/searchguard_logo.svg

# Run
nohup /apps/kibana/kibana-8.12.2/bin/kibana &> /dev/null &
```


9) Logstash Configuration
- Logstash Reference :https://princehood69.rssing.com/chan-69503895/article83.html, https://m.blog.naver.com/inggi/221816427585
- Path for Service

```bash
[logstash@localhost system]$ systemctl status logstash.service
● logstash.service - LSB: logstash
   Loaded: loaded (/etc/rc.d/init.d/logstash; bad; vendor preset: disabled)
   Active: active (running) since Wed 2024-06-19 08:42:25 EDT; 1 weeks 2 days ago
     Docs: man:systemd-sysv-generator(8)
  Process: 1213 ExecStart=/etc/rc.d/init.d/logstash start (code=exited, status=0/SUCCESS)
   CGroup: /system.slice/logstash.service
           └─1267 /apps/java/latest//bin/java -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly -XX:+DisableExplicitGC -Djava.awt.headless=true -Dfile.encoding=UTF-8 -XX:+HeapDumpOnOutOfMemoryError -Djava.security.egd=file:/dev/urandom -Dlo...
[logstash@localhost system]$ less /etc/rc.d/init.d/logstash
[logstash@localhost system]$
```

- Run with /config/conf.d/ : `/home/biadmin/ELK_UPGRADE/logstash-7.13.0/bin/logstash -f /home/biadmin/ELK_UPGRADE/logstash-7.13.0/config/conf.d/`
- /apps/logstash/logstash-8.12.2/bin/logstash -f /apps/logstash/logstash-8.12.2/config/conf.d/ (QA1/QA2 with `logstash` account)

```bash
input {
  stdin {}
}
output {
  elasticsearch {
    hosts => "localhost:9200"
    user => logstash
    password => logstash
    ssl => true
    ssl_certificate_verification => false
    truststore => "<logstash path>/config/truststore.jks"
    truststore_password => changeit
    index => "test"
    document_type => "test_doc"
  }
  stdout{
    codec => rubydebug
  }
}
```

10) Reindex
- To continue reindexing if there are conflicts, set the "conflicts" request body parameter to proceed.
- Set to create to only index documents that do not already exist (put if absent). Valid values: index, create. Defaults to index.
```bash
POST _reindex?wait_for_completion=false
{
  "conflicts": "proceed",
  "source": {
    "remote": {
      "host": "http://host.docker.internal:9209",
      "username": "elastic",
      "password": "your_password"
    },
    "index": "performance_metrics",
    "query": {
     "match_all": {}
    }
  },
  "dest": {
    "index": "cp99_performance_metrics",
    "op_type": "create"
  }
}


GET _tasks?detailed=true&actions=*reindex
GET _tasks/BH_UUNP2RjafE0aNHGi_Hw:216731707

```


### Pytest
- Run `py.test -sv tests` or `test-pytest.sh` to validate whether ingestion is working with sample records based on search-guard.
- SSL Cert Verfication : https://requests.readthedocs.io/en/latest/user/advanced/#ssl-cert-verification
- Sample (You can pass verify the path to a CA_BUNDLE file or directory with certificates of trusted CAs): `requests.get('https://github.com', verify='/path/to/certfile')`
```bash
$ py.test -v tests
============================= test session starts =============================
platform win32 -- Python 3.11.7, pytest-8.2.2, pluggy-1.5.0 -- C:\Users\euiyoung.hwang\Git_Workspace\ELK-upgrade\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\euiyoung.hwang\Git_Workspace\ELK-upgrade\tests
configfile: pytest.ini
collecting ... collected 3 items

tests\test_elasticsearch.py::test_elasticsearch_create_index_index PASSED [ 33%]
tests\test_elasticsearch.py::test_indics_analyzer_elasticsearch PASSED   [ 66%]
tests\test_elasticsearch.py::test_search_elasticsearch PASSED            [100%]

============================== 3 passed in 3.75s ==============================
(.venv)
```