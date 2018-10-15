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
        # config content
        # {       
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
            # print(jsonConfig[obfsparam])
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

    #load configs from gui-config.json    
    f = open("gui-config.json", "r")
    json_content=f.read()
    # print(json_content)

    jsonAll=json.loads(json_content)

    #get ssr:// list
    ssrlist=jsonconfigs2SSR(jsonAll['configs'])

    print(ssrlist)
    
    ssr_content='\n'.join(ssrlist)

    #convert to base64 string
    ssr_content_base64=base64_encode(ssr_content)
    print(ssr_content_base64)

    #save to ssr.txt
    fssr=open("ssr.txt","w")
    fssr.write(ssr_content_base64)

    fssr.close()

    print("Generate finished.")
       


