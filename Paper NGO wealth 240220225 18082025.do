import delimited "Dataset paper 31072025.csv", clear delimiter(";") varnames(1) encoding(utf8) 



************************************
***creating variables***
***********************************

*DEPENDENT VARIABLES

 
* Number of health nonprofits


gen healthnpnumberpc2015 = (totalhealthosc2015)/ (pop2015 ) *10000
gen healthnpnumberpc2016 = (totalhealthosc2016)/ (pop2016 ) *10000
gen healthnpnumberpc2017 = (totalhealthosc2017) / (pop2017 ) *10000
gen healthnpnumberpc2018 = (totalhealthosc2018) / (pop2018 ) *10000
gen healthnpnumberpc2019 = (totalhealthosc2019)/ (pop2019 ) *10000
gen healthnpnumberpc2020 = (totalhealthosc2020) / (pop2020 ) *10000

* Number of employees in health nonprofits

gen healthnpemployeespc2015 = (raisosc2015)/ (pop2015 ) *10000
gen healthnpemployeespc2016 = (raisosc2016)/ (pop2016 ) *10000
gen healthnpemployeespc2017 = (raisosc2017) / (pop2017 ) *10000
gen healthnpemployeespc2018 = (raisosc2018) / (pop2018 ) *10000
gen healthnpemployeespc2019 = (raisosc2019)/ (pop2019 ) *10000
gen healthnpemployeespc2020 = (raisosc2020) / (pop2020 ) *10000


* Number of health facilities managed by health nonprofits

gen healthnpfacilitiespc2015 = (cnesestosc2015)/ (pop2015 ) *10000
gen healthnpfacilitiespc2016 = (cnesestosc2016)/ (pop2016 ) *10000
gen healthnpfacilitiespc2017 = (cnesestosc2017) / (pop2017 ) *10000
gen healthnpfacilitiespc2018 = (cnesestosc2018) / (pop2018 ) *10000
gen healthnpfacilitiespc2019 = (cnesestosc2019)/ (pop2019 ) *10000
gen healthnpfacilitiespc2020 = (cnesestosc2020) / (pop2020 ) *10000


* Number of health procedures by health nonprofits

gen healthnpprocedurespc2015 = (mac2015)/ (pop2015 ) *10000
gen healthnpprocedurespc2016 = (mac2016)/ (pop2016 ) *10000
gen healthnpprocedurespc2017 = (mac2017) / (pop2017 ) *10000
gen healthnpprocedurespc2018 = (mac2018) / (pop2018 ) *10000
gen healthnpprocedurespc2019 = (mac2019)/ (pop2019 ) *10000
gen healthnpprocedurespc2020 = (mac2020) / (pop2020 ) *10000



*INDEPENDENT VARIABLE

gen  porkbarrelnppc2015 =  (pagofnsosc2015)/ (pop2015 ) *10000
gen  porkbarrelnppc2016 =  (pagofnsosc2016)/ (pop2016 ) *10000
gen  porkbarrelnppc2017 =  (pagofnsosc2017)/ (pop2017 ) *10000
gen  porkbarrelnppc2018 =  (pagofnsosc2018)/ (pop2018 ) *10000
gen  porkbarrelnppc2019 =  (pagofnsosc2019)/ (pop2019 ) *10000
gen  porkbarrelnppc2020 =  (pagofnsosc2020)/ (pop2020 ) *10000




*CONTROL VARIABLE
*values transformed from Reais to USD 1USD = 5R$


*Govfunding otherresources paid


gen fedgovfundingpc2015 = (fedgovfunding2015)/ (pop2015 )*10000
gen fedgovfundingpc2016 = (fedgovfunding2016)/ (pop2016 ) *10000
gen fedgovfundingpc2017 = (fedgovfunding2017)/ (pop2017 ) *10000
gen fedgovfundingpc2018 = (fedgovfunding2018)/ (pop2018 ) *10000
gen fedgovfundingpc2019 = (fedgovfunding2019)/ (pop2019 ) *10000
gen fedgovfundingpc2020 = (fedgovfunding2020)/ (pop2020 ) *10000



*Municipal govfunding nonprofits  

gen mungovfundingpc2015 = (finbrapagoosc2015)/ (pop2015 ) *10000
gen mungovfundingpc2016 = (finbrapagoosc2016)/ (pop2016 ) *10000
gen mungovfundingpc2017 = (finbrapagoosc2017)/ (pop2017 ) *10000
gen mungovfundingpc2018 = (finbrapagoosc2018)/ (pop2018 ) *10000
gen mungovfundingpc2019 = (finbrapagoosc2019)/ (pop2019 ) *10000
gen mungovfundingpc2020 = (finbrapagoosc2020)/ (pop2020 ) *10000




*Proportion of associational non profit sector  (does not include health nonprofits)

gen associationalnppc2015 = osc2015 / (pop2015 ) *10000
gen associationalnppc2016 = osc2016 / (pop2016)  *10000
gen associationalnppc2017 = osc2017 / (pop2017 ) *10000
gen associationalnppc2018 = osc2018 / (pop2018) *10000
gen associationalnppc2019 = osc2019 / (pop2019 ) *10000
gen associationalnppc2020 = osc2020 / (pop2020 ) *10000


* Proportion of poverty (individuals registered at CadUnico)

gen povertypc2015 = cadunico2015 / (pop2015)*10000
gen povertypc2016 = cadunico2016 / (pop2016)*10000
gen povertypc2017 = cadunico2017 / (pop2017 ) *10000
gen povertypc2018 = cadunico2018 / (pop2018 ) *10000
gen povertypc2019 = cadunico2019 / (pop2019) *10000
gen povertypc2020 = cadunico2020 / (pop2020 ) *10000


* Proportion of healthdependents (individuals with health plan - no data available for 2017, calculated as mean of 2016 and 2018)

gen healthplanpc2015 = planosau2015 / (pop2015 ) *10000
gen healthplanpc2016 = planosau2016 / (pop2016) *10000
gen healthplanpc2018 = planosau2018 / (pop2018 ) *10000
gen healthplanpc2019 = planosau2019 / (pop2019 ) *10000
gen healthplanpc2020 = planosau2020 /  (pop2020 ) *10000

gen healthplanpc2017 = (healthplanpc2016 + healthplanpc2018)/2




*transforming dataset from wide to long
reshape long     healthnpnumberpc  healthnpemployeespc  healthnpfacilitiespc  healthnpprocedurespc porkbarrelnppc fedgovfundingpc  mungovfundingpc associationalnppc povertypc healthplanpc        pibpercapita        pib vlagricultura vlindustria vlservicos vladmpub pop, i( ibge ) j(Year)

xtset ibge Year


 **drop unecessary variables 
drop   ibge7 amazonialegal2015 semiarido2015 centrolocal centrosubregional capitalregional centrozona nucleo municipio municipio2 uf munhierarchy  healthosc2015 healthosc2016 healthosc2017 healthosc2018 healthosc2019 healthosc2020 totalhealthosc2015 totalhealthosc2016 totalhealthosc2017 totalhealthosc2018 totalhealthosc2019 totalhealthosc2020 cnesestosc2015 cnesestosc2016 cnesestosc2017 cnesestosc2018 cnesestosc2019 cnesestosc2020 cnesestosc2021 raisosc2015 raisosc2016 raisosc2017 raisosc2018 raisosc2019 raisosc2020 raisosc2021 mac2015 mac2016 mac2017 mac2018 mac2019 mac2020 mac2021 index pagofnsosc2015 pagofnspub2015 pagofnsosc2016 pagofnspub2016 pagofnsosc2017 pagofnspub2017 pagofnsosc2018 pagofnspub2018 pagofnsosc2019 pagofnspub2019 pagofnsosc2020 pagofnspub2020 pagofnsosc2021 pagofnspub2021 pagofnsosc2022 pagofnspub2022 pagofnsosc2023 pagofnspub2023 vltotal2014 impostos2014 vltotal2015 impostos2015 vltotal2016 impostos2016 vltotal2017 impostos2017 vltotal2018 impostos2018 vltotal2019 impostos2019 vltotal2020 impostos2020 vlagricultura vlindustria vlservicos vladmpub vltotal2021 impostos2021   cadunico2012 cadunico2013 cadunico2014 cadunico2015 cadunico2016 cadunico2017 cadunico2018 cadunico2019 cadunico2020 cadunico2021 cadunico2022 fedgovfunding2015 fedgovfunding2016 fedgovfunding2017 fedgovfunding2018 fedgovfunding2019 fedgovfunding2020 osc2014 osc2015 osc2016 osc2017 osc2018 osc2019 osc2020 finbrapagoosc2015 finbrapagoosc2016 finbrapagoosc2017 finbrapagoosc2018 finbrapagoosc2019 finbrapagoosc2020 planosau2022 planosau2021 planosau2020 planosau2019 planosau2018 planosau2016 planosau2015

drop if Year == 2014
drop if Year ==2021

rename pibpercapita MunGDPpc
rename pib MunGDP


**Analysis of the variables**

*DV
sum healthnpnumberpc, detail
sum healthnpemployeespc, detail
sum healthnpfacilitiespc, detail
sum healthnpprocedurespc, detail

*Other variables

sum porkbarrelnppc, detail
sum fedgovfundingpc, detail
sum mungovfundingpc, detail
sum associationalnppc, detail
sum povertypc, detail
sum healthplanpc, detail 
sum MunGDPpc, detail
sum MunGDP, detail


* We checked variable skeweness

* Deleted negative values (8 observations) of FinbrapagoOSCpc
replace mungovfundingpc = 0 if mungovfundingpc < 0

*Log of highly skewed variables - all variables*

gen log_healthnpnumberpc = log(healthnpnumberpc + 1)
gen log_healthnpemployeespc = log(healthnpemployeespc + 1)
gen log_healthnpfacilitiespc = log(healthnpfacilitiespc + 1)
gen log_healthnpprocedurespc = log(healthnpprocedurespc + 1)


gen log_porkbarrelnppc = log(porkbarrelnppc + 1)
gen log_fedgovfundingpc = log(fedgovfundingpc + 1)
gen log_mungovfundingpc = log(mungovfundingpc + 1)
gen log_associationalnppc = log(associationalnppc + 1)
gen log_povertypc = log(povertypc)
gen log_healthplanpc = log(healthplanpc + 1)
gen log_MunGDPpc = log(MunGDPpc)
gen log_MunGDP = log(MunGDP)
gen log_pop = log(pop)

 
 



*****************************************************************************************
***Descriptive stats**not logged********************************************
*************************************************************************************************



sum  healthnpnumberpc    healthnpemployeespc   healthnpfacilitiespc    porkbarrelnppc   fedgovfundingpc mungovfundingpc associationalnppc povertypc healthplanpc MunGDPpc  pop



pwcorr healthnpnumberpc    healthnpemployeespc   healthnpfacilitiespc    porkbarrelnppc fedgovfundingpc mungovfundingpc associationalnppc povertypc healthplanpc MunGDPpc pop, star(.05)







*****************************************************************************************
***Testing unit-root*********************************************
*************************************************************************************************


*Checking if the dependent variables are sationary -  "fluctuates around a stable trend" — it has no drift, no persistent shocks, and returns to equilibrium - meaning they are suitable for a dynamic model. They are all stationary.

 xtunitroot llc healthnpnumberpc  
 
 xtunitroot llc healthnpemployeespc
 
 xtunitroot llc healthnpfacilitiespc  
 

   

******************************************************************************************
***Analysis if pork barrel unstable funding influences NGO density**  
*******************************************************************************************


***TESTING H1

**OLS

reg log_healthnpnumberpc L.log_porkbarrelnppc L.log_fedgovfundingpc L.log_mungovfundingpc log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop, robust

estimates store ModelNUMBEROLS

 
reg log_healthnpemployeespc  L.log_porkbarrelnppc L.log_fedgovfundingpc L.log_mungovfundingpc log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop, robust

estimates store ModelEMPLOYEESOLS



reg log_healthnpfacilitiespc  L.log_porkbarrelnppc L.log_fedgovfundingpc L.log_mungovfundingpc log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop, robust

estimates store ModelFACILITIESOLS






**FIXED EFFECTS

xtreg log_healthnpnumberpc L.log_porkbarrelnppc L.log_fedgovfundingpc L.log_mungovfundingpc log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop i.Year , fe cluster(ibge)

estimates store ModelNUMBERXTREG


xtreg log_healthnpemployeespc L.log_porkbarrelnppc L.log_fedgovfundingpc L.log_mungovfundingpc log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop i.Year , fe cluster(ibge)

estimates store ModelEMPLOYEESXTREG



xtreg log_healthnpfacilitiespc L.log_porkbarrelnppc L.log_fedgovfundingpc L.log_mungovfundingpc log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop i.Year , fe cluster(ibge)

estimates store ModelFACILITIESXTREG







**XTABOND2


xtabond2 log_healthnpnumberpc   L.log_healthnpnumberpc L.log_porkbarrelnppc         L.log_fedgovfundingpc L.log_mungovfundingpc  log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop i.Year,     gmm(L.log_healthnpnumberpc, lag(2 4) collapse)     iv(L2.log_porkbarrelnppc L2.log_fedgovfundingpc L2.log_mungovfundingpc      log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop i.Year)     twostep robust small

estimates store ModelNUMBERtotalAB

xtabond2 log_healthnpemployeespc   L.log_healthnpemployeespc L.log_porkbarrelnppc          L.log_fedgovfundingpc L.log_mungovfundingpc log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop i.Year,     gmm(L.log_healthnpemployeespc, lag(2 4) collapse)     iv(L2.log_porkbarrelnppc L2.log_fedgovfundingpc L2.log_mungovfundingpc      log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop i.Year)     twostep robust small

estimates store ModelEMPLOYEEStotalAB

xtabond2 log_healthnpfacilitiespc   L.log_healthnpfacilitiespc L.log_porkbarrelnppc          L.log_fedgovfundingpc L.log_mungovfundingpc log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop i.Year,     gmm(L.log_healthnpfacilitiespc, lag(2 4) collapse)     iv(L2.log_porkbarrelnppc L2.log_fedgovfundingpc L2.log_mungovfundingpc      log_associationalnppc log_povertypc log_healthplanpc log_MunGDPpc log_pop i.Year)     twostep robust small

estimates store ModelFACILITIEStotalAB





**TESTING H2

*Standardizing all explanatory variables for analysis (Dawson, 2014 Doi 10.1007/s10869-013-9308-7)

foreach var in    log_porkbarrelnppc log_MunGDPpc log_fedgovfundingpc  log_mungovfundingpc log_associationalnppc log_povertypc log_healthplanpc   log_pop {    
	egen z_`var' = std(`var') 
}
 

**FIXED EFFECTS - WITH INTERACTION

xtreg log_healthnpnumberpc       L1.z_log_porkbarrelnppc c.L1.z_log_porkbarrelnppc##c.z_log_MunGDPpc       L1.z_log_fedgovfundingpc L1.z_log_mungovfundingpc       z_log_associationalnppc z_log_povertypc z_log_healthplanpc z_log_MunGDPpc z_log_pop i.Year,       fe cluster(ibge)

estimates store ModelNUMBERtotalABINT


margins, dydx(L1.z_log_porkbarrelnppc) at(z_log_MunGDPpc=(-2 -1 0 1 2))
marginsplot, name(FEplotnumber, replace)     title("Interaction effect Pork barrel X GDP percapita - FE")     xtitle("GDPpercapita (std)") ytitle("Marginal Effect on Number of health nonprofits")
graph save "FEplotnumber.gph", replace
 

xtreg log_healthnpemployeespc          L1.z_log_porkbarrelnppc c.L1.z_log_porkbarrelnppc##c.z_log_MunGDPpc       L1.z_log_fedgovfundingpc L1.z_log_mungovfundingpc       z_log_associationalnppc z_log_povertypc z_log_healthplanpc z_log_MunGDPpc z_log_pop i.Year,   fe cluster(ibge)
	  
estimates store ModelEMPLOYEESXTREGINT

margins, dydx(L1.z_log_porkbarrelnppc) at(z_log_MunGDPpc=(-2 -1 0 1 2))
marginsplot, name(FEplotemployees, replace)     title("Interaction effect Pork barrel X GDP percapita - FE")     xtitle("GDPpercapita (std)") ytitle("Marginal Effect on Number of health nonprofits employees")
graph save "FEplotemployees.gph", replace

xtreg log_healthnpfacilitiespc         L1.z_log_porkbarrelnppc c.L1.z_log_porkbarrelnppc##c.z_log_MunGDPpc       L1.z_log_fedgovfundingpc L1.z_log_mungovfundingpc       z_log_associationalnppc z_log_povertypc z_log_healthplanpc z_log_MunGDPpc z_log_pop i.Year,       fe cluster(ibge)

estimates store ModelFACILITIESXTREGINT




**SYSTEM GMM - WITH INTERACTION



xtabond2 log_healthnpnumberpc L.log_healthnpnumberpc    L1.z_log_porkbarrelnppc c.L1.z_log_porkbarrelnppc##c.z_log_MunGDPpc     L1.z_log_fedgovfundingpc L1.z_log_mungovfundingpc     z_log_associationalnppc z_log_povertypc z_log_healthplanpc z_log_MunGDPpc z_log_pop i.Year,    gmm(L.log_healthnpnumberpc, lag(2 4) collapse)     iv(L2.z_log_porkbarrelnppc L2.z_log_fedgovfundingpc L1.z_log_mungovfundingpc        z_log_associationalnppc z_log_povertypc z_log_healthplanpc z_log_MunGDPpc z_log_pop i.Year)     twostep robust small

margins, dydx(L1.z_log_porkbarrelnppc) at(z_log_MunGDPpc=(-2 -1 0 1 2))
marginsplot, name(GMMplotnumber, replace)     title("Interaction effect Pork barrel X GDP percapita - GMM")     xtitle("GDPpercapita (std)") ytitle("Marginal Effect on Number of health nonprofits")
graph save "GMMplotnumber.gph", replace

estimates store ModelNUMBERtotalABINT

* Repeat for the other dependent variable measures:

xtabond2 log_healthnpemployeespc L.log_healthnpemployeespc     L1.z_log_porkbarrelnppc c.L1.z_log_porkbarrelnppc##c.z_log_MunGDPpc     L1.z_log_fedgovfundingpc L1.z_log_mungovfundingpc     z_log_associationalnppc z_log_povertypc z_log_healthplanpc z_log_MunGDPpc z_log_pop i.Year,     gmm(L.log_healthnpemployeespc, lag(2 4) collapse)     iv(L2.z_log_porkbarrelnppc L2.z_log_fedgovfundingpc L1.z_log_mungovfundingpc        z_log_associationalnppc z_log_povertypc z_log_healthplanpc z_log_MunGDPpc z_log_pop i.Year)     twostep robust small

margins, dydx(L1.z_log_porkbarrelnppc) at(z_log_MunGDPpc=(-2 -1 0 1 2))
marginsplot, name(GMMplotemployees, replace)     title("Interaction effect Pork barrel X GDP percapita - GMM")     xtitle("GDPpercapita (std)") ytitle("Marginal Effect on Number of health nonprofits employees")
graph save "GMMplotemployees.gph", replace

estimates store ModelEMPLOYEEStotalABINT

xtabond2 log_healthnpfacilitiespc L.log_healthnpfacilitiespc   L1.z_log_porkbarrelnppc c.L1.z_log_porkbarrelnppc##c.z_log_MunGDPpc     L1.z_log_fedgovfundingpc L1.z_log_mungovfundingpc     z_log_associationalnppc z_log_povertypc z_log_healthplanpc z_log_MunGDPpc z_log_pop i.Year,     gmm(L.log_healthnpfacilitiespc, lag(2 4) collapse)    iv(L2.z_log_porkbarrelnppc L2.z_log_fedgovfundingpc L1.z_log_mungovfundingpc        z_log_associationalnppc z_log_povertypc z_log_healthplanpc z_log_MunGDPpc z_log_pop i.Year)     twostep robust small

margins, dydx(L1.z_log_porkbarrelnppc) at(z_log_MunGDPpc=(-2 -1 0 1 2))
marginsplot, name(GMMplot, replace)     title("Interaction effect Pork barrel X GDP percapita - GMM")     xtitle("GDPpercapita (std)") ytitle("Marginal Effect on Number of health nonprofits facilities")


estimates store ModelFACILITIEStotalABINT




*Moderation analysis graphs

graph combine  FEplotnumber GMMplotnumber  FEplotemployees GMMplotemployees
	   


*ALL MODELS
estout ModelNUMBEROLS ModelEMPLOYEESOLS  ModelFACILITIESOLS   ModelNUMBERXTREG ModelEMPLOYEESXTREG  ModelFACILITIESXTREG ModelPROCEDURESXTREG ModelNUMBERXTINT  ModelEMPLOYEESXTINT  ModelFACILITIESXTINT  ModelNUMBERtotalAB ModelEMPLOYEEStotalAB ModelFACILITIEStotalAB  ModelNUMBERtotalABINT ModelEMPLOYEEStotalABINT ModelFACILITIEStotalABINT , cells(b(star fmt(8))p(fmt(3)) se(par fmt(2)))legend label varlabels(_cons constant)  stats(r2 rho df_r bic N)  starlevels(+ 0.10 * 0.05) 

*FOR THE PAPER - TABLE FOR H1
estout  ModelNUMBERXTREG ModelEMPLOYEESXTREG  ModelFACILITIESXTREG        ModelNUMBERtotalAB ModelEMPLOYEEStotalAB ModelFACILITIEStotalAB   , cells(b(star fmt(8))p(fmt(3)) se(par fmt(2)))legend label varlabels(_cons constant)  stats(r2 rho df_r bic N)  starlevels(+ 0.10 * 0.05) 


*FOR THE PAPER - TABLE FOR H2

estout   ModelNUMBERtotalABINT ModelEMPLOYEESXTREGINT ModelFACILITIESXTREGINT  ModelNUMBERtotalABINT ModelEMPLOYEEStotalABINT ModelFACILITIEStotalABINT , cells(b(star fmt(8))p(fmt(3)) se(par fmt(2)))legend label varlabels(_cons constant)  stats(r2 rho df_r bic N)  starlevels(+ 0.10 * 0.05) 


