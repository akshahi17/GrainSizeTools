![](https://raw.githubusercontent.com/marcoalopez/GrainSizeTools/master/FIGURES/new_header.png)

*This project is maintained by [Marco A. Lopez-Sanchez](https://marcoalopez.github.io/) - Last update (website): 2018/06/12*  

[GrainSizeTools script](http://marcoalopez.github.io/GrainSizeTools/) is a free, open-source, cross-platform script written in [Python](https://www.python.org/) that provides several tools for visualizing and estimating grain size in polycrystalline materials. The script is able to **estimate differential stress through paleopiezometers**, implementing multiple piezometric relations for comparison, and to derive the actual (3D) grain size distribution from thin sections using the Saltykov and the two-step methods. The script only requires as input the areas of the grain profiles measured grain-by-grain in a thin section and **does not require previous experience with Python programming language** (see documentation below and [FAQ](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/FAQ.md)). For users with coding skills, the script is organized in a modular way facilitating its reuse and code extension.

**Last release 2018/03/27, v1.4.5 //  Version 2.0 will be released soon and will include important new features !** 


## Features at a glance

- Extract tabular-like data from text (.txt, .csv) or excel files.
- Calculate apparent diameters of grain profiles via the equivalent circular diameter.
- Estimate different apparent 1D grain size measures including the mean, median, area-weighted mean, and frequency peak using a Gaussian Kernel Density Estimator. Grain size scales can be linear, logarithmic, or square root.
- Includes several algorithms to estimate the optimal bin size of histograms and the optimal bandwidth of the Gaussian KDE based on the population features.
- Approximate the actual 3D grain size distribution from data collected in thin sections (2D data) using the Saltykov method. This includes estimating the volume of a particular grain size fraction.
- Approximate the shape of the 3D grain size distribution via the two-step method and characterize the shape of the distribution using a single parameter (the MSD - *Multiplicative Standard Deviation*) .
- Estimate differential stress via paleopiezometers including multiple piezometric relations for quartz, olivine, calcite, and albite. Other phases available soon!
- Ready-to-publish plots in bitmap or vector format (see screenshots below for examples).
- Estimate robust confidence intervals using the student's t-distribution

## Download

You can download the script at the following sites:  
https://github.com/marcoalopez/GrainSizeTools/releases  
http://figshare.com/articles/GrainSizeTools_script/1383130  
https://sourceforge.net/projects/grainsizetools/

[View project on GitHub](https://github.com/marcoalopez/GrainSizeTools)

## Documentation

* [Requirements](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/Requirements.md)
* [Scope](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/Scope.md)
* [Getting started: A step-by-step tutorial](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md)
    * [Open and running the script](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md#open-and-running-the-script)
    * [A brief note on the organization of the script](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md#a-brief-note-on-the-organization-of-the-script)
    * [Using the script to visualize and estimate the grain size features](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md#using-the-script-to-visualize-and-estimate-the-grain-size-features)
      * [Loading the data and extracting the areas of the grain profiles](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md#loading-the-data-and-extracting-the-areas-of-the-grain-profiles)
      * [Estimating the apparent diameters from the areas of the grain profiles](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md#estimating-the-apparent-diameters-from-the-areas-of-the-grain-profiles)
      * [Obtaining apparent grain size measures](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md#obtaining-apparent-grain-size-measures)
      * [Estimating differential stress using piezometric relations (paleopiezometry)](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md#estimating-differential-stress-using-piezometric-relations-paleopiezometry)
      * [Estimating a robust confidence interval](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md#estimating-a-robust-confidence-interval)
      * [Derive the actual 3D distribution of grain sizes from thin sections](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md#derive-the-actual-3d-distribution-of-grain-sizes-from-thin-sections)
      * [Comparing different grain size populations using box plots](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md#comparing-different-grain-size-populations-using-box-plots)
      * [Other methods of interest](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/brief_tutorial.md#general-methods-of-interest)
* [Quick tutorial](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/quick_tutorial.md)
* [How to measure the areas of the grain profiles with ImageJ](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/imageJ_tutorial.md)
* [References](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/references.md)
* [FAQs](https://github.com/marcoalopez/GrainSizeTools/blob/master/DOCS/FAQ.md)

## Screenshots


###### Estimate of different apparent grain size measures in the same population, in this example using a linear (number- and area-weighted), square root, and logarithmic scales.

![](https://raw.githubusercontent.com/marcoalopez/GrainSizeTools/master/FIGURES/apparent_GS.png)  


###### Estimate of the actual (3D) grain size distribution and volume of a particular grain size fraction using the Saltykov method  

![](https://github.com/marcoalopez/GrainSizeTools/blob/master/FIGURES/figure_2.png?raw=true)  


###### Estimate of the shape of the grain size distribution using the two-step method

![](https://github.com/marcoalopez/GrainSizeTools/blob/master/FIGURES/2step.png?raw=true)  


###### Boxplots comparing different unimodal grain size distributions

![](https://raw.githubusercontent.com/marcoalopez/GrainSizeTools/master/FIGURES/readme05.png)  


## Citation guidelines

If you need references, the following are available:

***Script reference***   
Lopez-Sanchez, Marco A. (2018): GrainSizeTools script. figshare. http://dx.doi.org/10.6084/m9.figshare.1383130

***Frequency peak apparent grain size based on Gaussian kernel density estimator***  
Lopez-Sanchez MA and Llana-Fúnez S (2015) An evaluation of different measures of dynamically recrystallized grain size for paleopiezometry or paleowattmetry studies. *Solid Earth* 6, 475-495. doi:[10.5194/se-6-475-2015](http://dx.doi.org/10.5194/se-6-475-2015)

***Two-step method***  
Lopez-Sanchez MA and Llana-Fúnez (2016) An extension of the Saltykov method to quantify 3D grain size distributions in mylonites. *Journal of Structural Geology*, 93, 149-161. doi:[10.1016/j.jsg.2016.10.008](http://dx.doi.org/10.1016/j.jsg.2016.10.008).

***Saltykov method***  
The procedure implemented in the GrainSizeTools script is partially based on general formulation developed by Sahagian and Proussevitch (1998) *J. Volcanol. Geotherm. Res.* 84, 173–196. [http://dx.doi.org/10.1016/S0377-0273(98)00043-2](http://dx.doi.org/10.1016/S0377-0273(98)00043-2) and is described in the Appendix A in Lopez-Sanchez and Llana-Fúnez (2016) http://dx.doi.org/10.5194/se-6-475-2015

## License

GrainSizeTools script is licensed under the [Apache License, Version 2.0 (the "License")](http://www.apache.org/licenses/LICENSE-2.0)

The documentation of GrainSizeTools script is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).  

# 
*Copyright © 2018 Marco A. Lopez-Sanchez*  

*Information presented on this website and the documentation of the script is provided without any express or implied warranty and may include technical inaccuracies or typing errors; the author reserve the right to modify or enhance the content of this website as well as the documentation of the script at any time without previous notice. This webpage and the documentation is not liable for the content of external links.*  

*Hosted on GitHub Pages — This website was created with [Typora](https://typora.io/)*