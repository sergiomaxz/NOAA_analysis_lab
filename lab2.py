from spyre import server
import pandas as pd
import matplotlib.pyplot as plt

AREAS = {
    1: 'Вінницька',
    2: 'Волинська',
    3: 'Дніпропетровська',
    4: 'Донецька',
    5: 'Житомирська',
    6: 'Закарпатська',
    7: 'Запорізька',
    8: 'Івано-Франківська',
    9: 'Київська',
    10: 'Кіровоградська',
    11: 'Луганська',
    12: 'Львівська',
    13: 'Миколаївська',
    14: 'Одеська',
    15: 'Полтавська',
    16: 'Рівенська',
    17: 'Сумська',
    18: 'Тернопільська',
    19: 'Харківська',
    20: 'Херсонська',
    21: 'Хмельницька',
    22: 'Черкаська',
    23: 'Чернівецька',
    24: 'Чернігівська',
    25: 'Республіка Крим',
    26: 'Київ',
    27: 'Севастополь'
}


class SimpleApp(server.App):
    title = "NOAA Data Analysis"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'Тип індексу',
            "options": [
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}],
            "value": 'VCI',
            "key": 'col_type',
            "action_id": 'update_data'
        },

        {
            "type": 'dropdown',
            "label": 'Область',
            "options": [
                {"label": 'Вінницька', "value": 1},
                {"label": 'Волинська', "value": 2},
                {"label": 'Дніпропетровська', "value": 3},
                {"label": 'Донецька', "value": 4},
                {"label": 'Житомирська', "value": 5},
                {"label": 'Закарпатська', "value": 6},
                {"label": 'Запорізька', "value": 7},
                {"label": 'Івано-Франківська', "value": 8},
                {"label": 'Київська', "value": 9},
                {"label": 'Кіровоградська', "value": 10},
                {"label": 'Луганська', "value": 11},
                {"label": 'Львівська', "value": 12},
                {"label": 'Миколаївська', "value": 13},
                {"label": 'Одеська', "value": 14},
                {"label": 'Полтавська', "value": 15},
                {"label": 'Рівенська', "value": 16},
                {"label": 'Сумська', "value": 17},
                {"label": 'Тернопільська', "value": 18},
                {"label": 'Харківська', "value": 19},
                {"label": 'Херсонська', "value": 20},
                {"label": 'Хмельницька', "value": 21},
                {"label": 'Черкаська', "value": 22},
                {"label": 'Чернівецька', "value": 23},
                {"label": 'Чернігівська', "value": 24},
                {"label": 'Республіка Крим', "value": 25},
                {"label": 'Київ', "value": 26},
                {"label": 'Севастополь', "value": 27}],
            "value": 'Вінницька',
            "key": 'area',
            "action_id": 'update_data'
        },

        {
            "type": 'text',
            "label": 'Інтервал тижнів',
            "value": "1-52",
            "key": 'week_range',
            "action_id": 'update_data'
        },

        {
            "type": 'slider',
            "label": 'Рік',
            "min": 1981,
            "max": 2023,
            "key": 'year',
            "action_id": 'update_data'
        }
    ]

    controls = [{"type": "hidden", "id": "update_data"}]

    tabs = ['Plot', 'Table']

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]

    def GetData(self, params):
        path = 'obl_full.csv'
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'area']
        df = pd.read_csv(path, header=1, names=headers)
        start_week, end_week = map(int, params['week_range'].split('-'))
        df = df[(df.area.astype(str) == str(params['area']))
                & (df.Year.astype(str) == str(int(params['year'])))
                & (df.Week <= end_week) & (df.Week >= start_week)]
        return df

    def getPlot(self, params):
        df = self.GetData(params)
        gr = df.plot(x='Week', y=params['col_type'], legend=False)
        gr.set_ylabel(params['col_type'])
        gr.set_xlabel('Тижні')
        gr.set_title(f'{params["col_type"]} для області {AREAS[int(params["area"])]} за {int(params["year"])} рік, '
                     f'{params["week_range"]} тижні')
        fig = gr.get_figure()
        return fig

    def getTable(self, params):
        return self.GetData(params)[['Year', 'Week', 'SMN', 'SMT', str(params['col_type'])]]


app = SimpleApp()
app.launch(port=5555)
