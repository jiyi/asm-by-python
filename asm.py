import requests
import base64
import time
import configparser

# 读取配置文件
cfg = configparser.ConfigParser()
cfg.read('config.ini')
hostname = cfg.get('user', 'hostname')
username = cfg.get('user', 'username')
password = cfg.get('user', 'password')
ip = cfg.get('user', 'ip')
mac = cfg.get('user', 'mac')

# 字符串转base64编码，用于转换用户名和密码
def str_base64(string):
  return bytes.decode(base64.b64encode(str.encode(string)))

# 字符串转字典型，用于转换从服务器得到的结果
def str_dict(string):
  # 在eval()中用到以下两个变量
  length = 'length'
  def parseInt(num):
    return int(num)

  sdict = string[string.index(r'{'):]
  return eval(sdict)

# 创建xml字符串用于提交查询信息
def create_dev_xml(ip, mac):
  dev_xml = []
  dev_xml.append(r'<?xml version="1.0" encoding="gb2312"?><MSAC><DeviceName>MSHOME\jiy</DeviceName><OS>MACVersion 10.14.3 (Build 18D109)</OS><Ip>')
  dev_xml.append(ip)
  dev_xml.append(r'</Ip><Mac>')
  dev_xml.append(mac)
  dev_xml.append(r'</Mac><IeVersion>Safari</IeVersion><Mark>255.255.255.0</Mark><GateWay></GateWay><DiskId>49C8BE1C7BC45BE9A4846F61AD9D7CEA</DiskId></MSAC>')
  return ''.join(dev_xml)

# 查询信息
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

# 登陆信息
def get_netAuth(deviceId):
  return {
  'tradecode': 'net_auth',
  'type': 'User',
  'user_name': str_base64(username),
  'password': str_base64(password),
  'deviceid': deviceId,
  'is_mobile': '1'
}

while True:
  checkStatus = requests.get(hostname + '/a/ajax.php', params = getDeviceInfo)
  deviceId = str_dict(checkStatus.text)['DeviceID']
  longin = requests.get(hostname + '/a/ajax.php', params = get_netAuth(deviceId))
  print(longin.text)
  time.sleep(60)
  newDeviceId = deviceId
  while newDeviceId == deviceId:
    keepMacAlive = requests.get(hostname + '/KeepMacAlive.html', params={'deviceid': deviceId})
    print(keepMacAlive.text)
    checkStatus = requests.get(hostname + '/a/ajax.php', params = getDeviceInfo)
    newDeviceId = str_dict(checkStatus.text)['DeviceID']
    time.sleep(30)
