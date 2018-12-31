
import time
from collections import Counter, defaultdict
import sys
sys.path.append(r'D:\SourceModules\Python\others\dxfgrabber')

import dxfgrabber

def add_entities_by_layer(dxf):
    '''Reads the Drawing and appends another dict indexing each entity to
    its layer, .entities_by_layer.'''
    entities_by_layer = defaultdict(list)
    for an_entity in dxf.entities:
        dbg = True
        entities_by_layer[an_entity.layer].append(an_entity)
    dxf.entities_by_layer = entities_by_layer


def print_items_on_layer(dxf, layer_names):
    '''Print all items in specified layer'''
    if isinstance(layer_names, list):
        layer_list = layer_names
    else:
        layer_list = [layer_names]

    for aLayer in layer_list:
        entities = dxf.entities_by_layer[aLayer]
        print('Layer {0} has {1} entities.'.format(aLayer, len(entities)))
        for an_entity in entities:
            print()
            print("Entity {}".format(an_entity.dxftype))
            if an_entity.dxftype == 'LINE':
                print("      {0} to {1}".format(an_entity.start,
                                                an_entity.end))
            elif an_entity.dxftype == 'ARC':
                an_entity.deflection = an_entity.end_angle = \
                    an_entity.start_angle
                print("      R: {0}    Defl: {1}"
                      .format(an_entity.radius,
                              an_entity.deflection))
            elif an_entity.dxftype == 'SPLINE':
                end_points = (an_entity.control_points[0],
                              an_entity.control_points[-1])
                print("      {0}"
                      .format(end_points))


def print_layers(counter):
    print("used Layers: {}".format(len(counter)))
    for item in sorted(counter.items()):
        print("Layer: {} has {} entities".format(*item))


filename = r"D:\Research\Datasets\Roadway Design\NCDOT\R-2100B\r2100b_rdy_aln_only.dxf"

if __name__ == '__main__':
    print("reading file: {}".format(filename))
    starttime = time.time()
    dxf = dxfgrabber.readfile(filename)
    endtime = time.time()
    add_entities_by_layer(dxf)
    print("time to read: {:.2f}s".format(endtime-starttime))
    print("entities: {:d}".format(len(dxf.entities)))
    print("defined Layers: {}".format(len(dxf.layers)))
    print_layers(Counter(entity.layer for entity in dxf.entities))
    print_items_on_layer(dxf, 'Prop Horizontal Alignment')

    dbg = True

