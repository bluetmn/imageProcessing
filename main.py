import ee
service_account = 'my-service-account@...gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, '.private-key.json')
ee.Initialize(credentials)

print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())
