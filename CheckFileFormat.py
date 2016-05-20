import sys
import os

#only check file in this directory
G_OnlyCheckInDirectory="Content/StarVR"

#key:value key should be put into value directory
G_PrefixFormatList={
    "BP_"  :  "Blueprints",
    "BPI_" :  "Blueprints",
    "BPF_" :  "Blueprints",
    "BPM_" :  "Blueprints",

    "UMG_" :  "UMG",
    "UI_"  :  "UMG",

    "M_"   :  "Materials",
    "MF_"  :  "Materials",
    "MPC_" :  "Materials",

    "T_"   :  "Textures",

    "P_"   :  "Effects",

    "BT_"  :  "AI",
    "BDD_" :  "AI",
    "BTT_" :  "AI",
    "BTS_" :  "AI",
    "EQ_"  :  "AI",

    "L_"   :  "Maps",

    "BPA_" :  "Animations",
    "A_"   :  "Animations",
    "AO_"  :  "Animations",
    "BS_"  :  "Animations",

    "S_"   :  "Sounds",

    "PP_"  :  "Paper2D",
    "FB_"  :  "Paper2D",

    "PM_"  :  "Physics",

    "SKM_" :  "SkeletalMesh",

    "SM_"  :  "StaticMesh",
    }

#key:value key should only have value files
G_DirectoryFormatList={
    "Blueprints":"BP_,BPI_,BPF_,BPM_",
    "UMG":"UMG_,UI_",
    "Materials":"M_,MF_,MPC_",
    "Textures":"T_",
    "Effects":"P_",
    "AI":"BT_,BDD_,BTT_,BTS_,EQ_",
    "Maps":"L_",
    "Animations":"BPA_,A_,AO_,BS_",
    "Sounds":"S_",
    "Paper2D":"PP_,FB_",
    "Physics":"PM_",
    "SkeletalMesh":"SKM_",
    "StaticMesh":"SM_",
    #"Misc":(),
    }

#return WhetherError(true is error),ErrorString
def checkFileName(FileName):
    BaseName = os.path.basename(FileName)
    DirName = os.path.dirname(FileName)

    #if is directory,do nothing
    if BaseName == "":
        return False,""

    if not G_OnlyCheckInDirectory in DirName:
        return False,""

    Name,Ext = os.path.splitext(BaseName)
    if Ext != ".uasset":
        return True,"file[%s] is not unreal 4 asset."%BaseName

    Prefix = BaseName.split("_")[0]
    Prefix = Prefix + "_"
    #if have prefix,committer should be aware of directory category
    if Prefix in G_PrefixFormatList.keys():
        if not G_PrefixFormatList[Prefix] in DirName:
            return True,"file[%s] have perfix[%s] should be put into diretory[%s]"%(BaseName,Prefix,G_PrefixFormatList[Prefix])
        else:
            return False,""
    else:
        if "Misc" in DirName:
            return False,""

        for (Dir,Files) in G_DirectoryFormatList.items():
            if Dir in DirName:
                return True,"file[%s] in directory[%s] should have prefix[%s]"%(BaseName,Dir,Files)

        return False,""


def main():
    if len(sys.argv) < 2:
        exit(1)

    FileList = sys.argv[1].split("\n")
    CheckFailed = False
    ErrorOutput = "=====================================\n"
    for File in FileList:
        RealFileName = File.split()[1]
        HaveError,ErrorString = checkFileName(RealFileName)
        if HaveError:
            CheckFailed = True
            ErrorOutput = ErrorOutput + ErrorString + "\n"
    ErrorOutput = ErrorOutput + "=====================================\n"

    if CheckFailed:
        sys.stderr.write(ErrorOutput)
        exit(1)


if __name__ == "__main__":
    main()



