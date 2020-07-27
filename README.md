# LRG codebase for omics integration 

Lewis Research Group (LRG) codebase for omics data generation, processing, quality control and integration. 

##  Download and install from source

    git clone https://github.com/LSARP/lrg_omics
    cd lrg_omics
    
    conda env create -y -f environment.yml
    conda activate omics
    pip install -e . 

    jupyter labextension install jupyterlab-plotly@4.8.2
    jupyter labextension install @jupyter-widgets/jupyterlab-manager plotlywidget@4.8.2
    ipython kernel install --name "LRG" --user


## Test data

You can download test data from https://soerendip.com/dl/lrg_omics_test_data

E.g. with `wget`:

    wget -R https://soerendip.com/dl/lrg_omics_test_data
    
    
