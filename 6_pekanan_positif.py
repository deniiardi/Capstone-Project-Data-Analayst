import numpy as np
import pandas as pd
import requests
resp_jateng = requests.get('https://data.covid19.go.id/public/api/prov_detail_JAWA_TENGAH.json', verify=False)
cov_jateng_raw = resp_jateng.json()
cov_jateng = pd.DataFrame(cov_jateng_raw['list_perkembangan'])

cov_jateng_tidy = (cov_jateng.drop(columns=[item for item in cov_jateng.columns 
                                               if item.startswith('AKUMULASI') 
                                                  or item.startswith('DIRAWAT')])
                           .rename(columns=str.lower)
                           .rename(columns={'kasus': 'kasus_baru'})
                  )
cov_jateng_tidy['tanggal'] = pd.to_datetime(cov_jateng_tidy['tanggal']*1e6, unit='ns')

cov_jateng_pekanan = (cov_jateng_tidy.set_index('tanggal')['kasus_baru']
                                   .resample('W')
                                   .sum()
                                   .reset_index()
                                   .rename(columns={'kasus_baru': 'jumlah'})
                    )
cov_jateng_pekanan['tahun'] = cov_jateng_pekanan['tanggal'].apply(lambda x: x.year)
cov_jateng_pekanan['pekan_ke'] = cov_jateng_pekanan['tanggal'].apply(lambda x: x.weekofyear)
cov_jateng_pekanan = cov_jateng_pekanan[['tahun', 'pekan_ke', 'jumlah']]

cov_jateng_pekanan['jumlah_pekanlalu'] = cov_jateng_pekanan['jumlah'].shift().replace(np.nan, 0).astype(np.int)
cov_jateng_pekanan['lebih_baik'] = cov_jateng_pekanan['jumlah'] < cov_jateng_pekanan['jumlah_pekanlalu']

import matplotlib.pyplot as plt

plt.clf()
jml_tahun_terjadi_covid19 = cov_jateng_pekanan['tahun'].nunique()
tahun_terjadi_covid19 = cov_jateng_pekanan['tahun'].unique()
fig, axes = plt.subplots(nrows=jml_tahun_terjadi_covid19,
            figsize=(10,3*jml_tahun_terjadi_covid19))

fig.suptitle('Kasus Pekanan Positif COVID-19 di Jawa Tengah \nPeriode Februari 2020 - Oktober 2022',
      y=1.00, fontsize=16, fontweight='bold', ha='center')
for i, ax in enumerate(axes):
  ax.bar(data=cov_jateng_pekanan.loc[cov_jateng_pekanan['tahun']==tahun_terjadi_covid19[i]],
      x='pekan_ke', height='jumlah',
      color=['mediumseagreen' if x is True else 'salmon'
        for x in cov_jateng_pekanan['lebih_baik']])
  if i == 0:
    ax.set_title('Kolom hijau menunjukkan penambahan kasus baru lebih sedikit dibandingkan satu pekan sebelumnya', 
           fontsize=10)
  elif i == jml_tahun_terjadi_covid19-1:
    ax.text(1, -0.3, 'Sumber data: covid19.go.id', color='blue',
      ha='right', transform=ax.transAxes)
      
  ax.set_xlim([0, 52.5])
  ax.set_ylim([0, max(cov_jateng_pekanan['jumlah'])])
  ax.set_xlabel('')
  ax.set_ylabel('Jumlah kasus %d'%(tahun_terjadi_covid19[i],))
  ax.grid(axis='y')
      
plt.tight_layout()
plt.show()
