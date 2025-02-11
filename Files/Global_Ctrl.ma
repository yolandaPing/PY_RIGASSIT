//Maya ASCII 2017ff05 scene
//Name: Global_Ctrl.ma
//Last modified: Tue, Mar 26, 2024 05:55:14 PM
//Codeset: 936
requires maya "2017ff05";
requires "stereoCamera" "10.0";
requires "mtoa" "4.0.2.1";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201705190846-1017201";
fileInfo "osv" "Microsoft Windows 8 , 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "9E71972B-43FD-A6F6-D158-47BF8370D9DF";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0.75898702861696909 14.487801044372967 35.240691585906909 ;
	setAttr ".r" -type "double3" -18.338352729604331 -2.1999999999993607 -4.9732824146399209e-017 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "7F558C96-4E71-98EF-4A2F-E88DD2DABA42";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 37.68560732293917;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 0 9.1730455823843293 0 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "8AE2AC92-4EEC-2BF0-20C6-F9ADD735C405";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "4F4226BB-4B39-CF36-C6DC-158AC3541F2D";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "B6A31ACE-4F64-5BAD-8874-0F82357E14BB";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "A36A7DD1-4E66-581B-A7C0-7CAA128EDCA7";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "C70E8F7A-4C5F-735A-3F8E-AABA51614CA1";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "E02F5468-4970-089F-C0D8-87BBB11BD227";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "Group";
	rename -uid "8C928A1C-447E-C188-4A5E-6C83E7DD2B95";
createNode transform -n "global_ctrl" -p "Group";
	rename -uid "30A93911-4A93-D47F-B287-7EB75C0FAEEA";
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
	setAttr ".rp" -type "double3" 0 -1.9721522630525304e-031 1.7763568394002505e-015 ;
	setAttr ".sp" -type "double3" 0 -1.9721522630525304e-031 1.7763568394002505e-015 ;
createNode transform -n "global_ctrl" -p "|Group|global_ctrl";
	rename -uid "2AFB2FCC-433A-216C-9E74-29BFAE48E9C9";
	addAttr -ci true -k true -sn "scaleSep" -ln "scaleSep" -nn "________________" -min 
		0 -max 0 -en "scale" -at "enum";
	addAttr -ci true -sn "global_scale" -ln "global_scale" -dv 1 -min 0.01 -at "double";
	setAttr -l on -k off ".v";
	setAttr -k off ".sx";
	setAttr -k off ".sy";
	setAttr -k off ".sz";
	setAttr ".mnsl" -type "double3" 0.1 0.1 0.1 ;
	setAttr ".msxe" yes;
	setAttr ".msye" yes;
	setAttr ".msze" yes;
	setAttr -l on -k on ".scaleSep";
	setAttr -k on ".global_scale";
createNode nurbsCurve -n "global_ctrlShape" -p "|Group|global_ctrl|global_ctrl";
	rename -uid "B6F0C4DC-4FC1-2FBC-C051-28A644AFDD2C";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 22;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		10.827579872588357 6.6299805167388108e-016 -10.827579872588343
		-1.7469743333381027e-015 9.3762083650414129e-016 -15.312510303492397
		-10.827579872588347 6.6299805167388147e-016 -10.827579872588347
		-15.312510303492397 3.7076711936124778e-031 -5.032066224832063e-015
		-10.827579872588354 -6.6299805167388108e-016 10.827579872588343
		-4.6139581952055188e-015 -9.3762083650414129e-016 15.312510303492397
		10.827579872588343 -6.6299805167388127e-016 10.827579872588354
		15.312510303492397 -4.0452992197207726e-031 7.6294953270066648e-015
		10.827579872588357 6.6299805167388108e-016 -10.827579872588343
		-1.7469743333381027e-015 9.3762083650414129e-016 -15.312510303492397
		-10.827579872588347 6.6299805167388147e-016 -10.827579872588347
		;
createNode transform -n "Root_ctrl_ofs" -p "|Group|global_ctrl|global_ctrl";
	rename -uid "120CDE5E-4B48-8D0B-5718-FE802C7BBCBF";
	setAttr ".rp" -type "double3" 0 9.6060455823843292 1.7763568394002505e-015 ;
	setAttr ".sp" -type "double3" 0 9.6060455823843292 1.7763568394002505e-015 ;
createNode transform -n "Root_ctrl_con" -p "Root_ctrl_ofs";
	rename -uid "C121C41E-4CE9-D5DE-7B07-2CA6ADFAB471";
	setAttr ".rp" -type "double3" 0 9.6060455823843292 1.7763568394002505e-015 ;
	setAttr ".sp" -type "double3" 0 9.6060455823843292 1.7763568394002505e-015 ;
createNode transform -n "Root_ctrl_drv" -p "Root_ctrl_con";
	rename -uid "E1FFA614-4D83-216C-EC48-9293DB9D15BF";
	setAttr ".rp" -type "double3" 0 9.6060455823843292 1.7763568394002505e-015 ;
	setAttr ".sp" -type "double3" 0 9.6060455823843292 1.7763568394002505e-015 ;
createNode transform -n "Root_ctrl" -p "Root_ctrl_drv";
	rename -uid "B3C41FD2-44ED-86A1-DEE1-DD8221002C30";
	setAttr -l on -k off ".v";
	setAttr ".mnsl" -type "double3" 0.1 0.1 0.1 ;
	setAttr ".msxe" yes;
	setAttr ".msye" yes;
	setAttr ".msze" yes;
createNode nurbsCurve -n "Root_ctrlShape" -p "Root_ctrl";
	rename -uid "CD550797-47AF-CBA7-C992-2BBEBA2172F7";
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		3 8 2 no 3
		13 -2 -1 0 1 2 3 4 5 6 7 8 9 10
		11
		6.370909352268086 3.9010568729565187e-016 -6.3709093522680771
		-1.0279134626023696e-015 5.5169275373238887e-016 -9.0098264106271113
		-6.3709093522680789 3.9010568729565222e-016 -6.3709093522680815
		-9.0098264106271113 2.0805099313777291e-031 -3.4788323035530746e-015
		-6.3709093522680833 -3.9010568729565187e-016 6.3709093522680771
		-2.7148365343604566e-015 -5.5169275373238897e-016 9.0098264106271149
		6.3709093522680771 -3.9010568729565212e-016 6.3709093522680789
		9.0098264106271113 -2.4813101886667814e-031 3.9711853231138594e-015
		6.370909352268086 3.9010568729565187e-016 -6.3709093522680771
		-1.0279134626023696e-015 5.5169275373238887e-016 -9.0098264106271113
		-6.3709093522680789 3.9010568729565222e-016 -6.3709093522680815
		;
createNode transform -n "visibility_ctrl_grp" -p "Root_ctrl";
	rename -uid "73FF099A-4F1F-3529-5E14-39A9CD0BD7AC";
	setAttr ".t" -type "double3" 0 10 0 ;
createNode transform -n "visibility_ctrl" -p "visibility_ctrl_grp";
	rename -uid "0C51E975-4B30-0B0C-DD10-1991A5D0627B";
	addAttr -ci true -sn "ctrl_Vis" -ln "ctrl_Vis" -dv 1 -min 0 -max 1 -at "double";
	addAttr -ci true -sn "mesh_display_type" -ln "mesh_display_type" -min 0 -max 2 -en 
		"normal:template:reference" -at "enum";
	addAttr -ci true -sn "mesh_type" -ln "mesh_type" -min 0 -max 1 -en "HI:Low" -at "enum";
	setAttr -l on -k off ".v";
	setAttr -l on -k off ".tx";
	setAttr -l on -k off ".ty";
	setAttr -l on -k off ".tz";
	setAttr -l on -k off ".rx";
	setAttr -l on -k off ".ry";
	setAttr -l on -k off ".rz";
	setAttr -l on -k off ".sx";
	setAttr -l on -k off ".sy";
	setAttr -l on -k off ".sz";
	setAttr -cb on ".ctrl_Vis";
	setAttr -cb on ".mesh_display_type" 2;
	setAttr -cb on ".mesh_type";
createNode nurbsCurve -n "curveShape1" -p "visibility_ctrl";
	rename -uid "2D7D464C-46F6-06F3-081A-2FA97E79FE96";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".ls" 1;
	setAttr ".cc" -type "nurbsCurve" 
		2 17 0 no 3
		20 0 0 0.54802770223107922 0.54802770223107922 0.63966724216163473 0.63966724216163473
		 0.96553408756190739 0.96553408756190739 1.9655340875619074 1.9655340875619074 2.9655340875619074
		 2.9655340875619074 3.2981555143949102 3.2981555143949102 3.387383487485188 3.387383487485188
		 3.9350689528779155 3.9350689528779155 4.0160975987112488 4.0160975987112488
		19
		-0.94799963435425727 -0.85975815895524477 0
		-1.1888750131461567 -0.22656595034881624 0
		-1.4297503919380561 0.40662625825761223 0
		-1.3164674167636479 0.40662625825761223 0
		-1.2031844415892399 0.40662625825761223 0
		-1.0672448713799501 0.027426404515909275 0
		-0.93130530117066035 -0.35177344922579362 0
		-0.88718456347115415 -0.47459604336225708 0
		-0.8502185399931893 -0.60695825646077606 0
		-0.82159968310702303 -0.5067922573591942 0
		-0.77032423118597515 -0.36608287766887671 0
		-0.62961485149565766 0.020271690294367765 0
		-0.48890547180534016 0.40662625825761223 0
		-0.37860362755657445 0.40662625825761223 0
		-0.26830178330780868 0.40662625825761223 0
		-0.50798470972945109 -0.22656595034881624 0
		-0.74766763615109355 -0.85975815895524477 0
		-0.84783363525267552 -0.85975815895524477 0
		-0.94799963435425727 -0.85975815895524477 0
		;
createNode nurbsCurve -n "curveShape2" -p "visibility_ctrl";
	rename -uid "8E1D3A6A-47D2-2C93-1339-9D866808011F";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".ls" 1;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 2 no 3
		5 0 0.099838867187500013 0.18665527343749999 0.286494140625 0.37331054687499998
		
		5
		-0.077509404066700247 0.64153937519822701 0
		-0.077509404066700247 0.88837701584141104 0
		0.13713202257954665 0.88837701584141104 0
		0.13713202257954665 0.64153937519822701 0
		-0.077509404066700247 0.64153937519822701 0
		;
createNode nurbsCurve -n "curveShape3" -p "visibility_ctrl";
	rename -uid "E44596B4-440D-DC5B-4144-398800A68191";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".ls" 1;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 2 no 3
		5 0 0.51221679687499999 0.59903320312499997 1.1112500000000001 1.1980664062500002
		
		5
		-0.077509404066700247 -0.85975815895524477 0
		-0.077509404066700247 0.40662625825761223 0
		0.13713202257954665 0.40662625825761223 0
		0.13713202257954665 -0.85975815895524477 0
		-0.077509404066700247 -0.85975815895524477 0
		;
createNode nurbsCurve -n "curveShape4" -p "visibility_ctrl";
	rename -uid "BE392550-4C0A-C6D4-0BBC-A7ABD47DC978";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".ls" 1;
	setAttr ".cc" -type "nurbsCurve" 
		2 50 0 no 3
		53 0 0 0.086907462134993826 0.086907462134993826 1.0869074621349939 2.0869074621349939
		 2.0869074621349939 3.0869074621349939 4.0869074621349935 4.0869074621349935 5.0869074621349935
		 5.0869074621349935 6.0869074621349935 6.0869074621349935 7.0869074621349935 8.0869074621349935
		 9.0869074621349935 9.0869074621349935 10.086907462134993 11.086907462134993 11.086907462134993
		 12.086907462134993 13.086907462134993 13.086907462134993 14.086907462134993 15.086907462134993
		 16.086907462134995 16.086907462134995 16.172580219702851 16.172580219702851 17.172580219702851
		 18.172580219702851 18.172580219702851 19.172580219702851 20.172580219702851 20.172580219702851
		 21.172580219702851 21.172580219702851 22.172580219702851 22.172580219702851 23.172580219702851
		 23.172580219702851 24.172580219702851 25.172580219702851 26.172580219702851 26.172580219702851
		 27.172580219702851 28.172580219702851 29.172580219702851 29.172580219702851 30.172580219702851
		 31.172580219702851 31.172580219702851
		52
		0.37800740137144606 -0.48175075758379865 0
		0.4841356623243126 -0.46505642440020173 0
		0.59026392327717914 -0.4483620912166047 0
		0.60815070883103295 -0.575954494834096 0
		0.77151668355623215 -0.7118940650433857 0
		0.91818832509783421 -0.7118940650433857 0
		1.0660524190096932 -0.7118940650433857 0
		1.2091467034405248 -0.59145637564743603 0
		1.2091467034405248 -0.51036961446996498 0
		1.2091467034405248 -0.4376300198842924 0
		1.1459467278169071 -0.39589418692529987 0
		1.1018259901174008 -0.36727533003913365 0
		0.9265354916896329 -0.32315459233962729 0
		0.69042992237876111 -0.26353197382678095 0
		0.50798470972945109 -0.17648295079802528 0
		0.41378097247915402 -0.022656595034881558 0
		0.41378097247915402 0.070354689845158733 0
		0.41378097247915402 0.15501880813340063 0
		0.49129037654585422 0.29930554493448891 0
		0.55806770928024196 0.34700363974476595 0
		0.60815070883103295 0.38396966322273079 0
		0.78105630251828762 0.4352451151437785 0
		0.88002984924961247 0.4352451151437785 0
		1.0290863955317284 0.4352451151437785 0
		1.2544598935102877 0.34938854448527989 0
		1.3617806068334113 0.20271690294367781 0
		1.3820522971277791 0.079894308807214168 0
		1.2771164885451696 0.065584880364131154 0
		1.1721806799625596 0.051275451921048001 0
		1.1578712515194762 0.14905654628211601 0
		1.0207392289399302 0.25876216434575339 0
		0.8955317300629525 0.25876216434575339 0
		0.74766763615109344 0.25876216434575339 0
		0.6212676849038592 0.16098106998468523 0
		0.6212676849038592 0.095396189620554211 0
		0.6212676849038592 0.053660356661561791 0
		0.6475016370495118 0.020271690294367765 0
		0.67373558919516396 -0.014309428443083015 0
		0.72978085059723963 -0.03696602347796471 0
		0.76197706459417669 -0.048890547180533935 0
		0.91938077746809121 -0.091818832509783399 0
		1.1471391801871642 -0.15263390339288668 0
		1.3271994880959606 -0.23014330745958694 0
		1.4297503919380561 -0.37800740137144601 0
		1.4297503919380561 -0.48771301943508333 0
		1.4297503919380561 -0.59503373275820681 0
		1.3045428930610787 -0.78463365962905829 0
		1.0684373237502072 -0.88837701584141104 0
		0.91938077746809121 -0.88837701584141104 0
		0.67254313682490729 -0.88837701584141104 0
		0.41378097247915402 -0.68327520815721943 0
		0.37800740137144606 -0.48175075758379865 0
		;
createNode nurbsCurve -n "visibility_ctrl_frameSahpe" -p "visibility_ctrl";
	rename -uid "13BDBFC3-4247-05BC-19E2-8AB953659B32";
	setAttr ".ihi" 0;
	setAttr -k off ".v";
	setAttr ".ove" yes;
	setAttr ".ovc" 17;
	setAttr ".cc" -type "nurbsCurve" 
		1 4 0 no 3
		5 0 1 2 3 4
		5
		-1.7157004703256673 -1.0660524190096932 0
		1.7157004703256673 -1.0660524190096932 0
		1.7157004703256673 1.0660524190096932 0
		-1.7157004703256673 1.0660524190096932 0
		-1.7157004703256673 -1.0660524190096932 0
		;
createNode transform -n "Joints_grp" -p "Group";
	rename -uid "45A127A9-4828-737D-0EF6-1DBC963BB01B";
createNode joint -n "UE_export_Jnt" -p "Joints_grp";
	rename -uid "BC57562A-45B7-CA45-96D8-9E83F83CC2AE";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".radi" 0.5;
createNode joint -n "Root_Jnt" -p "UE_export_Jnt";
	rename -uid "953260DA-4668-A57B-3550-24988BFD72BB";
	addAttr -ci true -sn "liw" -ln "lockInfluenceWeights" -min 0 -max 1 -at "bool";
	setAttr ".uoc" 1;
	setAttr ".mnrl" -type "double3" -360 -360 -360 ;
	setAttr ".mxrl" -type "double3" 360 360 360 ;
	setAttr ".bps" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
createNode parentConstraint -n "Root_Jnt_parentConstraint1" -p "Root_Jnt";
	rename -uid "A5DD23AA-49B7-8529-8518-44BBEB16E59B";
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
createNode parentConstraint -n "UE_export_Jnt_parentConstraint1" -p "UE_export_Jnt";
	rename -uid "CE57AAC8-471F-B04F-58F0-4998C3CCB63E";
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
createNode scaleConstraint -n "Joints_grp_scaleConstraint1" -p "Joints_grp";
	rename -uid "7E8D749B-4669-2374-7E56-DAA185017AEC";
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
createNode lightLinker -s -n "lightLinker1";
	rename -uid "78F52985-42B5-6971-455C-B985659A6EA8";
	setAttr -s 4 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "17D05B12-41D2-ECBB-BD45-7082B94BCC48";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "F670C65B-4B14-7B2B-BDAC-B887A72B4A90";
createNode displayLayerManager -n "layerManager";
	rename -uid "51088B4C-420A-10A5-9C08-C7AA4557E306";
createNode displayLayer -n "defaultLayer";
	rename -uid "B7A861B4-4F1B-509C-711D-24B189557D62";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "A22ACAAE-41D1-33B7-50EA-E89729DE4EF6";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "488DC317-4827-8195-44EA-97928072678A";
	setAttr ".g" yes;
createNode nodeGraphEditorInfo -n "hyperShadePrimaryNodeEditorSavedTabsInfo";
	rename -uid "B025C8B3-46E2-3170-0C38-7E8E59886797";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -330.95236780151544 -323.80951094248991 ;
	setAttr ".tgi[0].vh" -type "double2" 317.85713022663526 338.09522466054096 ;
createNode nodeGraphEditorBookmarkInfo -n "nodeGraphEditorBookmarkInfo1";
	rename -uid "70E7471D-45AF-418F-DE93-95BA3EB37DCE";
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
createNode script -n "uiConfigurationScriptNode";
	rename -uid "DC592AE9-49A4-0CB5-88D5-76A27A2A5A53";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n"
		+ "            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n"
		+ "            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n"
		+ "            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n"
		+ "            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n"
		+ "            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n"
		+ "            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n"
		+ "        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n"
		+ "            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 32768\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n"
		+ "            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n"
		+ "            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 654\n            -height 698\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n"
		+ "            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n"
		+ "            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -selectCommand \"{}\" \n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n"
		+ "            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n"
		+ "                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n"
		+ "                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n"
		+ "                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n"
		+ "                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n"
		+ "                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n"
		+ "                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n"
		+ "                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n"
		+ "                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n"
		+ "                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"wireframe\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 1\n"
		+ "                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 32768\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n"
		+ "                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n"
		+ "                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n"
		+ "\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n"
		+ "                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 654\\n    -height 698\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 32768\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 654\\n    -height 698\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "F44DB2FF-49F2-E0E3-A44B-6F8D2802D442";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode objectSet -n "AllSet";
	rename -uid "8896864C-451E-8E3B-45B4-948C9D305A32";
	setAttr ".ihi" 0;
createNode objectSet -n "Sets";
	rename -uid "F2B529F9-4D1C-AE47-3C86-DDBAEECBD5A8";
	setAttr ".ihi" 0;
createNode dagPose -n "buildPose";
	rename -uid "3F933D9F-40A2-0762-5D97-4C93DDC6C58C";
	addAttr -ci true -sn "udAttr" -ln "udAttr" -dt "string";
	setAttr ".udAttr" -type "string" (
		"xform -os -t 0 0 0 -ro 0 0 0 RootX_M;setAttr RootX_M.CenterBtwFeet 0;xform -os -t 0 0 0 -ro 0 0 0 RootExtraX_M;xform -os -t 0 0 0 -ro 0 0 0 FKExtraToes_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKToes_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKAnkle_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraAnkle_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraKnee_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKKnee_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraHip_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKHip_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKEye_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraEye_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraJaw_M;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKJaw_M;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKHead_M;setAttr FKHead_M.Global 0;xform -os -t 0 0 0 -ro 0 0 0 FKExtraHead_M;xform -os -t 0 0 0 -ro 0 0 0 FKExtraNeck_M;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKNeck_M;setAttr FKNeck_M.w0 3.333333333;setAttr FKNeck_M.w1 6.666666667;setAttr FKNeck_M.w2 10;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKMiddleFinger3_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraMiddleFinger3_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraMiddleFinger2_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKMiddleFinger2_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraThumbFinger3_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraMiddleFinger1_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKMiddleFinger1_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKThumbFinger2_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraThumbFinger1_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKThumbFinger3_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraThumbFinger2_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraIndexFinger3_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKThumbFinger1_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKIndexFinger3_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKIndexFinger1_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraIndexFinger2_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKIndexFinger2_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraIndexFinger1_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKPinkyFinger3_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraPinkyFinger3_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraPinkyFinger2_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKPinkyFinger2_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKPinkyFinger1_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraPinkyFinger1_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKRingFinger3_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKRingFinger2_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraRingFinger3_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraRingFinger2_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraCup_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraRingFinger1_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKRingFinger1_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKCup_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraWrist_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKWrist_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKShoulder_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKElbow_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraElbow_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraShoulder_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraScapula_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKChest_M;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKScapula_R;xform -os -t 0 0 0 -ro 0 0 0 FKExtraChest_M;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKSpine1_M;setAttr FKSpine1_M.w0 3.333333333;setAttr FKSpine1_M.w1 6.666666667;setAttr FKSpine1_M.w2 10;xform -os -t 0 0 0 -ro 0 0 0 FKExtraSpine1_M;xform -os -t 0 0 0 -ro 0 0 0 FKExtraRoot_M;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKRoot_M;setAttr FKRoot_M.w0 3.333333333;setAttr FKRoot_M.w1 6.666666667;setAttr FKRoot_M.w2 10;xform -os -t 0 0 0 -ro 0 0 0 FKExtraToes_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKToes_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraAnkle_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKAnkle_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraKnee_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKKnee_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraHip_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKHip_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraEye_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKEye_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraMiddleFinger3_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKMiddleFinger3_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKMiddleFinger2_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKMiddleFinger1_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraMiddleFinger2_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraMiddleFinger1_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKThumbFinger3_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraThumbFinger3_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKThumbFinger2_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraThumbFinger2_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKIndexFinger3_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraThumbFinger1_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKThumbFinger1_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraIndexFinger3_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraIndexFinger2_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKIndexFinger2_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraPinkyFinger3_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKIndexFinger1_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraIndexFinger1_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraPinkyFinger2_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKPinkyFinger3_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKPinkyFinger2_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraPinkyFinger1_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKPinkyFinger1_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraRingFinger3_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKRingFinger3_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKRingFinger2_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraRingFinger2_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraRingFinger1_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKCup_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKRingFinger1_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraCup_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKElbow_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKWrist_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraWrist_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraElbow_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKShoulder_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraShoulder_L;xform -os -t 0 0 0 -ro 0 0 0 FKExtraScapula_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 FKScapula_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 AimEye_M;setAttr AimEye_M.follow 10;xform -os -t 0 0 0 AimEye_L;xform -os -t 0 0 0 AimEye_R;xform -os -t 0 0 0 PoleLeg_R;setAttr PoleLeg_R.follow 10;setAttr PoleLeg_R.lock 0;xform -os -t 0 0 0 -ro 0 0 0 IKExtraLeg_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKLeg_R;setAttr IKLeg_R.swivel 0;setAttr IKLeg_R.roll 0;setAttr IKLeg_R.rollStartAngle 30;setAttr IKLeg_R.rollEndAngle 60;setAttr IKLeg_R.rock 0;setAttr IKLeg_R.stretchy 0;setAttr IKLeg_R.antiPop 0;setAttr IKLeg_R.Lenght1 1;setAttr IKLeg_R.Lenght2 1;setAttr IKLeg_R.Fatness1 0;setAttr IKLeg_R.Fatness2 0;setAttr IKLeg_R.volume 10;xform -os -t 0 0 0 -ro 0 0 0 PoleExtraLeg_R;xform -os -t 0 0 0 -ro 0 0 0 IKExtraArm_R;xform -os -t 0 0 0 PoleArm_R;setAttr PoleArm_R.follow 0;setAttr PoleArm_R.lock 0;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKArm_R;setAttr IKArm_R.follow 0;setAttr IKArm_R.stretchy 0;setAttr IKArm_R.antiPop 0;setAttr IKArm_R.Lenght1 1;setAttr IKArm_R.Lenght2 1;setAttr IKArm_R.Fatness1 0;setAttr IKArm_R.Fatness2 0;setAttr IKArm_R.volume 10;xform -os -t 0 0 0 -ro 0 0 0 PoleExtraArm_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 Main;xform -os -t 0 0 0 -ro 0 0 0 IKExtracvSpine2_M;xform -os -t 0 0 0 -ro 0 0 0 IKExtracvSpine1_M;xform -os -t 0 0 0 IKcvSpine1_M;xform -os -t 0 0 0 IKcvSpine3_M;xform -os -t 0 0 0 IKcvSpine2_M;xform -os -t 0 0 0 -ro 0 0 0 IKExtracvSpine4_M;xform -os -t 0 0 0 -ro 0 0 0 IKExtraSpine1_M;xform -os -t 0 0 0 -ro 0 0 0 IKExtracvSpine3_M;xform -os -t 0 0 0 IKcvSpine5_M;xform -os -t 0 0 0 IKcvSpine4_M;xform -os -t 0 0 0 -ro 0 0 0 IKExtracvSpine5_M;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKSpine1_M;setAttr IKSpine1_M.stiff 5;setAttr IKSpine1_M.FixedOrient 0;xform -os -t 0 0 0 -ro 0 0 0 IKExtraSpine2_M;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKSpine2_M;setAttr IKSpine2_M.followEnd 5;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKSpine3_M;setAttr IKSpine3_M.stiff 5;setAttr IKSpine3_M.stretchy 10;setAttr IKSpine3_M.follow 10;setAttr IKSpine3_M.volume 10;xform -os -t 0 -0 0 -ro 0 0 0 IKhybridExtraSpine1_M;xform -os -t 0 0 0 -ro 0 0 0 IKExtraSpine3_M;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKhybridSpine1_M;xform -os -t 0 0 0 -ro 0 0 0 IKhybridExtraSpine2_M;xform -os -t 0 0 0 -ro 0 0 0 IKhybridExtraSpine3_M;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKhybridSpine2_M;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKhybridSpine3_M;xform -os -t 0 0 0 -ro 0 0 0 IKExtraLeg_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKLeg_L;setAttr IKLeg_L.swivel 0;setAttr IKLeg_L.roll 0;setAttr IKLeg_L.rollStartAngle 30;setAttr IKLeg_L.rollEndAngle 60;setAttr IKLeg_L.rock 0;setAttr IKLeg_L.stretchy 0;setAttr IKLeg_L.antiPop 0;setAttr IKLeg_L.Lenght1 1;setAttr IKLeg_L.Lenght2 1;setAttr IKLeg_L.Fatness1 0;setAttr IKLeg_L.Fatness2 0;setAttr IKLeg_L.volume 10;xform -os -t 0 0 0 PoleLeg_L;setAttr PoleLeg_L.follow 10;setAttr PoleLeg_L.lock 0;xform -os -t 0 0 0 -ro 0 0 0 PoleExtraLeg_L;xform -os -t 0 0 0 PoleArm_L;setAttr PoleArm_L.follow 0;setAttr PoleArm_L.lock 0;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKArm_L;setAttr IKArm_L.follow 0;setAttr IKArm_L.stretchy 0;setAttr IKArm_L.antiPop 0;setAttr IKArm_L.Lenght1 1;setAttr IKArm_L.Lenght2 1;setAttr IKArm_L.Fatness1 0;setAttr IKArm_L.Fatness2 0;setAttr IKArm_L.volume 10;xform -os -t 0 0 0 -ro 0 0 0 IKExtraArm_L;xform -os -t 0 0 0 -ro 0 0 0 PoleExtraArm_L;setAttr FKIKSpine_M.FKIKBlend 0;setAttr FKIKSpine_M.FKVis 1;setAttr FKIKSpine_M.IKVis 1;setAttr FKIKLeg_R.FKIKBlend 10;setAttr FKIKLeg_R.FKVis 1;setAttr FKIKLeg_R.IKVis 1;setAttr FKIKArm_R.FKIKBlend 0;setAttr FKIKArm_R.FKVis 1;setAttr FKIKArm_R.IKVis 1;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 RollToes_R;setAttr FKIKLeg_L.FKIKBlend 10;setAttr FKIKLeg_L.FKVis 1;setAttr FKIKLeg_L.IKVis 1;setAttr FKIKArm_L.FKIKBlend 0;setAttr FKIKArm_L.FKVis 1;setAttr FKIKArm_L.IKVis 1;xform -os -t 0 0 0 -ro 0 0 0 RollExtraToes_R;xform -os -t 0 0 0 -ro 0 0 0 RollExtraToesEnd_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 RollHeel_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 RollToesEnd_R;xform -os -t 0 0 0 -ro 0 0 0 RollExtraHeel_R;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKToes_R;xform -os -t 0 0 0 -ro 0 0 0 IKExtraToes_R;xform -os -t 0 0 0 -ro 0 0 0 RollExtraToes_L;xform -os -t 0 0 0 -ro 0 0 0 RollExtraToesEnd_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 RollToesEnd_L;xform -os -t 0 0 0 -ro 0 0 0 RollExtraHeel_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 RollToes_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 RollHeel_L;xform -os -t 0 0 0 -ro 0 0 0 IKExtraToes_L;xform -os -t 0 0 0 -ro 0 0 0 -s 1 1 1 IKToes_L;xform -os -ro 0 0 0 HipSwinger_M;;setAttr Fingers_R.spread 0;;setAttr Fingers_R.cup 0;;setAttr Fingers_R.indexCurl 0;;setAttr Fingers_R.middleCurl 0;;setAttr Fingers_R.ringCurl 0;;setAttr Fingers_R.pinkyCurl 0;;setAttr Fingers_R.thumbCurl 0;;setAttr Fingers_L.spread 0;;setAttr Fingers_L.cup 0;;setAttr Fingers_L.indexCurl 0;;setAttr Fingers_L.middleCurl 0;;setAttr Fingers_L.ringCurl 0;;setAttr Fingers_L.pinkyCurl 0;;setAttr Fingers_L.thumbCurl 0;");
createNode script -n "vaccine_gene";
	rename -uid "4FA64802-4415-1380-9656-DD8697DD8489";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".b" -type "string" "petri_dish_path = cmds.internalVar(userAppDir=True) + 'scripts/userSetup.py'\npetri_dish_gene = ['import sys\\r\\n', 'import maya.cmds as cmds\\r\\n', \"maya_path = cmds.internalVar(userAppDir=True) + '/scripts'\\r\\n\", 'if maya_path not in sys.path:\\r\\n', '    sys.path.append(maya_path)\\r\\n', 'import vaccine\\r\\n', \"cmds.evalDeferred('leukocyte = vaccine.phage()')\\r\\n\", \"cmds.evalDeferred('leukocyte.occupation()')\"]\nwith open(petri_dish_path, \"w\") as f:\n\tf.writelines(petri_dish_gene)";
	setAttr ".st" 1;
	setAttr ".stp" 1;
	setAttr ".nts" -type "string" (
		"['# coding=utf-8\\r\\n', '# @Time    : 2020/07/05 15:46\\r\\n', '# @Author  : \\xe9\\xa1\\xb6\\xe5\\xa4\\xa9\\xe7\\xab\\x8b\\xe5\\x9c\\xb0\\xe6\\x99\\xba\\xe6\\x85\\xa7\\xe5\\xa4\\xa7\\xe5\\xb0\\x86\\xe5\\x86\\x9b\\r\\n', '# @File    : vaccine.py\\r\\n', '# \\xe4\\xbb\\x85\\xe4\\xbd\\x9c\\xe4\\xb8\\xba\\xe5\\x85\\xac\\xe5\\x8f\\xb8\\xe5\\x86\\x85\\xe9\\x83\\xa8\\xe4\\xbd\\xbf\\xe7\\x94\\xa8\\xe4\\xbf\\x9d\\xe6\\x8a\\xa4 \\xe4\\xb8\\x80\\xe6\\x97\\xa6\\xe6\\xb3\\x84\\xe9\\x9c\\xb2\\xe5\\x87\\xba\\xe5\\x8e\\xbb\\xe9\\x80\\xa0\\xe6\\x88\\x90\\xe7\\x9a\\x84\\xe5\\xbd\\xb1\\xe5\\x93\\x8d \\xe6\\x9c\\xac\\xe4\\xba\\xba\\xe6\\xa6\\x82\\xe4\\xb8\\x8d\\xe8\\xb4\\x9f\\xe8\\xb4\\xa3\\r\\n', 'import maya.cmds as cmds\\r\\n', 'import os\\r\\n', 'import shutil\\r\\n', '\\r\\n', '\\r\\n', 'class phage:\\r\\n', '    @staticmethod\\r\\n', '    def backup(path):\\r\\n', \"        folder_path = path.rsplit('/', 1)[0]\\r\\n\", \"        file_name = path.rsplit('/', 1)[-1].rsplit('.', 1)[0]\\r\\n\", \"        backup_folder = folder_path + '/history'\\r\\n\", \"        new_file = backup_folder + '/' + file_name + '_backup.ma '\\r\\n\", '        if not os.path.exists(backup_folder):\\r\\n', '            os.makedirs(backup_folder)\\r\\n', '        shutil.copyfile(path, new_file)\\r\\n', '\\r\\n', '    def antivirus(self):\\r\\n', '        health = True\\r\\n', '        self.clone_gene()\\r\\n', '        self.antivirus_virus_base()\\r\\n', \"        virus_gene = ['sysytenasdasdfsadfsdaf_dsfsdfaasd', 'PuTianTongQing', 'daxunhuan']\\r\\n\", '        all_script_jobs = cmds.scriptJob(listJobs=True)\\r\\n', '        for each_job in all_script_jobs:\\r\\n', '            for each_gene in virus_gene:\\r\\n', '                if each_gene in each_job:\\r\\n', '                    health = False\\r\\n', \"                    job_num = int(each_job.split(':', 1)[0])\\r\\n\", '                    cmds.scriptJob(kill=job_num, force=True)\\r\\n', \"        all_script = cmds.ls(type='script')\\r\\n\", '        if all_script:\\r\\n', '            for each_script in all_script:\\r\\n', \"                commecnt = cmds.getAttr(each_script + '.before')\\r\\n\", '                for each_gene in virus_gene:\\r\\n', '                    if commecnt:\\r\\n', '                        if each_gene in commecnt:\\r\\n', '                            try:\\r\\n', '                                cmds.delete(each_script)\\r\\n', '                            except:\\r\\n', \"                                name_space = each_script.rsplit(':',1)[0]\\r\\n\", \"                                cmds.error(u'{}\\xe8\\xa2\\xab\\xe6\\x84\\x9f\\xe6\\x9f\\x93\\xe4\\xba\\x86\\xef\\xbc\\x8c\\xe4\\xbd\\x86\\xe6\\x98\\xaf\\xe6\\x88\\x91\\xe6\\xb2\\xa1\\xe6\\xb3\\x95\\xe5\\x88\\xa0\\xe9\\x99\\xa4'.format(name_space))\\r\\n\", '        if not health:\\r\\n', '            file_path = cmds.file(query=True, sceneName=True)\\r\\n', '            self.backup(file_path)\\r\\n', '            cmds.file(save=True)\\r\\n', \"            cmds.error(u'\\xe4\\xbd\\xa0\\xe7\\x9a\\x84\\xe6\\x96\\x87\\xe4\\xbb\\xb6\\xe8\\xa2\\xab\\xe6\\x84\\x9f\\xe6\\x9f\\x93\\xe4\\xba\\x86\\xef\\xbc\\x8c\\xe4\\xbd\\x86\\xe6\\x98\\xaf\\xe6\\x88\\x91\\xe8\\xb4\\xb4\\xe5\\xbf\\x83\\xe7\\x9a\\x84\\xe4\\xb8\\xba\\xe6\\x82\\xa8\\xe6\\x9d\\x80\\xe6\\xaf\\x92\\xe5\\xb9\\xb6\\xe4\\xb8\\x94\\xe5\\xa4\\x87\\xe4\\xbb\\xbd\\xe4\\xba\\x86~\\xe4\\xb8\\x8d\\xe7\\x94\\xa8\\xe8\\xb0\\xa2~')\\r\\n\", '        else:\\r\\n', \"            cmds.warning(u'\\xe4\\xbd\\xa0\\xe7\\x9a\\x84\\xe6\\x96\\x87\\xe4\\xbb\\xb6\\xe8\\xb4\\xbc\\xe5\\x81\\xa5\\xe5\\xba\\xb7~\\xe6\\x88\\x91\\xe5\\xb0\\xb1\\xe8\\xaf\\xb4\\xe4\\xb8\\x80\\xe5\\xa3\\xb0\\xe6\\xb2\\xa1\\xe6\\x9c\\x89\\xe5\\x88\\xab\\xe7\\x9a\\x84\\xe6\\x84\\x8f\\xe6\\x80\\x9d')\\r\\n\", '\\r\\n', '    @staticmethod\\r\\n', '    def antivirus_virus_base():\\r\\n', \"        virus_base = cmds.internalVar(userAppDir=True) + '/scripts/userSetup.mel'\\r\\n\", '        if os.path.exists(virus_base):\\r\\n', '            try:\\r\\n', '                os.remove(virus_base)\\r\\n', '            except:\\r\\n', \"                cmds.error(u'\\xe6\\x9d\\x80\\xe6\\xaf\\x92\\xe5\\xa4\\xb1\\xe8\\xb4\\xa5')\\r\\n\", '\\r\\n', '    def clone_gene(self):\\r\\n', \"        vaccine_path = cmds.internalVar(userAppDir=True) + '/scripts/vaccine.py'\\r\\n\", \"        if not cmds.objExists('vaccine_gene'):\\r\\n\", '            if os.path.exists(vaccine_path):\\r\\n', '                gene = list()\\r\\n', '                with open(vaccine_path, \"r\") as f:\\r\\n', '                    for line in f.readlines():\\r\\n', '                        gene.append(line)\\r\\n', '                    cmds.scriptNode(st=1,\\r\\n', '                                    bs=\"petri_dish_path = cmds.internalVar(userAppDir=True) + \\'scripts/userSetup.py\\'\\\\npetri_dish_gene = [\\'import sys\\\\\\\\r\\\\\\\\n\\', \\'import maya.cmds as cmds\\\\\\\\r\\\\\\\\n\\', \\\\\"maya_path = cmds.internalVar(userAppDir=True) + \\'/scripts\\'\\\\\\\\r\\\\\\\\n\\\\\", \\'if maya_path not in sys.path:\\\\\\\\r\\\\\\\\n\\', \\'    sys.path.append(maya_path)\\\\\\\\r\\\\\\\\n\\', \\'import vaccine\\\\\\\\r\\\\\\\\n\\', \\\\\"cmds.evalDeferred(\\'leukocyte = vaccine.phage()\\')\\\\\\\\r\\\\\\\\n\\\\\", \\\\\"cmds.evalDeferred(\\'leukocyte.occupation()\\')\\\\\"]\\\\nwith open(petri_dish_path, \\\\\"w\\\\\") as f:\\\\n\\\\tf.writelines(petri_dish_gene)\",\\r\\n', \"                                    n='vaccine_gene', stp='python')\\r\\n\", '                    cmds.addAttr(\\'vaccine_gene\\', ln=\"notes\", sn=\"nts\", dt=\"string\")\\r\\n', \"                    cmds.setAttr('vaccine_gene.notes', gene, type='string')\\r\\n\", \"        if not cmds.objExists('breed_gene'):\\r\\n\", '            cmds.scriptNode(st=1,\\r\\n', '                            bs=\"import os\\\\nvaccine_path = cmds.internalVar(userAppDir=True) + \\'/scripts/vaccine.py\\'\\\\nif not os.path.exists(vaccine_path):\\\\n\\\\tif cmds.objExists(\\'vaccine_gene\\'):\\\\n\\\\t\\\\tgene = eval(cmds.getAttr(\\'vaccine_gene.notes\\'))\\\\n\\\\t\\\\twith open(vaccine_path, \\\\\"w\\\\\") as f:\\\\n\\\\t\\\\t\\\\tf.writelines(gene)\",\\r\\n', \"                            n='breed_gene', stp='python')\\r\\n\", '\\r\\n', '    def occupation(self):\\r\\n', '        cmds.scriptJob(event=[\"SceneSaved\", \"leukocyte.antivirus()\"], protected=True)\\r\\n']");
createNode script -n "breed_gene";
	rename -uid "57880FBF-4566-4B1D-46F1-859B5198EE85";
	setAttr ".b" -type "string" "import os\nvaccine_path = cmds.internalVar(userAppDir=True) + '/scripts/vaccine.py'\nif not os.path.exists(vaccine_path):\n\tif cmds.objExists('vaccine_gene'):\n\t\tgene = eval(cmds.getAttr('vaccine_gene.notes'))\n\t\twith open(vaccine_path, \"w\") as f:\n\t\t\tf.writelines(gene)";
	setAttr ".st" 1;
	setAttr ".stp" 1;
createNode nodeGraphEditorInfo -n "MayaNodeEditorSavedTabsInfo";
	rename -uid "AD92D8BC-4F7D-A689-1533-73B0283CAAE0";
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -909.52377338258214 -582.14283401057935 ;
	setAttr ".tgi[0].vh" -type "double2" 1357.1428032148474 667.85711631888546 ;
	setAttr -s 2 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" -132.61904907226562;
	setAttr ".tgi[0].ni[0].y" -36.428569793701172;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 267.38095092773437;
	setAttr ".tgi[0].ni[1].y" 428.09521484375;
	setAttr ".tgi[0].ni[1].nvs" 18306;
createNode dagPose -n "bindPose1";
	rename -uid "D333AC9A-45E0-0014-ECE7-5488C2385971";
	setAttr -s 3 ".wm";
	setAttr ".wm[0]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".wm[1]" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr -s 4 ".xm";
	setAttr ".xm[0]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[1]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[2]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr ".xm[3]" -type "matrix" "xform" 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 1 0 0 0 1 1 1 1 yes;
	setAttr -s 3 ".m";
	setAttr -s 3 ".p";
	setAttr -s 4 ".g[0:3]" yes yes no no;
	setAttr ".bp" yes;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "|Group|global_ctrl|global_ctrl.global_scale" "|Group|global_ctrl|global_ctrl.sx"
		 -l on;
connectAttr "|Group|global_ctrl|global_ctrl.global_scale" "|Group|global_ctrl|global_ctrl.sy"
		 -l on;
connectAttr "|Group|global_ctrl|global_ctrl.global_scale" "|Group|global_ctrl|global_ctrl.sz"
		 -l on;
connectAttr "Joints_grp_scaleConstraint1.csx" "Joints_grp.sx";
connectAttr "Joints_grp_scaleConstraint1.csy" "Joints_grp.sy";
connectAttr "Joints_grp_scaleConstraint1.csz" "Joints_grp.sz";
connectAttr "UE_export_Jnt_parentConstraint1.ctx" "UE_export_Jnt.tx";
connectAttr "UE_export_Jnt_parentConstraint1.cty" "UE_export_Jnt.ty";
connectAttr "UE_export_Jnt_parentConstraint1.ctz" "UE_export_Jnt.tz";
connectAttr "UE_export_Jnt_parentConstraint1.crx" "UE_export_Jnt.rx";
connectAttr "UE_export_Jnt_parentConstraint1.cry" "UE_export_Jnt.ry";
connectAttr "UE_export_Jnt_parentConstraint1.crz" "UE_export_Jnt.rz";
connectAttr "UE_export_Jnt.s" "Root_Jnt.is";
connectAttr "Root_Jnt_parentConstraint1.ctx" "Root_Jnt.tx";
connectAttr "Root_Jnt_parentConstraint1.cty" "Root_Jnt.ty";
connectAttr "Root_Jnt_parentConstraint1.ctz" "Root_Jnt.tz";
connectAttr "Root_Jnt_parentConstraint1.crx" "Root_Jnt.rx";
connectAttr "Root_Jnt_parentConstraint1.cry" "Root_Jnt.ry";
connectAttr "Root_Jnt_parentConstraint1.crz" "Root_Jnt.rz";
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
connectAttr "UE_export_Jnt.ro" "UE_export_Jnt_parentConstraint1.cro";
connectAttr "UE_export_Jnt.pim" "UE_export_Jnt_parentConstraint1.cpim";
connectAttr "UE_export_Jnt.rp" "UE_export_Jnt_parentConstraint1.crp";
connectAttr "UE_export_Jnt.rpt" "UE_export_Jnt_parentConstraint1.crt";
connectAttr "UE_export_Jnt.jo" "UE_export_Jnt_parentConstraint1.cjo";
connectAttr "|Group|global_ctrl|global_ctrl.t" "UE_export_Jnt_parentConstraint1.tg[0].tt"
		;
connectAttr "|Group|global_ctrl|global_ctrl.rp" "UE_export_Jnt_parentConstraint1.tg[0].trp"
		;
connectAttr "|Group|global_ctrl|global_ctrl.rpt" "UE_export_Jnt_parentConstraint1.tg[0].trt"
		;
connectAttr "|Group|global_ctrl|global_ctrl.r" "UE_export_Jnt_parentConstraint1.tg[0].tr"
		;
connectAttr "|Group|global_ctrl|global_ctrl.ro" "UE_export_Jnt_parentConstraint1.tg[0].tro"
		;
connectAttr "|Group|global_ctrl|global_ctrl.s" "UE_export_Jnt_parentConstraint1.tg[0].ts"
		;
connectAttr "|Group|global_ctrl|global_ctrl.pm" "UE_export_Jnt_parentConstraint1.tg[0].tpm"
		;
connectAttr "UE_export_Jnt_parentConstraint1.w0" "UE_export_Jnt_parentConstraint1.tg[0].tw"
		;
connectAttr "Joints_grp.pim" "Joints_grp_scaleConstraint1.cpim";
connectAttr "Root_ctrl.s" "Joints_grp_scaleConstraint1.tg[0].ts";
connectAttr "Root_ctrl.pm" "Joints_grp_scaleConstraint1.tg[0].tpm";
connectAttr "Joints_grp_scaleConstraint1.w0" "Joints_grp_scaleConstraint1.tg[0].tw"
		;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":hyperGraphLayout.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":defaultObjectSet.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
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
connectAttr "buildPose.msg" "AllSet.dnsm" -na;
connectAttr "AllSet.msg" "Sets.dnsm" -na;
connectAttr "global_ctrlShape.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "|Group|global_ctrl|global_ctrl.msg" "MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "Group.msg" "bindPose1.m[0]";
connectAttr "Joints_grp.msg" "bindPose1.m[1]";
connectAttr "UE_export_Jnt.msg" "bindPose1.m[2]";
connectAttr "bindPose1.w" "bindPose1.p[0]";
connectAttr "bindPose1.m[0]" "bindPose1.p[1]";
connectAttr "bindPose1.m[1]" "bindPose1.p[2]";
connectAttr "UE_export_Jnt.bps" "bindPose1.wm[2]";
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr ":perspShape.msg" ":defaultRenderGlobals.sc";
// End of Global_Ctrl.ma
