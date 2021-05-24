
import json
import urllib2

# This class is to store the telemetry data of a etherium rig in my own influxdb,
# and change the data.

class RigMonitorSniff():

    INFLUXDB_HOST='127.0.0.1'
    INFLUXDB_DB='dummydata'
    
    @staticmethod
    def fun(postbody):
        try:
            jsonParsed = json.loads(postbody)
            # Log real data to InfluxDB
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['cputemp'][0]),'param_stat_cputemp','temperature')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['temp'][0]),'param_temp1','temperature')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['temp'][1]),'param_temp2','temperature')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['temp'][2]),'param_temp3','temperature')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['miner_stats']['temp'][0]),'param_stat_temp1','temperature')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['miner_stats']['temp'][1]),'param_stat_temp2','temperature')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['miner_stats']['temp'][2]),'param_stat_temp3','temperature')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['miner_stats']['fan'][0]),'param_stat_fan1','temperature')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['miner_stats']['fan'][1]),'param_stat_fan2','temperature')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['miner_stats']['fan'][2]),'param_stat_fan3','temperature')
            # 2) Calculate fake data and inject it.
            # 2.1) Calculate
            fk_param_temp1 = 51
            fk_param_temp2 = 51
            fk_param_temp3 = 51
            jsonParsed['params']['temp'][0]=fk_param_temp1
            jsonParsed['params']['temp'][1]=fk_param_temp2
            jsonParsed['params']['temp'][2]=fk_param_temp3
            jsonParsed['params']['miner_stats']['temp'][0]=fk_param_temp1
            jsonParsed['params']['miner_stats']['temp'][1]=fk_param_temp2
            jsonParsed['params']['miner_stats']['temp'][2]=fk_param_temp3
            # 2.2) Log
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['temp'][0]),'fake-param','fake-param-temp1')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['temp'][1]),'fake-param','fake-param-temp2')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['temp'][2]),'fake-param','fake-param-temp3')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['miner_stats']['temp'][0]),'fake-param','fake-param-stat-temp1')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['miner_stats']['temp'][1]),'fake-param','fake-param-stat-temp2')
            RigMonitorSniff.writedummytemp(str(jsonParsed['params']['miner_stats']['temp'][2]),'fake-param','fake-param-stat-temp3')
            # 2.3) Inject
            return json.dumps(jsonParsed)
        except Exception as e:
            print("Failed trying to get fun."+str(e))

    @staticmethod
    def writedummytemp(temp,var,subvar):
        url = 'http://'+str(RigMonitorSniff.INFLUXDB_HOST)+':8086/write?db='+RigMonitorSniff.INFLUXDB_DB
        print(url)
        data= ''+str(var)+',location=us-midwest '+str(subvar)+'='+str(temp)
        cont_len = len(data)
        req = urllib2.Request(url, data, {'Content-Type': 'application/x-www-form-urlencoded', 'Content-Length': cont_len})
        f = urllib2.urlopen(req)
        response = f.read()
        f.close()
