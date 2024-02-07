import pickle as p
import cv2, json, scipy.misc, math
import numpy as np
from skimage.draw import line
from skimage.morphology import thin
import matplotlib.pyplot as plt
from PIL import Image
import xml.etree.ElementTree as ET
from io import StringIO
from pathlib import Path

def get_label(inkml_file_abs_path):
    lebel = ""
    tree = ET.parse(inkml_file_abs_path)
    root = tree.getroot()
    doc_namespace = "{http://www.w3.org/2003/InkML}"

    for child in root:
        if (child.tag == doc_namespace + 'annotation') and (child.attrib == {'type': 'truth'}):
            return child.text

def get_traces_data(inkml_file_abs_path):

        traces_data = []

        tree = ET.parse(inkml_file_abs_path)
        root = tree.getroot()
        doc_namespace = "{http://www.w3.org/2003/InkML}"

        'Stores traces_all with their corresponding id'
        traces_all = [{'id': trace_tag.get('id'),
                        'coords': [[round(float(axis_coord)) if float(axis_coord).is_integer() else round(float(axis_coord) * 10000) \
                                        for axis_coord in coord[1:].split(' ')] if coord.startswith(' ') \
                                    else [round(float(axis_coord)) if float(axis_coord).is_integer() else round(float(axis_coord) * 10000) \
                                        for axis_coord in coord.split(' ')] \
                                for coord in (trace_tag.text).replace('\n', '').split(',')]} \
                                for trace_tag in root.findall(doc_namespace + 'trace')]

        'Sort traces_all list by id to make searching for references faster'
        traces_all.sort(key=lambda trace_dict: int(trace_dict['id']))

        'Always 1st traceGroup is a redundant wrapper'
        traceGroupWrapper = root.find(doc_namespace + 'traceGroup')

        if traceGroupWrapper is not None:
            for traceGroup in traceGroupWrapper.findall(doc_namespace + 'traceGroup'):

                label = traceGroup.find(doc_namespace + 'annotation').text
                id = traceGroup.get('{http://www.w3.org/XML/1998/namespace}id')     

                'traces of the current traceGroup'
                traces_curr = []
                for traceView in traceGroup.findall(doc_namespace + 'traceView'):

                    'Id reference to specific trace tag corresponding to currently considered label'
                    traceDataRef = int(traceView.get('traceDataRef'))

                    'Each trace is represented by a list of coordinates to connect'
                    single_trace = traces_all[traceDataRef]['coords']
                    traces_curr.append(single_trace)


                traces_data.append({'label': label, 'trace_group': traces_curr, 'id':id})

        else:
            'Consider Validation data that has no labels'
            [traces_data.append({'trace_group': [trace['coords']]}) for trace in traces_all]

        return traces_data
    
def inkml2img(input_path, output_path):
    fout = open(output_path.split('.')[0] + '.txt', 'w+')
    fout.write(get_label(input_path))
    fout.close()

    traces = get_traces_data(input_path)
    fig, ax = plt.subplots()
    ax.invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    ax.set_axis_off()
    for elem in traces:
        ls = elem['trace_group']
        for subls in ls:
            data = np.array(subls)
            x,y=zip(*data)
            ax.plot(x,y,linewidth=2,c='black')
    fig.set_frameon(False)
    fig.savefig(output_path, bbox_inches='tight', dpi=100, transparent=False)
    plt.close()
    
def extract_symbols(input_path,output_dir,name):
    # output_path = output_path.split('.')[0]
    
    traces = get_traces_data(input_path)
    fig, ax = plt.subplots()
    ax.invert_yaxis()
    ax.set_aspect('equal', adjustable='box')
    ax.set_axis_off()    
    for elem in traces:
        ls = elem['trace_group']
        for subls in ls:
            data = np.array(subls)
            x,y=zip(*data)
            ax.plot(x,y,linewidth=4,c='black')
        fig.set_frameon(False)
        if elem['label'] == '/':
            elem['label'] = 'slash'
        if elem['label'] == '.':
            elem['label'] = 'dec'
        Path(output_dir+elem['label']+'/').mkdir(parents=True, exist_ok=True)
        fig.savefig(output_dir+elem['label']+'/'+elem['id']+name, bbox_inches='tight', dpi=100, transparent=False)   
        ax.clear()
        ax.invert_yaxis()
        ax.set_aspect('equal', adjustable='box')
        ax.set_axis_off()    
    plt.close()