# Unified Code for Units of Measure (UCUM)
Sam Tomioka

This repository contains the evaluation results of the [Unified Code for Units of Measure (UCUM) Resources](https://ucum.nlm.nih.gov/ucum-lhc/index.html) and the [test version](http://www.xml4pharma.com/UCUM/Instructions_for_testing_the_RESTful_web_service_for_molar_mass_unit_conversions.pdf).


## 1. Background
The verification of scientific units and conversion from the reported units to standard units have been always challenging for Data Science due to several reasons:

1. Need a lookup table that consists of all possible input and output units for measurements, name of the measurements (e.g. Glucose, Weight, ...), conversion factors, molar weights etc.
2. The names of the measurement in the lookup table and incoming data must match
3. The incoming units must be in the lookup table
4. Maintenance of the lookup table must be synched with standard terminology update
5. Require careful medical review in addition to laborsome Data Science review
and more...

Despite the challenges, the lookup table approach is the norm for many companies for verification of the units and conversion. Consideration was given for more systematic approach that does not require to use the lab test names[1], but some units rely on molar weight and/or valence of ion of the specific lab tests, so this approach does not solve the problem. The regulatory agencies require the sponsor to use standardized units for reporting and analysis[2]. The PMDA requires SI units for all reporting and analysis[3,4]. The differences in requirement force us to maintain region specific conversion for some measurements which add additional complexity.

The approach Jozef Aerts discussed uses RestAPI available through [Unified Code for Units of Measure (UCUM) Resources](https://ucum.nlm.nih.gov/ucum-lhc/index.html) which is maintained by the US National Library of Medicine (NLM)[5]. The benefit is obvious that we can potentially eliminate the maintenance of the lab conversion lookup table. Here is what they say about themselves.

>The Unified Code for Units of Measure (UCUM) is a code system intended to include all units of measures being contemporarily used in international science, engineering, and business. The purpose is to facilitate unambiguous electronic communication of quantities together with their units. The focus is on electronic communication, as opposed to communication between humans. A typical application of The Unified Code for Units of Measure are electronic data interchange (EDI) protocols, but there is nothing that prevents it from being used in other types of machine communication.

The UCUM is the ISO 11240 compliant standard and has been used in ICSR E2B submissions for regulators adopted ICH E2B(R3). [FDA requires the UCUM codes](https://www.fda.gov/industry/fda-resources-data-standards/units-measurement) for the [eVAERS ICSR E2B (R3) submissions](https://www.fda.gov/media/98617/download), [dosage strength in both content of product labeling](https://www.fda.gov/industry/fda-resources-data-standards/structured-product-labeling-resources) and [Drug Establishment Registration and Drug Listing](https://www.fda.gov/regulatory-information/search-fda-guidance-documents/providing-regulatory-submissions-electronic-format-drug-establishment-registration-and-drug-listing). UCUM codes have been adopted by HL7 [FHIR](https://www.hl7.org/fhir/terminologies-systems.html).

### 1-1 Update May 2019
Jozef Aerts [announced](http://www.xml4pharma.com/UCUM/Instructions_for_testing_the_RESTful_web_service_for_molar_mass_unit_conversions.pdf) an updated RESTful API which accounts for the molecular weights of the analyte into the conversion between molar and mass concentrations. This additional functionality would facilitate the conversion of the lab results, verification of the standardized lab results and LOINC code provided by the vendors.

Although CDISC released a downloadable [CDISC UNIT and UCUM mapping xlsx file](https://www.cdisc.org/standards/terminology), this evaluation will not use it since CDISC UNIT does not cover all reported units used by the clinical laboratory/bioanalytical/PK vendors. Regular expression along with UCUM unit validity service was used to convert and verify the units provided by the lab vendors before using conversion RestAPI.

## 2. Findings

1. The initial evaluation was done on RestAPI available through [Unified Code for Units of Measure (UCUM) Resources](https://ucum.nlm.nih.gov/ucum-lhc/index.html) and the findings are summarized [here](https://stomioka.github.io/ucum/docs/usum_201902.html).
2. The second evaluation is completed on the test version of RestAPI provided by Jozef Aerts at [xml4pharma](http://www.xml4pharma.com/). The findings are summarized [here](https://stomioka.github.io/ucum/docs/ucum_201905-test-large-sample.html).
3. The third evaluation is completed on the test version of RestAPI provided by Jozef Aerts at [xml4pharma](http://www.xml4pharma.com/). Several improvements were implemented since the second evaluation was completed.
* The return message contains the MW that was used for the conversion.

  ![](docs/images/newmsg.png)

* Previously, there was one kind of error message related to LOINC. For example,
>Error message "ERROR: No MW value for the LOINC code xxx-x is available or the LOINC code is invalid"

The updated service returns LOINC related error message either
  1. Invalid LOINC code XXXX
  2. No MW found for LOINC Part Number LPxxxx for LOINC code yyyy<br>
    This updates allow us to investigate issues without browsing LOINC.

* The list of MW for the LOINC-component-part  was extended

The findings are summarized [here](https://stomioka.github.io/ucum/docs/ucum_201905-test-large-sample-update.html).
