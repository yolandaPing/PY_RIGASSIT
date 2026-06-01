//Maya ASCII 2018ff09 scene
//Name: WaveCtrl.ma
//Last modified: Sun, Jun 11, 2023 05:25:56 PM
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
	setAttr ".t" -type "double3" 7.9555380606682871 6.2847330009827402 -0.92397310262126853 ;
	setAttr ".r" -type "double3" -37.538352729500367 94.199999999984399 2.5444437451708134e-14 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 8.7852912807538903;
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
	setAttr ".ow" 12.921914357682637;
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
createNode transform -n "Wave_ctrl_ofs";
	setAttr ".t" -type "double3" 0 3.3306690738754696e-16 0 ;
	setAttr ".rp" -type "double3" 0 -3.3306690738754696e-16 0 ;
	setAttr ".sp" -type "double3" 0 -3.3306690738754696e-16 0 ;
createNode transform -n "Wave_ctrl_con" -p "Wave_ctrl_ofs";
	setAttr ".rp" -type "double3" 0 -3.3306690738754696e-16 0 ;
	setAttr ".sp" -type "double3" 0 -3.3306690738754696e-16 0 ;
createNode transform -n "Wave_ctrl_drv" -p "Wave_ctrl_con";
	setAttr ".rp" -type "double3" 0 -3.3306690738754696e-16 0 ;
	setAttr ".sp" -type "double3" 0 -3.3306690738754696e-16 0 ;
createNode transform -n "Wave_ctrl" -p "Wave_ctrl_drv";
	addAttr -ci true -sn "AttrSet" -ln "AttrSet" -nn "--------" -min 0 -max 0 -en "SetAttr" 
		-at "enum";
	addAttr -ci true -sn "waveWidth" -ln "waveWidth" -dv 4 -at "double";
	addAttr -ci true -sn "follow" -ln "follow" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "offset" -ln "offset" -at "double";
	setAttr -l on -k off ".v";
	setAttr -cb on ".AttrSet";
	setAttr -k on ".waveWidth";
	setAttr -cb on ".follow";
	setAttr -k on ".offset";
createNode nurbsCurve -n "Wave_ctrlShape" -p "Wave_ctrl";
	setAttr -k off ".v";
	setAttr ".wfcc" -type "float3" 1 0.442 0.70599997 ;
	setAttr ".uoc" 2;
	setAttr ".cc" -type "nurbsCurve" 
		1 16 0 no 3
		17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16
		17
		1.2225774543186086e-09 -2.2458383636888433e-25 -0.50058871429008822
		-1.3716866771843086e-16 0.67841676048312849 0.500588714290088
		-1.0519312589285174e-16 0.53273589009327516 0.38174307844755406
		-7.9235879387928083e-17 0.36673246681305682 0.29351118414765487
		-6.0117066176780053e-17 0.186998246752763 0.23844819387778471
		1.0234843992822384e-09 -1.8801107127943284e-25 0.21941119876301832
		1.2225774543186086e-09 -2.2458383636888433e-25 -0.50058871429008822
		0.67841676048312838 -1.2462313713203698e-16 0.50058871429008822
		0.53273589392253462 -9.7861996092470443e-17 0.38174307844755384
		0.36673246850360464 -6.7367661554452066e-17 0.29351118414765515
		0.18699824969464304 -3.4351021190205349e-17 0.23844819387778432
		1.0234843992822384e-09 -1.8801107127943284e-25 0.21941119876301832
		-0.18699824675276305 3.4351020649790707e-17 0.23844819387778468
		-0.36673246681305688 6.73676612439034e-17 0.29351118414765481
		-0.53273589009327527 9.7861995389046822e-17 0.38174307844755395
		-0.6784167604831286 1.2462313713203698e-16 0.50058871429008789
		1.2225774543186086e-09 -2.2458383636888433e-25 -0.50058871429008822
		;
// End of WaveCtrl.ma
