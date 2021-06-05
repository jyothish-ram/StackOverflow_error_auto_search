"""python script for automatically searching stack overflow 
for the errors using stackexchange api"""
import shlex
from subprocess import Popen , PIPE
import requests

def error(cmd) :
    #get error(exitcode, stdout & stderr) from the external command
    args = shlex.split(cmd)
    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    return out, err

def make_request(error):
    #searching error in stackexchange search api
    print("searching for "+error)
    response = requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=activity&tagged=python&sort=activity&intitle={}&site=stackoverflow".format(error))
    return response.json()

def get_urls(json_dict):
    #extract urls from json
    url_list = []
    count = 0
    for i in json_dict['items']:
            if i["is_answered"]:
                url_list.append(i["link"])
            count+=1
            if count == len(i) or count == 3:
                break
    import webbrowser
    for i in url_list:
        webbrowser.open(i)


if __name__ == "__main__":
    #extracting & filter error messsage
    out, err = error("python test.py")
    error_message = err.decode("utf-8").strip().split("\r\n") [-1]
    print(error_message)
    if error_message:
        filter_out = error_message.split(":")
        print(filter_out)
        print(filter_out[0])
        json1 = make_request(filter_out[0])
        json2 = make_request(filter_out[1])
        json = make_request(error_message)
        get_urls(json1)
        get_urls(json2)
        get_urls(json)
    else:
        print("No errors found")
