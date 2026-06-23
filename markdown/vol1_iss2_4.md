# JPMorgan Chase London Whale C: Risk Limits, Metrics, and Models[1] 

Arwin G. Zeissler[2] Andrew Metrick[3] 

Yale Program on Financial Stability, Case Study 2014-2c-V1 December 1, 2014, Revised: July 20, 2015 

## **Abstract** 

Value at Risk (VaR) is one of the most commonly used ways to measure and monitor market risk. At JPMorgan Chase (JPM), very large derivative positions established by Bruno Iksil in the Synthetic Credit Portfolio (SCP) caused the bank’s Chief Investment Office (CIO) to exceed its VaR limit for four days in a row in January 2012. In response, the CIO changed to a new VaR model on January 30, which appeared to immediately reduce VaR by half. However, JPM soon discovered that this new VaR model had not been properly implemented and the bank went back to using the previous model. In addition, Iksil, other SCP staff, and their managers also disregarded several other risk metrics and limits during the first quarter of 2012. However, after JPM’s Chief Investment Officer learned on March 23 that Iksil and the SCP had breached the CIO’s mark-to-market Credit Spread Widening 10% risk limit the day before, she ordered trading of the SCP to be halted immediately. 

> 1 This case is one of nine produced by the Yale Program on Financial Stability (YPFS) examining issues related to the JPMorgan Chase London Whale. The following are the other case studies in this case series. 

- _JP Morgan Chase London Whale A: Risky Business_ 

- _JP Morgan Chase London Whale B: Derivatives Valuation_ 

- _JP Morgan Chase London Whale D: Risk-Management Practices_ 

- _JP Morgan Chase London Whale E: Supervisory Oversight_ 

- _JP Morgan Chase London Whale F: Required Securities Disclosures_ 

- _JP Morgan Chase London Whale G: Hedging Versus Proprietary Trading_ 

- _JP Morgan Chase London Whale H: Cross-Border Regulation_ 

- _JP Morgan Chase London Whale Z: Background and Overview_ 

Cases are available at the Journal of Financial Crises. 

> 2  Project Editor, Case Study and Research, YPFS, Yale School of Management. **The authors acknowledge helpful comments from Sirio Aramonte** . 

> 3  Janet L. Yellen Professor of Finance and Management, and YPFS Program Director, Yale School of Management 


## **1. Introduction** 

With $2.266 trillion in total assets at December 31, 2011, but only $184 billion of total stockholders’ equity, JPMorgan Chase & Company (JPM) needed to accurately measure and closely monitor the risks that it took, since a decrease of 8.1% in the value of the bank’s total assets would have eliminated the entire equity balance. Not surprisingly, JPM devoted over 40 consecutive pages in its 2011 annual Form 10-K to discussing the major risks that it faced and how it managed those risks. 

However, in 2012, JPM’s risk management fell short of the high standard to which the firm held itself, as Bruno Iksil and a small team of derivatives traders in the bank’s London office undertook an ill-fated trading strategy that ultimately cost the bank $6.2 billion. Senior trader Iksil, junior trader Julien Grout, and their superior Javier Martin-Artajo were employed by JPM’s Chief Investment Office (CIO) to help hedge the credit risk facing the bank. They did this using CIO’s Synthetic Credit Portfolio (SCP), which consisted of long and short positions in various credit default swaps and other credit derivatives. 

Despite various deficiencies in CIO’s risk management function, discussed in a separate case module (See Zeissler and Metrick 2015), the possibility of excessive CIO risk taking was still constrained in theory. All major financial institutions use various risk limits and metrics, often based on mathematical models, to measure and monitor the risk of their lending and investing activities. The amount of risk taken is measured on a daily or weekly basis using various risk metrics, and these amounts are compared with the relevant limits. If a risk limit is exceeded, JPM policy requires that such breaches be reported to senior management in a timely fashion, and that the affected line of business reduce the size of its trading positions or consult with senior management on the appropriate action. In practice, these risk limits and the accompanying metrics and models provided little or no restraint on the risk that was taken by CIO. In some cases, risk was not measured properly, whereas in other cases, risk limits were raised repeatedly and/or breaches were ignored. 

One of the most commonly used ways to measure and monitor market risk is known as Value at Risk (VaR), which is an integral part of the calculation of regulatory capital and is also commonly used for internal risk management. VaR is an estimate of the most that one or more financial instruments could lose in value over a fixed time period (e.g., one day) with a given level of confidence (e.g., 95%). Large derivative positions in the SCP book caused CIO to exceed its own $95 million VaR limit on January 16, 2012, and were also the main contributor to the breach of the $125 million firm-wide VaR limit. These VaR breaches continued until January 19, with Chief Executive Officer Jamie Dimon and the members of the JPM Operating Committee notified each day that the firm-wide VaR limit was exceeded. 

Irvin Goldman, the recently appointed CIO Chief Risk Officer, informed JPM Chief Risk Officer John Hogan that the new VaR calculation model that CIO planned to implement by the end of January would halt the breaches. As a result, on January 23, Dimon and Hogan approved a temporary increase in the firm-wide VaR limit from $125 million to $140 million until the end of January. On January 30, CIO’s new VaR model was approved, which immediately reduced the unit’s VaR by half from $132 million to only $66 million. However, JPM later discovered that the new CIO VaR model was not properly implemented and included formula and calculation errors, causing the bank to go back to using the old CIO model. 

In addition to exceeding department-wide and firm-wide VaR limits, Mr. Iksil and the CIO traders responsible for the SCP book also disregarded several other risk metrics during the 


early months of 2012. For example, the Comprehensive Risk Measure (CRM) is an estimate of the most that a portfolio could lose over one year with a 99.9% level of confidence and is another element of the regulatory capital calculation. Unfortunately, JPM was unable to compute CIO CRM for a critical five-week period between January 18 and February 22 due to technical difficulties experienced by the Quantitative Research team. By that point, CIO CRM had doubled from $3.2 billion to $6.3 billion. Peter Weiland, CIO head of Market Risk, dismissed the latter amount as “garbage” at the time, although this figure proved remarkably close to the $6.2 billion in market losses that JPM ultimately incurred in 2012 as a result of the London Whale trades. 

As SCP losses mounted, CIO also exceeded stress-loss limits (on the estimated loss that would be incurred from hypothetical unusual events, such as another credit crisis) and stop-loss limits (on the dollar amount that a portfolio can lose over a specified time period before some action is taken). The only risk limit that CIO management heeded is known as Credit Spread Widening 10% (CSW10%), which calculates the expected change in portfolio value if the credit spread on each position simultaneously widened by 10% of its current amount (e.g., from 2.00% to 2.20%). Ina Drew, who was JPM’s Chief Investment Officer and head of CIO, viewed CSW10% as the most important risk limit. After Drew learned on March 23 that SCP had breached the CIO’s mark-to-market CSW10% limit of plus/minus $200 million the previous day, she ordered trading of the SCP portfolio to be halted immediately. 

The remainder of the case is organized as follows. Section 2 briefly explains how JPM set risk limits and monitored market risk at the firm and line of business levels at the beginning of 2012. Section 3 introduces how Value at Risk is defined by banking regulators and applied by JPM. Sections 4 and 5 discuss in detail why CIO made the decision to switch to a new internally-developed VaR model and the errors later found in the new model, respectively. Section 6 describes a number of other risk limits at JPM, as well as CIO employees’ opinion and application of these limits. Section 7 concludes with the aftermath of the repeated breaches of CIO risk limits caused by the SCP book, including changes by JPM to its use of risk limits, metrics, and models resulting from regulatory action and the bank’s own investigation into the 2012 London Whale losses. See Appendix 1 for a timeline of key events pertinent to this case module. 

## **Questions** 

1. How do financial firms measure and monitor quantitative risks? 

2. What are the strengths and weaknesses of various statistical and non-statistical risk measures? 

3. Why might weaknesses in a particular risk metric cause risk management and trading personnel to ignore the metric? 

4. What are the limits to rule-based supervision? 

## **2. Setting Risk Limits and Monitoring Risk at JPMorgan Chase** 

In its 2011 10-K, JPM begins a 43-page discussion of the primary risks that the bank faces and how it manages those risks by stating, “Risk is an inherent part of JPMorgan Chase’s business activities. The Firm’s risk management framework and governance structure are intended to provide comprehensive controls and ongoing management of the major risks inherent in its business activities” (JPM 10-K 2011, 125). 


The risk management framework and governance structure include both quantitative and qualitative pieces. (JPM’s use of quantitative risk limits, metrics, and models is explored herein, while deficiencies in certain non-quantitative parts of JPM’s risk management function are addressed in Zeissler, et al. 2014D.) 

During the first quarter of 2012, when Bruno Iksil was making the credit derivatives trades that would earn him the nickname the “London Whale,” risk limits at the JPM firm-wide level and the line-of-business level were categorized as either Level 1, Level 2, or Threshold, which determined which bank official set the limit and was notified if the limit was exceeded, with Level 1 limits being the most important. Firm-wide risk limits were set by JPM’s Chief Executive Officer Jamie Dimon and the Chief Risk Officer (Barry Zubrow to January 2012, and John Hogan thereafter). Both Dimon and the Chief Risk Officer had to approve any changes in or waivers of firm-wide Level 1 limits. In the same manner, both the head of a business unit and its Chief Risk Officer had to approve changes in or waivers of the unit’s Level 2 limits. 

JPM’s CIO invested a $350 billion pool that included the bank's excess deposits (the unit’s main responsibility), and also attempted to hedge some of the default risk to which JPM was exposed as part of its lending activities. The hedging of default risk mainly took the form of trading in credit default swaps and other credit derivatives held in CIO’s London-based SCP. 

CIO’s risk limits depended in turn on JPM’s own risk appetite, and these limits were discussed at an annual “Business Review.” CIO’s 2012 Business Review was held in February and included Dimon, Zubrow, Hogan, Douglas Braunstein (JPM Chief Financial Officer), Ina Drew (JPM Chief Investment Officer and head of CIO), and Achilles Macris (the International Chief Investment Officer and Drew’s subordinate), among others. 

In practice, risk limits were routinely breached or exceeded at JPM and other financial firms, with the response depending on the cause of the breach. For example, firms may respond more aggressively to a breach caused by positions that are “too large” than to a breach resulting from an increase in market volatility. 

JPM’s 2011 Form 10-K states that “the affected line-of-business is required to reduce trading positions or consult with senior management on the appropriate action” in case of a limit breach (JPM 10-K 2011, 162). However, Dimon testified before the United States (US) Senate that breach of either a Level 1 or a Level 2 limit was not intended to lead to an automatic reduction in risk, but rather to a discussion about the matter. (Likewise, the breach of a Threshold limit also would not lead to an automatic risk reduction, since Threshhold limits were lower in the hierarchy.) The CIO followed similar practice (US Senate Report, 159-160). 

## **3. Introduction to Model Risk Management and to Value at Risk** 

The Board of Governors of the Federal Reserve System regulates the JPM bank holding company, and the Office of the Comptroller of the Currency (OCC) regulates JPM’s national bank subsidiaries and, by extension, the CIO. (The other parts of JPM’s global businesses are supervised by various domestic and foreign regulators.) 

In April 2011, the Board of Governors of the Federal Reserve System and the OCC issued joint “Supervisory Guidance on Model Risk Management” for the banks under their supervision. The guidance notes that banks use quantitative analysis and models “in most aspects of financial decision making,” including underwriting loans, estimating the fair value of financial assets and liabilities, and measuring risk, among other activities (OCC 2011-12, 1). A model is a “quantitative method, system, or approach that applies statistical, economic, 


financial, or mathematical theories, techniques, and assumptions to process input data into quantitative estimates” (OCC 2011-12, 3). 

Since models are simplified representations of complex real-world phenomena, the use of financial models inevitably brings with it “model risk,” which is the possibility of bad outcomes (financial loss, poor decision making, reputational damage) because models may contain fundamental errors and thus produce inaccurate outputs, and since even sound models may be used incorrectly or inappropriately (OCC 2011-12, 3-4). 

[FIGURE id=vol1_iss2_4_f1 type=figure label="Figure 1" file=figure_1.png caption="VaR Basic Definitions"]
### **Figure 1: VaR Basic Definitions**

## OCC defines Value at Risk as follows: 

“Value-at-Risk (VaR) means the estimate of the maximum amount that the value of one or more positions could decline due to market price or rate movements during a fixed holding period within a stated confidence interval” (US Senate Report, 198). 

## For internal risk management at JPM: 

“VaR is calculated using a one day time horizon and an expected tail-loss methodology, and approximates a 95% confidence level. This means that, assuming current changes in market values are consistent with the historical changes used in the simulation, the Firm would expect to incur losses greater than that predicted by VaR estimates five times in every 100 trading days, or about 12 to 13 times a year. However, differences between current and historical market price volatility may result in fewer or greater VaR exceptions than the number indicated by historical simulation” (JPM 10-K 2011, 126). 

_Source: U.S. Senate Report and JPMorgan 10-K._ 

Since model risk cannot be eliminated, the Federal Reserve and the OCC suggest that banks manage model risk just as they manage other types of risk. The key to managing model risk is “effective challenge” of the models to identify important assumptions and limitations of the models and to make changes to the models if needed. Effective challenge requires staff with appropriate incentives, competence, and influence (OCC 2011-12, 4). 

The Basel bank capital regulatory framework encourages banks to develop internal risk models, since banks may be required to hold less capital if using an internally-developed model than if using a standard model. Therefore, banking regulators’ duties evolved to “determining whether proposed models meet detailed regulatory requirements, overseeing model changes and variations, examining model implementation which can raise complex operational issues, and overseeing back-testing of the models to evaluate their accuracy” (US Senate Report, 166). 

Value at Risk (VaR) was developed by JPM in the early 1990s and has since become one of the most common methods employed by financial institutions to measure and monitor market risk by using data about the volatilities of and correlations among financial securities to measure potential loss. JPM defines “market risk” as the “exposure to an adverse change in the market value of portfolios and financial instruments caused by a change in market prices or rates” (JPM 10-K 2011, 158). 

Financial institutions use VaR models to calculate regulatory capital and for internal risk management. Though the OCC allows banks under its supervision to develop their own VaR 


models used for regulatory purposes, it provides detailed guidance on how these VaR models should function. Furthermore, the OCC must approve the regulatory VaR models that the banks create. However, the OCC does not review or approve VaR models used by banks for internal risk management (US Senate Report, 167). 

(For more information about VaR, including three common calculation methods, see discussion by RiskMetrics, which was spun off by JPM in 1998 and is now owned by MSCI.) 

## **4. Reducing Risk by Switching to a Different VaR Model** 

JPM uses numerous VaR models to calculate the market risk of individual positions, products, and trading desks, with different models typically used to calculate regulatory capital and for internal risk management. JPM’s most important VaR calculation for internal risk management is the one used in quarterly 10-Q and annual 10-K filings. This so-called “10-Q VaR” is based on a one-day holding period and a 95% confidence level, as noted in Section 3, and is a Level-1 risk limit. 

In 2011, CIO decided to replace its then-current 10-Q VaR model, which had been created by Keith Stephan, a London-based CIO risk management employee. After developing two other VaR models earlier in the year, Patrick Hagan (the head of the CIO quantitative analytics group) was assigned by his superior Javier Martin-Artajo to design the new 10-Q VaR model for CIO.  Martin-Artajo pressured Hagan to work quickly because JPM wanted the bank’s VaR models to be compliant with Basel III regulatory capital requirements as soon as possible and well in advance of the 2013 start of the Basel III transition period. 

[FIGURE id=vol1_iss2_4_f2 type=figure label="Figure 2" file=figure_2.png caption="Distribution of Profit and Loss"]
### **Figure 2: Distribution of Profit and Loss**
![Figure 2](assets/vol1_iss2_4/figure_2.png)


_- Source: JPM 10 K 2011, 128._ 


Furthermore, Mr. Hagan and the CIO traders considered the existing 10-Q VaR model to be too conservative, that is, overstating the market risks that CIO was taking (US Senate Report, 169). Since JPM calculated 10-Q VaR using a 95% confidence level, it expected losses greater than those predicted by the model 5 times in every 100 trading days, or about 13 times per year. As can be seen in Figure 2, although JPM suffered market risk related losses at the firmwide level on 27 of the 260 trading days in 2011, only three of those losses exceeded the VaR threshold. However, one should question if a single year was a long enough sample period for CIO staff to have concluded that the existing VaR model was too conservative. 

Most of the design work on the replacement 10-Q VaR model took place in October and November 2011, and Hagan submitted the new model for approval on November 25. The following month, Dimon and Braunstein instructed CIO to reduce its Risk-Weighted Assets (RWA) as part of a bank-wide effort to prepare for the new Basel III capital requirements. Because synthetic assets such as credit derivatives would require far more capital under Basel III than under the prior regime, the main source of RWA reduction within CIO was to come from the SCP. 

The most direct way of reducing the size of the SCP, as measured by RWA, would be to reduce or eliminate some of the derivative positions in the SCP book. However, the SCP traders proposed other options. First, the traders could buy and sell credit derivatives that would offset the risk exposures currently in the portfolio (described more fully in Zeissler, et al. 2014A). Second, the traders hoped that the new Comprehensive Risk Measure (CRM, described in Section 6) model that Mr. Hagan was also developing could lead to a material reduction in capital charges. Mr. Martin-Artajo saw this latter option as particularly promising (US Senate Report, 189). 

Consistent with other financial institutions, JPM calculated the VaR of its portfolios on a daily basis. CIO’s VaR was based on “positions, primarily in debt securities and credit products, used to manage structural and other risks including interest rate, credit and mortgage risks arising from the Firm’s ongoing business activities” (JPM 10-K 2011, 159). 

CIO VaR ranged from a minimum of $44 million to a maximum of $80 million in 2010, with an average VaR of $61 million. (See Figure 3.) During 2011, the comparable CIO VaR figures were the same or lower (from $30 million to $80 million, averaging $57 million). Importantly, CIO VaR was $77 million at December 31, 2011, near the maximum amount attained for the year. 

[FIGURE id=vol1_iss2_4_f3 type=figure label="Figure 3" file=figure_3.png caption="Chief Investment Office Value at Risk, 2009-2011"]
### **Figure 3: Chief Investment Office Value at Risk, 2009-2011**

|Amounts in<br>millions|2009|2010|2011|
|---|---|---|---|
|Minimum|$71|$44|$30|
|Average|$103|$61|$57|
|Maximum|$126|$80|$80|
|At December 31|$76|$56|$77|



_Source: JPM 10-K 2010, 168; JPM 10-K 2011, 127._ 

JPM risk-management staff would compare actual VaR usage to the maximum VaR limit set by senior management. At January 1, 2012, JPM’s firm-wide 10-Q VaR limit was $125 million, and CIO’s equivalent limit was $95 million, reflecting that much of JPM’s market risk came 


from the CIO. On January 9, several weeks before the rapid expansion of the SCP book that ultimately caused the $6.2 billion 2012 CIO loss, JPM VaR was $123 million and CIO VaR was $88 million, already rapidly approaching their respective limits. 

Particularly large trading activity by SCP on Monday, January 16, caused CIO to exceed its own $95 million VaR limit and was also the main contributor to the breach of the $125 million firm-wide VaR limit. Both of these VaR breaches continued until Thursday, January 19. As required by firm policy, Dimon and the other members of the JPM Operating Committee were notified each day that the firm-wide VaR limit was exceeded. However, JPM did not have to inform the OCC of this firm-wide risk limit breach because the 10-Q VaR limit was used for internal risk management, rather than for regulatory purposes (US Senate Report, 174-175). 

However, Drew did not order the CIO traders to reduce the size of the risky positions within the SCP book in response to the limit breaches. Irvin Goldman, the recently appointed CIO Chief Risk Officer, e-mailed his superior Hogan that the most important solution to stop the breaches was the new VaR model that CIO planned to implement by the end of January. As a result, on January 23, Dimon and Hogan approved a temporary increase in the firm-wide VaR limit from $125 million to $140 million until January 31. Ms. Drew likewise temporarily raised the CIO VaR limit from $95 million to $105 million (JPM Task Force 2013, 124). 

To try to balance the competing objectives placed upon himself and his team by management, Iksil proposed a trading strategy at a meeting of the CIO International Senior Management Group on January 26 to aggressively buy and sell large volumes of various credit derivatives. Iksil and his small team of traders began implementation right away. SCP VaR reached $126 million by January 27, and total CIO VaR was $132 million, both more than $20 million in excess of CIO’s temporarily increased VaR limit of $105 million (US Senate Report, 179). 

On Monday, January 30, JPM’s Model Review Group (part of the risk-management function) approved CIO’s new VaR model. The new model was immediately used to recalculate VaR for the previous trading day, January 27. The difference was dramatic, with the new model reducing CIO VaR by half from the initially reported $132 million to only $66 million. Hagan told the US Senate that even he was surprised by the magnitude of the immediate drop in CIO VaR. Later analysis conducted by the Model Review Group pointed to calculation errors in the new model as a likely cause of the sharp decrease in reported VaR (US Senate Report, 180-181). The nature and impact of errors in the new model are discussed more fully in Section 5. 

Though the CIO VaR limit was reset to $95 million as planned when January expired, the limit was not recalibrated (i.e., decreased) to reflect the new VaR model. As a result, though CIO VaR would have been above the VaR limit from late January through April had the old model still been used, it remained below the limit using the new model, only approaching the limit well after SCP trading activity had been halted on March 23. (See Figure 4. **)** 

## **5. Implementation and Calculation Errors in the New VaR Model** 

Hagan headed the CIO quantitative analytics group and held a Ph.D. in applied mathematics from the California Institute of Technology, but he had not previously designed a VaR model before developing several such models for CIO in 2011, including the important 10-Q VaR model. To mitigate such possible weaknesses in model development, the bank’s Model Review Group was responsible for testing, reviewing, and approving all bank VaR models. 


Before approving a new model, one of the Model Review Group’s routine practices was to compare the VaR that would have been calculated for some past time period using the new model with the actual profit and loss for the same time period, a process known as “backtesting.” However, the Model Review Group was only able to back-test CIO’s new VaR model for two months, a much shorter time frame than desired, because “CIO lacked the data necessary for more extensive back-testing of the model.” Neither the Model Review Group nor CIO Market Risk expressed reservations that CIO did not maintain a longer history of position data, despite playing a crucial role in hedging risk across the entire bank (JPM Task Force 2013, 123). 

[FIGURE id=vol1_iss2_4_f4 type=figure label="Figure 4" file=figure_4.png caption="Chief Investment Office Value at Risk (10Q VaR):"]
### **Figure 4: Chief Investment Office Value at Risk (10Q VaR):**
![Figure 4](assets/vol1_iss2_4/figure_4.png)


_Source: US Senate Exhibits, 19._ 

Another best practice recommended by the OCC before approving a new model was to run the proposed model and the existing model in parallel for several months to evaluate how the new model performed in practice and to understand differences in the results produced by the old and new models. However, the rush to put the new CIO VaR model into place resulted in limited parallel testing. Consequently, calculation errors produced by the new model were not detected until several months had passed. 

After developing the new CIO VaR model, Hagan was also assigned to implement the model and to run it on a daily basis. Because CIO held both long and short positions across numerous fixed income securities and credit derivatives, best practice would suggest that VaR should be calculated by automatically and directly transferring data from the firm’s 


trading software into the CIO VaR model. However, Hagan was not given the funds to create such an automatic data feed, so he would manually enter trading data into multiple spreadsheets every day (US Senate Report, 185). This process was cumbersome, prone to error, and would not have been feasible had the number of different trading positions held by CIO increased to any great extent. The Model Review Group recommended that CIO replace this manual approach with an automated process, and also found several other operational flaws with the new CIO VaR model, asking Hagan to provide an action plan and timetable for fixing these problems. Hagan ultimately provided neither. 

On April 13, JPM issued its first-quarter 2012 earnings release. Included in the release was a table appearing to show that average CIO VaR had slightly decreased from $69 million during the fourth quarter of 2011 to $67 million during the first quarter of 2012, seemingly indicating that CIO’s risk exposure at the start of 2012 was approximately the same as at the end of 2011 (JPM 8-K 20120413, 42). However, the earnings release made no mention of the change in CIO’s VaR model during the quarter. 

JPM finalized its first-quarter financial results in a May 10 Form 10-Q filing. By this time, the JPMorgan Chase Management Task Force (JPM Task Force) investigating the CIO losses discovered that frequent changes to formulas in the new CIO VaR model were made without sufficient verification, resulting in calculation errors involving volatility and correlation estimates that incorrectly reduced VaR (JPM Task Force 2013, 105). 

As a result, JPM scrapped the new CIO VaR model and went back to using the previous model. JPM revised average first-quarter CIO VaR from $67 million in the earnings release of April 13 to $129 million in the Form 10-Q of May 10. JPM noted that the higher revised amount “supersedes the Firm’s VaR disclosures included in its Form 8-K filed on April 13, 2012,” and emphasized that the revised amount “was calculated using a methodology consistent with the methodology used to calculate CIO’s VaR in 2011,” but made no mention in the 10-Q filing of the reason for the change (JPM 10-Q 2012Q1, 73). However, in a May 10 business update call with financial analysts, Dimon elaborated that JPM had implemented a new VaR model during the first quarter that the firm now deemed “inadequate” (JPM Business Update Call, 2). 

## **6. Breaching Other Risk Limits** 

In addition to exceeding department-wide and firm-wide VaR limits, CIO personnel disregarded several other risk limits and metrics during the early months of 2012. Importantly, all of the limits described below applied to CIO as a whole, which meant that “there were no limits of any kind specific to the Synthetic Credit Portfolio” (JPM Task Force 2013, 103). 

## _**Comprehensive Risk Measure**_ 

As with VaR, the Comprehensive Risk Measure (CRM) is a dollar measure of potential loss. Though calculated in a similar way, CRM results in a much larger measure of potential loss than 10-Q VaR, because CRM is based on a one-year time horizon and a 99.9% level of confidence, whereas 10-Q VaR is based on a one-day time horizon and a 95% level of confidence (US Senate Report, 187). 

CRM was introduced by Basel 2.5 as one of the components of capital requirements, and it can also be used to gauge the riskiness of a portfolio. CIO calculated CRM on a weekly basis, as required by regulators. CIO CRM increased rapidly in January 2012, from $2.0 billion on 


January 4, to $2.3 billion on January 11, and then to $3.2 billion by January 18, an increase of over 60% in two weeks. Soon thereafter, JPM’s Quantitative Research team had technical difficulties and was not able to calculate CIO CRM again until February 22, at which point it had almost doubled to $6.3 billion. 

When Peter Weiland, CIO head of market risk, learned of the $6.3 billion CRM figure in early March, he dismissed it as “garbage” and unreliable in an e-mail to Martin-Artajo (US Senate Report, 190). However, C.S. Venkatakrishnan, the head of the bank’s Model Risk and Development Group, disputed this characterization, asserting instead that the $33 billion increase in the notional value of default protection sold by SCP during this period led to the $3 billion increase in CIO CRM between January 18 and February 22. SCP losses from the London Whale trades eventually totaled $6.2 billion, an amount remarkably close to the $6.3 billion of potential losses estimated by the CIO CRM measure. 

## _**Credit Spread Widening 01, also known as Credit Spread Basis Point Value**_ 

With credit default swaps (CDS), one party sells credit protection to a second party against the possible default of a corporate or sovereign borrower. In exchange for receiving this protection, the protection buyer makes premium payments to the protection seller. These payments are determined by the amount of protection purchased (notional) and the cost of protection, also referred to as the “CDS spread,” which is measured in basis points (1/100 of 1%, or 0.0001). For example, a buyer of protection for a premium of 120 basis points on a notional amount of $100 million would pay a premium of $1.2 million per year, equal to $100,000,000 multiplied by 1.20%. 

As the probability of default by the underlying borrower changes over time, the credit spread for new CDS changes and the fair value of existing CDS contracts will likewise change. If the default risk of the borrower increases, then the credit spread “widens” and the value of the protection buyer’s existing CDS increases. Conversely, if the default risk of the borrower decreases, then the credit spread “narrows” and the value of the protection buyer’s existing CDS decreases. 

At JPM, the risk metric known as Credit Spread Widening 01 (CS01) measured the expected dollar profit or loss if the spread on a credit derivative widened by one basis point. For example, how much would JPM profit from the change in fair value of protection that it had purchased on a high yield CDS whose spread widened from 500 to 501 basis points, or how much would JPM lose from the change in fair value of protection that it had sold on an investment grade CDS whose spread widened from 200 to 201 basis points? CS01 was also referred to as Credit Spread Basis Point Value (CSBPV). 

CIO calculated CSBPV for each of its fixed income securities and credit derivatives, summed these, and compared the total to the aggregate risk limit of $12 million. Those securities and derivatives subject to mark-to-market accounting had a $5 million limit. SCP first exceeded CIO’s $5 million mark-to-market CSBPV limit on January 6 and then remained continuously in breach until the limit was replaced in May, at which time actual CSBPV was approximately $60 million, or fully 12 times the limit (US Senate Exhibits, 310). SCP first exceeded the related CIO aggregate CSBPV limit on January 18, again on January 25, and then remained continuously in breach until that limit was also replaced in May. However, Drew was not routinely notified about these CSBPV breaches in her role as head of CIO because CSBPV is a Level 2 limit, and she was not informed of Level 2 breaches. 

In response to these breaches, CIO market risk personnel began suggesting in early February that the mark-to-market CSBPV limit be raised from $5 million to $20 million, $25 million, 


or even $30 million. Though these proposed limit increases were not granted, Drew also did not require traders to reduce risk even after learning about the ongoing breach a couple weeks later. In fact, Drew characterized the CSBPV metric in an e-mail as being “old and outdated,” though she gave no explanation why (US Senate Report, 201). 

Weiland also faulted CSBPV, just as he criticized the results of the CRM metric. He considered CSBPV to be an unsophisticated measure of risk exposure, since CSBPV assumed that all credit spreads, both large and small, widened by exactly one basis point (as implied by the name) regardless of the actual volatility of credit spreads. In practice, CDS on more risky high-yield corporate bonds typically trade at larger and more volatile credit spreads than CDS on less risky investment-grade bonds. However, an improved metric, known as betaadjusted CSBPV, was already in use at JPM’s Investment Bank and could have provided more accurate loss estimates at CIO for the SCP book (US Senate Report, 204). 

## _**Credit Spread Widening 10%**_ 

Closely related to the CSBPV risk metric just discussed is the Credit Spread Widening 10% (CSW10%) metric, which is the expected profit or loss to a portfolio if the spread on each credit position simultaneously widened by 10% of its current amount. For example, how much would JPM profit from the change in fair value of protection that it had purchased on a high-yield CDS whose spread widened from 500 to 550 basis points, or how much would JPM lose from the change in fair value of protection that it had sold on an investment-grade CDS whose spread widened from 200 to 220 basis points? 

In contrast with their general disregard for CRM and CSBPV, both Drew and Weiland felt that CSW10% was useful in measuring and monitoring risk.  Weiland thought CSW10% “better reflect[ed] the risk of the portfolio in material market moves,” and Drew looked to CSW10% as the “overriding” risk limit. In fact, after SCP first breached CIO’s mark-to-market CSW10% limit of plus/minus $200 million on March 22, Drew halted trading of the SCP the very next day. 

## _**Stress-Loss Limits**_ 

According to the JPM Task Force, the bank performs stress tests on a weekly basis “by applying a defined set of shocks, which vary in magnitude and by asset class, to a portfolio” to estimate the loss that would be incurred from hypothetical unusual events, such as another collapse in equity markets, a credit crisis, or an oil crisis (JPM Task Force 2013, 8283). 

One week after breaching the CSW10% limit on March 22, SCP’s credit derivative positions caused CIO to exceed its stress-loss limits on March 29. With this breach, which continued for a month, CIO had exceeded all Level 1 and Level 2 limits used to monitor its trading activity (US Senate Report, 207). 

## _**Stop-Loss Limits**_ 

Whereas VaR, CRM, CSBPV, CSW10%, and the stress-loss limits are based on estimates of how a portfolio will perform under certain predefined conditions, stop-loss limits are based on actual daily profit and loss, and place an upper limit on the dollar amount that a portfolio can lose over a specified time period (one, five, and 20 trading days in the case of JPM) (US Senate Report, 208). 


Even though stop-loss limits should be a risk measurement and monitoring tool that is easy to understand and to apply, CIO’s use of stop-loss limits suffered from several shortcomings. First, the OCC determined that CIO used the stop-loss limit as an advisory limit only, whereas the Investment Bank actively enforced its stop-loss limits. Second, in an unusual step, each of CIO’s one-day, five-day, and 20-day stop-loss limits was set at the same dollar amount. Third, CIO raised each of the stop-loss limits from $60 million to $70 million in December 2011, shortly before the acceleration in SCP trading activity (US Senate Report, 209-210). 

## _**Concentration Limits**_ 

As is typical practice at financial firms, JPM’s Investment Bank used concentration limits as a rudimentary tool to restrict total exposure to a specific financial instrument, asset type, risk factor, or counterparty. However, CIO did not use concentration limits during the relevant period, only implementing them later in 2012 after trading of the SCP book had already been halted (US Senate Report, 211). 

## **7. Aftermath** 

As noted in Section 6, Drew ordered the traders to halt active buying and selling of the SCP positions on March 23 after learning that they breached the CSW10% risk limit the previous day. Year-to-date losses were reported as $222 million at this date, though that amount would be revised higher after the JPM Task Force discovered evidence that SCP traders had not complied with US Generally Accepted Accounting Principles when recording the fair value of certain derivatives in an effort to hide their losses from bank management. However, the various long and short derivative positions in the SCP book still existed, and losses escalated and risk limits continued to be exceeded as a result, even as the trading book was being dismantled. 

In late April 2012, JPM senior management ordered a team of derivatives experts from the Investment Bank to analyze each of the approximately 130 positions within the SCP book. After its review, most SCP credit derivatives were transferred during the second quarter to the Investment Bank, which closed out these positions throughout the remainder of the year. SCP-caused trading losses ultimately reached $6.2 billion by December 31, 2012 (US Senate Report, 94). 

In response to a November 2012 OCC Supervisory Letter identifying deficiencies in CIO risk management, as well as the January 2013 JPM Task Force Report on the CIO losses, JPM implemented a number of reforms, some of which are directly pertinent to the bank’s use of risk limits, metrics, and models. JPM reviewed and revised market risk limits across all lines of business, adding more granular limits. For example, CIO had 260 risk limits by January 2013, including concentration limits and portfolio-specific limits for the first time. In addition, the Chief Executive Officer, Chief Risk Officer, and Head of Market Risk for both JPM and the affected line of business will be notified whenever a risk limit is breached by more than 30% or for more than three consecutive business days, unless the breach results from a data-quality issue (JPM Task Force 2013, 115). 

However, some observers were uncertain whether these changes would prove effective, since CIO often chose to disparage and ignore the risk limits that were already in place, and because senior bank management, including Dimon and Hogan, had been informed of certain risk limit breaches, notably the four-day breach of firm-wide VaR in January (US Senate Report, 214). 


JPM also began to identify the most significant risk models across its business units, to house all models in a central database, to improve the functionality of and support for that models database, to minimize differences in how various models treat the same products, and to review old or rarely used models. The Model Review Group’s role and staffing will be expanded from model review and approval to include implementation and ongoing monitoring (JPM Task Force 2013, 113). 

In September and October 2013, banking regulators in the US and the United Kingdom announced a global settlement with JPM, penalizing the firm a total of approximately $1 billion. As part of the global settlement, the OCC levied a $300 million penalty against JPM for unsafe and unsound banking practices, and the Federal Reserve Board penalized JPM $200 million for failing to inform the Board of deficiencies in risk management. These issues are explored in greater detail in Zeissler, et al. 2014D. (See also McNamara, et al. 2014C, which provides an overview of the internal-risk models used by banks to satisfy the riskbased capital requirements established by the Basel regime.) 

## **References** 

JPMorgan Chase & Company. 2010. _Form 10-K._ Filed February 28, 2011, for the year ended December 31, 2010. 168. (JPM 10-K 2010) 

___________. 2011. _Form 10-K._ Filed February 29, 2012, for the year ended December 31, 2011. 93-131. (JPM 10-K 2011) 

___________. 2012. _Form 8-K._ Filed April 13. 67. (JPM 8-K 20120413) 

___________. 2012. _Form 10-Q._ Filed May 10 for the quarter ended March 31. 73. (JPM 10-Q 2012Q1) 

___________. 2012. _Transcript: Business Update Call._ Recorded May 10. 1-20. (JPM Business Update Call) 

___________. 2013. Report of JPMorgan Chase &. Co. Management Task Force Regarding 2012 CIO Losses. January 16. 1-28, 78-96, 106-108. (JPM Task Force 2013) 

McNamara Christian and Andrew Metrick, 2014C _Basel III C: Internal Risk Models,_ Yale Program on Financial Stability Case Study 2014-1C-V1. November. 

Office of the Comptroller of the Currency. 2011. _OCC Bulletin 2011-12: Supervisory Guidance on Model Risk Management._ April 4. 1-21. (OCC 2011-12) 

RiskMetrics. Undated. “VaR: Parametric Method, Monte Carlo Simulation, Historical Simulation.” Accessed at http://help.riskmetrics.com/RiskManager3/Content/Statistics_Reference/VaR.htm 

United States Senate Permanent Subcommittee on Investigations. 2013. _JPMorgan Chase Whale Trades: A Case History of Derivatives Risks and Abuses (Exhibits)._ March 15. 15-30, 310 [note: page numbers as used in the Adobe Acrobat page navigation toolbar]. (US Senate Exhibits) 

___________. . 2013. _JPMorgan Chase Whale Trades: A Case History of Derivatives Risks and Abuses (Majority and Minority Staff Report)._ March 15. 185-246. (US Senate Report) 


Zeissler, Arwin G., Daisuke Ikeda, and Andrew Metrick. 2014A. _JPMorgan Chase London Whale A: Risky Business_ , Yale Program on Financial Stability Case Study 2014-2A-V1, December 1, 2014, Revised: July 17, 2015 

Zeissler, Arwin G. and Andrew Metrick. 2014D, 2015. _JPMorgan Chase London Whale D: Risk Management Practices_ , Yale Program on Financial Stability Case Study 2014-2D-V1, December 1, 2014, Revised: July 20, 2015 

Development of this case has been supported by a generous grant from the Alfred P. Sloan Foundation to the Yale Program on Financial Stability. 

Copyright 2014, 2015, 2019 © Yale University. All rights reserved. To order copies of this material or to receive permission to reprint any or all of this document, please contact the Yale Program for Financial Stability at ypfs@yale.edu. 


## **Appendix 1: Timeline of Key Events** 

- 2011 October – Patrick Hagan developed the new 10-Q Value at Risk (VaR) November model used by the Chief Investment Office (CIO) for financial reporting. 

- December Jamie Dimon (Chief Executive Officer) and Douglas Braunstein (Chief Financial Officer) instructed CIO to reduce Risk Weighted Assets so that JPMorgan Chase & Company (JPM) could reduce its regulatory capital requirements. CIO’s 1-day, 5-day, and 20-day stop-loss advisory limits were each raised from $60 million to $70 million. 

- 2012 January 1 JPM 10-Q VaR limit = $125 million. CIO 10-Q VaR limit = $95 million. 

- January 6 CIO Credit Spread Basis Point Value (CSBPV) $5 million markto-market limit first breached; CIO remained continuously over this limit until May. 

- January 16CIO’s Synthetic Credit Portfolio (SCP) breached the CIO VaR 19 limit and firm-wide VaR limit for 4 days, which was reported to Mr. Dimon. 

- January 18 CIO Comprehensive Risk Measure (CRM) = $3.2 billion. JPM’s quant team was not able to calculate CIO CRM for the next five weeks. CIO CSBPV $12 million global limit first breached. 

- January 23 Dimon and John Hogan (Chief Risk Officer) approved an increase in the firm-wide VaR from $125 million to $140 million until January 31. 

- January 25 CIO CSBPV $12 million global limit breached again; CIO remained continuously over this limit until May. 

- January 26 CIO meeting at which Bruno Iksil proposed purchasing additional long credit derivatives to offset short positions. The proposal was approved and implemented immediately. 

- January 27 SCP VaR = $126 million, over its temporary limit of $105 million. 

- January 30 CIO received JPM approval to adopt a revised VaR model, which reduced CIO and SCP VaR by 50%. 

- February CIO held its 2012 annual Business Review of risk limits. February CIO CRM = $6.3 billion, dismissed by Peter Weiland as 22 “garbage.” March 22 SCP breached the CIO mark-to-market CSW10% limit. 


||March 23|Ina Drew (JPM Chief Investment Officer and head of CIO)|
|---|---|---|
|||ordered the CIO traders to stop trading the SCP.|
||March 29|SCP caused CIO’s stress-loss limits to be exceeded.|
||April 6|Bloomberg and the_Wall Street Journal_published the first|
|||news stories about the “London Whale.”|
||April 13|JPM issued its first-quarter 2012 earnings release, appearing|
|||to show that average CIO VaR barely changed from $69<br>million during the fourth quarter of 2011 to $67 million|
|||during the first quarter of 2012. However, the earnings|
|||release made no mention of the change in CIO’s VaR model.|
||May 10|JPM finalized its first-quarter financial results. By this time,|
|||the JPMorgan Chase Management Task Force discovered|
|||errors in the new CIO VaR model that incorrectly reduced CIO|
|||VaR. JPM went back to the old model, revised average first-|
|||quarter CIO VaR from $67 million to $129 million, but made|
|||no mention in the Form 10-Q filing of the reason for the|
|||change.|
||November|OCC sent JPM a Supervisory Letter outlining deficiencies in|
||6|CIO risk management. JPM did not dispute the findings or the<br>recommendations.|
||December|Year-to-date SCP losses = $6.2 billion.|
||31||
|2013|September-|Four regulators in the US and one in the UK reached|
||October|settlement agreements with JPM, totaling $1.020 billion in<br>penalties.|
