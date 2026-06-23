## **Anatomy of the Repo Rate Spikes in September 2019[1]** 

_R. Jay Kahn,_[2] _Matthew McCormick,_[3] _Vy Nguyen,_[4] _Mark Paddrik,_[5] _and H. Peyton Young_[6] 

## **Abstract** 

Repurchase agreement (repo) markets represent one of the largest sources of funding and risk transformation in the US financial system. Despite the large volume, repo rates can be quite volatile, and in the extreme, they have exhibited intraday spikes that are five to 10 times the rate on a typical day. This paper uses a unique combination of intraday timing data from the repo market to examine the potential causes of the dramatic spike in repo rates in mid-September 2019. We conclude that, in large part, the spike resulted from a confluence of factors that, when taken individually, would not have been nearly as disruptive. Our work highlights how a lack of information transmission across repo segments and stickiness in customer-to-dealer markets most likely exacerbated the spike. These findings are instructive in the context of repo market liquidity, demonstrating how the segmented structure of the market can contribute to its fragility. 

**Keywords:** financial intermediation, market segmentation, rate spikes, repurchase agreements, short-term funding 

## **JEL Classifications:** D40, D82, G14 

> 1 The views expressed in this working paper are those of the authors and do not necessarily indicate concurrence by the Office of Financial Research (OFR), the US Department of the Treasury, the Federal Reserve Board of Governors, or the Federal Reserve System. Any errors are the sole responsibility of the authors. The authors thank Sebastian Infante, Ram Yamarthy, and participants at an OFR brownbag and the Yale Program on Financial Stability’s 2023 conference, “Fighting a Financial Crisis,” for helpful comments and suggestions. 

> 2 R. Jay Kahn, senior economist, Board of Governors of the Federal Reserve System, jay.kahn@frb.gov. 

> 3 Matthew McCormick, senior financial sector advisor, Federal Reserve Bank of Dallas, matthew.mccormick@dal.frb.org. 

> 4 Vy Nguyen, international economist, Office of International Trade and Investment Policy, US Department of the Treasury, vy.nguyen2@treasury.gov. 

> 5 Mark Paddrik, associate director of financial institutions, Office of Financial Research, US Department of the Treasury, mark.paddrik@ofr.treasuty.gov. 

> 6 H. Peyton Young, research principal, Office of Financial Research, US Department of the Treasury , hobart.young@ofr.treasury.gov. 


## **I. Introduction** 

Repurchase agreement (repo) markets represent one of the largest sources of funding and risk transformation in the US financial system. They provide a relatively stable and flexible source of secure short-term funding for banks, securities dealers, and other large financial institutions that rely on the market to fund short-term liquidity provision and leveraged investments. Currently, the daily volume of transactions on all US repo markets exceeds $3 trillion. Despite the large volume, repo rates can be quite volatile, and in the extreme, they have exhibited intraday spikes that are five to 10 times the rate on a typical day. A notable example, and the focus of this work, occurred on September 17, 2019—when the intraday repo rate rose to more than 300 basis points above the upper end of the federal funds target range. This was 30 times larger than the same spread during the preceding week (see Figure 1). Although short-lived, this event and its spillover into other short-term funding markets, such as the federal funds market, prompted the Federal Reserve to step in and introduce cash to the market through a repo facility. 

[FIGURE id=vol5_iss4_1_f1 type=chart page=4 label="Figure 1" file=figure_1.png caption="Repo Rate Spikes, August 2014–September 2019"]
### **Figure 1: Repo Rate Spikes, August 2014–September 2019**
![Figure 1](assets/vol5_iss4_1/figure_1.png)


Notes: Tri-party repo average rate is the weighted average daily rate on new overnight Treasury repo transactions from Bank of New York Mellon repo data. All rates are spreads over the federal funds target range midpoint. The upper dashed line shows the interest rate on excess reserves and the lower dashed line shows the Overnight Reverse Repurchase (ON RRP) Facility rate. The y axis of this graph is truncated at 1%, cutting off the y-value for September 17, 2019, which stood at 3.06%. 

_Sources: FRB BONY Tri-Party Repo Collection; FRBNY Effective Federal Funds Rate; FRED; authors’ analysis._ 

Using a unique combination of data sources available to the US Department of the Treasury’s Office of Financial Research (OFR), we examine the potential causes of the dramatic spike in repo rates in mid-September 2019. Although the spike was likely driven in part by the low level of reserves, as has been previously suggested in Afonso et al. (2021); Copeland, Duffie, and Yang (2021); and Correa, Du, and Liao (2020), we argue low reserves alone may be unable to account for either the timing of the spike or its severity. Instead, we suggest that a 


confluence of more immediate factors such as tax payments and Treasury issuance dates contributed to the size of the spike.[7] We provide evidence that a lack of transparency plus imperfect intermediation may have substantially contributed to the disruption on September 17, and to a large pullback in funding by money market funds (MMFs) caused by corporate tax deadlines on the 16th. 

A novel contribution of the paper is its detailed analysis of the intraday and interday dynamics of different repo market segments, which sheds light on the roles of different classes of intermediaries in the market. We use this data to show that on the 16th, decreases in money market fund assets associated with corporate tax payments translated almost one for one into decreases in repo investments. We also use the intraday pattern of rate movements on September 16–17 to suggest that a lack of transparency plus imperfect intermediation may have substantially contributed to the disruption. Finally, we examine how the Federal Reserve’s interventions in the repo market affected lending by dealers, using a high-frequency event study to show that there was a sizable and speedy passthrough from Federal Reserve lending to dealers into their cleared repo activity. 

Understanding the sources of volatility in repo rates is important not just for financial institutions but for policymakers as well. The repo market underpins the Secured Overnight Financing Rate (SOFR), which has supplanted LIBOR as the primary reference rate for a diverse range of financial products.[8] By shedding light on how segmented markets can increase the fragility of the repo market during stress times, our work informs future policy considerations for strengthening repo market functioning. 

## **II. Structure of the Repo Market** 

Before proceeding, we present a brief overview of the main repo markets and how they differ in participation, clearing, transparency, type of collateral, and settlement times.[9] Understanding these differences is key to understanding how structural features of the repo market can exacerbate price volatility. 

A repo transaction involves the sale of assets together with an agreement to repurchase them on a specified future date at a prearranged price. Market participants use repos for many reasons, including financing their portfolios, using cash as collateral to borrow securities, and as a safer alternative to uninsured deposits. Central banks also use repos as important monetary policy tools. 

Assets underlying a repo are used as collateral to protect cash lenders against the risk that cash borrowers will fail to return the cash. Cash lenders typically require 

> 7 For a discussion of some of these factors, see Afonso et al. (2021); Anbil, Anderson, and Senyuz (2021); Copeland, Duffie, and Yang (2021); and Correa, Du, and Yang (2020). 

> 8 See Consumer Financial Protection Bureau (2021). 

> 9 For more detailed reviews about the repo market, see Adrian et al. (2014); Baklanova, Copeland, and McCaughrin (2015); and Kahn and Olson (2021). 


overcollateralization, and thus, the value of the assets pledged as collateral is discounted. This discount is typically referred to as a haircut. Additionally, repo transactions specify the types of securities that are acceptable as collateral, as well as the associated haircuts or initial margin requirements. Although most repos are overnight transactions, they can be entered into with a range of maturities. The interest rate on these transactions is calculated based on the difference between the sale price and the repurchase price of the assets underlying the repo, and the rate can be negotiated on either a fixed or a floating basis. 

## **Repo Market Segments** 

The US repo market has four distinct segments. One way of describing these segments is by distinguishing between transactions that are settled on the books of a tri-party custodian bank and transactions that are settled bilaterally. Two segments settle on the books of a triparty custodian: (1) the non-centrally cleared tri-party repo segment, in which the Bank of New York Mellon (BONY) serves as the custodian; and (2) the centrally cleared General Collateral Finance (GCF) repo segment, which is cleared by the Fixed Income Clearing Corporation (FICC). The tri-party segment primarily consists of dealers and large banks borrowing from smaller dealers, MMFs, and other asset managers. Tri-party is also the segment through which the Federal Reserve intervenes in the repo market. The GCF segment largely consists of transactions between large financial institutions such as dealers, banks, and government-sponsored enterprises (GSEs).[10] 

Bilateral transactions occur in two additional segments: (3) those cleared by FICC’s Deliveryto-Payment (DVP) repo service, and (4) non-centrally cleared bilateral repos (NCCBRs). DVP is a large segment among clearing members that allows dealers to trade specific securities. It also includes trades with certain other institutions, such as MMFs and hedge funds, that are not direct clearing members but are allowed to participate through sponsorship by a clearing member. These trades are known as sponsored DVP repo. Meanwhile, the noncentrally cleared bilateral repo market serves as an important source of leverage for hedge funds, and it is also the primary venue for repo lending by primary dealers. However, data on this market is not available for September 2019, and thus, it is not a part of our dataset. 

Figure 2 displays these four distinct segments of the market and the flow of funds between the principal participants. 

> 10 The FICC also offers a Sponsored General Collateral service that includes transaction types similar to those offered by the existing FICC GCF repo service. However, the Sponsored General Collateral service allows entities that are not direct clearing members of FICC to participate in these transactions. Because this market began trading in September 2021, following its approval by the Securities and Exchange Commission (SEC), it is not part of our discussion. 


[FIGURE id=vol5_iss4_1_f2 type=figure page=7 label="Figure 2" file=figure_2.png caption="Segments of the Repo Market"]
### **Figure 2: Segments of the Repo Market**
![Figure 2](assets/vol5_iss4_1/figure_2.png)


Note: Arrows denote the flow of cash from cash lenders to cash borrowers. 

_Source: Authors’ illustration._ 

## **Daily Repo Clearing Cycle** 

The majority of funding provided through repos in the US financial system is overnight and therefore can be renegotiated on a daily basis. Figure 3 presents the average intraday clearing cycle for GCF, DVP, and tri-party. This figure highlights the fact that most of the activity in each repo market segment occurs during only a few hours in the morning. Within each market segment, hourly rates typically vary by just a few basis points over the course of the day. Trades in cleared DVP and GCF generally occur slightly earlier than in tri-party, in part because of settlement timing differences between these markets.[11] Moreover, the concentration of volumes at the beginning of the day has been explained by market participants as a response to overdraft fees assessed by clearing banks at 8:30 a.m. 

> 11 See Clark et al. (2021); Copeland, Duffie, and Yang (2021); and Paddrik, Ramírez, and McCormick (2021). Additionally, these figures are calculated over 2021, so the tri-party timing figure likely reflects the presence of the Federal Reserve’s ON RRP facility, which operates later in the day than many private repo transactions. 


[FIGURE id=vol5_iss4_1_f3 type=figure page=8 label="Figure 3" file=figure_3.png caption="Daily Clearing Cycle for Tri-party, GCF, and DVP"]
### **Figure 3: Daily Clearing Cycle for Tri-party, GCF, and DVP**
![Figure 3](assets/vol5_iss4_1/figure_3.png)


Notes: Blue line shows the cumulative percent of total daily volume in each market transacted before each 15minute interval of the day averaged over all days in 2021. The dashed lines show the 25th and 75th percentiles across days. 

_Source: OFR Cleared Repo Collection; FRB BONY Tri-Party Repo Collection; authors’ calculations._ 

## **III. Potential Causes of Rate Spikes** 

Our analysis begins with a review of a variety of factors that may have contributed to the abrupt spike in repo rates in September 2019. Some factors are transitory, while others result from long-term trends that brought about an overall tightening in money markets, and both were exacerbated by frictions in the repo market. We begin with the long-term trends, specifically in the reserve balances banks maintained with the Federal Reserve and the amount of Treasuries outstanding. 

## **Long-term Trends: Reserve Balances and Treasuries Outstanding** 

A wealth of papers have provided evidence that low levels of reserves and high levels of outstanding Treasuries played a key role in driving the September 2019 repo spike and other spikes in the preceding years, including Afonso et al. (2021); Correa, Du, and Liao (2020); Copeland, Duffie, and Yang (2021); and d’Avernas, Han, and Vandeweyer (2023). In October 2014, reserves stood at a high of roughly $2.8 trillion, but from 2017 to 2019, the Federal Reserve gradually reduced the size of its balance sheet by not reinvesting a part of its maturing securities. Consequently, aggregate reserves declined to a multiyear low of less than $1.4 trillion by mid-September 2019 (see Figure 4). Simultaneously, marketable Treasuries outstanding increased from $12.3 trillion in October 2014 to more than $16 trillion by the beginning of September 2019 owing in part to the Tax Cuts and Jobs Act of 2017. 


[FIGURE id=vol5_iss4_1_f4 type=figure page=9 label="Figure 4" file=figure_4.png caption="Reserves and Treasuries Outstanding, 2010-2021"]
### **Figure 4: Reserves and Treasuries Outstanding, 2010-2021**
![Figure 4](assets/vol5_iss4_1/figure_4.png)


Notes: The level of reserves is estimated from weekly data on reserves from the Federal Reserve’s H.4.1 release, and daily changes in key factors affecting reserves and Treasuries outstanding are estimated using daily data on Treasury issuance. 

_Sources:  Daily Treasury Statement; FRB H.4.1. Factors Affecting Reserves Release; FRBNY Repo Operations Data; TreasuryDirect; authors’ calculations._ 

Many papers provide a theoretical link between the level of reserves or of reserves relative to Treasuries and either the level of repo rates or the potential for repo spikes.[12] Although the microfoundations for these papers may differ, the essential point is that the repo market allows participants to temporarily convert their Treasury holdings into cash. The repo rate, which provides the cost for this conversion, should therefore respond to the relative supply of Treasuries and of cash, which in turn is determined by the supply of reserves. The amount of cash available to dealers to lend in repo markets may decline as reserves decline. Similarly, increased Treasuries outstanding may increase the demand for repo borrowing by dealers to finance their positions in Treasuries. 

In Figure 5, we examine the relationship between the ratio of reserves to Treasuries outstanding and the repo rate from August 22, 2014, to September 17, 2019, following from a similar figure in d’Avernas, Han, and Vandeweyer (2023). Since data on reserves is not publicly available on a daily frequency, we construct a daily estimate using the weekly series on reserves provided in the Federal Reserve’s H.4.1 release and subtracting changes in ON RRP volumes and changes in the Treasury General Account (TGA) and adding System Open Market Account (SOMA) net securities purchases in the intervening week.[13] We then divide this series by outstanding Treasuries calculated from daily data on issuance. This is plotted 

> 12 For two examples, see d’Avernas, Han, and Vandeweyer (2023) and Yang (2020). 

> 13 These estimates are imperfect since they do not capture other balance sheet items that are not reported on a daily basis, for instance, the foreign repo pool, currency in circulation, and centrally bank liquidity swaps. However, regressing the true weekly release on our daily estimate obtains a coefficient very close to 1 and an R-squared above 99%, which shows that our daily estimate is extremely close to the true value on days where we can observe the true value of reserves. Moreover, we obtain almost identical results working backward from the next H.4.1 release instead of forward from the last release. 


against the spread of the Tri-party General Collateral Rate (TGCR) over the interest rate on reserve balances. 

[FIGURE id=vol5_iss4_1_f5 type=chart page=10 label="Figure 5" file=figure_5.png caption="Reserves and Repo Spreads, August 22, 2014–September 17, 2019"]
### **Figure 5: Reserves and Repo Spreads, August 22, 2014–September 17, 2019**
![Figure 5](assets/vol5_iss4_1/figure_5.png)


Notes: The ratio of reserves to Treasuries outstanding is calculated using estimates from weekly data on reserves from the Federal Reserve’s H.4.1 release and daily changes in key factors affecting reserves and daily data on Treasury issuance. The spread is calculated using daily data on the Tri-party General Collateral Rate and the interest rate on excess reserves (IOER). The black line is the OLS best fit for a regression of the TGCRIOER spread on reserves over outstanding Treasuries for data through September 13, 2019. 

_Sources:  Daily Treasury Statement; FRB H.4.1. Factors Affecting Reserves Release; FRBNY Reference Rates; FRBNY Repo Operations Data; TreasuryDirect; authors’ calculations._ 

Examining Figure 5, a clear pattern emerges between the level of reserves relative to Treasuries, and spreads between funding markets. Low levels of reserves are associated with higher repo rates, and vice versa. However, there are two important caveats to this relationship. 

First, the relationship is highly nonlinear. September 17 remains an extreme outlier relative to the black line, which shows a fitted line estimated using data through September 13. In Figure 6, we show the evolution of reserves and the SOFR over the two weeks surrounding the repo spike. Examining this table, we can see that reserves were at their lowest point on September 16, having fallen by $81 billion from September 13. However, rates on the 16th were at only 2.43%, while on the 17th, after reserves had increased by $35 billion, rates spiked to 5.25%. Even if one subtracts the reserves added by the Federal Reserve’s repo operations, the total decline in reserves from the 16th to the 17th would have been only $6 billion. While this may reflect constraints on banks that become extremely binding at low reserves as suggested by Afonso et al. (2021), it is also important to note that many other days with quite low levels of reserves did not have similarly high repo rates. We propose that the gentle slope of most of the relationship between reserves and funding spreads is best 


reconciled with the extreme nonlinearity when reserves are relatively low by considering the role of informational frictions. 

[FIGURE id=vol5_iss4_1_f6 type=diagram page=11 label="Figure 6" file=figure_6.png caption="Changes in Federal Reserve Balances and Treasury Cash Flow in Sept. 2019"]
### **Figure 6: Changes in Federal Reserve Balances and Treasury Cash Flow in Sept. 2019**

|**Date**|**SOFR**<br>**(%)**|**Federal Reserve Balances**<br>**($ billions)**|**Federal Reserve Balances**<br>**($ billions)**|**Federal Reserve Balances**<br>**($ billions)**|**Federal Reserve Balances**<br>**($ billions)**|**Treasury Cash Flow**<br>**($ billions)**|**Treasury Cash Flow**<br>**($ billions)**|**Treasury Cash Flow**<br>**($ billions)**|
|---|---|---|---|---|---|---|---|---|
||||**($ billions)**||||||
||||||||||
|||**Reserves**|**TGA**|**ON RRP**|**Repo**|**ΔTGA**|**Coupon**<br>**Issuance**|**Corporate**<br>**Tax**<br>**Payments**|
|**09/09**|2.12|1,441|190|3|0|9|0|0|
|**09/10**|2.14|1,437|194|4|0|4|0|1|
|**09/11**|2.15|1,459|184|4|0|–10|0|1|
|**09/12**|2.20|1,447|195|3|0|12|0|3|
|**09/13**|2.20|1,428|216|3|0|20|0|16|
|**09/16**|2.43|1,347|299|2|0|83|54|35|
|**09/17**|5.25|1,382|308|2|41|9|0|1|
|**09/18**|2.55|1,385|303|19|52|–5|0|0|
|**09/19**|1.95|1,395|314|5|56|11|0|0|
|**09/20**|1.86|1,399|311|8|59|–3|0|0|



Notes: Reserve balances with asterisks are from weekly data on reserves from the Federal Reserve’s H.4.1 release. Reserve balances without asterisks are estimated using daily changes in key factors affecting reserves. TGA is the Treasury General Account, ON RRP is the Overnight Reverse Repurchase Facility, and Repo is outstanding Federal Reserve repo operations. Coupon issuance is the total issuance of all coupon Treasuries, and corporate tax payments are total income tax payments reported by the Treasury. 

_Sources: Daily Treasury Statement; FRB H.4.1. Factors Affecting Reserves Release; FRBNY Reference Rates; FRBNY Repo Operations Data; TreasuryDirect; authors’ calculations._ 

A second caveat relevant to September 16 is that larger spikes occurred before September 16 when reserves were more abundant, implying that reserves alone cannot explain the timing of the spike; factors other than the level of reserves may have been important in triggering the extreme increase in rates. While reserves and the supply of Treasuries certainly played a key role, we argue that segmentation and the microstructure of the repo market may have been crucial for both the magnitude and timing of the spike. These factors depended more on the proximate causes of the spike, to which we now turn. 


## **Proximate Causes** 

One starting point for examining the proximate causes is the detail Figure 6 provides on what drove the decrease in reserves from September 13 to September 16. The table shows that the decrease in reserves of $81 billion was driven primarily by an increase in the Treasury General Account, which increased by $83 billion. The TGA is the account at the Federal Reserve that the Treasury uses to hold its cash balances. When the Treasury borrows or takes in more tax payments than it spends, it increases the balance in the TGA, which then reduces reserves. Previous work has pointed out the importance of the TGA in the repo spike, notably Correa, Du, and Liao (2020). 

The last two columns in Figure 6 show two important components of the increase in the TGA account: a net coupon Treasury settlement on the 16th of $54 billion, and payments to the Treasury of $35 billion for the corporate income tax for the third quarter of 2019, which also had a deadline on the 16th. Since both actions increase the cash held by the Treasury on the 16th, all else equal, they lead to an increase in the TGA and a decrease in reserves. However, Treasury issuance and corporate tax payments not only affect the repo rate through the supply of reserves but also alter the needs of specific borrowers and lenders to transact. We discuss the effects of these two actions in more detail over the remainder of this section, as well as some other potential proximate causes of the repo spike. 

## _Treasury Settlement_ 

Settlement of large issuances of Treasury notes and bonds generates additional demand for repo to finance purchases of these Treasury securities. A significant share of repo demand comes from primary dealers, which normally absorb a substantial share of Treasury issuances onto their balance sheets until they can gradually sell them to their customers. Dealers rely heavily on repo to fund these initial purchases and generally decrease their funding of a new issuance through repo gradually as they have time to sell off the issue. 

The effects of issuance may have been exacerbated by the large increase in Treasuries outstanding over the previous three years, combined with limited demand from foreign purchasers of Treasuries. Combined, these two forces contributed to a larger amount of Treasuries remaining on dealer balance sheets for longer. With net Treasury positions held by primary dealers near all-time highs in September, it is possible that the additional debt issued added to the already strained dealer balance sheets by increasing their repo borrowing, thus further strengthening upward pressure on repo rates (Anbil, Anderson, and Senyuz 2020). 

While the Treasury issuance on the 16th has received a great deal of attention, it is also important to recognize that it may not have had as direct an effect on primary dealers as many other settlements. Of the $78 billion in gross Treasuries settling on the 16th, $40 billion was in Treasuries being reopened, in particular a 30-year bond and 10-year note being reopened for the first time. Reopenings are not new issues but rather additional issuance of existing securities. Since these securities already exist, dealers will frequently short-sell these Treasuries in advance of their issuance, often at a penalty rate known as a special 


collateral rate.[14] When the issue is reopened, dealers who have lent against it are able to purchase the securities at auction using the repayment by their borrowers and return the securities to their lenders. Figure 7 shows that the on-the-run bond and note were indeed trading at a special collateral rate before their reopening on the 16th. This means that on the 16th, dealers may have been better able to prepare for the effects of issuance, since through short-selling they may have effectively already sourced the funding for their purchase of the securities before the settlement date. 

[FIGURE id=vol5_iss4_1_f7 type=chart page=13 label="Figure 7" file=figure_7.png caption="General Collateral and On-the-run Collateral Repo Rates, Aug.–Sept. 2023"]
### **Figure 7: General Collateral and On-the-run Collateral Repo Rates, Aug.–Sept. 2023**
![Figure 7](assets/vol5_iss4_1/figure_7.png)


Notes: Dark vertical line denotes a new issuance of the 10-year and 30-year on-the-run bond and note; light gray line denotes the reopening on September 16. 

_Source: Refinitiv._ 

## _Quarterly Tax Payments_ 

While Treasury settlements may make dealers less elastic in their demand for repo funding, corporate tax payments tend to be associated with reduced lending from money market funds as corporations withdraw cash to meet their obligations to the Treasury. Repo is one of the more liquid assets money market funds have at their disposal and tends to be the first asset they sell when they need to meet these outflows. 

To provide some detail on the drivers of MMF activity and their relationship to these tax payments, we assemble a daily series of MMF total assets from Crane’s Money Market Fund Monitor. We then match each MMF to lenders across tri-party and DVP markets at the fund family level. Matching at the family level is key because market participants report that MMFs make joint decisions within a family on their allocations of cash to repo. This mapping allows us to establish a daily panel of MMF family assets matched with repo lending in both DVP and tri-party. 

> 14 See D’Amico and Pancost (2021) and Hempel and Kahn (2021) for more detailed discussions of special collateral rates before reopenings. 


In Figure 8, we show a daily series of MMF total assets. The effect of the tax deadline was a decrease in MMF total assets by about $35 billion on September 16 from the week before. This is in line with decreases observed on previous tax dates. As we will show in Section IV, this reduction in MMF assets corresponds almost one-to-one with the decrease in MMFs’ repo lending. 

[FIGURE id=vol5_iss4_1_f8 type=figure page=14 label="Figure 8" file=figure_8.png caption="Money Market Fund Assets, August 1–October 1, 2019"]
### **Figure 8: Money Market Fund Assets, August 1–October 1, 2019**
![Figure 8](assets/vol5_iss4_1/figure_8.png)


Notes: Data is for money market funds that appear throughout the sample. 

_Sources: Crane’s Money Market Fund Monitor; authors’ calculations._ 

## _Other Proximate Causes_ 

Some market commentators have suggested that sponsored repo borrowing by hedge funds, which rely on repo to fund arbitrage basis trades using highly leveraged positions, may have been a contributing factor.[15] As we shall see in Section IV, however, increased borrowing by hedge funds through sponsored DVP repo was quite minor compared to other changes in supply and demand in mid-September 2019. Other observers have suggested that an unanticipated oil shock in Saudi Arabia led to a surge in margin calls at commodity exchanges, which in turn reduced the amount of cash available for repo lending (Domm 2019; Kaminska 2019). Given data limitations, however, we have not been able to verify either of these potential explanations. 

In addition, the events of the 16th occurred in a brief window between two GSE “float periods,” which may have reduced the availability of cash in repo markets. Before the introduction of the uniform mortgage-backed security (MBS), Freddie Mac and Fannie Mae paid principal and interest on MBSs on the 15th and 25th of the month, respectively 

15 See in particular Avalos, Ehlers, and Eren (2019) and Smith (2019). For more on hedge fund involvement in the basis trade, see Barth and Kahn (2021). 


(Anderson and Huther 2016). During periods of approximately five days leading up to these payment dates, the GSEs hold cash reserves used for payments at the Federal Reserve, or they invest in repos. September 16 would have been the Freddie Mac payment date, and it occurred before Fannie Mae would have begun building up cash reserves, leading to a likely net outflow of cash from repo markets relative to the week before. 

## **Exacerbating Frictions** 

It is worth considering some of the frictions repo market participants face that can exacerbate these factors affecting supply and demand for funds. Internal frictions may have played a role in increasing banks’ demand for reserves and reducing their flexibility in responding to price signals in repo. While the aggregate supply of reserves was still large relative to the period preceding the 2007–09 financial crisis, the level of reserves banks required may have increased owing to the suite of regulatory and supervisory programs put in place following the 2007–09 financial crisis. In particular, the liquidity coverage ratio (LCR) and Regulation YY’s requirements for resolution liquidity adequacy and positioning (RLAP) may have increased banks’ demand for reserves. Broadly, the LCR requires banks to prefund a sufficient amount of high-quality liquid assets (HQLA) (for example, assets such as Treasuries or reserves that can be converted into cash) to meet their projected net cash outflows over a 30-day stress period. Although reserves and Treasuries are both HQLA of equivalent standing, Andolfatto and Ihrig (2019) report that banks occasionally feel pressured to hold reserves rather than Treasuries to satisfy their HQLA requirements. More importantly, RLAP imposes additional restrictions by requiring each individual subsidiary to hold enough HQLA to meet expected intraday outflows without relying on transfers from affiliates. This requirement reduces banks’ flexibility in sourcing funds internally, making them less likely to increase repo lending by sourcing cash from other parts of the firm. 

More generally, the spillovers from the September 2019 repo episode to the foreign exchange (FX) swaps market noted by Tran (2020) and others are likely indicative of such internal frictions. Some spillover between these markets would naturally result from foreign banks choosing to source US dollars in FX swaps instead of repo. However, the FX swaps market is heavily intermediated by the same global systemically important banks (GSIBs) that are active in repo, and lending in FX swaps increased relative to repo despite a smaller increase in rates (Correa, Du, and Liao 2020). These latter facts provide suggestive evidence that frictions in banks’ ability to internally reallocate capital led to these adjustments being made instead on an external margin. 

Finally, the US repo market is highly segmented. In the tri-party segment, deals are negotiated bilaterally, and thus, trading dynamics depend on strong relationships between dealers and MMFs. In contrast, the FICC-cleared DVP segment is brokered, so the identities of borrowers and lenders remain anonymous. Moreover, only a few primary dealers and banks can access both segments, while smaller dealers are confined to the FICC-cleared segment only. As a result of this segmentation, Anbil, Anderson, and Senyuz (2021) observe that on September 16 and 17, smaller dealers faced higher funding costs—almost 1 percentage point higher, relative to other FICC participants—given their lack of access to the tri-party segment. Higher repo rates in the FICC-cleared segment then transmitted to the tri- 


party segment because MMFs were able to extract higher rates from dealers, which were willing to pass on profits to maintain these strong trading relationships.[16] The effects of segmentation may have been exacerbated by a great deal of uncertainty among lenders about the reason for the sudden spike in rates, which discouraged them from stepping in promptly (Afonso et al. 2021). 

In this paper, we highlight the importance of lack of transparency in driving high repo rates on September 17. We show that because of the segmented nature of the repo market, and because customers may have limited visibility into repo markets on a high-frequency basis, rates for large cash providers such as MMFs lagged behind interdealer rates when cash became scarce on September 16. Then, we show that on September 17, when cash became less scarce following the Federal Reserve’s intervention, the rates MMFs demanded remained high. This suggests that limited transparency or stickiness in MMFs’ investment decisions played a role in the extreme rate highs on September 17, since the scarcity of funds in the interdealer segment of the market was not reflected in the returns MMFs could receive for introducing more cash into the market. 

## **IV. Interday and Intraday Analysis of September 16–18, 2019** 

In this section, we take a closer look at the intraday pattern of rates and the changes in supply and demand for funding on September 16–18. 

## **Lending and Borrowing Behavior** 

First, we examine the lending and borrowing behavior of different categories of firms on September 16–18, relative to an average day during the week before, when conditions were fairly quiet. Figures 9a and 9b show the changes in aggregate lending and borrowing, respectively, over three repo markets (tri-party + DVP + GCF) for nine categories of firms. Figure 9c provides a unified picture by showing the net change in lending minus borrowing for each class of participants. 

> 16 For a broader discussion of repo market trading dynamics, see Anbil, Anderson, and Senyuz (2021) and Han, Nikolaou, and Tase (2022). 


[FIGURE id=vol5_iss4_1_f9 type=figure page=17 label="Figure 9" file=figure_9.png caption="Interday Changes in Repo Activity, September 16–18, 2019"]
### **Figure 9: Interday Changes in Repo Activity, September 16–18, 2019**

a) Change in Lending b) Change in Borrowing c) Change in Net Lending 


[FIGURE id=vol5_iss4_1_f10 type=figure page=17 label="Exhibit 10" file=exhibit_10.png caption=""]
![Exhibit 10](assets/vol5_iss4_1/exhibit_10.png)



[FIGURE id=vol5_iss4_1_f11 type=figure page=17 label="Exhibit 11" file=exhibit_11.png caption=""]
![Exhibit 11](assets/vol5_iss4_1/exhibit_11.png)



[FIGURE id=vol5_iss4_1_f12 type=figure page=17 label="Exhibit 12" file=exhibit_12.png caption=""]
![Exhibit 12](assets/vol5_iss4_1/exhibit_12.png)





Notes: These figures show the change in repo lending, repo borrowing, and net repo lending in billions of dollars on September 16–18, 2019, relative to the average day in the week before across different types of lenders and borrowers. The data is for the sum of tri-party, DVP, and GCF segments of the market. 

_Sources: OFR Cleared Repo Collection; FRB BONY Tri-Party Repo Collection; authors’ calculations._ 

In aggregate, the total change in transaction volume on September 16 was not particularly large compared to day-to-day changes over the subsequent period of December 2019–July 2022. Total volume over all three markets declined by 1.7%, compared with the volume on the previous trading day (September 13). Although this change is much larger than that seen on an average day, which is about 0.11%, the standard deviation of day-to-day changes is considerable, at 2.47%. Hence, the increase on September 16 was not exceptionally large, relative to the previous period. Figure 9c shows that the largest decrease in lending behavior resulted from MMFs’ pulling back by about $35 billion. 

On September 17 and 18, the total volume of repo lending increased by $75 billion, to $125 billion, compared to the week before and by $230 billion compared to the day before. This exceptionally large increase owed in large part to repo lending by the Federal Reserve to primary dealers and foreign banks through the tri-party market. On net, hedge funds increased their sponsored repo borrowing by about $8 billion, but this amount is quite small compared to the overall changes in lending and borrowing. This finding suggests a limited role for hedge funds’ sponsored activity in the repo spike. 


[FIGURE id=vol5_iss4_1_f13 type=figure page=18 label="Figure 10" file=figure_10.png caption="Regression of Repo Lending by MMFs on Change in MMF Assets"]
### **Figure 10: Regression of Repo Lending by MMFs on Change in MMF Assets**

|**Dependent Variable**|**Change in MMF Repo Lending**|
|---|---|
|**Change in MMF Assets**||
|Coefficient|0.993|
|_t_-statistic|(7.68)|
|**R-squared**|0.546|



Notes: This table shows the results of a cross-sectional regression of the change in repo lending by MMFs on September 16 on the change in MMF assets over the week before. Change in repo lending includes all MMF transactions across DVP and tri-party markets. The regression is conducted at the family level. The _t_ -statistic for the test of the null hypothesis that the coefficient is equal to zero is in parentheses, and strongly rejects the null. 

_Sources: Crane’s Money Market Fund Monitor; FRB BONY Tri-Party Repo Collection; OFR Cleared Repo Collection; authors’ calculations._ 

Money market funds represented the largest decrease in net lending on September 16. Notably, the reduction in MMFs’ lending corresponds very nearly to the $35 billion decrease in their assets over the week before, as we noted in Section III. In Figure 10, we estimate a regression of MMF family lending on September 16 in different repo segments on the sevenday change in total assets for the fund family. The results show that a $1 billion decrease in a fund family’s assets corresponded to a $0.993 billion decrease in their total repo lending activities across both DVP and tri-party. In other words, the total reduction in MMF assets corresponds almost one-to-one with the decrease in MMF lending into repo.[17] Figure 11 plots the coefficient in Figure 10 along with a binned scatter of changes in MMF net assets (x axis) and their average change in repo (y axis). Although we do not show it here, the majority of the decrease was in DVP, which is consistent with DVP’s serving as a vehicle for MMFs investing excess cash. As noted by Afonso et al. (2021), this dynamic may have increased the intermediation costs for dealers that rely on funding from MMFs through sponsored repo, since netting benefits would have decreased. 

> 17 In contrast, Afonso et al. (2021) estimates that over the period 2016–2019, for every dollar change in assets held by MMFs, the repo investment of MMFs changed by 0.69. Our estimates apply to behavior on the specific date of September 16, 2019, not to average behavior over the previous period. 


[FIGURE id=vol5_iss4_1_f14 type=figure page=19 label="Figure 11" file=figure_11.png caption="Binned Scatter Plot of Change in MMF Assets September 9–16, 2019, and Change in Repo Lending on September 16, 2019"]
### **Figure 11: Binned Scatter Plot of Change in MMF Assets September 9–16, 2019, and Change in Repo Lending on September 16, 2019**
![Figure 11](assets/vol5_iss4_1/figure_11.png)


Notes: This figure shows a binned scatter plot of change in MMF assets between September 9 and September 16 and change in repo lending on September 9. A best fit line from the underlying data is also shown, corresponding to the regression in Figure 10. 

_Sources: Crane’s Money Market Fund Monitor; FRB BONY Tri-Party Repo Collection; OFR Cleared Repo Collection; authors’ calculations._ 

## **Intraday Pattern of Rates** 

Next, we take a closer look at the trajectory of rates in two segments of the market: (1) the tri-party market, which is a non–centrally cleared market mostly composed of banks and MMFs lending to dealers, and (2) the FICC-cleared DVP market, which is an interdealerbrokered market. As shown in Figure 12, starting at about noon on September 16, maximum rates spiked to about 4% in tri-party and 8% in DVP. Average rates remained fairly steady at about 2% in tri-party, suggesting that only a limited number of firms were impacted by higher rates. Volume was relatively low because 70% to 80% of the day’s trades had already been negotiated by the time these spikes erupted. 


[FIGURE id=vol5_iss4_1_f15 type=chart page=20 label="Figure 12" file=figure_12.png caption="Intraday Average and Maximum Rates, September 16–18, 2019"]
### **Figure 12: Intraday Average and Maximum Rates, September 16–18, 2019**
![Figure 12](assets/vol5_iss4_1/figure_12.png)


Notes: Lines are volume-weighted averages and maximums for 30-minute increments of time. The two vertical lines indicate the times when the Federal Reserve announced its intention to provide additional liquidity (9am) and the implementation of the liquidity injection (9:55am). 

_Sources: FRB BONY Tri-Party Repo Collection; OFR Cleared Repo Collection; authors’ calculations._ 

On the morning of September 17, the tri-party average rate rose to 6% and remained high for much of the traded volume that day. The two vertical lines in Figure 12 indicate the times when the Federal Reserve announced its intention to provide additional liquidity (9am) and the implementation of the liquidity injection (9:55am). Note that this injection was intended to take place at 9:30am but was delayed because of technical difficulties. Following the Federal Reserve’s intervention, rates declined substantially in the DVP-brokered market but remained elevated in tri-party. By the start of trading on September 18, average rates had fallen to about 2%, but the market remained very skittish, as shown by several spikes in both the tri-party and DVP segments of the market. 

The intraday pattern of rates highlights two important points. First, rates did not increase until the afternoon of September 16 and began increasing in the interdealer market. This highlights a general unawareness on the part of dealers about the potential scarcity of funds available in the market—otherwise, dealers would have had an incentive to borrow earlier in the morning and lend excess funds. Second, there was substantial heterogeneity in the response of rates across different segments of the repo market. The dispersion of rates in the DVP and tri-party segments on the 16th suggests that although a few market participants started to learn that cash supplies were scarce, others did not realize it or were unable to lend in response to increased tightness. 


## **Intraday Pattern of Lending and Borrowing by Dealers** 

Reserves enable banks and bank-affiliated dealers to provide settlement liquidity to other market participants and avoid intraday stress on their own balance sheets because of these intermediation activities. Although we cannot directly test whether banks may have reached their minimum comfortable level of reserves (referred to here as reserve limits, though these do not reflect hard regulatory constraints) during the September stress, the intraday data does provide some suggestive evidence that reserve constraints on banks and bank-affiliated dealers may have played a contributing role in the repo spike. Figures 13a and 13b show cumulative net lending in DVP on September 16 and 17, relative to lending on an average day during the previous week, for two categories of dealers: domestic bank-affiliated and nonbank-affiliated dealers. 

[FIGURE id=vol5_iss4_1_f16 type=figure page=21 label="Figure 13" file=figure_13.png caption="Intraday Cumulative DVP Net Lending by Dealers, September 16–17, 2019"]
### **Figure 13: Intraday Cumulative DVP Net Lending by Dealers, September 16–17, 2019**







[FIGURE id=vol5_iss4_1_f17 type=figure page=21 label="Exhibit 17" file=exhibit_17.png caption=""]
![Exhibit 17](assets/vol5_iss4_1/exhibit_17.png)



[FIGURE id=vol5_iss4_1_f18 type=figure page=21 label="Exhibit 18" file=exhibit_18.png caption=""]
![Exhibit 18](assets/vol5_iss4_1/exhibit_18.png)


Notes: These figures show the cumulative level of DVP net lending by dealers on September 16 and 17 in 30minute increments relative to the same 30-minute increment on an average day in the previous week for domestic, bank-affiliated dealers, and nonbank dealers in billions of US dollars. 

_Sources: OFR Cleared Repo Collection; authors’ calculations._ 

On the morning of the 16th, domestic bank-affiliated dealers increased net lending. But by 9am, they had ceased to lend more, and net lending stayed flat even as rates began to rise at about noon, which should have provided an additional incentive to lend. On the other hand, nonbank dealers (which are not required to hold reserves) did not lend more in response to the higher rates and instead borrowed an additional $10 billion. 

Why did bank-affiliated dealers not increase their lending after noon, despite higher rates? One possible explanation is dealers’ preference for avoiding daylight overdraft fees that would have come if dealers had borrowed elsewhere to lend into the repo market. However, an alternative explanation is that these bank-affiliated dealers may have reached their minimum comfortable level of reserves. The intraday pattern of dealers’ lending on the 17th 


suggests that this second explanation is more likely. As on the day before, on the 17th, bankaffiliated dealers began increasing lending in the morning by $20 billion over the usual levels but stopped lending for a short period. It was only after the Fed provided additional liquidity at 9:30am that they increased their lending by a further $10 billion. These results are consistent with the possibility that some key lenders had reached their minimum comfortable level of reserves by the time the Fed intervened. 

For further supportive evidence of the effects of the Fed’s intervention, Figure 14 examines the relationship between the amount lent by dealers from 9:30am to 10am in DVP and the amount borrowed from the Fed’s repo facility at 9:55am. We observe that for every dollar borrowed from the Fed, a substantial share was passed through to DVP. That helps to explain the cross-sectional increase in lending on the 17th between 9:30am and 10am. In other words, the Fed’s action appears to have rapidly eased reserve pressure on these bankdealers, enabling them to lend more in DVP. Owing to the tight nature of the window around the announcement we employ, and our focus on the introduction of this facility, this table provides the best identified evidence to date on the effect of the Federal Reserve’s repo operation on the repo market, and shows this facility was effective in increasing lending by dealers. 

[FIGURE id=vol5_iss4_1_f19 type=figure page=22 label="Figure 14" file=figure_14.png caption="Regression of Repo Lending by MMFs on Change in MMF Assets, Sept. 17, 2019"]
### **Figure 14: Regression of Repo Lending by MMFs on Change in MMF Assets, Sept. 17, 2019**

|**Dependent Variable**|**Change in Repo Lending (9:30–10am)**|
|---|---|
|**Borrowing from Fed (9:55am)**||
|Coefficient|0.465|
|_t_-statistic|(2.86)|
|**R-squared**|0.546|
|**Adjusted R-squared**|0.356|
|**Observations**|14|



Notes: This table shows the relationship between the amount lent by dealers from 9:30am to 10am on September 17, 2019, in DVP and the amount borrowed from the Fed’s repo facility at 9:55am. The _t_ -statistic for the test of the null hypothesis that the coefficient is equal to zero is in parentheses, and strongly rejects the null. 

_Sources: FRBNY Historical Repo Transaction Data; OFR Cleared Repo Collection; authors’ calculations._ 

Nonetheless, as Figure 12 shows, maximum rates continued to be extremely elevated in some segments of the market on September 17 and 18, after the Fed’s intervention. This finding suggests that the effective loosening of constraints on bank-affiliated dealers was not sufficient to eliminate spikes for several days and that other factors were at work in addition to reserve scarcity. 


## **V. Market Segmentation and Opacity** 

Let us return to the pattern of rates that evolved over the period from September 16 to September 18 in the tri-party and DVP segments of the market. Figure 15 shows average rates across three different segments of the repo market: (1) the tri-party market, which is a non-centrally cleared market mostly comprising banks and MMFs lending to dealers; (2) the DVP interdealer-brokered market; and (3) the unbrokered DVP market, which is primarily sponsored repo where dealers borrow from MMFs or lend to levered entities such as hedge funds. 

[FIGURE id=vol5_iss4_1_f20 type=chart page=23 label="Figure 15" file=figure_15.png caption="Intraday Average Rates by Segment, September 16–18, 2019"]
### **Figure 15: Intraday Average Rates by Segment, September 16–18, 2019**
![Figure 15](assets/vol5_iss4_1/figure_15.png)


Notes: The horizontal line indicates the federal funds target rate. Rates are volume-weighted averages for 30minute increments. 

_Sources: FRB BONY Tri-Party Repo Collection; OFR Cleared Repo Collection; authors’ calculations._ 

One pattern that emerges in these figures is that unbrokered rates such as those paid by MMFs did not track interdealer rates throughout September 16th and 17th. A scarcity of reserves should, in principle, be reflected across different segments of the repo market as interest rates increase to draw funds in from available investors of cash. But on the afternoon of the 16th, when cash was scarce in the market and rates began to rise in DVP, MMFs were still receiving low returns for investing in repo, as shown by the relatively flat tri-party rates through the day. 

One explanation for this heterogeneity in response to rates is the lack of transparency between segments of the repo market. More specifically, the interdealer-brokered market takes place on transparent screens where prices are updated frequently. Meanwhile, MMFs may not have access to these screens but instead may often rely on dealers and other market participants to obtain information on the prevailing rate. As a result, for a period of several hours, communication between different parts of the market might have been somewhat opaque, leading to a temporary dispersion in rates and uncertainty about the root cause. 


MMFs’ lack of transparency into repo rates also helps to explain the behavior of rates on September 17. In the interdealer market, rates began to decline following the Federal Reserve’s introduction of the repo facility. However, rates in tri-party and sponsored lending markets remained high throughout the day and began falling only at about 3:30pm. Thus, MMFs were slow not only to learn about the tightness in the repo market on the 16th but also to react to the decrease in tightness on the 17th. Either MMFs did not know the decrease in tightness had occurred, or the early trade activity of MMFs came in advance of the Federal Reserve’s announced intervention, which made it too late to reduce the high rates in the interdealer segment. 

However, note that alternative market factors might explain for the persistently low rates on the 16th and high rates on the 17th in tri-party. As noted in Paddrik, Ramírez, and McCormick (2021), tri-party timestamps may not be reliable, as some money market funds and other large asset managers may allocate trades among their funds later in the day, then they agree to a given rate. Therefore tri-party rates may be stale. However, we find no evidence of similar problems with the cleared repo data, so the matched pattern of unbrokered rates with tri-party rates suggests that the lack of transparency is the more likely explanation. 

These disparities suggest that segmentation and lack of transparency between different parts of the market played an important role in repo rate changes on the 16th and 17th. Because most of the repo market activity takes place within the first two-hour window of the day, the speed with which information about prices can be disseminated can exacerbate the impact of sudden shifts in supply and demand. It is worth considering whether, if clear price signals had been transmitted more quickly to MMFs, the MMFs would have been able to lend more into repo and potentially decrease the impact of reserve scarcity. More generally, providing greater transparency into the repo market is also crucial to improving price discovery and liquidity and preventing future repo spikes. 

## **VI. Conclusion** 

This paper is the first to bring together intraday timing data on the tri-party and cleared segments of the repo market for the purpose of studying the causes of the unusually large interest rate spike in repo markets in September 2019. We conclude that, in large part, the spike resulted from a confluence of factors—large Treasury issuances, corporate tax deadlines, and an overall lower level of reserves—that, when taken individually, would not have been nearly as disruptive. In addition, we highlight how a lack of information transmission across repo segments and internal frictions within banks most likely exacerbated the spike. These findings are instructive in the context of repo market liquidity, demonstrating how the segmented structure of the market can contribute to its fragility. 


## **VII. References** 

Adrian, Tobias, Brian Begalle, Adam Copeland, and Antoine Martin. 2014. “Repo and Securities Lending.” In _Risk Topography: Systemic Risk and Macro Modeling_ , edited by Markus Brunnermeier and Arvind Krishnamurthy, 131–48. Chicago: University of Chicago Press. https://www.nber.org/system/files/chapters/c12515/c12515.pdf 

Afonso, Gara, Marco Cipriani, Adam Copeland, Anna Kovner, Gabriele La Spada, and Antoine Martin. 2021. “The Market Events of Mid-September 2019.” Federal Reserve Bank of New York, _Economic Policy Review_ 27, no. 2: 1–24. https://www.newyorkfed.org/medialibrary/media/research/epr/2021/epr_2021_market -events_afonso.pdf 

Anbil, Sriya, Alyssa G. Anderson, and Zeynep Senyuz. 2020. “What Happened in Money Markets in September 2019?” Board of Governors of the Federal Reserve System, _Finance and Economics Discussion Series (FEDS) Notes,_ February 27, 2020. 

https://www.federalreserve.gov/econres/notes/feds-notes/what-happened-in-moneymarkets-in-september-2019-20200227.html 

———. 2021. “Are Repo Markets Fragile? Evidence from September 2019.” Board of Governors of the Federal Reserve System, _Finance and Economics Discussion Series (FEDS),_ August 16, 2021. 

https://www.federalreserve.gov/econres/feds/are-repo-markets-fragile-evidence-fromseptember-2019.htm 

Anderson, Alyssa G., and Jeffrey W. Huther. 2016. “Modelling Overnight RRP Participation.” Board of Governors of the Federal Reserve System, _Finance and Economics Discussion Series (FEDS),_ February 16, 2016. 

https://www.federalreserve.gov/econres/feds/modelling-overnight-rrp-participation.htm 

Andolfatto, David, and Jane E. Ihrig. 2019. “Why the Fed Should Create a Standing Repo Facility.” _Federal Reserve Bank of St. Louis on the Economy Blog,_ March 6, 2019. https://www.stlouisfed.org/on-the-economy/2019/march/why-fed-create-standing-repofacility 

Avalos, Fernando, Torsten Ehlers, and Egemen Eren. 2019. “September Stress in Dollar Repo Markets: Passing or Structural?” _BIS Quarterly Review_ (December): 12–14. https://www.bis.org/publ/qtrpdf/r_qt1912v.htm 

Baklanova, Viktoria, Adam Copeland, and Rebecca McCaughrin. 2015. “Reference Guide to U.S. Repo and Securities Lending Markets.” Federal Reserve Bank of New York Staff Report No. 740, September 2015. 

https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr740.pdf 


Barth, Daniel, and R. Jay Kahn. 2021. “Hedge Funds and the Treasury Cash-Futures Disconnect.” US Department of the Treasury, Office of Financial Research Working Paper No. 21-01, April 2021. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3817544 

Clark, Kevin, Adam Copeland, R. Jay Kahn, Antoine Martin, Mark E. Paddrik, and Benjamin Taylor. 2021. “Intraday Timing of General Collateral Repo Markets.” Federal Reserve Bank of New York, _Liberty Street Economics,_ July 14, 2021. 

https://libertystreeteconomics.newyorkfed.org/2021/07/intraday-timing-of-generalcollateral-repo-markets/ 

Consumer Financial Protection Bureau. 2021. Facilitating the LIBOR Transition (Regulation Z). December 7, 2021 (codified at 12 C.F.R. \S 1026). https://www.federalregister.gov/documents/2021/12/08/2021-25825/facilitating-thelibor-transition-regulation-z 

Copeland, Adam, Darrell Duffie, and Yilin Yang. 2021. “Reserves Were Not So Ample after All.” NBER Working Paper No. 29090 _,_ July 2021. 

https://www.nber.org/system/files/working_papers/w29090/w29090.pdf 

Correa, Ricardo, Wenxin Du, and Gordon Liao. 2020. “U.S. Banks and Global Liquidity.” Board of Governors of the Federal Reserve System, International Finance Discussion Paper No. 1289 _,_ July 2020. https://www.federalreserve.gov/econres/ifdp/u-s-banks-and-global-liquidity.htm 

D’Amico, Stefania, and N. Aaron Pancost. 2021. “Special Repo Rates and the Cross-Section of Bond Prices: The Role of the Special Collateral Risk Premium.” _Review of Finance_ 26, no. 1: 117–62. 

https://doi.org/10.1093/rof/rfab028 

d’Avernas, Adrien, Baiyang Han and Quentin Vandeweyer. 2023. “Intraday Liquidity and Money Market Dislocations.” University of Chicago, Working Paper, July 2023. https://www.adriendavernas.com/papers/repomadness.pdf 

Domm, Patti. 2019. “The Fed’s Fix of the Crucial Repo Lending Market for Banks Will Be Put to the Test on Monday.” CNBC, September 27, 2019. 

https://www.cnbc.com/2019/09/27/fed-fix-of-repo-market-to-be-put-to-test-monday-asthird-quarter-ends.html 

Han, Song, Kleopatra Nikolaou, and Manjola Tase. 2022. “Trading Relationships in Secured Markets: Evidence from Triparty Repos.” _Journal of Banking & Finance_ 139 (June): 1–12. https://doi.org/10.1016/j.jbankfin.2022.106486 

Hempel, Samuel J., and R. Jay Kahn. 2021. “Negative Rates in Bilateral Repo Markets.” US Department of the Treasury, Office of Financial Research Brief No. 21-03, September 2021 _._ . https://www.financialresearch.gov/briefs/files/OFRBr_2103_Negative_Rates_In_Bilateral_Repo_Markets.pdf 


Kahn, R. Jay, and Luke M. Olson. 2021. “Who Participates in Cleared Repo?” US Department of the Treasury, Office of Financial Research Brief No. 21-01 _,_ July 2021. https://www.financialresearch.gov/briefs/files/OFRBr_21-01_Repo.pdf 

Kaminska, Izabella. 2019. “Lookout, There’s a Dollar Crunch!” _FT Alphaville_ , September 17, 2019. 

https://www.ft.com/content/3a266602-1989-3b2e-8bab-eca00d39ae5f 

Paddrik, Mark E., Carlos A. Ramírez, and Matthew J. McCormick. 2021. “The Dynamics of the U.S. Overnight Triparty Repo Market.” Board of Governors of the Federal Reserve System, _Finance and Economics Discussion Series (FEDS) Notes_ , August 2, 2021. https://doi.org/10.17016/2380-7172.2948 

Smith, Robert Mackenzie. 2019. “All Clear? Structural Shifts Add to Repo Madness.” _Risk.net_ , November 5, 2019. 

https://www.risk.net/investing/markets/7133276/all-clear-structural-shifts-add-to-repomadness 

Tran, Hung. 2020. “EM Banks Exposed to Stress in FX Swaps, a Spillover from US Repo Markets.” _Financial Times,_ January 9, 2020. 

https://www.ft.com/content/5f8237cf-0e90-4f7d-9a0d-e4430f6fc7a1 

Yang, Yilin (David). 2020. “What Quantity of Reserves is Sufficient?” City University of Hong Kong, Working Paper, August 20, 2020. https://doi.org/10.2139/ssrn.3721785 

This open access article is distributed under the terms of the CC-BY-NC-ND 4.0 license, which allows sharing of this work provided the original author and source are cited. The work may not be changed or used commercially.
