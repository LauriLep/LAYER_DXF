Purpose of LAYER_DXF script is to speed up Autocad design process when
importing source drawing and need to remove walls and other layers 
that are not needed for design. 

Process flow when using LAYER_DXF -script:
1) import source pdf drawing and scale to architect plan
2) explode imported source drawing
3) copy source drawing and create a new drawing and save it as test.dxf
4) save test.dxf drawing to LAYER_DXF folder
5) run LAYER_DXF.py
6) open TEST_BY_COLOR_LINEWEIGHT.dxf
7) remove layers you dont need fast and easily by selecting with quick command "QSE" in Autocad 
