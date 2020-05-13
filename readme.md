# Small-Holder Agriculture Mitigation Benefit Assessment (SHAMBA) project. version 1.1

The shamba tool [user guide](docs/user-guide.md) has detailed instructions on how to install and use the SHAMBA tool.

The model_documentation folder contains the detailed scientific description of the model, as well documentation on how to implement the Plan Vivo Approved Approach for using SHAMBA.

View the `shamba_cl.py` file in a Python IDE for details on how to run SHAMBA with the excel_data_input_templates. The script is already set up to run with the example with the è `example_SHAMBA_input_output_uganda_tech_spec.xlsx` file.

## Community

For any help or issued, please contact the community here [https://framavox.org/shamba](https://framavox.org/shamba/).

## DATA

Please unzip the soil data file `./shamba/rasters/soil/hwsd.7z`.

## GUI version

See sample_input_files folder or projects/sample_project_gui/input for sample input files (climate, soil information, and tree growth) that can be loaded in the gui, and projects/sample_project_gui/output for sample raw output.

## Command-line version

To use the SHAMBA model sans GUI, see the `shamba_cl.py` file in the shamba directory for a sample of how to piece together the various modules (in the shamba.model package) to run the model. See model modules for specific info about each model and docstrings detailing the various alternate constructors (classmethods).
