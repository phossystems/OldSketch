#Author-Nico Schlueter
#Description-Adds the Sketch>Design toolbar to the Solid tab, similar to how it was before the tabbed toolbar.


# Add the ID's of CommandDefinitions you want on the toolbar here
promoted = [
    "DrawPolyline",
    "ShapeRectangleTwoPoint",
    "CircleCenterRadius",
    "DrawSpline"
] 

# List of ID's
#   DrawPolyline
#
#   ShapeRectangleTwoPoint
#   ShapeRectangleThreePoint
#   ShapeRectangleCenter
#
#   CircleCenterRadius
#   CircleTwoPoint
#   CircleThreePoint
#   CircleTanTanRadius
#   CircleThreeTangent
#
#   ArcThreePoint
#   ArcCenterTwoPoint
#   ArcTangent
#
#   ShapePolygonCircumscribed
#   ShapePolygonInscribed
#   ShapePolygonEdge
#
#   CircleElipse
#
#   ShapeSlotCenterToCenter
#   ShapeSlotOverall
#   ShapeSlotCenterPoint
#   ShapeArcSlotThreePoint
#   ShapeArcSlotCenterTwoPoint
#   
#   DrawSpline
#   DrawCVMSpline3D
#   DrawCVMSpline5D
#
#   ConicCurveCmd
#   DrawPoint
#   TextCmd
#   FitCurvesToSectionCommand
#   MirrorSketchCommand
#   CircularSketchPatternCommand
#   RectangularSketchPatternCommand
#   
#   ProjectNewCmd
#   IntersectCmd
#   Include3DGeometry
#   ProjectToSurface
#   IntersectionCurve
#   
#   SketchDimension


import adsk.core, adsk.fusion, adsk.cam, traceback

# API does not allow getting Dropdown names
names = {
    'RectangleDropDown' : "Rectangle",
    'CircleDropDown' : "Circle",
    'ArcDropDown' : "Arc",
    'PolygonDropDown' : "Polygon",
    'SlotDropDown' : "Slot",
    'SplineDropDown' : "Spline",
    'ProjectIncludeDropDown' : "Project / Include"
}

def run(context):
    ui = None
    try:
        ui = adsk.core.Application.get().userInterface

        sketchCreatePanel = ui.allToolbarPanels.itemById("SketchCreatePanel")
        solidTab = ui.allToolbarTabs.itemById("SolidTab")

        oldSketchCreatePanel = solidTab.toolbarPanels.add(
            "OldSketchCreatePanel",
            "Sketch",
            "SolidCreatePanel",
            True
        )

        for i in sketchCreatePanel.controls:
            addControl(oldSketchCreatePanel.controls, i)

    except:
        print(traceback.format_exc())


def stop(context):
    ui = None
    try:
        ui  = adsk.core.Application.get().userInterface

        oldSketchCreatePanel = ui.allToolbarPanels.itemById("OldSketchCreatePanel")
        if oldSketchCreatePanel:
            oldSketchCreatePanel.deleteMe()

    except:
        print(traceback.format_exc())


def addControl(controls, control):
    global promoted
    if(control.objectType == "adsk::core::CommandControl"):
        con = controls.addCommand(control.commandDefinition)
        con.isPromotedByDefault = control.commandDefinition.id in promoted
        # This worked once, but doesn't now. We can only hope it works again
        try:
            con.isPromoted = control.isPromoted
        except:
            pass

    elif(control.objectType == "adsk::core::DropDownControl"):
        con = controls.addDropDown(
            getNameFromId(control.id),
            ""
        )

        for i in control.controls:
            addControl(con.controls, i)

    elif(control.objectType == "adsk::core::SeparatorControl"):
        controls.addSeparator()


def getNameFromId(controlID):
    global name
    if(controlID in names):
        return names[controlID]
    return controlID
