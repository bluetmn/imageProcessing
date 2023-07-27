import ee
import folium
import matplotlib.pyplot as plt


service_account = 'my-service-account@...gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, '.private-key.json')
ee.Initialize(credentials)

# print(ee.Image("NASA/NASADEM_HGT/001").get("title").getInfo())

# ################################################
# # dem = ee.Image('USGS/SRTMGL1_003')
# # xy = ee.Geometry.Point([86.9250, 27.9881])
# # elev = dem.sample(xy, 30).first().get('elevation').getInfo()
# # print('Mount Everest elevation (m):', elev)
# ################################################

# region_of_interest = ee.Geometry.Rectangle([-122.5, 37.5, -122.3, 37.7])

# # Filter Sentinel-2 imagery by your region of interest and date range
# sentinel2_collection = ee.ImageCollection('COPERNICUS/S2_SR')\
#     .filterBounds(region_of_interest)\
#     .filterDate('2021-01-01', '2021-01-31')

# # Get the first image from the collection (you can also choose a specific image from the collection)
# sample_image = sentinel2_collection.first()

# #get image geometry
# sample_image_geometry = sample_image.geometry()

# #get bound of image latitude and longitude
# bounds = sample_image_geometry.bounds().getInfo()["coordinates"][0]

# print(bounds)

# minLong, minLat = bounds[0]
# maxLong, maxLat = bounds[2]

# bound_box = [minLong, minLat, minLong + .1, minLat + .1]

# roi = ee.Geometry.Rectangle(bound_box)

# clipped_image = sample_image.clip(roi)

# # Visualization parameters for RGB (Red, Green, Blue) bands
# vis_params = {
#     "bands": ['B4', 'B3', 'B2'],  # Red, Green, Blue bands
#     "min": 0,                      # Minimum pixel value
#     "max": 3000                   # Maximum pixel value
# }

# # Get a thumbnail URL for the image
# thumbnail_url = clipped_image.visualize(**vis_params).getThumbURL()

# # Display the thumbnail on a map using Folium
# map_center = [clipped_image.geometry().centroid().getInfo()['coordinates'][1],
#               clipped_image.geometry().centroid().getInfo()['coordinates'][0]]
# map = folium.Map(location=map_center, zoom_start=8)
# folium.Marker(location=map_center).add_to(map)
# folium.TileLayer(thumbnail_url, attr="Google Earth Engine", overlay=True, noWrap=True).add_to(map)
# map.save("sample_map.html")


aqCollection = ee.ImageCollection("COPERNICUS/S5P/NRTI/L3_AER_AI")

roi = ee.Geometry.Point([-93.26, 44.977])

start_date = '2023-01-01'
end_date = '2023-07-24'

filtered_aq = aqCollection.filterBounds(roi).filterDate(start_date, end_date)
print(filtered_aq.first().select('absorbing_aerosol_index').getInfo())


def get_AAI(image):
    return image.select('absorbing_aerosol_index')

time_series = filtered_aq.map(get_AAI)

AAI_values_list = time_series.getRegion(roi, scale=30).getInfo()

dates = [value[0] for value in AAI_values_list[1:]]
values = [value[-1] for value in AAI_values_list[1:]]

c = 0
while c < len(values):
    if values[c] == None:
        values.pop(c)
        dates.pop(c)
    else:
        c += 1

reducedDates = []
for c in range(len(dates)):
    if dates[c][4] == 0:
        newDate = dates[c][5:6] + '-' + dates[c][6:8]
    else:
        newDate = dates[c][4:6] + '-' + dates[c][6:8]
    dates[c] = newDate
    if c % 10 == 0:
        reducedDates.append(newDate)

print(dates)
print('\n\n\n')
print(values)


# Plot the time series
plt.figure(figsize=(10, 6))
plt.plot(dates, values, marker='o')
plt.xlabel('Date')
plt.ylabel('AAI')
plt.title(f'AAI Time Series')
plt.xticks(rotation=45)
plt.xticks(reducedDates)
plt.grid(True)
plt.tight_layout()
plt.show()


