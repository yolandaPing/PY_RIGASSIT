from maya import mel


def definePaintContextCallbacks():
    """
    Maya expects some mel procedures to be present for paint context metadata
    """

    mel.eval(
        """
        global proc ngst2PaintContextProperties() {
            setUITemplate -pushTemplate DefaultTemplate;
            setUITemplate -popTemplate;
            
        }
        
        global proc ngst2PaintContextValues(string $toolName) 
        {
            string $icon = "ngSkinToolsShelfIcon.png";
            string $help = "ngSkinTools2 - paint skin weights";
            toolPropertySetCommon $toolName $icon $help;    
        }
    """
    )
