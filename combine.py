import sys
import xml.etree.ElementTree as et
import logging as log
import re
import ntpath

from pysbs import context, sbsenum, sbsgenerator
import substance_wrapper as wsbs

wsbs.tools_path = "C:\Program Files\Allegorithmic\Substance Automation Toolkit"

# Init the context
myContext = context.Context()


def create_mat(aDestFileAbsPath, basec_in, rough_in, normal_in):
    aContext = context.Context()
    #aContext.getUrlAliasMgr().setAliasAbsPath(aAliasName = 'myAlias', aAbsPath = 'myAliasAbsolutePath')

    startPos = [48, 48, 0]
    xOffset  = [192, 0, 0]
    yOffset  = [0, 192, 0]

    try:
        # Create a new SBSDocument from scratch, with a graph named 'Material'
        sbsDoc = sbsgenerator.createSBSDocument(aContext,
                                aFileAbsPath = aDestFileAbsPath,
                                aGraphIdentifier = 'Material')

        # Get the graph 'Material'
        aGraph = sbsDoc.getSBSGraph(aGraphIdentifier = 'Material')

        if basec_in is not None:
            basecImg = sbsDoc.createLinkedResource(aResourcePath = basec_in,
                        aResourceTypeEnum = sbsenum.ResourceTypeEnum.BITMAP)
            baseColor = aGraph.createBitmapNode(aSBSDocument = sbsDoc,
                        aResourcePath = basecImg.getPkgResourcePath(),
                        aParameters   = {sbsenum.CompNodeParamEnum.COLOR_MODE: sbsenum.ColorModeEnum.COLOR},
                        aGUIPos       = startPos) 
            outBaseColor = aGraph.createOutputNode(aIdentifier = 'BaseColor',
                                aGUIPos = baseColor.getOffsetPosition(xOffset),
                                aUsages = {sbsenum.UsageEnum.BASECOLOR: sbsenum.ComponentsEnum.RGBA})
            aGraph.connectNodes(aLeftNode = baseColor, aRightNode = outBaseColor)
            startPos = baseColor.getOffsetPosition(yOffset)

        if rough_in is not None:
            roughImg = sbsDoc.createLinkedResource(aResourcePath = rough_in,
                        aResourceTypeEnum = sbsenum.ResourceTypeEnum.BITMAP)
            roughness = aGraph.createBitmapNode(aSBSDocument = sbsDoc,
                        aResourcePath = roughImg.getPkgResourcePath(),
                        aParameters   = {sbsenum.CompNodeParamEnum.COLOR_MODE: sbsenum.ColorModeEnum.GRAYSCALE},
                        aGUIPos       = startPos)     
            outRoughness = aGraph.createOutputNode(aIdentifier = 'Roughness',
                                aGUIPos = roughness.getOffsetPosition(xOffset),
                                aUsages = {sbsenum.UsageEnum.ROUGHNESS: sbsenum.ComponentsEnum.RGBA})
            aGraph.connectNodes(aLeftNode = roughness, aRightNode = outRoughness)
            startPos = roughness.getOffsetPosition(yOffset)

        metallic = aGraph.createCompFilterNode(aFilter = sbsenum.FilterEnum.UNIFORM,
                            aParameters = {sbsenum.CompNodeParamEnum.COLOR_MODE: sbsenum.ColorModeEnum.GRAYSCALE,
                                        sbsenum.CompNodeParamEnum.OUTPUT_COLOR: 0.0},
                            aGUIPos     = startPos)
        outMetallic = aGraph.createOutputNode(aIdentifier = 'Metallic',
                            aGUIPos = metallic.getOffsetPosition(xOffset),
                            aUsages = {sbsenum.UsageEnum.METALLIC: sbsenum.ComponentsEnum.RGBA})
        aGraph.connectNodes(aLeftNode = metallic,  aRightNode = outMetallic)
        startPos = metallic.getOffsetPosition(yOffset)

        if normal_in is not None:
            normalImg = sbsDoc.createLinkedResource(aResourcePath = normal_in,
                        aResourceTypeEnum = sbsenum.ResourceTypeEnum.BITMAP)
            normals = aGraph.createBitmapNode(aSBSDocument = sbsDoc,
                        aResourcePath = normalImg.getPkgResourcePath(),
                        aParameters   = {sbsenum.CompNodeParamEnum.COLOR_MODE: sbsenum.ColorModeEnum.COLOR},
                        aGUIPos       = startPos)     
            outNormal = aGraph.createOutputNode(aIdentifier = 'Normal',
                                aGUIPos = normals.getOffsetPosition(xOffset),
                                aUsages = {sbsenum.UsageEnum.NORMAL: sbsenum.ComponentsEnum.RGBA})
            aGraph.connectNodes(aLeftNode = normals,  aRightNode = outNormal)

        # Write back the document structure into the destination .sbs file
        sbsDoc.writeDoc()
        log.info("=> Resulting substance saved at %s", aDestFileAbsPath)
        return True

    except BaseException as error:
        log.error("!!! [demoHelloWorld] Failed to create the new package")
        raise error


print('Number of arguments:', len(sys.argv), 'arguments.')
arglist = sys.argv[1:]
print('Argument List:', str(arglist))

if len(arglist) > 0:
    sb_basec, sb_normal, sb_rough = None, None, None
    sb_name = ntpath.basename(arglist[0]).split('_')[0]
    print("Name:",sb_name)
    for arg in arglist:
        fname = ntpath.basename(arg)
        if 'COLOR' in fname.upper():
            sb_basec = fname
            print("Base color:", fname)
        if 'NORMAL' in fname.upper():
            sb_normal = fname
            print("Normal:", fname)
        if 'ROUGHNESS' in fname.upper():
            sb_rough = fname
            print("Roughness:", fname)
        #print(re.split(r"\W+", fname))

    mat_name = sb_name + ".sbs"
    create_mat(mat_name, sb_basec, sb_rough, sb_normal)

    # cook .sbs into .sbsar
    wsbs.sbscooker(inputs=mat_name)

    # print info about .sbsar
    print(wsbs.sbsrender.info(sb_name + ".sbsar"))

# try:
#     input("Press enter to continue")
# except SyntaxError:
#     pass