# GeSe-Based Non-Invasive Glucose Biosensor

**Flexible nanomaterial sensor for optical glucose detection using polarimetry and machine learning**

[![Paper 1](https://img.shields.io/badge/ACE_2024-Published-blue)](https://doi.org/10.54254/2755-2721/72)
[![Paper 2](https://img.shields.io/badge/Biosensors_&_Bioelectronics_2025-Published-blue)](https://doi.org/10.1016/j.bios.2025)
[![Patent](https://img.shields.io/badge/U.S._Patent-19%2F203%2C391-green)]()

## Overview

This project develops a flexible, wearable biosensor platform for continuous non-invasive glucose monitoring. The sensor uses **germanium selenide (GeSe) nanomaterial photodetectors** to measure glucose concentration through optical polarimetry, with machine learning algorithms for real-time calibration.

## Key Results

| Metric | Value |
|--------|-------|
| Coefficient of Determination (R²) | **0.94** |
| Mean Absolute Error (MAE) | **≈ 8.6 mg/dL** |
| Localization Method | Optical Polarimetry |
| ML Calibration | Supervised regression model |

## Methodology

### Sensing Principle
Glucose in biological fluids rotates the plane of polarized light. The GeSe photodetector measures this rotation with high sensitivity due to the material's anisotropic optical properties.

### Evolution of the Platform
1. **Generation 1:** Flexible GeSe nanomaterial sensor with conventional polarimetric detection and ML calibration
2. **Generation 2:** Polarizer-free architecture exploiting in-plane anisotropy of 2D GeSe for chiroptical biosensing, enabling a more compact wearable form factor

### Machine Learning Pipeline
- Feature extraction from raw optical signals
- Supervised regression for glucose concentration prediction
- Cross-validation against commercial glucometer reference

## Publications

1. M. B. Kopp, "Flexible Nanomaterial Sensors for Non-Invasive Health Monitoring," *Applied and Computational Engineering*, vol. 72, pp. 45-58, 2024.

2. M. B. Kopp, "Next-Generation Polarimetric Biosensors: Machine Learning-Driven GeSe Photodetectors for Noninvasive Glucose Monitoring," *Biosensors & Bioelectronics*, 2025 (open access).

3. M. B. Kopp, "Exploiting In-Plane Anisotropy of 2D GeSe for Polarizer-Free Chiroptical Biosensing: Machine Learning-Enhanced Wearable Glycemic Diagnostics." *(in preparation)*

## Awards

- **S.T. Yau High School Science Award** — Bronze Medal, Physics (North America Top 3), 2024
- **NJSHS National Symposium** — 3rd Place Poster Award (Dept. of Defense), 2024

## Tools & Technologies

- **Simulation:** COMSOL Multiphysics (optical modeling)
- **Data Analysis:** Python, MATLAB
- **Fabrication:** Nanomaterial synthesis, flexible substrate processing
- **ML Frameworks:** scikit-learn, custom calibration pipelines

## Repository Structure

```
gese-glucose-biosensor/
├── figures/            # Schematics and result visualizations
├── README.md
└── LICENSE
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contact

**Maximilian Kopp** — [maxkopptech.com](https://www.maxkopptech.com) | [ORCID](https://orcid.org/0009-0008-6431-8137) | [Google Scholar](https://scholar.google.com/citations?user=TrKuDMsAAAAJ)
