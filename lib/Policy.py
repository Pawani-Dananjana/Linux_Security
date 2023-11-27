import re
from lib.Config import policyPath

path = policyPath
config = {}
Rules = []

# Load policy file
def loadPolTxt(path):
    txt = ''
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if(line.strip().startswith('#')):
                pass
            else:
                txt = txt + line
        f.close()
    return txt

# Load variables from the policy file
def loadPolVar(txt):
    global config
    txt = re.sub('#.*?\n', '\n', txt)
    globalvartxt = re.compile(r'@@section GLOBAL(.*?)@@section FS')
    try:
        globalvar = globalvartxt.search(txt.replace('\n', '')).group(1)
        globalvar = re.sub('\s', '', globalvar)
        varname = re.findall(r'(\w*?)=', globalvar)
        varvalue = re.findall(r'=(.*?);', globalvar)
        for i in range(len(varname)):
            config[varname[i]] = varvalue[i].replace('\"', '')
    except:
        pass
    return config

# Load rules from the policy file
def loadPolRules(txt):
    global Rules
    txt = re.sub('#.*\n', '\n', txt)
    # Replace variables in the policy file
    for globalvar in config:
        txt = txt.replace('$(' + globalvar + ')', config[globalvar])
    results = re.findall('\((.*?)\).*?{(.*?)}', txt, re.S | re.M)
    for rule in results:
        txt = rule[0].replace('=', ':')
        Rulekey = re.sub('(\w*?):', '"\\1":', txt.replace(' ', ''), re.M).replace('false', '0').replace('true', '1')
        Rule = eval('{' + Rulekey + '}')
        txt = rule[1].replace('->', ':')
        txt = re.sub('[ \t\f\r\v]', '', txt)
        txt = re.sub('!(.*?);', '\\1:"",', txt, flags=re.S | re.M)
        Rulecontent = re.sub('(.*?):', '"\\1":', txt)
        Rulecontent = re.sub(':(.*?);', ':"\\1",', Rulecontent)
        Rule['content'] = eval('{' + Rulecontent + '}')
        for path in Rule['content']:
            Rule['content'][path] = checkRules(Rule['content'][path])
        Rules.append(Rule)
    return Rules

# Parse the items to check in the rules
def checkRules(rulestr: str):
    check = ''
    ignore = ''
    c = re.findall('\+([abcdgilmnprstuCHMS]+)', rulestr)
    ig = re.findall('-([abcdgilmnprstuCHMS]+)', rulestr)
    for i in c:
        check = check + i
    for i in ig:
        ignore = ignore + i
    for i in ignore:
        if i in check:
            check = check.replace(i, '')
    return check

# Return the rule name and check items for a given path
def setRule(path: str):
    dir = path.split('/')
    pathnew = []
    for Rule in Rules:
        RuleContent = Rule['content']
        for RulePath in RuleContent:
            if RulePath.startswith('r'):
                reRule = re.search("r'(.*?)'", RulePath)
                try:
                    reRule = reRule.group(1)
                except:
                    print('Error in writing regular expression in the policy file ->', RulePath)
                    print('Correct writing format ->', "r'/home.*'")
                if re.search(reRule, path) != None:
                    return Rule['rulename'], RuleContent[RulePath]

    for i in range(len(dir)):
        a = '/'
        a = a.join(dir[:i + 1])
        if a == '':
            a = '/'
        pathnew.append(a)
    pathnew.reverse()
    for i in pathnew:
        for Rule in Rules:
            if i in Rule['content']:
                return Rule['rulename'], Rule['content'][i]

# Get severity level for a given rule name
def getSeverity(ruleName: str):
    for rule in Rules:
        if ruleName in rule:
            if 'severity' in rule:
                return rule['severity']
            else:
                return 0
        else:
            print('Incorrect rule name')

# Load the policy file
def loadPol():
    global Rules
    try:
        txt = loadPolTxt(path=path)
        try:
            loadPolVar(txt)
            Rules = loadPolRules(txt)
            return {'code': 200, 'msg': 'Successfully opened the file', 'rules': Rules}
        except:
            return {'code': 1002, 'msg': 'Failed to load file format'}
    except:
        return {'code': 1001, 'msg': 'Failed to open the file'}


result = loadPol()
if result['code'] == 200:
    print('Policy file loaded successfully')
else:
    print(result['msg'])
    exit()
# print(Rules)

