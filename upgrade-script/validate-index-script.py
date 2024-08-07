


# -*- coding: utf-8 -*-
import sys
import json

from elasticsearch import Elasticsearch
import argparse
from dotenv import load_dotenv
import os
from datetime import datetime
import pandas as pd
from threading import Thread
from Search_Engine import Search
import logging
import warnings
warnings.filterwarnings("ignore")

load_dotenv()

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)




def work(es_source_client, es_target_client):
    '''
    Validate a list of indices from the source cluster and compare them to target cluster
    '''
    def try_exists_index(es_client, index):
        try:
            # logging.info(mapping)
            if es_client.indices.exists(index):
               return True
            return False
            
        except Exception as e:
            logging.error(e)
            pass
            
    
    es_source_client = es_source_client.replace('\r','')
    es_target_client = es_target_client.replace('\r','')
    
    logging.info(f"{es_source_client, es_target_client}")

    es_obj_s = Search(host=es_source_client)
    es_client = es_obj_s.get_es_instance()

    es_obj_t = Search(host=es_target_client)
    es_t_client = es_obj_t.get_es_instance()
    

    ''' extact a list of indices from the source cluster'''
    source_idx_lists = es_client.indices.get("*")
    # logging.info(source_idx_lists)
    is_not_exist_lists, different_doc = [], []
    for each_index in source_idx_lists:
        ''' exclude system indices in the source cluster such as .monitoring-es-7-2024.07.12'''
        if '.' not in each_index:
            ''' compare each index between source cluster and target cluster'''
            is_exist = try_exists_index(es_t_client, each_index)
            logging.info(f"validate index [{each_index}] exsits : results is {is_exist}")
            ''' check the number of count'''
            res_count_source = es_client.count(index=each_index, body={'query': { 'match_all' : {}}})["count"]
            res_count_target = es_t_client.count(index=each_index, body={'query': { 'match_all' : {}}})["count"]
            if res_count_source != res_count_target:
                different_doc.append({each_index : "{} vs {}".format(res_count_source, res_count_target)})

            # print(res)
            if not is_exist:
                is_not_exist_lists.append(each_index)

    print('\n')
    print('-'*50)
    print(f"Not exist lists : {json.dumps(is_not_exist_lists, indent=2)}")
    print(f"Differ Count : {json.dumps(different_doc, indent=2)}")
    print('-'*50)
    print('\n')
    


if __name__ == "__main__":
    
    '''
    (.venv) ➜  python ./upgrade-script/validate-index-script.py --es http://source_es_cluster:9200 ---ts http://target_es_cluster:9201

    '''
    parser = argparse.ArgumentParser(description="Index into Elasticsearch using this script")
    parser.add_argument('-e', '--es', dest='es', default="http://localhost:9200", help='host source')
    parser.add_argument('-t', '--ts', dest='ts', default="http://localhost:9201", help='host target')
    args = parser.parse_args()
    
    if args.es:
        es_source_host = args.es
        
    if args.ts:
        es_target_host = args.ts
        
    # --
    # Only One process we can use due to 'Global Interpreter Lock'
    # 'Multiprocessing' is that we can use for running with multiple process
    # --
    try:
        th1 = Thread(target=work, args=(es_source_host, es_target_host))
        th1.start()
        th1.join()
        
    except Exception as e:
        logging.error(e)
        pass
    