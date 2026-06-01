//Maya ASCII 2019 scene
//Name: GlobalCtrl.ma
//Last modified: Sun, Dec 28, 2025 12:05:20 PM
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
	setAttr ".t" -type "double3" 14.354056424373942 34.272871256374842 -52.684377405430951 ;
	setAttr ".r" -type "double3" -30.938352729516915 164.19999999998808 0 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 54.637743653655932;
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
createNode transform -n "Group";
createNode transform -n "global_ctrl_ofs" -p "Group";
	setAttr -l on ".v";
	setAttr -l on ".tx";
	setAttr -l on ".ty";
	setAttr -l on ".tz";
	setAttr -l on ".rx";
	setAttr -l on ".ry";
	setAttr -l on ".rz";
	setAttr -l on ".sx";
	setAttr -l on ".sy";
	setAttr -l on ".sz";
	setAttr ".rp" -type "double3" 0 -1.9721522630525304e-31 1.7763568394002505e-15 ;
	setAttr ".sp" -type "double3" 0 -1.9721522630525304e-31 1.7763568394002505e-15 ;
createNode transform -n "global_ctrl_con" -p "global_ctrl_ofs";
createNode transform -n "global_ctrl" -p "global_ctrl_con";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr ".mnsl" -type "double3" 0.1 0.1 0.1 ;
	setAttr ".msxe" yes;
	setAttr ".msye" yes;
	setAttr ".msze" yes;
createNode nurbsCurve -n "global_ctrlShape" -p "global_ctrl";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 22;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		10.827579872588357 6.6299805167388108e-16 -10.827579872588343
		-1.7469743333381027e-15 9.3762083650414129e-16 -15.312510303492397
		-10.827579872588347 6.6299805167388147e-16 -10.827579872588347
		-15.312510303492397 3.7076711936124778e-31 -5.032066224832063e-15
		-10.827579872588354 -6.6299805167388108e-16 10.827579872588343
		-4.6139581952055188e-15 -9.3762083650414129e-16 15.312510303492397
		10.827579872588343 -6.6299805167388127e-16 10.827579872588354
		15.312510303492397 -4.0452992197207726e-31 7.6294953270066648e-15
		10.827579872588357 6.6299805167388108e-16 -10.827579872588343
		-1.7469743333381027e-15 9.3762083650414129e-16 -15.312510303492397
		-10.827579872588347 6.6299805167388147e-16 -10.827579872588347
		;
createNode transform -n "Root_ctrl_ofs" -p "global_ctrl";
createNode transform -n "Root_ctrl_con" -p "Root_ctrl_ofs";
createNode transform -n "Root_ctrl_drv" -p "Root_ctrl_con";
createNode transform -n "Root_ctrl" -p "Root_ctrl_drv";
	addAttr -ci true -sn "SineAttr" -ln "SineAttr" -nn "----------------" -min 0 -max 
		0 -en "Mid Sine" -at "enum";
	addAttr -ci true -sn "mid_speed" -ln "mid_speed" -min 0 -max 50 -at "double";
	addAttr -ci true -sn "mid_width" -ln "mid_width" -min 0 -max 50 -at "double";
	addAttr -ci true -sn "mid_delay" -ln "mid_delay" -dv 0.65 -at "double";
	addAttr -ci true -sn "mid_add_width" -ln "mid_add_width" -dv -0.025 -at "double";
	addAttr -ci true -sn "mid_offset" -ln "mid_offset" -at "double";
	addAttr -ci true -k true -sn "In_sineSep" -ln "In_sineSep" -nn "________________" 
		-min 0 -max 0 -en "In_sine" -at "enum";
	addAttr -ci true -k true -sn "in_sped" -ln "in_sped" -at "double";
	addAttr -ci true -k true -sn "in_with" -ln "in_with" -at "double";
	addAttr -ci true -sn "in_delay" -ln "in_delay" -dv 0.65 -at "double";
	addAttr -ci true -k true -sn "in_add_with" -ln "in_add_with" -at "double";
	addAttr -ci true -k true -sn "in_offset" -ln "in_offset" -at "double";
	addAttr -ci true -sn "rotAttr" -ln "rotAttr" -nn "----------------" -min 0 -max 
		0 -en "RotAttr" -at "enum";
	addAttr -ci true -sn "Rot_X" -ln "Rot_X" -at "double";
	addAttr -ci true -sn "Rot_Y" -ln "Rot_Y" -at "double";
	addAttr -ci true -sn "Rot_Z" -ln "Rot_Z" -at "double";
	addAttr -ci true -sn "tailAttr" -ln "tailAttr" -nn "----------------" -min 0 -max 
		0 -en "TailAttr" -at "enum";
	addAttr -ci true -sn "tail_crimp" -ln "tail_crimp" -at "double";
	addAttr -ci true -sn "Crimp_Angle" -ln "Crimp_Angle" -dv 45 -at "double";
	addAttr -ci true -sn "falloff" -ln "falloff" -dv 1 -at "double";
	addAttr -ci true -sn "BodyBendSep" -ln "BodyBendSep" -nn "----------------" -min 
		0 -max 0 -en "BodybendAttr" -at "enum";
	addAttr -ci true -sn "bodyCrimp" -ln "bodyCrimp" -at "double";
	addAttr -ci true -sn "BendAngel" -ln "BendAngel" -dv 45 -at "double";
	addAttr -ci true -sn "bodyFalloff" -ln "bodyFalloff" -dv 1 -at "double";
	addAttr -ci true -sn "fatAttr" -ln "fatAttr" -nn "----------------" -min 0 -max 
		0 -en "FatAttr" -at "enum";
	addAttr -ci true -sn "fat_speed" -ln "fat_speed" -dv 2 -min 0 -max 100 -at "double";
	addAttr -ci true -sn "fat" -ln "fat" -at "double";
	addAttr -ci true -sn "Fat_animat" -ln "Fat_animat" -at "double";
	addAttr -ci true -sn "Fat_Delay" -ln "Fat_Delay" -dv 0.5 -at "double";
	setAttr -l on -k off ".v";
	setAttr ".mnsl" -type "double3" 0.1 0.1 0.1 ;
	setAttr ".msxe" yes;
	setAttr ".msye" yes;
	setAttr ".msze" yes;
	setAttr -l on -k on ".SineAttr";
	setAttr -k on ".mid_speed";
	setAttr -k on ".mid_width";
	setAttr -cb on ".mid_delay";
	setAttr -k on ".mid_add_width";
	setAttr -k on ".mid_offset";
	setAttr -l on -k on ".In_sineSep";
	setAttr -cb on ".in_delay";
	setAttr -l on -k on ".rotAttr";
	setAttr -k on ".Rot_X";
	setAttr -k on ".Rot_Y";
	setAttr -k on ".Rot_Z";
	setAttr -l on -k on ".tailAttr";
	setAttr -k on ".tail_crimp";
	setAttr -k on ".Crimp_Angle";
	setAttr -cb on ".falloff";
	setAttr -l on -k on ".BodyBendSep";
	setAttr -k on ".bodyCrimp";
	setAttr -k on ".BendAngel";
	setAttr -cb on ".bodyFalloff";
	setAttr -l on -k on ".fatAttr";
	setAttr -k on ".fat_speed";
	setAttr -k on ".fat";
	setAttr -k on ".Fat_animat";
	setAttr -cb on ".Fat_Delay";
createNode nurbsCurve -n "Root_ctrlShape" -p "Root_ctrl";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		6.370909352268086 3.9010568729565187e-16 -6.3709093522680771
		-1.0279134626023696e-15 5.5169275373238887e-16 -9.0098264106271113
		-6.3709093522680789 3.9010568729565222e-16 -6.3709093522680815
		-9.0098264106271113 2.0805099313777291e-31 -3.4788323035530746e-15
		-6.3709093522680833 -3.9010568729565187e-16 6.3709093522680771
		-2.7148365343604566e-15 -5.5169275373238897e-16 9.0098264106271149
		6.3709093522680771 -3.9010568729565212e-16 6.3709093522680789
		9.0098264106271113 -2.4813101886667814e-31 3.9711853231138594e-15
		6.370909352268086 3.9010568729565187e-16 -6.3709093522680771
		-1.0279134626023696e-15 5.5169275373238887e-16 -9.0098264106271113
		-6.3709093522680789 3.9010568729565222e-16 -6.3709093522680815
		;
createNode transform -n "Root_drv" -p "Root_ctrl";
createNode transform -n "Joints_grp" -p "Group";
createNode joint -n "Global" -p "Joints_grp";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".radi" 0.5;
createNode joint -n "Root_Jnt" -p "Global";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
createNode parentConstraint -n "Root_Jnt_parentConstraint1" -p "Root_Jnt";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "Root_ctrlW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode scaleConstraint -n "Root_Jnt_scaleConstraint1" -p "Root_Jnt";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "Root_ctrlW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode parentConstraint -n "Global_parentConstraint1" -p "Global";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "global_ctrlW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode scaleConstraint -n "Global_scaleConstraint1" -p "Global";
	addAttr -dcb 0 -ci true -k true -sn "w0" -ln "global_ctrlW0" -dv 1 -min 0 -at "double";
	setAttr -k on ".nds";
	setAttr -k off ".v";
	setAttr -k off ".tx";
	setAttr -k off ".ty";
	setAttr -k off ".tz";
	setAttr -k off ".rx";
	setAttr -k off ".ry";
	setAttr -k off ".rz";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".erp" yes;
	setAttr -k on ".w0";
createNode transform -n "Geometry" -p "Group";
createNode transform -n "notMove" -p "Group";
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 4 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
createNode displayLayerManager -n "layerManager";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -330.95236780151544 -323.80951094248991 ;
	setAttr ".tgi[0].vh" -type "double2" 317.85713022663526 338.09522466054096 ;
createNode nodeGraphEditorBookmarkInfo -n "nodeGraphEditorBookmarkInfo1";
	setAttr -s 15 ".ni";
	setAttr ".ni[0].nvs" 1696;
	setAttr ".ni[1].nvs" 1856;
	setAttr ".ni[2].nvs" 1696;
	setAttr ".ni[3].nvs" 1664;
	setAttr ".ni[4].nvs" 1696;
	setAttr ".ni[5].nvs" 1808;
	setAttr ".ni[6].nvs" 1696;
	setAttr ".ni[7].nvs" 1728;
	setAttr ".ni[8].nvs" 1920;
	setAttr ".ni[9].nvs" 2528;
	setAttr ".ni[10].nvs" 1952;
	setAttr ".ni[11].nvs" 2528;
	setAttr ".ni[12].nvs" 2304;
	setAttr ".ni[13].nvs" 1648;
	setAttr ".ni[14].nvs" 1648;
connectAttr "Global_parentConstraint1.ctx" "Global.tx";
connectAttr "Global_parentConstraint1.cty" "Global.ty";
connectAttr "Global_parentConstraint1.ctz" "Global.tz";
connectAttr "Global_parentConstraint1.crx" "Global.rx";
connectAttr "Global_parentConstraint1.cry" "Global.ry";
connectAttr "Global_parentConstraint1.crz" "Global.rz";
connectAttr "Global_scaleConstraint1.csx" "Global.sx";
connectAttr "Global_scaleConstraint1.csy" "Global.sy";
connectAttr "Global_scaleConstraint1.csz" "Global.sz";
connectAttr "Global.s" "Root_Jnt.is";
connectAttr "Root_Jnt_parentConstraint1.ctx" "Root_Jnt.tx";
connectAttr "Root_Jnt_parentConstraint1.cty" "Root_Jnt.ty";
connectAttr "Root_Jnt_parentConstraint1.ctz" "Root_Jnt.tz";
connectAttr "Root_Jnt_parentConstraint1.crx" "Root_Jnt.rx";
connectAttr "Root_Jnt_parentConstraint1.cry" "Root_Jnt.ry";
connectAttr "Root_Jnt_parentConstraint1.crz" "Root_Jnt.rz";
connectAttr "Root_Jnt_scaleConstraint1.csx" "Root_Jnt.sx";
connectAttr "Root_Jnt_scaleConstraint1.csy" "Root_Jnt.sy";
connectAttr "Root_Jnt_scaleConstraint1.csz" "Root_Jnt.sz";
connectAttr "Root_Jnt.ro" "Root_Jnt_parentConstraint1.cro";
connectAttr "Root_Jnt.pim" "Root_Jnt_parentConstraint1.cpim";
connectAttr "Root_Jnt.rp" "Root_Jnt_parentConstraint1.crp";
connectAttr "Root_Jnt.rpt" "Root_Jnt_parentConstraint1.crt";
connectAttr "Root_Jnt.jo" "Root_Jnt_parentConstraint1.cjo";
connectAttr "Root_ctrl.t" "Root_Jnt_parentConstraint1.tg[0].tt";
connectAttr "Root_ctrl.rp" "Root_Jnt_parentConstraint1.tg[0].trp";
connectAttr "Root_ctrl.rpt" "Root_Jnt_parentConstraint1.tg[0].trt";
connectAttr "Root_ctrl.r" "Root_Jnt_parentConstraint1.tg[0].tr";
connectAttr "Root_ctrl.ro" "Root_Jnt_parentConstraint1.tg[0].tro";
connectAttr "Root_ctrl.s" "Root_Jnt_parentConstraint1.tg[0].ts";
connectAttr "Root_ctrl.pm" "Root_Jnt_parentConstraint1.tg[0].tpm";
connectAttr "Root_Jnt_parentConstraint1.w0" "Root_Jnt_parentConstraint1.tg[0].tw"
		;
connectAttr "Root_Jnt.ssc" "Root_Jnt_scaleConstraint1.tsc";
connectAttr "Root_Jnt.pim" "Root_Jnt_scaleConstraint1.cpim";
connectAttr "Root_ctrl.s" "Root_Jnt_scaleConstraint1.tg[0].ts";
connectAttr "Root_ctrl.pm" "Root_Jnt_scaleConstraint1.tg[0].tpm";
connectAttr "Root_Jnt_scaleConstraint1.w0" "Root_Jnt_scaleConstraint1.tg[0].tw";
connectAttr "Global.ro" "Global_parentConstraint1.cro";
connectAttr "Global.pim" "Global_parentConstraint1.cpim";
connectAttr "Global.rp" "Global_parentConstraint1.crp";
connectAttr "Global.rpt" "Global_parentConstraint1.crt";
connectAttr "Global.jo" "Global_parentConstraint1.cjo";
connectAttr "global_ctrl.t" "Global_parentConstraint1.tg[0].tt";
connectAttr "global_ctrl.rp" "Global_parentConstraint1.tg[0].trp";
connectAttr "global_ctrl.rpt" "Global_parentConstraint1.tg[0].trt";
connectAttr "global_ctrl.r" "Global_parentConstraint1.tg[0].tr";
connectAttr "global_ctrl.ro" "Global_parentConstraint1.tg[0].tro";
connectAttr "global_ctrl.s" "Global_parentConstraint1.tg[0].ts";
connectAttr "global_ctrl.pm" "Global_parentConstraint1.tg[0].tpm";
connectAttr "Global_parentConstraint1.w0" "Global_parentConstraint1.tg[0].tw";
connectAttr "Global.pim" "Global_scaleConstraint1.cpim";
connectAttr "global_ctrl.s" "Global_scaleConstraint1.tg[0].ts";
connectAttr "global_ctrl.pm" "Global_scaleConstraint1.tg[0].tpm";
connectAttr "Global_scaleConstraint1.w0" "Global_scaleConstraint1.tg[0].tw";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr ":persp.msg" "nodeGraphEditorBookmarkInfo1.ni[0].dn";
connectAttr ":perspShape.msg" "nodeGraphEditorBookmarkInfo1.ni[1].dn";
connectAttr ":top.msg" "nodeGraphEditorBookmarkInfo1.ni[2].dn";
connectAttr ":topShape.msg" "nodeGraphEditorBookmarkInfo1.ni[3].dn";
connectAttr ":front.msg" "nodeGraphEditorBookmarkInfo1.ni[4].dn";
connectAttr ":frontShape.msg" "nodeGraphEditorBookmarkInfo1.ni[5].dn";
connectAttr ":side.msg" "nodeGraphEditorBookmarkInfo1.ni[6].dn";
connectAttr ":sideShape.msg" "nodeGraphEditorBookmarkInfo1.ni[7].dn";
connectAttr ":lightLinker1.msg" "nodeGraphEditorBookmarkInfo1.ni[8].dn";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr ":perspShape.msg" ":defaultRenderGlobals.sc";
// End of GlobalCtrl.ma
