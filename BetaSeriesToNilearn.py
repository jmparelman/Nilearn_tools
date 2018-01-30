import re
from nilearn.image import load_img
import glob

def BetaSeriesToNilearn(subPath, Selecting = None, critereonList = None, Beta = True):
    """
    Convenience function for importing betaseries beta estimates from spm first-level model.
    Returns data as nilearn nifti object. 
    
    args:
        subjPath: subject model path
        
        Selecting: if None, select all beta maps in subject directory. Other options 
                   are Include or Exclude
                   
        critereonList: if Selecting, a list of labels to include or exclude in import
        
        Beta = if True selects beta maps, if False selects spmT files. 
        
    returns: 
        image = 4D image nilearn nifti image
        beta_names = list of condition names
        
    """
    
    beta_names = []
    volumes = []
    
    stat = 'beta_*.hdr' if Beta else 'spmT_*.hdr'
    regex = '(?<=Sn\(.\) ).*(?=\*)' if Beta else '(?<=: )(.*)'
    
    for beta in glob.glob(subPath + stat):
        beta_image_header = str(load_img(beta).header.values()[28])
        try:
            beta_name = re.findall(regex,beta_image_header)[0]

            if Selecting:
                if Selecting == 'Exclude' and beta_name not in critereonList:
                    beta_names.append(beta_name)
                    volumes.append(beta)
                elif Selecting == 'Include' and beta_name in critereonList:
                    beta_names.append(beta_name)
                    volumes.append(beta)
            else:
                beta_names.append(beta_name)
                volumes.append(beta)

        except:
            continue
            
    image = load_img(volumes)
    return image, beta_names


