//Maya ASCII 2018ff09 scene
//Name: Path_BZ.ma
//Last modified: Thu, Jun 29, 2023 10:06:59 PM
//Codeset: 936
requires maya "2018ff09";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "2018";
fileInfo "cutIdentifier" "202004151615-e82ce49a8d";
fileInfo "osv" "Microsoft Windows 8 Business Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 66.906421835943732 64.270592036830266 -6.1680991913682099 ;
	setAttr ".r" -type "double3" -41.738352729656135 97.79999999999599 0 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 108.04575984457124;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 4.3789952569967712 1000.1 57.540646339569392 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 346.23521948822196;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "front";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "side";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 -0.52577445092334818 4.040161570253094 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 28.493709317289088;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -n "path_cur";
	setAttr ".rp" -type "double3" -1.11022e-16 0 -6 ;
	setAttr ".sp" -type "double3" -1.11022e-16 0 -6 ;
createNode bezierCurve -n "path_curshape" -p "path_cur";
	setAttr -k off ".v";
	setAttr ".cc" -type "dataBezierCurve" 
		3 34 0 no 3
		39 0 0 0 1 1 1 2 2 2 3 3 3 4 4 4 5 5 5 6 6 6 7 7 7 8 8 8 9 9 9 10 10 10 11
		 11 11 12 12 12
		37
		-1.11022e-16 0 -6
		-1.11022e-16 0 -1.9999980926513672
		-1.11022e-16 0 2.0000009536743164
		-1.11022e-16 0 6
		-1.11022e-16 0 9.6666684150695801
		-1.11022e-16 0 13.33333420753479
		-1.11022e-16 0 17
		-1.11022e-16 0 20.66666841506958
		-1.11022e-16 0 24.33333420753479
		-1.11022e-16 0 28
		-1.11022e-16 0 32.000001907348633
		-1.11022e-16 0 36.000000953674316
		-1.11022e-16 0 40
		-1.11022e-16 0 44.333335399627686
		-1.11022e-16 0 48.666667699813843
		-1.11022e-16 0 53
		-1.11022e-16 0 57.333335399627686
		-1.11022e-16 0 61.666667699813843
		-1.11022e-16 0 66
		-1.11022e-16 0 70.333335399627686
		-1.11022e-16 0 74.666667699813843
		-1.11022e-16 0 79
		-1.11022e-16 0 83.333335399627686
		-1.11022e-16 0 87.666667699813843
		-1.11022e-16 0 92
		-1.11022e-16 0 96.000001907348633
		-1.11022e-16 0 100.00000095367432
		-1.11022e-16 0 104
		-1.11022e-16 0 108.33333539962769
		-1.11022e-16 0 112.66666769981384
		-1.11022e-16 0 117
		-1.11022e-16 0 121.66666889190674
		-1.11022e-16 0 126.33333444595337
		-1.11022e-16 0 131
		-1.11022e-16 0 135.33333539962769
		-1.11022e-16 0 139.66666769981384
		-1.11022e-16 0 144
		;
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of Path_BZ.ma
