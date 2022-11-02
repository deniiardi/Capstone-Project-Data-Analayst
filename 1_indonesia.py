import requests
resp = requests.get('https://data.covid19.go.id/public/api/update.json', verify=False)
cov_id_raw = resp.json()
cov_id_update = cov_id_raw['update']

print('Identifikasi Kasus Coronavirus (COVID-19) di Indonesia')

print('Tanggal pembaharuan data penambahan kasus :', cov_id_update['penambahan']['tanggal'])
print('Jumlah penambahan kasus positif :', cov_id_update['penambahan']['jumlah_positif'])
print('Jumlah penambahan kasus dirawat :', cov_id_update['penambahan']['jumlah_dirawat'])
print('Jumlah penambahan kasus sembuh :', cov_id_update['penambahan']['jumlah_sembuh'])
print('Jumlah penambahan kasus meninggal :', cov_id_update['penambahan']['jumlah_meninggal'])
print('Jumlah total kasus positif hingga saat ini :', cov_id_update['total']['jumlah_positif'])
print('Jumlah total kasus dirawat hingga saat ini:', cov_id_update['total']['jumlah_dirawat'])
print('Jumlah total kasus sembuh hingga saat ini:', cov_id_update['total']['jumlah_sembuh'])
print('Jumlah total kasus meninggal hingga saat ini:', cov_id_update['total']['jumlah_meninggal'])
