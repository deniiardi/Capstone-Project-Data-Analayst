import requests
resp_jateng = requests.get('https://data.covid19.go.id/public/api/prov_detail_JAWA_TENGAH.json', verify=False)
cov_jateng_raw = resp_jateng.json()

print('Nama-nama elemen utama:\n', cov_jateng_raw.keys())
print('\nJumlah total kasus COVID-19 di Jawa Tengah : %d' %cov_jateng_raw['kasus_total'])
print('Persentase kematian akibat COVID-19 di Jawa Tengah : %f.2%%' %cov_jateng_raw['meninggal_persen'])
print('Persentase tingkat kesembuhan dari COVID-19 di Jawa Tengah : %f.2%%' %cov_jateng_raw['sembuh_persen'])
