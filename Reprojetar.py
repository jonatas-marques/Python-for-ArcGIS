# Python script: Reprojetar.py
# The script projects all shapefiles from given folder and
# projects them into a new coordinate system
# using a feature class as a spatial reference pattern


# Import ArcPy and os
import arcpy, os

# Print message 'the script is running'
currentScript = os.path.basename(__file__)
arcpy.AddMessage(u"Running script: " + currentScript)

try:
    # Get the input argument values
    folderInput = arcpy.GetParameterAsText(0)    # defines the file for the data to be Projected
    fcStandard = arcpy.GetParameterAsText(1)    # and the output spatial reference

    # Set the current workspace.
    arcpy.env.workspace = folderInput
    arcpy.env.overwriteOutput = True

    # Create a feature class list from the directory
    fcList = arcpy.ListFeatureClasses()
    count_fcList = len(fcList)

    # Return the spatial reference for the output data
    descStandard = arcpy.Describe(fcStandard)
    standardSR = descStandard.spatialReference

    # Set the progressor
    arcpy.SetProgressor("step", r"Projecting the shapefile into a new spatial reference...",
                        0, count_fcList, 1)

    # Create a list that contains the data projected
    projected_dataList = []

    # The loop begins
    arcpy.AddMessage(r"Projecting the following files:")

    for fc in fcList:
        # Return the spatial reference for each shapefile
        fcdesc = arcpy.Describe(fc)
        fcSR = fcdesc.spatialReference

        # Statement to compare the coordinate systems
        if fcSR.Name != standardSR.Name:
            # Add the term '_projetado' to the projected files
            nameOriginal = fc
            suffix = r"_projected.shp"
            if nameOriginal.endswith(".shp"):
                # remove .shp from each file name
                nameOriginal = nameOriginal.replace(".shp", suffix)

            # run project tool
            arcpy.Project_management(fc, nameOriginal, standardSR)

            # Add projected data to the projected data list
            projected_dataList.append(fc)

            # Update the progressor label for current shapefile
            arcpy.SetProgressorLabel(r"Projecting {0}...".format(fc))

            # Update the progressor position
            arcpy.SetProgressorPosition()

    arcpy.ResetProgressor()

    # Add message of the data projected
    # But first it is necessary to define a string variable for the message content
    msg = ""
    for p in projected_dataList:
        # Add the comma between the data before the last element of the list
        while p != projected_dataList[-1]:
            msg += p + ", "
            break
        # Add the end point after the last element of list
        else:
            msg += p + "."
    # Finally, prints the message as a list of the data projected
    arcpy.AddMessage(msg)

    # Report the success message
    arcpy.AddMessage(u"Done. The script " + currentScript + u" runs correctly!")

except:
    # Error message
    arcpy.AddError(u"Sorry. There is something wrong...")

    # Add any message from the last tool
    arcpy.AddMessage(arcpy.GetMessages())