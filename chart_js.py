
from IPython.display import display, HTML, IFrame
from matplotlib import colors as mcolors
import random


def del_brackets(string, list_of_words):
    for word in list_of_words:
        string = string.replace("'"+word+"'", word)
    return string


class cjs_dataset:
    def __init__(self, chart_type: str, name: str, data: list, labels: list, c='', fill=False, order=0):
        colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
        colors = list(colors.values())[8:]
        if c == '':
            c = random.choices(colors, k=1)[0]
        self.data = {
            'type': chart_type,
            'name': name,
            'data': data,
            'labels': labels,
            'order': order,
            'backgroundColor': c,
            'borderColor': c,
            'pointBackgroundColor': [c]*len(data),
            'fill': fill,
        }
        if chart_type == 'pie':
            sampling = random.choices(colors, k=len(data))
            self.data['backgroundColor'] = sampling
            self.data['borderColor'] = sampling
            self.data['fill'] = True

    def __repr__(self):
        return self.data


class cjs_plot:
    def __init__(self):
        self.datasets = {}
        self.options_dict = {}
    def add_dataset(self, chart_type: str, name: str, data: list, labels: list, c='', fill=False, order=0):
        self.datasets[name] = cjs_dataset(
            chart_type=chart_type, name=name, data=data, labels=labels, c=c, fill=fill, order=order)

    def union_datasets(self, datasets: list):
        full_labels = []
        full_types = []
        data_export = {}
        data_export['data'] = {}
        data_export['data']['datasets'] = []
        for dataset in datasets:
            full_labels += dataset.data['labels']
            full_types.append(dataset.data['type'])
            data_export['data']['datasets'].append(
                {'label': dataset.data['name'],
                 'data': dataset.data['data'],
                 'backgroundColor': dataset.data['backgroundColor'],
                 'borderColor': dataset.data['borderColor'],
                 'pointBackgroundColor': dataset.data['pointBackgroundColor'],
                 'fill': dataset.data['fill'],
                 })
        full_labels = list(set(full_labels))
        full_labels.sort()
        full_types = list(set(full_types))
        data_export['data']['labels'] = full_labels
        data_export['type'] = full_types[0]
        if len(full_types) > 1:
            for i, d in enumerate(data_export['data']['datasets']):
                d['order'] = i+1
                if i != 0:
                    d['type'] = full_types[i]
        full_types = list(set(full_types))
        data_export['type'] = full_types[0]
        data_export = str(data_export)
        data_export = del_brackets(
            data_export, ['pointBackgroundColor', 'fillOpacity', 'fill', 'data', 'label', 'labels', 'datasets', 'type', 'order', 'borderColor', 'backgroundColor'])
        data_export = data_export.replace(
            'True', 'true').replace('False', 'false')
        return data_export[1:-1]

    def add_options(self, name: str, x_name: str, y_name: str, display_legend=True, display_dataname=True, size=(2, 4)):
        self.render_params = {}
        self.render_params['height'] = str(size[0]*100)+"px"
        self.render_params['width'] = str(size[1]*100)+"px"
        self.render_params_export = str(self.render_params)[1:-1]
        self.render_params_export = self.render_params_export.replace(',', ' ')
        self.render_params_export = self.render_params_export.replace(
            ': ', '=')
        self.render_params_export = del_brackets(
            self.render_params_export, ['height', 'width'])
        self.options = {}
        self.options['legend'] = {}
        self.options['scales'] = {}
        self.options['title'] = {}
        self.options['title']['display'] = display_dataname
        self.options['title']['text'] = name
        self.options['legend']['display'] = display_dataname
        self.options['legend']['position'] = 'bottom'
        self.options['scales']['xAxes'] = [{}]
        self.options['scales']['yAxes'] = [{}]
        self.options['scales']['xAxes'][0]['display'] = display_legend
        self.options['scales']['yAxes'][0]['display'] = display_legend
        self.options['scales']['xAxes'][0]['scaleLabel'] = {}
        self.options['scales']['yAxes'][0]['scaleLabel'] = {}

        self.options['scales']['xAxes'][0]['scaleLabel']['labelString'] = x_name
        self.options['scales']['yAxes'][0]['scaleLabel']['labelString'] = y_name
        self.options['scales']['xAxes'][0]['scaleLabel']['display'] = display_legend
        self.options['scales']['yAxes'][0]['scaleLabel']['display'] = display_legend

        self.options = str(self.options)[1:-1]
        self.options = self.options.replace(
            'True', 'true').replace('False', 'false')
        self.options = del_brackets(self.options, ['scaleLabel',
                                                   'position', 'title', 'legend', 'scales', 'xAxes', 'yAxes', 'display', 'labelString', 'text'])
        self.options_export = [self.render_params_export, self.options]
        self.options_dict[name]=self.options_export
        # return self.options_export, self.data_export

    def render(self,datasets_names,options_names):
        dataets_values=[self.datasets.get(key) for key in datasets_names]
        option_values=self.options_dict[options_names]
        self.data_export = self.union_datasets(dataets_values)
        script_source = '''
        <iframe '''+option_values[0]+'''  frameborder="0" scrolling="no" srcdoc="
        <link href='Chart.min.css' rel='stylesheet'>
        <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.0/jquery.min.js'></script>
        <script src='https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/js/bootstrap.min.js'></script>
        <script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.min.js'></script>
        <div style='height:100%%;width100%%;'>
            <canvas id='chart_js' style='background-color:white;'></canvas>
        </div>
        <script>
            $(document).ready(function () {
                const chart_js_chart_config = {
                '''+self.data_export+'''
                    ,options: {'''+option_values[1]+'''}};
                const chart_js_context = document.getElementById('chart_js').getContext('2d');
                const chart_js_chart = new Chart(chart_js_context, chart_js_chart_config);
                chart_js_chart.update();
            });
        </script>"></iframe>
        '''
        r = HTML(script_source)
        display(r)

    def __repr__(self):
        return self.options_export

