
# options{'params':{'plist': [], 'pcurent': {}, 'pdefault': {}}, 'fields': {}, 'relations': {}}
# Загружаем данные из вншнего API
def load_data_from(url, options):
    
        import requests
        
        response_list = []
        pNum = 1
        while(True):
            opts = options.copy()
            opts['params']['pcurent']['pageNum'] = pNum # + 1

            url_response = requests.get(url, params = opts['params']['pcurent'])
            url_response_list = url_response.json()['data']
            pageCount = url_response.json()['pageCount']
            pNum = url_response.json()['pageNum']
            if pageCount == 0:
                response = {}
                response['fields'] = None
                response['relations'] = None
                response_list.append(response)
                return response_list
        
            for res_elem in url_response_list:
                response = {'fields': {}, 'relations': {}}
                for fkey, fval in opts['fields'].items():
                    if res_elem[fval] == "":
                        pass
                    else:
                        response['fields'][fkey] = res_elem[fval]
                        
                for relkey, relval in opts['relations'].items():
                    if res_elem[relval] == "":
                        pass
                    else:
                        response['relations'][relkey] = res_elem[relval]
                        
                response_list.append(response)
                
            pNum += 1
            if pNum > pageCount: break

        return response_list
