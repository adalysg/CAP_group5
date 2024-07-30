"""
Converts the raw data from kaggle to "cleaned_airbnb" data. 
This data contains only the [beds, bedrooms, guests, price, city, state, country] columns.
"""

import pandas as pd

# For converting from local currency to USD
currency_conversion_to_usd = {
    'Puerto Rico': 1.0,  # USD to USD (Puerto Rico uses USD)
    'Maldives': 0.065,  # MVR to USD
    'Åland Islands': 1.1,  # EUR to USD (Åland Islands use Euro)
    'Poland': 0.26,  # PLN to USD
    'Albania': 0.0092,  # ALL to USD
    'Hungary': 0.0034,  # HUF to USD
    'France': 1.1,  # EUR to USD
    'Costa Rica': 0.0017,  # CRC to USD
    'Saudi Arabia': 0.27,  # SAR to USD
    'Serbia': 0.0092,  # RSD to USD
    'Egypt': 0.032,  # EGP to USD
    'Bolivia': 0.14,  # BOB to USD
    'Kyrgyzstan': 0.011,  # KGS to USD
    'India': 0.012,  # INR to USD
    'Sweden': 0.11,  # SEK to USD
    'Sri Lanka': 0.0031,  # LKR to USD
    'Greece': 1.1,  # EUR to USD
    'Fiji': 0.45,  # FJD to USD
    'Congo': 0.0016,  # CDF to USD
    'Ukraine': 0.027,  # UAH to USD
    'Croatia': 0.16,  # HRK to USD
    'Armenia': 0.0025,  # AMD to USD
    'Argentina': 0.010,  # ARS to USD
    'Kazakhstan': 0.0023,  # KZT to USD
    'New Zealand': 0.61,  # NZD to USD
    'Kenya': 0.0071,  # KES to USD
    'Cyprus': 1.1,  # EUR to USD
    'Romania': 0.22,  # RON to USD
    'Germany': 1.1,  # EUR to USD
    'Uruguay': 0.026,  # UYU to USD
    'Portugal': 1.1,  # EUR to USD
    'Mexico': 0.053,  # MXN to USD
    'Finland': 1.1,  # EUR to USD
    'Malaysia': 0.22,  # MYR to USD
    'Canada': 0.75,  # CAD to USD
    'Philippines': 0.018,  # PHP to USD
    'Seychelles': 0.074,  # SCR to USD
    'United Kingdom': 1.3,  # GBP to USD
    'Vietnam': 0.000043,  # VND to USD
    'Panama': 1.0,  # USD to USD (Panama uses USD)
    'Oman': 2.60,  # OMR to USD
    'Svalbard & Jan Mayen': 0.10,  # NOK to USD (Norwegian Krone)
    'Taiwan': 0.032,  # TWD to USD
    'Italy': 1.1,  # EUR to USD
    'Guadeloupe': 1.1,  # EUR to USD
    'South Korea': 0.00084,  # KRW to USD
    'Malta': 1.1,  # EUR to USD
    'United States': 1.0,  # USD to USD
    'Mauritius': 0.023,  # MUR to USD
    'Jamaica': 0.0065,  # JMD to USD
    'St Martin': 1.1,  # EUR to USD (French side)
    'Hong Kong': 0.13,  # HKD to USD
    'Iceland': 0.0073,  # ISK to USD
    'Belgium': 1.1,  # EUR to USD
    'Norway': 0.10,  # NOK to USD
    'Turkey': 0.036,  # TRY to USD
    'Australia': 0.65,  # AUD to USD
    'Spain': 1.1,  # EUR to USD
    'Slovenia': 1.1,  # EUR to USD
    'Tunisia': 0.32,  # TND to USD
    'Brazil': 0.19,  # BRL to USD
    'Latvia': 1.1,  # EUR to USD
    'Honduras': 0.041,  # HNL to USD
    'Czechia': 0.045,  # CZK to USD
    'United Arab Emirates': 0.27,  # AED to USD
    'Belize': 0.50,  # BZD to USD
    'Nicaragua': 0.027,  # NIO to USD
    'French Polynesia': 0.0091,  # XPF to USD
    'Lebanon': 0.000066,  # LBP to USD
    'Chile': 0.0013,  # CLP to USD
    'Lithuania': 1.1,  # EUR to USD
    'Madagascar': 0.00022,  # MGA to USD
    'Rwanda': 0.00085,  # RWF to USD
    'Cayman Islands': 1.2,  # KYD to USD
    'Jordan': 1.41,  # JOD to USD
    'Cuba': 0.038,  # CUP to USD
    'Ireland': 1.1,  # EUR to USD
    'Greenland': 0.15,  # DKK to USD
    'Uganda': 0.00027,  # UGX to USD
    'Netherlands': 1.1,  # EUR to USD
    'Pakistan': 0.0036,  # PKR to USD
    'Vanuatu': 0.0084,  # VUV to USD
    'Mongolia': 0.00034,  # MNT to USD
    'Morocco': 0.10,  # MAD to USD
    'Indonesia': 0.000066,  # IDR to USD
    'Switzerland': 1.1,  # CHF to USD
    'Bulgaria': 0.57,  # BGN to USD
    'Thailand': 0.032,  # THB to USD
    'Bosnia & Herzegovina': 0.57,  # BAM to USD
    'Myanmar': 0.00047,  # MMK to USD
    'Kuwait': 3.29,  # KWD to USD
    'Cambodia': 0.00024,  # KHR to USD
    'Bangladesh': 0.012,  # BDT to USD
    'Bahamas': 1.0,  # BSD to USD
    'Namibia': 0.071,  # NAD to USD
    'South Africa': 0.071,  # ZAR to USD
    'Montenegro': 1.1,  # EUR to USD
    'Georgia': 0.37,  # GEL to USD
    'Colombia': 0.00025,  # COP to USD
    'Tanzania': 0.00043,  # TZS to USD
    'Estonia': 1.1,  # EUR to USD
    'Nepal': 0.0075,  # NPR to USD
    'Slovakia': 1.1,  # EUR to USD
    'Austria': 1.1,  # EUR to USD
    'Israel': 0.28,  # ILS to USD
    'Japan': 0.009,  # JPY to USD
    'Peru': 0.27,  # PEN to USD
    'Guatemala': 0.13,  # GTQ to USD
    'Brunei': 0.74,  # BND to USD
    'Uzbekistan': 0.000082,  # UZS to USD
    'Denmark': 0.15,  # DKK to USD
}

df_raw = pd.read_csv('airbnb.csv')

# Remove extraneous attributes
df = df_raw[['address', 'price', 'bathrooms', 'beds', 'guests', 'bedrooms']]

# If number of commas is over 2, then it is split into more than just city, state, country -> removed for easier parsing
for index, row in df.iterrows():
	commas = 0
	for char in row['address']:
		if char == ',':
			commas += 1
	if commas != 2:
		df = df.drop(index)

df[['city', 'state/province', 'country']] = df['address'].str.split(", ",expand=True)
df = df.drop(['address'], axis=1)

cleaned = df.dropna()

# Converting the local currencies to USD.
prices_list = cleaned['price'].to_list()
countries_list = cleaned['country'].to_list()

new_prices_converted = []
for i in range(0, len(prices_list)):
	new_prices_converted.append(prices_list[i]*currency_conversion_to_usd[countries_list[i]])

cleaned['price'] = new_prices_converted

# Make a new CSV file with the converted currencies.
cleaned.to_csv('cleaned_airbnb.csv', sep=',', encoding='utf-8', index=False, header=True)
