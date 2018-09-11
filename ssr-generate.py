import requests

#for convert ssr config to ssr subcribtion file

f = open("gui-config.json", "r")
json_content=f.read()
# print(json_content)
r = requests.post("https://www.ssrtool.com/tool/api/SSR_JsonToSSR",data={"json_content":json_content})
# print(r.text)

ssr_content=r.text.replace("\"","").replace(",","\n").replace("[","").replace("]","")
r2 = requests.post("https://www.ssrtool.com/tool/api/enBase64",data={"content":ssr_content})
# print(r2.text)
resJson=r2.json()
fssr=open("ssr.txt","w")
fssr.write(resJson["data"])
# print(resJson["data"])

print("Generate finished.")
