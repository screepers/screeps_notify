import importlib
from config import settings
driver_cache = {}
service_cache = {}
assert 'services' in settings
services = settings['services']


def getMessengerDriver(name):
    if name in service_cache:
        return service_cache[name]
    if name not in services:
        print('name not in services')
        return False
    service_settings = services[name]
    if 'type' not in service_settings:
        print('driver not in service settings')
        return False
    driver_module = getDriverModule(service_settings['type'])
    driver_class = getattr(driver_module, service_settings['type'])
    driver = driver_class(service_settings)

    service_cache[name] = driver
    return driver


# Dynamically import module
def getDriverModule(driver):
    if driver in driver_cache:
        return driver_cache[driver]
    driver = 'services.messengers.%s' % (driver,)
    driver_cache[driver] = importlib.import_module(driver, 'screeps_notify')
    return driver_cache[driver]
