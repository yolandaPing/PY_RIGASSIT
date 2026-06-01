//Maya ASCII 2018ff09 scene
//Name: TwistCtrl.ma
//Last modified: Mon, Jul 24, 2023 08:55:18 PM
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
	setAttr ".t" -type "double3" 26.32323231831365 13.05043767113847 -8.2061199595847629 ;
	setAttr ".r" -type "double3" -27.93835272969109 100.1999999999977 0 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 29.332636177464067;
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
createNode transform -n "prefix_Twist_ctrl_ofs";
createNode transform -n "prefix_Twist_ctrl_con" -p "prefix_Twist_ctrl_ofs";
createNode transform -n "prefix_Twist_ctrl_drv" -p "prefix_Twist_ctrl_con";
createNode transform -n "prefix_Twist_ctrl" -p "prefix_Twist_ctrl_drv";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "prefix_Twist_ctrlShape" -p "prefix_Twist_ctrl";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 20;
	setAttr ".cc" -type "nurbsCurve" 
		1 24 0 no 3
		25 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24
		25
		-6.8421033999186707e-31 -1.9824906243955456 3.0814094322304129e-15
		-2.9346756497432545e-16 -1.1013836802197463 0.88110694417579982
		-2.2010067373074417e-16 -1.1013836802197465 0.66083020813185023
		-2.20100673730744e-16 -0.66083020813184745 0.66083020813184956
		-3.668344562179066e-16 -0.66083020813184667 1.1013836802197488
		-3.668344562179067e-16 -0.88110694417579627 1.1013836802197492
		-6.6030202119223145e-16 3.3015101059611578e-15 1.9824906243955456
		-3.6683445621790606e-16 0.88110694417579993 1.1013836802197463
		-3.6683445621790615e-16 0.66083020813185034 1.1013836802197468
		-2.2010067373074358e-16 0.66083020813184967 0.66083020813184756
		-2.2010067373074341e-16 1.101383680219749 0.66083020813184679
		-2.9346756497432466e-16 1.1013836802197492 0.88110694417579638
		6.8421033999186707e-31 1.9824906243955456 -3.0814094322304129e-15
		2.9346756497432545e-16 1.1013836802197463 -0.88110694417579982
		2.2010067373074417e-16 1.1013836802197465 -0.66083020813185023
		2.20100673730744e-16 0.66083020813184745 -0.66083020813184956
		3.668344562179066e-16 0.66083020813184667 -1.1013836802197488
		3.668344562179067e-16 0.88110694417579627 -1.1013836802197492
		6.6030202119223145e-16 -3.3015101059611578e-15 -1.9824906243955456
		3.6683445621790606e-16 -0.88110694417579993 -1.1013836802197463
		3.6683445621790615e-16 -0.66083020813185034 -1.1013836802197468
		2.2010067373074358e-16 -0.66083020813184967 -0.66083020813184756
		2.2010067373074341e-16 -1.101383680219749 -0.66083020813184679
		2.9346756497432466e-16 -1.1013836802197492 -0.88110694417579638
		-6.8421033999186707e-31 -1.9824906243955456 3.0814094322304129e-15
		;

// End of TwistCtrl.ma
