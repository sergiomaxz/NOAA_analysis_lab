import glob
import urllib.request
from datetime import datetime
import pandas as pd


def get_data():
    for i in range(1, 29):
        now = datetime.now()
        date_and_time = now.strftime("%d-%m-%Y_%H-%M-%S")
        url = 'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={}&year1=1981&year2=2023&type=Mean'.format(i)
        with urllib.request.urlopen(url) as wp:
            with open('obl_id{}_{}.csv'.format(i, date_and_time), 'wb') as out:
                out.write(wp.read())
        print("Файл для {} області створено.".format(i))


def create_dataframe(filename, fnumb):
    headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
    headers_usecols = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
    df = pd.read_csv(filename, header=1, names=headers, usecols=headers_usecols)
    df = df.drop(df.loc[df['VHI'] == -1].index)
    df = df.dropna()
    df.loc[0, 'Year'] = str(df.loc[0, 'Year'])[-4:]
    df['area'] = fnumb
    return df


def index_correction(df):
    indexes = ["22", "24", "23", "25", "3", "4", "8", "19", "20", "21", "9", "26", "10",
               "11", "12", "13", "14", "15", "16", "27", "17", "18", "6", "1", "2", "7", "5"]
    oldIndex = 1
    for newIndex in indexes:
        df['area'].replace({oldIndex: newIndex}, inplace=True)
        oldIndex += 1
    for newIndex in indexes:
        df['area'].replace({newIndex: int(newIndex)}, inplace=True)
    df.to_csv('obl_full.csv')
    print("Індекси були змінені\n")
    return df


def vhi_display_for_year(df, area, year):
    frame_vhi = df[(df.area == area) & (df.Year.astype(str) == str(year))]

    vhi_list = []
    for i in frame_vhi['VHI']:
        vhi_list.append(i)

    print(f'\nРяд VHI в області з індексом {area} за {year} рік: {vhi_list}')
    print(f"Максимальне значення: {frame_vhi['VHI'].max()}")
    print(f"Мінімальне значення значення: {frame_vhi['VHI'].min()}\n")


def get_drought(df, area, percent, severity=None):
    if severity is None:
        severity = input('Вкажіть тип посухи "extreme" чи "mild": ')

    if severity == 'extreme':
        severity_level = 15
    elif severity == 'mild':
        severity_level = 35
        severity_low_level = 15
    else:
        print('Неправильний тип посухи!')
        return

    fresult = []
    all_years = df.Year.unique()
    df = df[(df['area'] == area)]

    vhi_list_all_years = list()
    for el in df['VHI']:
        vhi_list_all_years.append(el)
    print(f'Ряд VHI в області з індексом {area}: {vhi_list_all_years}')

    for year in all_years:
        year = year[-4:]
        frame = df[(df.Year.astype(str) == str(year))]
        numb_weeks = len(frame.index)

        if severity == 'extreme':
            df_drought = frame[(frame.VHI.astype(int) <= severity_level)]
        else:
            df_drought = frame[(frame.VHI.astype(int) >= severity_low_level) & (frame.VHI.astype(int) <= severity_level)]

        drought_weeks = len(df_drought.index)
        percentage = drought_weeks / numb_weeks * 100
        if percentage >= percent:
            fresult.append(year)

    print(f'Роки в області з індексом {area} з посухою типу {severity}, що перевищують {percent}%: {fresult}\n')


if __name__ == '__main__':
    path = 'D:\Python Projects\Data Science'
    get_data()

    lframes = []
    files = glob.glob(f'{path}\obl_id*.csv')
    for i in range(0, len(files)):
        index = int(files[i].split('_')[1][2:])
        lframes.append(create_dataframe(files[i], index))

    frame = pd.concat(lframes, axis=0, ignore_index=True)
    frame = index_correction(frame)

    try:
        area = int(input('Введіть індекс області: '))
        year = int(input('Введіть рік (з 1981 по 2023): '))
        percent = int(input('Введіть відсоток посухи: '))
    except TypeError:
        print('Вносіть тільки числа!')
        exit()

    vhi_display_for_year(df=frame, area=area, year=year)
    get_drought(df=frame, area=area, percent=percent, severity='extreme')
    get_drought(df=frame, area=area, percent=percent, severity='mild')
