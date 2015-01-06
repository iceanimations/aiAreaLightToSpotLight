'''
Created on Jan 5, 2015

@author: qurban.ali
'''
import operator
import pymel.core as pc

def getAttr(node, attribute):
    attr = (0, 0, 0)
    for i in range(200):
        attr = tuple(operator.add(attr, pc.PyNode(str(node)+ '.'+ attribute).get()))
        try:
            node= node.firstParent()
        except pc.MayaNodeError:
            break
    return attr

def convert():
    try:
        lights = pc.ls(sl=True, type=[pc.nt.AiAreaLight, pc.nt.AreaLight], dag=True)
    except AttributeError:
        pc.confirmDialog(title='Error', message='It seems like Arnold is not loaded or not installed', button='Ok')
        return
    
    if not lights:
        pc.confirmDialog(title='Warning', message='No selection found in the scene', button='Ok')
        return
    
    for areaLight in lights:
        spotLight = pc.PyNode(pc.Mel.eval('defaultSpotLight(1, 1,1,1, 0, 40, 0, 0, 0, 0,0,0, 1, 0);'))
        
        # intensity
        try:
            areaLight.intensity.inputs(plugs=True)[0].connect(spotLight.intensity)
        except IndexError:
            spotLight.intensity.set(areaLight.intensity.get())
        
        # color
        try:
            areaLight.color.inputs(plugs=True)[0].connect(spotLight.color)
        except IndexError:
            spotLight.color.set(areaLight.color.get())
        
        # exposure
        try:
            areaLight.aiExposure.inputs(plugs=True)[0].connect(spotLight.aiExposure)
        except IndexError:
            spotLight.aiExposure.set(areaLight.aiExposure.get())
        
        # color temperature
        try:
            areaLight.aiColorTemperature.inputs(plugs=True)[0].connect(spotLight.aiColorTemperature)
        except IndexError:
            spotLight.aiColorTemperature.set(areaLight.aiColorTemperature.get())

        areaTransform = areaLight.firstParent()
        
        spotLight.translate.set(getAttr(areaTransform, 'translate'))
        spotLight.rotate.set(getAttr(areaTransform, 'rotate'))
        
    for light in lights:
        pc.delete(light)