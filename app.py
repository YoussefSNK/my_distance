from flask import Flask, request, render_template
from math import sqrt
from datetime import datetime

app = Flask('my_distance')

distances = []

@app.route('/', methods=['GET', 'POST'])
def html_calculate():
    if request.method == 'GET':
    # Si get, afficher la page vide
        return render_template('index.html', result=None)
    if request.method == 'POST':
    # Si post, calculer et afficher le résultat
        end_point = tuple(int(x) for x in request.form['apoint'].split(',')[0:2])
        start_point = [int(y) for y in request.form['bpoint'].split(',')[0:2]]
        result_tmp = sqrt((end_point[1] - start_point[1])**2 + (end_point[0] - start_point[0])**2)
        result =             {
                    'requested_at': datetime.now(),
                    'result_distance': result_tmp,
                    'start_point': start_point,
                    'end_point': end_point
                }
        distances.append({
                    'requested_at': datetime.now(),
                    'result_distance': result_tmp,
                    'start_point': start_point,
                    'end_point': end_point
                })    
        return render_template('index.html', result=result)

@app.route('/api', methods=['GET'])
def index():
    return {}

@app.route('/api/distances', methods=['GET'])
def already_calculated():
    starttime = datetime.now()
    result = [
        {
            'requested_at': x['requested_at'],
            'result_distance': x['result_distance'],
            'start_point': x['start_point'],
            'end_point': x['end_point']
        }
        for x in distances
    ]
    end = datetime.now()
    print(f'result given in {end - starttime} secondes')
    return result

@app.route('/api/distance', methods=['POST', 'GET', 'PUT'])
def calculate():
    start_point = [int(y) for y in request.json['start_point'].split(',')[0:2]]
    end_point = tuple(int(x) for x in request.json['end_point'].split(',')[0:2])

    result_tmp = sqrt((end_point[1] - start_point[1])**2 + (end_point[0] - start_point[0])**2)
    result =             {
                'requested_at': datetime.now(),
                'result_distance': result_tmp,
                'start_point': start_point,
                'end_point': end_point
            }
    return result