import requests
import time
import optparse
import sys

BLUE='\033[94m'
RED='\033[91m'
GREEN='\033[92m'
YELLOW='\033[93m'
CLEAR='\x1b[0m'

print(BLUE + "RepoHunt[1.0] by ARPSyndicate" + CLEAR)
print(YELLOW + "hunt github repositories by keywords" + CLEAR)

if len(sys.argv)<2:
	print(RED + "[!] ./repohunt --help" + CLEAR)
	sys.exit()

else:
    parser = optparse.OptionParser()
    parser.add_option('-o', '--output', action="store", dest="output", help="output file")
    parser.add_option('-v', '--verbose', action="store_true", dest="verbose", help="prints error messages [default=false]", default=False)
    parser.add_option('-f', '--forks', action="store_true", dest="forks", help="include forks [default=false]", default=False)
    parser.add_option('-s', '--sleep', action="store", dest="sleep", help="sleep after each request in seconds [default=3]", default=3)
    parser.add_option('-k', '--keyword', action="store", dest="keyword", help="keyword to hunt for")
    parser.add_option('-t', '--token', action="store", dest="token", help="github token")
	
inputs,args  = parser.parse_args()
if not inputs.keyword:
	parser.error(RED + "[!] keyword not given" + CLEAR)
if not inputs.token:
	parser.error(RED + "[!] github token not given" + CLEAR)

output = str(inputs.output)
token = str(inputs.token)
search_key = str(inputs.keyword)
timeout = inputs.sleep
verbose = inputs.verbose
forks = inputs.forks


headers = {'Authorization': f'Bearer {token}'}
result = []

def search_repos():
    global timeout,headers,search_key
    if verbose:
        print(GREEN + "[*] Searching in Repositories" + CLEAR)
    items = []
    page = 1
    repos = []
    while(True):
        try:
            repos_res = requests.get("https://api.github.com/search/repositories?q={0}&per_page=100&page={1}".format(search_key,page), headers=headers)
            items.extend(repos_res.json()['items'])
        except:
            break
        page = page +1
        time.sleep(timeout)
    for res in items:
        repos.append(res['html_url'].replace("https://github.com/","").split("/")[0]+"/"+res['html_url'].replace("https://github.com/","").split("/")[1])
    if verbose:
        print(BLUE + "[+] Found {0} mentions".format(len(repos)) + CLEAR)
    return repos

def search_issues():
    global timeout,headers,search_key
    if verbose:
        print(GREEN + "[*] Searching in Issues & PRs" + CLEAR)
    items = []
    page = 1
    repos = []
    while(True):
        try:
            issues_res = requests.get("https://api.github.com/search/issues?q={0}&per_page=100&page={1}".format(search_key,page), headers=headers)
            items.extend(issues_res.json()['items'])
        except:
            break
        page = page +1
        time.sleep(timeout)
    for res in items:
        repos.append(res['html_url'].replace("https://github.com/","").split("/")[0]+"/"+res['html_url'].replace("https://github.com/","").split("/")[1])
    if verbose:
        print(BLUE + "[+] Found {0} mentions".format(len(repos)) + CLEAR)
    return repos


def search_commits():
    global timeout,headers,search_key
    if verbose:
        print(GREEN + "[*] Searching in Commits" + CLEAR)
    items = []
    page = 1
    repos = []
    while(True):
        try:
            commits_res = requests.get("https://api.github.com/search/commits?q={0}&per_page=100&page={1}".format(search_key,page), headers=headers)
            items.extend(commits_res.json()['items'])
        except:
            break
        page = page +1
        time.sleep(timeout)
    for res in items:
        repos.append(res['html_url'].replace("https://github.com/","").split("/")[0]+"/"+res['html_url'].replace("https://github.com/","").split("/")[1])
    if verbose:
        print(BLUE + "[+] Found {0} mentions".format(len(repos)) + CLEAR)
    return repos


def search_code():
    global timeout,headers,search_key
    if verbose:
        print(GREEN + "[*] Searching in Codes" + CLEAR)
    items = []
    page = 1
    repos = []
    while(True):
        try:
            code_res = requests.get("https://api.github.com/search/code?q={0}&per_page=100&page={1}".format(search_key,page), headers=headers)
            items.extend(code_res.json()['items'])
        except:
            break
        page = page +1
        time.sleep(timeout)
    for res in items:
        repos.append(res['html_url'].replace("https://github.com/","").split("/")[0]+"/"+res['html_url'].replace("https://github.com/","").split("/")[1])
    if verbose:
        print(BLUE + "[+] Found {0} mentions".format(len(repos)) + CLEAR)
    return repos

def filter_fork():
    global timeout,headers,result
    if verbose:
        print(GREEN + "[*] Filtering Forks" + CLEAR)
    filter_res = []
    for rep in result:
        fork_res = requests.get("https://api.github.com/repos/{0}".format(rep), headers=headers)
        if 'parent' not in fork_res.json():
            filter_res.append(rep)
        time.sleep(timeout)
    if verbose:
        print(BLUE + "[+] Removed {0} forks".format(len(result)-len(filter_res)) + CLEAR)
    return filter_res

result.extend(search_repos())
result.extend(search_issues())
result.extend(search_commits())
result.extend(search_code())
count = len(result)
if verbose:
    print(GREEN + "[*] Filtering Duplicates" + CLEAR)
result = list(set(result))
result.sort()
if verbose:
    print(BLUE + "[+] Removed {0} duplicates".format(count-len(result)) + CLEAR)
if not forks:
    result = filter_fork()
for item in result:
    print("https://github.com/"+item)
if inputs.output:
	with open(output, 'a') as f:
		f.writelines("https://github.com/%s\n" % line for line in result)
print(YELLOW + "done"+ CLEAR)