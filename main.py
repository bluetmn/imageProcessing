import ee
import folium
import matplotlib.pyplot as plt

def authenticateEE():
    service_account = 'my-service-account@...gserviceaccount.com'
    credentials = ee.ServiceAccountCredentials(service_account, '.private-key.json')
    ee.Initialize(credentials)

def graphAQ():
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

def main():
    authenticateEE()
    graphAQ()

if __name__ == "__main__":
    main()


