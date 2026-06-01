//Maya ASCII 2019 scene
//Name: Body_guide_File.ma
//Last modified: Sat, Dec 27, 2025 04:23:19 PM
//Codeset: 936
requires maya "2019";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2019";
fileInfo "version" "2019";
fileInfo "cutIdentifier" "201812112215-434d8d9c04";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 19045)\n";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 21.275393711479889 13.160939139029169 -1.5476573706971957 ;
	setAttr ".r" -type "double3" -30.338352729563312 91.7999999999968 0 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 26.015805494891556;
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
createNode transform -n "Body_guide_grp";
	setAttr ".rp" -type "double3" 0 0.5 0 ;
	setAttr ".sp" -type "double3" 0 0.5 0 ;
createNode transform -n "BodyLoc_grp" -p "Body_guide_grp";
	setAttr ".rp" -type "double3" 0 0.5 0 ;
	setAttr ".sp" -type "double3" 0 0.5 0 ;
createNode transform -n "HeadLoc_cur" -p "BodyLoc_grp";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "HeadLoc_curShape" -p "HeadLoc_cur";
	setAttr -k off ".v";
	setAttr -s 2 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 0 4.9935442741171885
		0 0 7.2543555305563112
		;
createNode transform -n "BodyLoc_cur" -p "BodyLoc_grp";
	setAttr -l on -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
createNode nurbsCurve -n "BodyLoc_curShape" -p "BodyLoc_cur";
	setAttr -k off ".v";
	setAttr -s 2 ".cp";
	setAttr ".cc" -type "nurbsCurve" 
		1 1 0 no 3
		2 0 1
		2
		0 0 4.9935442741171885
		0 0 -7.0064557258828115
		;
createNode transform -n "guide_con" -p "Body_guide_grp";
	addAttr -ci true -k true -sn "size" -ln "size" -at "double";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -k on ".size";
createNode nurbsCurve -n "guide_conShape" -p "guide_con";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		3.447891149521388 2.1112244300349284e-16 -3.4478911495213884
		2.9857222221688017e-16 2.9857222221688017e-16 -4.8760544252393059
		-3.447891149521388 2.1112244300349276e-16 -3.4478911495213875
		-4.8760544252393085 1.5478036723626521e-32 -2.5277552245109255e-16
		-3.447891149521388 -2.1112244300349281e-16 3.447891149521388
		-4.8843770666254193e-16 -2.9857222221688037e-16 4.8760544252393094
		3.447891149521388 -2.1112244300349276e-16 3.4478911495213875
		4.8760544252393085 -4.0716188524484445e-32 6.6494582034318206e-16
		3.447891149521388 2.1112244300349284e-16 -3.4478911495213884
		2.9857222221688017e-16 2.9857222221688017e-16 -4.8760544252393059
		-3.447891149521388 2.1112244300349276e-16 -3.4478911495213875
		;
createNode transform -n "Loc_con" -p "guide_con";
	setAttr ".ove" yes;
	setAttr ".ovc" 13;
	setAttr -l on ".tx";
	setAttr -l on ".tz";
	setAttr -l on ".r";
	setAttr -l on ".s";
	setAttr ".rp" -type "double3" 0 1 0 ;
	setAttr ".sp" -type "double3" 0 1 0 ;
createNode locator -n "Loc_conShape" -p "Loc_con";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 0 1 0 ;
	setAttr ".los" -type "double3" 0.5 0.5 0.5 ;
createNode transform -n "head_Loc" -p "Loc_con";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".rp" -type "double3" 0 0 7.2543555305563112 ;
	setAttr ".sp" -type "double3" 0 0 7.2543555305563112 ;
createNode locator -n "head_LocShape" -p "head_Loc";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 0 0 7.2543555305563112 ;
	setAttr ".los" -type "double3" 0.5 0.5 0.5 ;
createNode transform -n "neck_Loc" -p "Loc_con";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".rp" -type "double3" 0 0 4.9935442741171885 ;
	setAttr ".sp" -type "double3" 0 0 4.9935442741171885 ;
createNode locator -n "neck_LocShape" -p "neck_Loc";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 0 0 4.9935442741171885 ;
	setAttr ".los" -type "double3" 0.5 0.5 0.5 ;
createNode transform -n "tail_Loc" -p "Loc_con";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".rp" -type "double3" 0 0 -7.0064557258828115 ;
	setAttr ".sp" -type "double3" 0 0 -7.0064557258828115 ;
createNode locator -n "tail_LocShape" -p "tail_Loc";
	setAttr -k off ".v";
	setAttr ".lp" -type "double3" 0 0 -7.0064557258828115 ;
	setAttr ".los" -type "double3" 0.5 0.5 0.5 ;
createNode transform -n "body_Loc_distanceD" -p "Loc_con";
	setAttr ".ovdt" 2;
	setAttr ".ove" yes;
createNode distanceDimShape -n "body_Loc_distanceD" -p "|Body_guide_grp|guide_con|Loc_con|body_Loc_distanceD";
	setAttr -k off ".v";
connectAttr "neck_LocShape.wp" "HeadLoc_curShape.cp[0]";
connectAttr "head_LocShape.wp" "HeadLoc_curShape.cp[1]";
connectAttr "neck_LocShape.wp" "BodyLoc_curShape.cp[0]";
connectAttr "tail_LocShape.wp" "BodyLoc_curShape.cp[1]";
connectAttr "|Body_guide_grp|guide_con|Loc_con|body_Loc_distanceD|body_Loc_distanceD.dist" "guide_con.size"
		;
connectAttr "tail_LocShape.wp" "|Body_guide_grp|guide_con|Loc_con|body_Loc_distanceD|body_Loc_distanceD.ep"
		;
connectAttr "neck_LocShape.wp" "|Body_guide_grp|guide_con|Loc_con|body_Loc_distanceD|body_Loc_distanceD.sp"
		;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "guide_con.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn";
connectAttr "|Body_guide_grp|guide_con|Loc_con|body_Loc_distanceD.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "neck_LocShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn";
connectAttr "guide_conShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn";
connectAttr "tail_LocShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn";
connectAttr "|Body_guide_grp|guide_con|Loc_con|body_Loc_distanceD|body_Loc_distanceD.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;

// End of Body_guide_File.ma
