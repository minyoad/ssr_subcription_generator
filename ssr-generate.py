import requests
import base64
import json
import re


#for convert ssr config to ssr subcribtion file

def base64_encode(str):
    resstr=base64.b64encode(str.encode()).decode()
    return re.sub('\/','_',resstr.replace('=','').replace('+','-'))
    

# ssr://server:port:protocol:method:obfs:password_base64/?params_base64
# obfsparam=obfsparam_base64&protoparam=protoparam_base64&remarks=remarks_base64&group=group_base64
def jsonconfigs2SSR(jsonConfigs):
    ssr_list=[]

    for jsonConfig in jsonConfigs:        
		# 	"remarks" : "aabite",
		# 	"id" : "A0E5360C67576B63CFB07114085F6E33",
		# 	"server" : "aabite.com",
		# 	"server_port" : 2333,
		# 	"server_udp_port" : 0,
		# 	"password" : "mybacc.com",
		# 	"method" : "aes-256-cfb",
		# 	"protocol" : "auth_chain_a",
		# 	"protocolparam" : "",
		# 	"obfs" : "plain",
		# 	"obfsparam" : "",
		# 	"remarks_base64" : "YWFiaXRl",
		# 	"group" : "JP",
		# 	"enable" : true,
		# 	"udp_over_tcp" : false
		# }

        obfsparams=['obfsparam','protocolparam','remarks','group']
        obfsparams_base64=[]
        for obfsparam in obfsparams:
            print(jsonConfig[obfsparam])
            obfsparams_base64.append(obfsparam+'='+(base64_encode(jsonConfig[obfsparam])))
        
        obfsparam="&".join(obfsparams_base64)
        password_base64=base64_encode(jsonConfig['password'])

        ssrconfigs=['server','server_port','protocol','method','obfs']
        ssrcontents=[]
        for ssrconfig in ssrconfigs:
            ssrcontents.append(str(jsonConfig[ssrconfig]))
        
        ssr_content=':'.join(ssrcontents)
        
        allssr=ssr_content+':'+password_base64+'/?'+obfsparam
        ssr_list.append('ssr://'+base64_encode(allssr))

    return ssr_list
if __name__ == "__main__":

    f = open("gui-config.json", "r")
    json_content=f.read()
    # print(json_content)

    jsonAll=json.loads(json_content)

    ssrlist=jsonconfigs2SSR(jsonAll['configs'])

    print(ssrlist)
    # r = requests.post("https://www.ssrtool.com/tool/api/SSR_JsonToSSR",data={"json_content":json_content})
    # print(r.text)
    ssr_content='\n'.join(ssrlist)

    ssr_content_base64=base64_encode(ssr_content)
    print(ssr_content_base64)
    # ssr_content=r.text.replace("\"","").replace(",","\n").replace("[","").replace("]","")
    # r2 = requests.post("https://www.ssrtool.com/tool/api/enBase64",data={"content":ssr_content})
    # print(r2.text)
    # resJson=r2.json()
    fssr=open("ssr.txt","w")
    # fssr.write(resJson["data"])
    fssr.write(ssr_content_base64)

    fssr.close()
    
    print("Generate finished.")
       


