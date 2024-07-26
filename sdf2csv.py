import os
import sys
import pandas as pd
from rdkit import Chem

def sdf2csv(sdf_filename):
    suppl = Chem.SDMolSupplier(sdf_filename)
    print(f'# of molecuels in the input sdf file = {len(suppl)}')
    
    props_dict = dict()
    for idx, mol in enumerate(suppl):
        try:
            prop_dict = mol.GetPropsAsDict()
        except UnicodeDecodeError:
            prop_dict = dict()
            for name in mol.GetPropNames():
                try:
                    prop_dict[name] = mol.GetProp(name)
                except UnicodeDecodeError:
                    prop_dict[name] = ''

        prop_dict['SMILES'] = Chem.MolToSmiles(mol)
        props_dict[str(idx)] = prop_dict
    
    props_df = pd.DataFrame(props_dict).T
#     print(props_df.shape)
    props_df.to_csv(f'{os.path.splitext(sdf_filename)[0]}.csv', index=False)
    

if __name__ == '__main__':
    sdf2csv(sys.argv[1])