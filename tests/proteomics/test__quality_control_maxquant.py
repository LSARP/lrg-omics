import pandas as pd
import os

from lrg_omics.proteomics.quality_control.maxquant import maxquant_qc, maxquant_qc_summary, \
     maxquant_qc_protein_groups, maxquant_qc_peptides, maxquant_qc_msmScans, maxquant_qc_evidence

PATH = os.path.join('tests', 'data', 'maxquant', 'tmt11', 'example-0')


class TestClass:
    def test__maxquant_qc_summary(self):
        out = maxquant_qc_summary(PATH)

        # check if type(out) is pd.Series
        assert isinstance(out, pd.Series), f'It is a {type(out)} not a Series'

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file
        expected_cols = ["MS", "MS/MS", "MS3", "MS/MS Submitted", "MS/MS Identified", "MS/MS Identified [%]",
                         "Peptide Sequences Identified", "Av. Absolute Mass Deviation [mDa]", "Mass Standard "
                                                                                              "Deviation [mDa]"]

        assert len(expected_cols) - len(out.index) == 0, f'New columns {out.index[len(expected_cols):]} in output ' \
                                                         f'file. Adjust expected_cols variable accordingly'

        # check for mismatches between columns in expected_cols and out
        assert len(list(set(expected_cols) - set(out.index))) == 0, list(set(expected_cols) - set(out.index))

        # check if there is any NaN value in out
        assert ~out.isnull().values.any(), f'NaN value at {out.index[out.isna().any()].tolist()}'

    def test__maxquant_qc_protein_groups(self):
        out = maxquant_qc_protein_groups(PATH, protein=None)

        # check if type(out) is pd.Series
        assert isinstance(out, pd.Series), f'It is a {type(out)} not a Series'

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file
        expected_cols = ["N_protein_groups", "N_protein_true_hits", "N_protein_potential_contaminants",
                         "N_protein_reverse_seq", "Protein_mean_seq_cov [%]", "TMT1_missing_values",
                         "TMT2_missing_values", "TMT3_missing_values", "TMT4_missing_values", "TMT5_missing_values",
                         "TMT6_missing_values", "TMT7_missing_values", "TMT8_missing_values", "TMT9_missing_values",
                         "TMT10_missing_values", "TMT11_missing_values", "N_of_Protein_qc_pepts",
                         "N_Protein_qc_missing_values", "reporter_intensity_corrected_Protein_qc_ave",
                         "reporter_intensity_corrected_Protein_qc_sd", "reporter_intensity_corrected_Protein_qc_cv"]

        assert len(expected_cols) - len(out.index) == 0, f'New columns {out.index[len(expected_cols):]} in output ' \
                                                         f'file. Adjust expected_cols variable accordingly'

        # check for mismatches between columns in expected_cols and out
        assert len(list(set(expected_cols) - set(out.index))) == 0, list(set(expected_cols) - set(out.index))

        # check if there is any NaN values in out
        assert ~out.isnull().values.any(), f'NaN value at {out.index[out.isna().any()].tolist()}'

    def test__maxquant_qc_peptides(self):
        out = maxquant_qc_peptides(PATH)

        # check if type(out) is pd.Series
        assert isinstance(out, pd.Series), f'It is a {type(out)} not a Series'

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file
        expected_cols = ['N_peptides', 'N_peptides_potential_contaminants', 'N_peptides_reverse', 'Oxidations [%]',
                         'N_missed_cleavages_total', 'N_missed_cleavages_eq_0 [%]', 'N_missed_cleavages_eq_1 [%]',
                         'N_missed_cleavages_eq_2 [%]', 'N_missed_cleavages_gt_3 [%]',
                         'N_peptides_last_amino_acid_K [%]', 'N_peptides_last_amino_acid_R [%]',
                         'N_peptides_last_amino_acid_other [%]']

        assert len(expected_cols) - len(out.index) == 0, f'New columns {out.index[len(expected_cols):]} in output ' \
                                                         f'file. Adjust expected_cols variable accordingly'

        # check for mismatches between columns in expected_cols and out
        assert len(list(set(expected_cols) - set(out.index))) == 0, list(set(expected_cols) - set(out.index))

        # check if there is any NaN values in out
        assert ~out.isnull().values.any(), f'NaN value at {out.index[out.isna().any()].tolist()}'

    def test__maxquant_qc_msmScans(self):
        out = maxquant_qc_msmScans(PATH)

        # check if type(out) is pd.Series
        assert isinstance(out, pd.Series), f'It is a {type(out)} not a Series'

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file
        expected_cols = ['Mean_parent_int_frac']

        assert len(expected_cols) - len(out.index) == 0, f'New columns {out.index[len(expected_cols):]} in output ' \
                                                         f'file. Adjust expected_cols variable accordingly'

        # check for mismatches between columns in expected_cols and out
        assert len(list(set(expected_cols) - set(out.index))) == 0, list(set(expected_cols) - set(out.index))

        # check if there is any NaN values in out
        assert ~out.isnull().values.any(), f'NaN value at {out.index[out.isna().any()].tolist()}'

    def test__maxquant_qc_evidence(self):
        out = maxquant_qc_evidence(PATH, pept_list=None)

        # check if type(out) is pd.Series
        assert isinstance(out, pd.Series), f'It is a {type(out)} not a Series'

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file
        expected_cols = ['Uncalibrated - Calibrated m/z [ppm] (ave)', 'Uncalibrated - Calibrated m/z [ppm] (sd)',
                         'Uncalibrated - Calibrated m/z [Da] (ave)', 'Uncalibrated - Calibrated m/z [Da] (sd)',
                         'Peak Width(ave)', 'Peak Width (std)', 'qc1_peptide_charges', 'N_qc1_missing_values',
                         'reporter_intensity_corrected_qc1_ave', 'reporter_intensity_corrected_qc1_sd',
                         'reporter_intensity_corrected_qc1_cv', 'calibrated_retention_time_qc1', 'retention_length_qc1',
                         'N_of_scans_qc1', 'qc2_peptide_charges', 'N_qc2_missing_values',
                         'reporter_intensity_corrected_qc2_ave', 'reporter_intensity_corrected_qc2_sd',
                         'reporter_intensity_corrected_qc2_cv', 'calibrated_retention_time_qc2', 'retention_length_qc2',
                         'N_of_scans_qc2']

        assert len(expected_cols) - len(out.index) == 0, f'New columns {out.index[len(expected_cols):]} in output ' \
                                                         f'file. Adjust expected_cols variable accordingly'

        # check for mismatches between columns in expected_cols and out
        assert len(list(set(expected_cols) - set(out.index))) == 0, list(set(expected_cols) - set(out.index))

        # check if there is any NaN values in out
        assert ~out.isnull().values.any(), f'NaN value at {out.index[out.isna().any()].tolist()}'

    def test__maxquant_qc_columns(self):

        result =  maxquant_qc(PATH, protein=None, pept_list=None)
        actual_cols = result.columns.to_list()

        # check if the lengths of expected_cols and out are different. Useful to see if new columns were added in
        # maxquant.py but not in the test file
        expected_cols = ['Date', 'MS', 'MS/MS', 'MS3', 'MS/MS Submitted', 'MS/MS Identified', 'MS/MS Identified [%]', 'Peptide Sequences Identified', 'Av. Absolute Mass Deviation [mDa]', 'Mass Standard Deviation [mDa]', 'N_protein_groups', 'N_protein_true_hits', 'N_protein_potential_contaminants', 'N_protein_reverse_seq', 'Protein_mean_seq_cov [%]', 'TMT1_missing_values', 'TMT2_missing_values', 'TMT3_missing_values', 'TMT4_missing_values', 'TMT5_missing_values', 'TMT6_missing_values', 'TMT7_missing_values', 'TMT8_missing_values', 'TMT9_missing_values', 'TMT10_missing_values', 'TMT11_missing_values', 'N_peptides', 'N_peptides_potential_contaminants', 'N_peptides_reverse', 'Oxidations [%]', 'N_missed_cleavages_total', 'N_missed_cleavages_eq_0 [%]', 'N_missed_cleavages_eq_1 [%]', 'N_missed_cleavages_eq_2 [%]', 'N_missed_cleavages_gt_3 [%]', 'N_peptides_last_amino_acid_K [%]', 'N_peptides_last_amino_acid_R [%]', 'N_peptides_last_amino_acid_other [%]', 'Mean_parent_int_frac', 'Uncalibrated - Calibrated m/z [ppm] (ave)', 'Uncalibrated - Calibrated m/z [ppm] (sd)', 'Uncalibrated - Calibrated m/z [Da] (ave)', 'Uncalibrated - Calibrated m/z [Da] (sd)', 'Peak Width(ave)', 'Peak Width (std)', 'qc1_peptide_charges', 'N_qc1_missing_values', 'reporter_intensity_corrected_qc1_ave', 'reporter_intensity_corrected_qc1_sd', 'reporter_intensity_corrected_qc1_cv', 'calibrated_retention_time_qc1', 'retention_length_qc1', 'N_of_scans_qc1', 'qc2_peptide_charges', 'N_qc2_missing_values', 'reporter_intensity_corrected_qc2_ave', 'reporter_intensity_corrected_qc2_sd', 'reporter_intensity_corrected_qc2_cv', 'calibrated_retention_time_qc2', 'retention_length_qc2', 'N_of_scans_qc2', 'N_of_Protein_qc_pepts', 'N_Protein_qc_missing_values', 'reporter_intensity_corrected_Protein_qc_ave', 'reporter_intensity_corrected_Protein_qc_sd', 'reporter_intensity_corrected_Protein_qc_cv']
        
        print(actual_cols)

        assert actual_cols == expected_cols, 'Columns do not match'

     



