//Maya ASCII 2018ff09 scene
//Name: IKCtrl_SM.ma
//Last modified: Sun, Apr 09, 2023 10:56:35 AM
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
	setAttr ".t" -type "double3" 29.340639833793855 15.937965629552769 -0.34540789293313923 ;
	setAttr ".r" -type "double3" -24.938352729603338 81.400000000000645 1.0634792445108559e-14 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 31.755739633012062;
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
createNode transform -n "IK_con_sm_ctrl_ofs";
	setAttr ".t" -type "double3" 0 3.3306690738754696e-16 0 ;
	setAttr ".rp" -type "double3" 0 -3.3306690738754696e-16 0 ;
	setAttr ".sp" -type "double3" 0 -3.3306690738754696e-16 0 ;
createNode transform -n "IK_con_sm_ctrl_con" -p "IK_con_sm_ctrl_ofs";
	setAttr ".rp" -type "double3" 0 -3.3306690738754696e-16 0 ;
	setAttr ".sp" -type "double3" 0 -3.3306690738754696e-16 0 ;
createNode transform -n "IK_con_sm_ctrl_drv" -p "IK_con_sm_ctrl_con";
	setAttr ".rp" -type "double3" 0 -3.3306690738754696e-16 0 ;
	setAttr ".sp" -type "double3" 0 -3.3306690738754696e-16 0 ;
createNode transform -n "IK_con_sm_sec_ctrl" -p "IK_con_sm_ctrl_drv";
	setAttr ".rp" -type "double3" 0 -3.3306690738754696e-16 0 ;
	setAttr ".sp" -type "double3" 0 -3.3306690738754696e-16 0 ;
createNode transform -n "IK_con_sm_pri_ctrl" -p "IK_con_sm_sec_ctrl";
	setAttr ".rp" -type "double3" 0 -3.3306690738754696e-16 0 ;
	setAttr ".sp" -type "double3" 0 -3.3306690738754696e-16 0 ;
createNode transform -n "IK_sm_ctrl" -p "IK_con_sm_pri_ctrl";
	setAttr ".ove" yes;
	setAttr ".ovc" 6;
	setAttr ".t" -type "double3" 0 -3.3306690738754696e-16 0 ;
createNode nurbsCurve -n "curveShape7" -p "IK_sm_ctrl";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		1 15 0 no 3
		16 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15
		16
		0.59999999999999998 0.59999999999999998 -0.19999999999999987
		-0.59999999999999998 0.59999999999999998 -0.20000000000000015
		-0.59999999999999998 -0.59999999999999998 -0.20000000000000015
		0.59999999999999998 -0.59999999999999998 -0.19999999999999987
		0.59999999999999998 0.59999999999999998 -0.19999999999999987
		0.59999999999999998 0.59999999999999998 0.20000000000000015
		-0.59999999999999998 0.59999999999999998 0.19999999999999987
		-0.59999999999999998 0.59999999999999998 -0.20000000000000015
		-0.59999999999999998 -0.59999999999999998 -0.20000000000000015
		-0.59999999999999998 -0.59999999999999998 0.19999999999999987
		-0.59999999999999998 0.59999999999999998 0.19999999999999987
		0.59999999999999998 0.59999999999999998 0.20000000000000015
		0.59999999999999998 -0.59999999999999998 0.20000000000000015
		-0.59999999999999998 -0.59999999999999998 0.19999999999999987
		0.59999999999999998 -0.59999999999999998 0.20000000000000015
		0.59999999999999998 -0.59999999999999998 -0.19999999999999987
		;

// End of IKCtrl_SM.ma
