   
def pmdata(data):
    result = {}     
    result["pm_ug_per_m3"] = {}
    result["pm_per_1l_air"] = {}
    result["pm_ug_per_m3"]["atmospheric_environment=True"] = {}
    result["pm_ug_per_m3"]["atmospheric_environment=False"] = {}
    result["pm_ug_per_m3"]["atmospheric_environment=True"]["1.0"] = data.pm_ug_per_m3(1.0,atmospheric_environment=True)
    result["pm_ug_per_m3"]["atmospheric_environment=True"]["2.5"] = data.pm_ug_per_m3(2.5,atmospheric_environment=True)
    result["pm_ug_per_m3"]["atmospheric_environment=True"]["None"] =data.pm_ug_per_m3(None,atmospheric_environment=True)
    result["pm_ug_per_m3"]["atmospheric_environment=False"]["1.0"] = data.pm_ug_per_m3(1.0,atmospheric_environment=False)
    result["pm_ug_per_m3"]["atmospheric_environment=False"]["2.5"] = data.pm_ug_per_m3(2.5,atmospheric_environment=False)
    result["pm_ug_per_m3"]["atmospheric_environment=False"]["10.0"] =data.pm_ug_per_m3(10,atmospheric_environment=False)
    result["pm_per_1l_air"]["0.3"] =data.pm_per_1l_air(0.3)
    result["pm_per_1l_air"]["0.5"] =data.pm_per_1l_air(0.5)
    result["pm_per_1l_air"]["1.0"] =data.pm_per_1l_air(1.0)
    result["pm_per_1l_air"]["2.5"] =data.pm_per_1l_air(2.5)
    result["pm_per_1l_air"]["5.0"] =data.pm_per_1l_air(5)
    result["pm_per_1l_air"]["10"] =data.pm_per_1l_air(10)
    return result

def pmdatadescribe():
    result = {}     
    result["pm_ug_per_m3"] = {}
    result["pm_per_1l_air"] = {}
    result["pm_ug_per_m3"]["atmospheric_environment=True"] = {}
    result["pm_ug_per_m3"]["atmospheric_environment=False"] = {}
    result["pm_ug_per_m3"]["atmospheric_environment=True"]["1.0"] = "PM1.0 ug/m3 (atmos env)"
    result["pm_ug_per_m3"]["atmospheric_environment=True"]["2.5"] = "PM2.5 ug/m3 (atmos env)" 
    result["pm_ug_per_m3"]["atmospheric_environment=True"]["None"] = "PM10 ug/m3 (atmos env)"
    result["pm_ug_per_m3"]["atmospheric_environment=False"]["1.0"] = "PM1.0 ug/m3 (ultrafine particles)"
    result["pm_ug_per_m3"]["atmospheric_environment=False"]["2.5"] = "PM2.5 ug/m3 (combustion particles, organic compounds, metals)"
    result["pm_ug_per_m3"]["atmospheric_environment=False"]["10.0"] = "PM10 ug/m3 (dust, pollen, mould spores)"
    result["pm_per_1l_air"]["0.3"] = ">0.3um in 0.1L air"
    result["pm_per_1l_air"]["0.5"] = ">0.5um in 0.1L air"
    result["pm_per_1l_air"]["1.0"] = ">1.0um in 0.1L air"
    result["pm_per_1l_air"]["2.5"] = ">2.5um in 0.1L air"
    result["pm_per_1l_air"]["5.0"] = ">5.0um in 0.1L air"
    result["pm_per_1l_air"]["10"] = ">10um in 0.1L air"
    return result
