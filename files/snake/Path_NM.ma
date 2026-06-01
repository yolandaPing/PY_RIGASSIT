//Maya ASCII 2018ff09 scene
//Name: Path_NM.ma
//Last modified: Tue, Jun 06, 2023 11:46:05 PM
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
	setAttr ".t" -type "double3" 55.43305413015517 162.42815910313365 65.361368729188555 ;
	setAttr ".r" -type "double3" -68.138352729780181 87.79999999999211 -8.2853248389372558e-14 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 174.23146511243857;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
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
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -n "path_cur";
	setAttr ".rp" -type "double3" -1.1102200000000001e-16 0 -6 ;
	setAttr ".sp" -type "double3" -1.1102200000000001e-16 0 -6 ;
createNode nurbsCurve -n "path_curshape" -p "path_cur";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		3 23 0 no 3
		28 0 0 0 0.043478260869565216 0.086956521739130432 0.13043478260869565 0.17391304347826086
		 0.21739130434782608 0.2608695652173913 0.30434782608695654 0.34782608695652173 0.39130434782608697
		 0.43478260869565216 0.47826086956521741 0.52173913043478259 0.56521739130434778 0.60869565217391308
		 0.65217391304347827 0.69565217391304346 0.73913043478260865 0.78260869565217395 0.82608695652173914
		 0.86956521739130432 0.91304347826086951 0.95652173913043481 1 1 1
		26
		-1.1102200000000001e-16 0 -6
		-1.1102199999999991e-16 0 0.040000000000003262
		-1.8581537466181195e-15 0 6.0799999999999974
		-2.2784271584310041e-15 0 12.119999999999997
		-3.036437012164261e-15 0 18.160000000000011
		-3.8327908792540511e-15 0 24.199999999999989
		-4.5587687006434415e-15 0 30.239999999999974
		-5.3290705182007514e-15 0 36.280000000000015
		-6.0316689862685324e-15 0 42.319999999999958
		-6.7744852692479113e-15 0 48.360000000000035
		-7.503210120565595e-15 0 54.399999999999977
		-8.2472280557234147e-15 0 60.440000000000005
		-8.9901715935214218e-15 0 66.480000000000018
		-9.7240219195290282e-15 0 72.519999999999996
		-1.0466997253065145e-14 0 78.560000000000016
		-1.1211022361668432e-14 0 84.600000000000037
		-1.1939672274565509e-14 0 90.640000000000029
		-1.2682518800794498e-14 0 96.680000000000035
		-1.3442011276897079e-14 0 102.71999999999997
		-1.4155363917488185e-14 0 108.7600000000001
		-1.4881210666249216e-14 0 114.80000000000007
		-1.5678036081159335e-14 0 120.84000000000015
		-1.6435965261784654e-14 0 126.87999999999987
		-1.6855068189023049e-14 0 132.92000000000004
		-1.8603188667125034e-14 0 138.95999999999987
		-1.8603188667125034e-14 0 145
		;
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
// End of Path_NM.ma
