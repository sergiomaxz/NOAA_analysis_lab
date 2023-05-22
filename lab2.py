from spyre import server

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
                {},
                {},
                {},
                {}],
            "value": 'Вінницька'
        },

        {
            "type": 'slider',
            "label": 'Інтервал тижнів',
            "min": 1,
            "max": 54,

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

    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Update"
    }]

    tabs = ['Plot', 'Table']

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot"},
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        }
    ]
