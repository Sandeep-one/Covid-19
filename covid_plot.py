import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import num2date

df = pd.read_csv('complete.csv')
df.drop(['Latitude', 'Longitude'], inplace=True, axis=1)
df.loc[:, 'Date'] = pd.to_datetime(df.Date)
df.rename(columns={'Name of State / UT': 'State', 'Total Confirmed cases': 'Total_Cases',
                   'Cured/Discharged/Migrated': 'Discharged', 'New cases': 'New_cases'}, inplace=True)
india = df.groupby('Date').agg('sum')
delhi = df.loc[df.State == 'Delhi']
delhi.set_index('Date', inplace=True)
up = df.loc[df.State == 'Uttar Pradesh']
up.set_index('Date', inplace=True)
delhi = delhi[['New_cases']]
up = up[['New_cases']]
ndf = delhi.join(up, how='outer', lsuffix='_delhi', rsuffix='_up')
ndf.fillna(0, inplace=True)
ndf6 = ndf.loc[(ndf.index > pd.Timestamp('2020-6-1')) & (ndf.index < pd.Timestamp('2020-7-15'))]
ndf7 = ndf.loc[(ndf.index > pd.Timestamp('2020-7-15'))]

fig = plt.figure(figsize=(12.80, 7.20))
ax = [None, None]
s = plt.GridSpec(1, 3)
# fig,ax=plt.subplots(1,2,figsize=[10,5])
ax[0] = plt.subplot(s[0:2])
ax[0].plot(ndf.index, ndf.New_cases_delhi, label='Delhi', color='darkblue', lw=1.5, zorder=5)
ax[0].plot(ndf.index, ndf.New_cases_up, label='Uttar Pradesh', color='red', lw=1.5, zorder=5)
ax[0].grid(True, axis='y', zorder=0, lw=0.7, alpha=0.5)
ax[0].grid(True, axis='x', zorder=0, lw=0.5, alpha=0.4)

ax[0].fill_between(ndf.index, ndf.New_cases_delhi, ndf.New_cases_up, color='violet', alpha=0.15, zorder=6)
ax[0].legend(loc='upper left', fontsize='large')
ax[0].set_xticklabels(['March', 'April', 'May', 'June', 'July', 'August'], fontsize=13)

ax[0].spines['right'].set_visible(False)
ax[0].spines['top'].set_visible(False)
ax[0].spines['bottom'].set_visible(False)
ax[0].spines['left'].set_alpha(0.5)

ax[0].tick_params(axis='y', left=False, which='both')
ax[0].tick_params(axis='x', bottom=False, which='both')

ax[0].axvline(pd.Timestamp('2020/3/25'), color='olivedrab', lw=1, linestyle='--')
ax[0].axvline(pd.Timestamp('2020/5/31'), color='olivedrab', lw=1, linestyle='--')
ax[0].text(pd.Timestamp('2020/3/31'), 4000, '  Lock Down Period', fontstyle='italic', fontsize=18,
           backgroundcolor='whitesmoke')
ax[0].set_title('Number of New Cases of Covid-19 per Day', fontsize=20, backgroundcolor='whitesmoke',
                position=[0.5, 1.05])

# plt.savefig('g1.png')
plt.tight_layout()

# fig,ax=plt.subplots(figsize=(5,5))
ax[1] = plt.subplot(s[2])
ax[1].set_title('Average of No. of Cases', fontsize=18, fontweight='normal')
x = np.array([1, 3])
b1 = ax[1].bar(x - 0.25, [ndf6.New_cases_delhi.mean(), ndf7.New_cases_delhi.mean()], edgecolor='black', alpha=0.5,
               width=0.5, label='Delhi', color='indigo')
b2 = ax[1].bar(x + 0.25, [ndf6.New_cases_up.mean(), ndf7.New_cases_up.mean()], edgecolor='black', width=0.5, alpha=0.9,
               label='Uttar Pradesh', color='tab:red')
ax[1].set_xlim(0, 4)
ax[1].set_xticks([1, 3])
ax[1].set_xticklabels(['1-June to 7-July', '7-July to 6-August'], fontsize=12)
ax[1].set_xlabel('\nTime Period', fontsize=12)

ax[1].spines['right'].set_visible(False)
ax[1].spines['top'].set_visible(False)
ax[1].spines['left'].set_alpha(False)
ax[1].tick_params(axis='y', left=False, labelleft=False)
for b in b1:
    ax[1].text(b.get_x() + 0.01, b.get_height() - 200, '{:.0f}'.format(b.get_height()), fontweight='bold', fontsize=12)
for b in b2:
    ax[1].text(b.get_x() + 0.03, b.get_height() - 200, '{:.0f}'.format(b.get_height()), fontweight='bold', fontsize=12)

ax[1].legend(fontsize='large')
plt.tight_layout()
plt.show()

# plt.savefig('g.png', format='png', dpi=300)
