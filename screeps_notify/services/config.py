import os
import sys
import yaml

settings = False
cwd = os.getcwd()
path = cwd + '/.settings.yaml'
assert os.path.isfile(path)
with open(path, 'r') as f:
    settings = yaml.load(f)

def getSettings():
    return settings

def getServicesFromGroups(groups):
    ret_services = []
    for group in groups:
        if group in settings['groups']:
            if settings['groups'][group] == 'all':
                return list(settings['services'].keys())
            for service in settings['groups'][group]:
                if service not in ret_services:
                    ret_services.append(service)
    if len(ret_services) < 1:
        if 'default' not in groups:
            return getServicesFromGroups(['default'])
    return ret_services
