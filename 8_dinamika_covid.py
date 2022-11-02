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

cov_jateng_akumulasi = cov_jateng_tidy[['tanggal']].copy()
cov_jateng_akumulasi['akumulasi_aktif'] = (cov_jateng_tidy['kasus_baru'] - cov_jateng_tidy['sembuh'] - cov_jateng_tidy['meninggal']).cumsum()
cov_jateng_akumulasi['akumulasi_sembuh'] = cov_jateng_tidy['sembuh'].cumsum()
cov_jateng_akumulasi['akumulasi_meninggal'] = cov_jateng_tidy['meninggal'].cumsum()

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.clf()
fig, ax = plt.subplots(figsize=(10,5))
cov_jateng_akumulasi_ts = cov_jateng_akumulasi.set_index('tanggal')
cov_jateng_akumulasi_ts.plot(kind='line', ax=ax, lw=3,
						   color=['salmon','slategrey','olivedrab'])

ax.set_title('Dinamika Kasus COVID-19 di Jawa Tengah',
			y=1, fontsize=16, fontweight='bold', ha='center')
ax.set_xlabel('')
ax.set_ylabel('Akumulasi aktif')
ax.text(1, -0.2, 'Sumber data: covid19.go.id', color='blue',
	   ha='right', transform=ax.transAxes)

plt.grid()
plt.tight_layout()
plt.show()
