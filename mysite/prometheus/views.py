from django.shortcuts import render
from django.http import JsonResponse
import requests
from requests.auth import  HTTPBasicAuth
from django.views.decorators.csrf import csrf_exempt

PROMETHEUS_URL = 'https://prometheus-vm.ces.myfiinet.com'  
username = 'prometheus'
password = 'vSTJ456'


#获取数据的值
def fetch_prometheus_data(metric_name):
    response = requests.get(f'{PROMETHEUS_URL}/api/v1/series?match[]={metric_name}', auth=HTTPBasicAuth(username, password), verify=False)
    if response.status_code == 200:
        return response.json().get('data', [])
    else:
        print(f"Error: Unable to fetch data for metric {metric_name}, status code: {response.status_code}")
        return None
    
#通过查询指标获取所有标签
def get_labels_for_metric(metric_name):
    data = fetch_prometheus_data(metric_name)
    if data is not None:
        labels = set()
        for series in data:
            labels.update(series.keys())
        labels.discard('__name__')
        return list(sorted(labels))
    return None

#获取标签的值
def get_values_for_metric(metric_name, label_name):
    data = fetch_prometheus_data(metric_name)
    if data is not None:
        values = set()
        for series in data:
            if label_name in series:
                values.add(series[label_name])
        return list(sorted(values))
    

@csrf_exempt
def index(request):
    metric_name = ''
    labels = []
    if request.method == 'POST':
        metric_name = request.POST.get('metric_name')
        if not metric_name:
            return JsonResponse({"error": "Metric name is required"}, status=400)
        labels = get_labels_for_metric(metric_name)
        if labels is None:
            return JsonResponse({"error": "Failed to retrieve labels"}, status=500)
    print(f"Metric Name: {metric_name}")
    return render(request, 'prometheus/searchlabel.html', {'labels': labels, 'metric_name': metric_name})
@csrf_exempt
def get_label_values(request):
    label_name = request.GET.get('label_name')
    metric_name = request.GET.get('metric_name')
    if not label_name or not metric_name:
        return JsonResponse({"error": "Label name and metric name are required"}, status=400)
    values = get_values_for_metric(metric_name, label_name)
    if values is None:
        return JsonResponse({"error": "Failed to retrieve label values"}, status=500)
    return JsonResponse(values, safe=False)