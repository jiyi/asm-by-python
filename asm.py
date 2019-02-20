import requests
# import urllib
import base64
import time

hostname='http://172.20.2.115'
username = ''
password = ''
# deviceId = '70378'
ip = ''
mac = ''

def str_base64(string):
  return bytes.decode(base64.b64encode(str.encode(string)))

def str_dict(string):
  length = 'length'
  def parseInt(num):
    return int(num)

  sdict = string[string.index(r'{'):]
  return eval(sdict)

def create_dev_xml(ip, mac):
  dev_xml = []
  dev_xml.append(r'<?xml version="1.0" encoding="gb2312"?><MSAC><DeviceName>MSHOME\jiy</DeviceName><OS>MACVersion 10.14.3 (Build 18D109)</OS><Ip>')
  dev_xml.append(ip)
  dev_xml.append(r'</Ip><Mac>')
  dev_xml.append(mac)
  dev_xml.append(r'</Mac><IeVersion>Safari</IeVersion><Mark>255.255.255.0</Mark><GateWay></GateWay><DiskId>49C8BE1C7BC45BE9A4846F61AD9D7CEA</DiskId></MSAC>')
  return ''.join(dev_xml)

# dev_xml = create_dev_xml(ip, mac)
# dev_xml = urllib.parse.quote(dev_xml, safe='')
# print(dev_xml)

getDeviceInfo = {
  'tradecode': 'getdeviceinfoprocess',
  'gettype': 'control',
  'depart_id': '0',
  'username': 'python',
  'tel': '',
  'remark': 'iosagent',
  'device_id': '',
  'positions': '',
  'dev_xml': create_dev_xml(ip, mac),
  'is_mobile': '1',
  'is_guest': '0',
  'os_platform': 'MAC'
}

# def get_deviceId():
#   return deviceId

def get_netAuth(deviceId):
  return {
  'tradecode': 'net_auth',
  'type': 'User',
  'user_name': str_base64(username),
  'password': str_base64(password),
  'deviceid': deviceId,
  'is_mobile': '1'
}

# netAuth = {
#   'tradecode': 'net_auth',
#   'type': 'User',
#   'user_name': str_base64(username),
#   'password': str_base64(password),
#   'deviceid': get_deviceId(),
#   'is_mobile': '1'
# }

# keepMacAlive = requests.get(hostname + '/KeepMacAlive.html', params={'deviceid': deviceId})
# r = requests.get(hostname + '/a/ajax.php', params = getDeviceInfo)
# r = requests.get(hostname + '/a/ajax.php', params = netAuth)
# print(str_dict(r.text)['DeviceID'])

# print(get_netAuth())
# deviceId = 2
# print(get_netAuth())

while True:
  checkStatus = requests.get(hostname + '/a/ajax.php', params = getDeviceInfo)
  deviceId = str_dict(checkStatus.text)['DeviceID']
  longin = requests.get(hostname + '/a/ajax.php', params = get_netAuth(deviceId))
  print(longin.text)

  # time.sleep(60)

  newDeviceId = deviceId
  while newDeviceId == deviceId:
    keepMacAlive = requests.get(hostname + '/KeepMacAlive.html', params={'deviceid': deviceId})
    print(keepMacAlive.text)
    checkStatus = requests.get(hostname + '/a/ajax.php', params = getDeviceInfo)
    newDeviceId = str_dict(checkStatus.text)['DeviceID']
    time.sleep(30)
