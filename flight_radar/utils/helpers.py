def field_mapper(data: dict) -> dict:
    if data.get('flyFrom'):
        data['flight_from_code'] = data.get('flyFrom')
    if data.get('flyTo'):
        data['flight_to_code'] = data.get('flyTo')
    if data.get('cityFrom'):
        data['city_from'] = data.get('cityFrom')
    if data.get('cityTo'):
        data['city_to'] = data.get('cityTo')
    if data.get('baglimit'):
        data['bag_limit'] = data.get('baglimit')
    if data.get('conversion'):
        data['price_conversion'] = data.get('conversion')
    if data.get('countryTo'):
        data['country_to_code'] = data.get('countryTo').get('code')
    if data.get('countryFrom'):
        data['country_from_code'] = data.get('countryFrom').get('code')
    if data.get('conversion'):
        data['price_conversion'] = data.get('conversion')

    return data
