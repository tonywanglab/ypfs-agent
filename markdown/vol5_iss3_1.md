## **Zombification and Central Bank Risk-Taking: The Lender of Last Resort as a Signal Extraction Problem** 

_Ulrich Bindseil, Juliusz Jabłecki_[1, 2] 

## **Abstract** 

In the liquidity crises since 2008, central banks have extended the ability of banks to take recourse to central bank credit operations through changes of the collateral framework. Remarkably, in March 2020, the European Central Bank (ECB) even lowered haircuts across a broad range of assets, and the Federal Reserve in March 2023 established a credit facility with securities accepted at par (without any haircut). Although such measures aim at stabilizing the banking system, some observers have warned that they would increase central bank risk exposure, encourage moral hazard, and ultimately lead to inefficiencies, as wasteful enterprises and “zombie” firms are kept afloat. We provide a simple four-sector model of the economy that illustrates the key trade-offs inherent in central banks’ responses to liquidity crises. Specifically, we derive central bank lender-of-last-resort (LOLR) policies as optimal from the perspective of a signal extraction problem, in which liquidity needs of banks toward the central bank are noisy signals of underlying firms’ performance. LOLR policies thus need to balance costs of default of illiquid but viable firms against the costs of letting unproductive zombie firms continue to operate. We explain why in a financial crisis, in which liquidity shocks become more erratic, central banks allow for greater potential recourse of banks to central bank credit. The model also shows the endogeneity of counterparty and issuer risks to the central bank’s collateral and related risk-control framework. Finally, the model allows identifying the circumstances under which the counterintuitive case arises in which a relaxation of the central bank collateral policy may reduce its expected losses while also supporting growth. 

**Keywords:** central bank, collateral policy, economic growth, LOLR, risk-taking, zombification 

## **JEL Classifications:** E58, G32 

> 1 Ulrich Bindseil: DG, Market Infrastructure and Payments, and DG, Market Operations, European Central Bank, email: ulrich.bindseil@ecb.europa.eu; Juliusz Jabłecki: Financial Risk Management Dept., National Bank of Poland, and Faculty of Economic Sciences, University of Warsaw, email: juliusz.jablecki@nbp.pl. 

> 2 We would like to thank Benoît Cœuré and Benjamin Sahel, as well as colleagues from the Risk Management Office at the ECB, in particular Carlos Bernadell, Alessandro Calza, Fabian Eser, Fernando Gonzalez, Thomas Kostka, Andrés Manzanares, Fernando Monar, and Stephan Sauer, for useful comments. Our thanks also go to participants of the ECB seminar on Dec. 7, 2012, in particular: Philippine Cour-Thimann, Diego Palenzuela, Philippe de Rougemont, Edgar Vogel, and Bernhard Winkler, as well as participants of the Fields Quantitative Finance Seminar on Feb. 27, 2013, organized by the Fields Institute, Toronto. Finally, we are grateful to the editors of the ECB Working Paper Series and an anonymous referee for useful comments. All remaining mistakes are ours. The views in this paper do not necessarily reflect the views of the respective central banks. 


## **1. Introduction** 

When describing the early experiences of the Bank of England with containing financial crises, Walter Bagehot (1873) lays the foundations for the modern view of the central bank as lender of last resort (LOLR). He argues that at times of panic, the central bank should lend “freely and vigorously to the public” and believes this policy to be consistent with the safety of the central bank. Bagehot seems to have been well aware of the higher ex ante risk-taking associated with enhanced liquidity provision in a crisis—which he calls the “brave plan”— but argues that it is the only “safe plan,” necessary to safeguard financial stability but also minimize the central bank’s ex post losses that would materialize as a result of a financial meltdown. In recent decades, central banks have operationalized the Bagehot approach through changes of collateral frameworks intended to extend commercial banks’ access to liquidity facilities. We recall briefly four episodes in which central banks reacted in recent financial crises with a supportive adjustment of their collateral framework: 

- **Lehman Brothers crisis:** As summarized by the Bank for International Settlements (BIS) Markets Committee (2013, 8–9), major central banks decided in Q3/Q4 2008 to allow the temporary acceptance of additional types of collateral, a temporary lowering of the minimum rating requirements of existing eligible collateral or a temporary relaxation of haircut standards.” 

- **European sovereign debt crisis:** In December 2011, the European Central Bank (ECB) decided to “increase collateral availability by (i) reducing the rating threshold for certain asset-backed securities (ABS) and (ii) accept[ing] as collateral additional performing . . . bank loans . . . that satisfy specific eligibility criteria” (ECB 2011). 

- **Covid-19:** In April 2020, the ECB “Governing Council decided to temporarily increase its risk tolerance level in credit operations through a general reduction of collateral valuation haircuts by a fixed factor of 20%,” such as to “support the provision of credit via its refinancing operations” (ECB 2020). 

- **Silicon Valley Bank (SVB) and Credit Suisse bank runs:** In March 2023, the Federal Reserve Board announced a “new Bank Term Funding Program (BTFP), offering loans of up to one year in length to . . . eligible depository institutions pledging U.S. Treasuries, agency debt and mortgage-backed securities, and other qualifying assets as collateral. These assets will be valued at par. The BTFP will be an additional source of liquidity against high-quality securities, eliminating an institution’s need to quickly sell those securities in times of stress” (Fed 2023). The Swiss National Bank [SNB] announced on March 19, 2023, in the context of the takeover of Credit Suisse by UBS, “a liquidity assistance loan of up to CHF 100 billion backed by a federal default guarantee . . . By providing substantial liquidity assistance, the SNB is fulfilling its mandate to contribute to the stability of the financial system” (SNB 2023). 

The March 2023 events show that the bank run problem has not been suppressed by the intensified regulatory and supervisory scrutiny deployed after the Global Financial Crisis of 2007–09. Quite the contrary; the speed of the runs on both banks suggest that the problem 


has grown with the ability of depositors to move large volumes of money electronically. As noted by Citigroup Chief Executive Officer Jane Fraser, “mobile apps and consumers’ ability to move millions of dollars with a few clicks of a button mark a sea change for how bankers manage and regulators respond to the risk of bank runs. . . . It’s a complete game changer from what we’ve seen before. . . . There were a couple of Tweets and then this thing went down much faster than has happened in history” (Surane 2023). Deposit outflows from Credit Suisse would have topped 10 billion Swiss Francs (CHF) per day before its merger with Credit Suisse (Noonan et al. 2023), a magnitude of deposit outflows never experienced before. The speed of deposit outflows for both SVB and Credit Suisse was also striking, as both banks were not considered to be close to insolvency but would have appeared to still have relatively solid capital buffers. 

Although the goal of these measures was to stem market malfunctioning (and to protect the flow of credit to the real economy), they may raise concerns about risks accumulating in central banks’ balance sheets, bailing out failing enterprises and banks (cf. “zombification”; Caballero, Hoshi, and Kashyap 2008; Laeven et al. 2020) as well as promoting moral hazard. 

Against such background, in this paper, we propose a simple model that can serve as a framework for analyzing the above trade-offs, integrating the issue of central bank lenderof-last-resort policies, financial risk management, and economic growth. The model is based on a comprehensive system of financial accounts, which makes it intuitive and ensures that all key financial flows are properly reflected. The model is driven by depositors who receive noisy signals on the quality of banks’ assets and may decide to withdraw funding on that basis. In contrast, the central bank is assumed to have no particular information on corporates’ economic performance and the quality of loan portfolios—since in a world of incomplete information, there is no way for the central bank to perfectly assess the healthiness of firms with funding stress—at least not in real time. This challenge is also highlighted in CGFS (2017, sec. 5): 

Assessing the solvency of a financial firm with certainty is a complex task even in the best circumstances, due to balance sheet opacity and leverage. It becomes particularly challenging in the situations surrounding the decision to grant [liquidity assistance] not least because of time pressure. . . . 

The key difficulty in assessing solvency is to distinguish insolvent from merely illiquid firms in real time. In some cases, illiquidity is the first step down a path that leads to insolvency. In other cases, solvency may itself depend on whether liquidity assistance is available and the terms on which it is offered. The assessment of solvency therefore always entails a degree of uncertainty, which can be even greater in times of stress. Hence the provider of liquidity assistance is exposed to some credit risk and may have to consider the prospect of the recipient institution failing before it exits liquidity assistance. 

Faced with this constraint, central banks must do the best in front of a signal extraction problem in which liquidity needs of banks toward the central bank are noisy signals of underlying firms’ performance. 


Central banks thus need to provide liquidity to banks in a way that minimizes the expected costs of two possible errors: (i) letting a fundamentally sound bank default due to illiquidity; (ii) keeping up zombies, that is, preventing defaults of unsound banks that can be expected to generate future losses and thereby harm economic growth if not wound down. The one model parameter of the central bank to achieve the optimum response to the signal extraction problem is the haircut it imposes on collateral accepted in its credit operations.[3] 

The model shows that economic growth (defined as the change in the value of the stock of real assets) and central bank expected losses can be non-monotonic functions of haircuts. This means that, depending on economic circumstances, increasing haircuts can either increase or decrease central bank risk-taking, and either promote or hamper growth, with the two potential outcomes not necessarily aligned. One counterintuitive result is that in stressed market conditions, characterized, for example, by high costs of default and low correlation of liquidity shocks with fundamentals, central bank risk-taking can increase with the level of haircuts. Hence, paradoxically, extending the collateral framework may under some circumstances be perfectly consistent with protecting the central bank’s balance sheet, as suggested by Bagehot (1873) when arguing that the “brave plan” of the Bank of England is the “safe plan.”[4] This reasoning is a specific consequence of a more general insight that financial sector risk tends to be endogenous with respect to central bank’s emergency liquidity assistance (ELA). To the extent that the central bank’s emergency liquidity operations manage to overcome the negative feedback loops characteristic of systemic financial turmoil, these actions should then also potentially reduce the central bank’s longterm risk exposure and associated losses. 

Although there is a burgeoning literature on central bank financial crisis management, it has so far focused mainly on providing rigorous rationale for the LOLR function, but without incorporating explicitly central bank risk management and zombification concerns (Diamond and Dybvig 1983; Goodhart 1999; as well as Freixas et al. 2000 and Freixas, Rochet, and Parigi 2004). Our contribution lies primarily in integrating these two traditionally distinct strands, but we also propose a number of modeling innovations relative to previous approaches. 

First, unlike Freixas, Rochet, and Parigi (2004), we assume more realistically that liquidity and solvency shocks are correlated, and we explicitly model central bank risk-taking as a major concern that may be relevant for the decisions taken by the central bank and for economic performance, while earlier papers do not consider this aspect. Freixas, Rochet, and Parigi (2004) and others also focus mainly on the pricing of emergency central bank credit as a means to discourage moral hazard, while in our view, in the case of a liquidity crisis, the availability of credit (not its price) is the overriding issue, and therefore, constraining central 

> 3 The bank run model of Bindseil and Lanari (2022) also explicitly models the role of the LOLR as specified by the central bank collateral framework and explains why a sudden unanticipated reduction of asset liquidity, or a tightening of the collateral framework, can trigger a bank run. 

> 4 CGFS (2017, sec. 6) seems to assume that a more restrictive collateral framework generally reduces the risktaking of the central bank: “The central bank can significantly reduce the financial risk it incurs in the course of liquidity assistance provision by restricting collateral to assets that can be easily valued, and/or can be relatively easily disposed of, and also by applying haircuts and concentration limits.” 


bank lending to the right extent seems to be the more relevant parameter to address moral hazard. Similar as in Ashcraft, Gârleanu, and Pederson (2010), haircuts also affect economic growth in our model, but in a very different way: nonoptimal central bank haircuts reduce expected economic growth, as they will lead to either an excessive number of defaults (if haircuts are too high) or an excessive survival rate of firms with poor performance (if haircuts are too low). In contrast, in the model of Ashcraft, Gârleanu, and Pederson, lowering central bank haircuts always means a more accommodating monetary policy and hence, at least temporarily, a positive impulse on growth. We also go beyond Chapman, Chiu, and Molico (2011) by stressing that central bank’s risk management is different from that of granular players not only because it may “affect portfolio choices of other agents” but because for the central bank, unlike for other agents, loosening the collateral framework might be fully consistent with protecting the balance sheet. Brunnermeier and Krishnamurthy (2020), like our paper, elaborates on the trade-offs to be considered in crafting public credit support programs between the social costs of firm default vs. those of unduly delaying defaults (that is, allowing for zombification, or the survival of firms with a debt overhang). One of the authors’ conclusions is that “policy should inject liquidity into small and medium sized firms that are liquidity constrained and for which social costs of bankruptcy are high.” However, they do not focus on the specific case of the central bank as LOLR, nor do they look at collateral haircuts as a key parameter in choosing the optimal point in the trade-off identified. 

The rest of this paper proceeds as follows. In Section 2 we review the particularities of central bank risk management and provide some recent and more distant historical illustration. Section 3 outlines our model and presents simulation results that demonstrate how one crucial central bank risk control parameter, namely haircuts on central bank collateral, influences both central bank risk-taking and economic performance in a way that depends on economic circumstances. Section 4 draws conclusions. 

## **2. Central Bank LOLR Policies: Risk Implications and Rationale** 

While Bagehot (1873) considers enhanced liquidity provision (“advance freely and vigorously to the public”) to be the only possibility to safeguard financial stability in a panic, he furthermore argues that such measures would be necessary to minimize the central bank’s eventual own financial risks: 

[M]aking no loans as we have seen will ruin it [Bank of England]; making large loans and stopping, as we have also seen, will ruin it. The only safe plan for the Bank [of England] is the brave plan, to lend in a panic on every kind of current security, or every sort on which money is ordinarily and usually lent. This policy may not save the Bank; but if it does not, nothing will save it. 

What Bagehot suggests is that, in specific cases, a tightening (loosening) of the collateral framework of the central bank could lead to an increase (decrease) of long-term expected central bank losses. Indeed, the aim of “loosening” measures should be to contribute to avoid 


worst-case scenarios by restoring confidence in a panic with negative feedback loops and multiple equilibria. If the funding stress of banks, together with negative macroeconomic factors, leads to a continued credit crunch and economic downward spiral, solvency deteriorates over time and probabilities of default increase, such as to also increase expected losses of the central bank. If restoring confidence through a more forthcoming collateral and risk control framework allows a central bank to prevent such a development from materializing, it could well be that it reduces expected financial losses to that central bank (apart from all other positive social welfare aspects of such measures). 

As a starting point, one would expect that extended liquidity provision by central banks during a crisis comes at the cost of larger potential risks compared with normal times. The increase in financial risk is driven by three main factors. 

- First, **probabilities of default of central bank counterparties and issuers of debt instruments used as collateral tend to increase during a crisis.** For example, Standard and Poor’s (2023) shows that default frequencies for banks and nonbanks, across all rating categories, fluctuate significantly through the financial cycles. Moreover, correlation risks between central bank counterparties and collateral credit quality increase during a financial crisis because common risk factors (instead of idiosyncratic ones) become predominant. Therefore, the likelihood of the worst-case scenario for repurchase agreement (repo) operations, that of a simultaneous default of both the counterparty and the collateral issuer, increases significantly in a financial crisis. 

- Second, **central bank lending shifts toward stressed counterparties.** During financial crises, stressed banks lose market access and experience funding gaps, which are often addressed through increased recourse to central bank credit, while stronger banks hoard funds with the central bank. Hence, central bank lending becomes more concentrated on weaker counterparties, which implies that the asset side of its balance sheet becomes, on average, more risky and moreover less diversified. 

- Third, the **central bank’s balance sheet may also lengthen due to a flight of households out of bank deposits into banknotes** (as happened in the US and many other countries in the 1930s and more recently during the COVID-19 pandemic) **or a flight of other parties with access to the central bank balance sheet into higher central bank deposits** (for example, foreign central banks and sovereign wealth funds shifting deposits from commercial banks into the central banks issuing reserve currencies). 

The question now arises as to why exactly central banks should be ready to accept higher exposures and potential risks and not tighten their collateral frameworks. We distinguish four main reasons for the central bank to act as the lender of last resort in a financial crisis and to provide elastic credit. 

- **Risk endogeneity:** The availability of collateral to access central bank credit can determine whether banks have access to deposits and market funding. As shown by Bindseil and Lanari (2022), a supportive collateral framework can, in a given 


situation (say, after an exogenous shock that leads to an asset liquidity freeze), prevent bank runs from happening, and therefore allow banks to avoid taking recourse to central bank credit, while with a tighter collateral framework (in the same situation), the same banks can become subject to a depositor run, forcing them to take recourse to central bank credit and nevertheless eventually defaulting, requiring the central bank to liquidate the collateral and possibly facing losses.[5] Also, the model we outline in Section 3 takes up the idea of risk endogeneity, although in a simpler way, without an explicit modeling of the bank run/no-run equilibriums. In our model, the run, if any, is driven by noisy signals depositors receive, and if the information content of the signals is low, then liquidating illiquid banks that suffered a run and selling the collateral they posted can lead also to unnecessary central bank losses. 

- **Negative social externalities of funding liquidity stress and default due to illiquidity** include the following forms: (i) fire-sale spirals that liquidity problems of individual banks induce (Brunnermeier et al. 2009); (ii) the generalized drying up of funding and market liquidity in the financial system as a consequence of hoarding; and (iii) an eventual credit crunch that affects negatively the real economy and hence households. Central banks as public agents should care about negative externalities and should try to prevent them or address them for the sake of reducing deviations from the social optimum. Of course, this objective does not imply that there are no drawbacks of a too supportive liquidity provision, which may allow for the survival of underperforming, unproductive businesses. Such zombification, as a negative aspect of an overly supportive liquidity provision, is captured in the model we present. 

- **Central banks have been endowed with the monopoly and freedom to issue the legal tender, thus—unlike leveraged financial institutions—they are not threatened by illiquidity** in their own currency. It seems only natural that, in case of a liquidity crisis when all agents attach a high price to liquidity, the central bank remains more willing than others to hold (as collateral or outright) assets that are less liquid. Preventing costs of default in this sense through central bank liquidity does not invoke negative externalities, market failures, and the public nature of the central bank. In the model presented in Section 3, the cost of corporate default is one crucial parameter for the optimal degree of elasticity of central bank credit provision. The model also allows for positive effects of default—namely to stop corporates/banks with low performance from continuing to operate in view of the likely persistence in the future of their low performance (which may be viewed as a form of moral hazard). 

- **Ability to mitigate risk through haircuts: Haircuts are a powerful risk mitigation tool if credit risk is asymmetric and the cash investor (repo lender) is of very high credit standing.** The power of haircuts is limited if the cash taker and 

> 5 A practical recent example of this very logic can be found in Jordan (2023), justifying the exceptional liquidity assistance to Credit Suisse: “In granting ELA+, we are going to the limits of what is feasible for the SNB, because with this loan preferential rights in bankruptcy proceedings are the sole security. We provided this liquidity only because rapid action was critical to restoring counterparties’ confidence in Credit Suisse and stopping the outflow of client funds. Without the SNB’s willingness to provide further liquidity via ELA+, a global financial and economic crisis could easily have been set in motion.” 


cash lender are equally credit risky since although haircuts protect the buyer, they expose the seller to unsecured credit risk, which increases with the haircut level (Ewerhart and Tapking 2008). 

## **3. A Model of Central Bank Lending and Risk Management with Real Asset Value Shocks** 

This section provides a model to illustrate the impact that central bank collateral policy can have on economic growth and central bank risk-taking. Central bank collateral policies affect growth by, broadly speaking, minimizing the sum of the damage to growth as a result of zombification (allowing the survival of underperformers) and the damage due to illiquidityinduced defaults of high-growth, competitive companies (which are not saved by being granted a sufficient supply of central bank funding). The impact of collateral policies on central bank risk-taking is perhaps less clear-cut, as it is determined by the endogeneity of risks with respect to the central bank’s collateral policies themselves. By presenting a formal, yet simple, model of both effects, we develop rigorous arguments that can be useful in assessing the LOLR measures central bank introduce to manage liquidity crises but also support future policymaking. 

The model is motivated by the recognition that a financial crisis almost always originates from an asset value shock (Aliber and Kindleberger 2015). Performance problems do not lead directly to default, as it is assumed that they are discovered only with a time lag, reflecting the difficulties in valuing nonliquid assets and more generally the opaqueness of banks’ and nonbank firms’ balance sheets. However, liquidity problems are correlated with low quality of loan portfolios, as investors receive noisy signals on asset values and tend to withdraw funding on the basis of these signals. The model is cast in a system of financial accounts representing key economic sectors, that is, households, corporates, banks, and the central bank. The exposition is stylized, but it allows us to understand one key element of the central bank’s role in liquidity crises. 

## **3.1 Model Setup** 

At the outset, households are endowed with real assets of an amount _E_ (equal to their equity). They exchange parts of these real assets into corporate equity _P_ , bank equity _Q_ , banknotes _B_ , and bank deposits _D_ (assumed to be divided equally between Bank 1 and Bank 2). Corporates finance their projects by bank loans (equal to _D+B+Q_ ) and the equity endowment from households ( _P_ ). The financial sector, consisting of banks and the central bank, is the intermediary between households and corporates (apart from equity stakes in corporates). It offers deposits _D_ to households and invests them in loans offered to corporates. The banking sector also intermediates between the households and the central bank with respect to the issuance of banknotes _B_ . Banks use banknotes to purchase real assets from households, which they sell on to corporates that finance them through loans from the banks. Thus, total funding, and hence total assets held by banks, amounts to _B+D+Q_ . The resulting financial structure of the economy is presented in Figure 1. 


[FIGURE id=vol5_iss3_1_f1 type=diagram label="Figure 1" file=figure_1.png caption="Financial Accounts in the Model"]
### **Figure 1: Financial Accounts in the Model**

|**inancial Accounts in the Model**|**inancial Accounts in the Model**|**inancial Accounts in the Model**|**inancial Accounts in the Model**|
|---|---|---|---|
|||||
|Households/Investors||||
|Assets||Liabilities||
|Real assets|𝐸−𝐷−𝐵−𝑄−𝑃|Equity|𝐸|
|Deposits Bank 1|𝐷/2|||
|Deposits Bank 2|𝐷/2|||
|Bank equity|𝑄|||
|Corporate equity|𝑃|||
|Banknotes|𝐵|||



|Corporate 1|Corporate 1|Corporate 1|Corporate 1|Corporate 1|
|---|---|---|---|---|
|Assets|||Liabilities||
|Real assets||(𝐷+ 𝐵+ 𝑃+ 𝑄)/2|Loans from Bank 1|(𝐷+ 𝐵+ 𝑄)/2|
||||Equity|𝑃/2|
||||||
|||Corporate 2|||
|Assets|||Liabilities||
|Real assets||(𝐷+ 𝐵+ 𝑃+ 𝑄)/2|Loans from Bank 2|(𝐷+ 𝐵+ 𝑄)/2|
||||Equity|𝑃/2|
||||||
|||Bank 1|||
|Assets|||Liabilities||
|Loans to Corporate 1||(𝐷+ 𝐵+ 𝑄)/2|Households’ deposits|𝐷/2|
||||Central bank borrowing|𝐵/2|
||||Equity|𝑄/2|
||||||
|||Bank 2|||
|Assets|||Liabilities||
|Loans to Corporate 2||(_D_+_B_+_Q_)/2|Households’ deposits|_D_/2|
||||Central bank borrowing|_B_/2|
||||Equity|_Q_/2|
||||||
|||Central bank|||
|Assets|||Liabilities||
|Credit operations|𝐵||Banknotes|𝐵|



_Source: Authors’ calculations._ 


In the model, bank defaults are assumed to trigger corporate defaults (as corporates are unable to roll over credit, while other banks cannot take over quickly enough because they cannot easily assess the quality and solvency of the enterprise). In turn, corporate defaults entail management changes, liquidation of assets (possibly at distressed prices), changes to the assets needed to make them fit into new companies (implying losses of asset value relating to asset specificity; see Williamson 1985), a period of legal uncertainty and associated inertia, etc. Hence, corporate defaults have real costs (see, for example, Davydenko, Strebulaev, and Zhao 2012 for empirical estimates of the costs of default events). 

The model intends to describe the situation of a financial crisis in which: (i) the relevant interbank markets have broken down and (ii) capital market access and deposit flows are uncertain and volatile. This constraint means that banks can offset liquidity shortfalls only through recourse to central bank credit. The central bank’s elastic liquidity provision can thus prevent defaults of illiquid institutions, which can promote growth if it ensures uninterrupted operation of sound business projects. However, depositors may have withdrawn funding from banks for good reasons, as they receive (noisy) signals on bank/corporate asset values. In that case, preventing illiquidity through central bank credit contributes to zombification, that is, the preservation of fundamentally unsound projects, which reduces the value of productive assets in the economy and hence depresses growth. In view of this potential outcome, the better option may sometimes be to discontinue a project through default, go through the one-off cost of reorganization, and then allow again for a more productive use of the freed-up resources. 

The central bank in the model is assumed to have no particular information on solvency of banks and corporates, that is, it does not receive even the noisy signals that investors pick up. This assumption deserves a comment. Clearly, the central bank does monitor the health of its counterparties, and often the central bank also acts as the supervisor of the banking system. However, in the midst of a financial crisis, it remains rather difficult for the central bank to perfectly assess, on a real-time basis, the asset quality of banks and nonbank firms (to which banks are exposed) with sudden funding stress. This is particularly true for complex global organizations such as Credit Suisse or when the economic fundamentals and the interest rate environments are subject to particular change, as in 2008 or around March 2023. 

Still, the central bank can aim at providing liquidity to banks in a way that achieves the optimum with regard to minimizing the expected costs of two possible errors: 

- Error 1: letting a fundamentally sound bank default due to illiquidity; and 

- Error 2: keeping up zombies, that is, preventing defaults of unsound banks that can be expected to generate future losses if not wound down. 

In the model, the parameter of the central bank to achieve the optimum balance between the two errors is the haircut imposed on collateral. The optimum haircut will depend in particular on the information content of liquidity shocks with regard to individual banks’ 


solvency/performance problems. If this information content is high, then more conservative haircuts should be optimal, compared to the case of low information content. 

We capture the issue of optimal central bank liquidity provision in a two-period model with the following sequence of events. 

## _Period 1_ 

1. Asset value shocks materialize, which are modeled as zero-mean random normal variables: 𝜂1 – shock affecting the assets held by Corporate 1; η2 – shock affecting the assets held by Corporate 2; the uncertainty around each shock 𝜂1,2 is modeled by their respective standard deviation, 𝜎𝜂1,2. 

2. Idiosyncratic liquidity shock materializes, defined as 𝑘= θ + β(η1 −η2), with θ a zeromean normal random variable and β a positive constant; 𝑘 represents the shift of deposits out of Bank 2 into Bank 1. This shift is assumed to be correlated with asset value shocks, reflecting the intuition that liquidity shocks can have information content on debtors’ economic performance and solvency. 

3. Funding liquidity shocks force banks to adjust their borrowing from the central bank (that is, Bank 1 adjusts its recourse to central bank credit by 𝑘, and Bank 2 by −𝑘). The banks predeposit all their assets with the central bank as collateral. Recourse to central bank credit cannot exceed available collateral after haircuts. The haircut level is ℎ, so that potential 1 borrowing from the central bank is limited to (1 −ℎ)(𝐵+ 𝐷+ 𝑄). 2 

4. A bank defaults if it hits its central bank collateral constraint. This result has two implications. First, the corporate defaults, as it depended on the bank for financing (a “credit crunch” occurs). This default is assumed to cause a damage to corporate asset value of 𝑥. On that basis, the values of the corporate liabilities can be established (assuming the juniority of equity relative to debt). Second, bankruptcy proceedings are initiated, and banks’ solvency is evaluated, whereby the value of remaining bank assets is divided among the creditors— the central bank and the households qua investors. First, the central bank liquidates its collateral (in fact, by assumption, all assets of the bank), and the remaining asset value is then divided pari passu between the central bank (as far as it still has claims after the liquidation of collateral) and the households. 

## _Period 2_ 

1. Banks and corporates that have not defaulted continue to exist, and the model assumes that the idiosyncratic real asset shock of Period 1 repeats itself precisely. This premise reflects the assumed persistence of economic performance of individual firms. Corporates that default are subject to a new draw of the idiosyncratic shock η̃1,2 . which reflects the fact that they have installed new management and been reorganized. 

2. Corporates’ economic performance and central bank losses are evaluated. Corporates’ economic performance is expressed in terms of the expected change in the stock of real 


assets in the economy over the two periods. Thus, it can be interpreted as economic growth, and we will henceforth use the two terms interchangeably. The change in the stock of real assets is defined as the sum of asset value shocks in Period 1, costs of default (if any), and asset value shocks in Period 2. The latter are equal to a new draw of asset value shocks (in case of default) or Period 1 shocks (in case no default occurred). Formally: 




where 𝕀𝑓𝑎𝑖𝑙,𝑖 is equal to 1 if default of Bank I occurs (𝑖=1,2) and 0 otherwise. 

Central bank losses arise from the cascading of asset value shocks and defaults through the respective balance sheets. In Section 3.2 we compare expected economic outcomes, 𝔼(Δ), with the riskiness of the central bank balance sheet (expressed as expected losses on the collateral portfolio) for a number of parameter sets representing various states of the financial system. Since the expected loss on an exposure is defined as the product of a counterparty’s probability of default (PD) and the loss given default, changes in the central bank’s expected losses will have a clear interpretation in terms of changes in counterparties’ PD levels, thus reflecting also risk endogeneity. In this setup, the objective of the central bank is to find the optimum level of haircuts that maximizes expected economic performance (or “economic growth,” the precise measure in the model being the growth of the value of the real asset stock of the economy) and minimizes central bank losses.[6] 

## **3.2 The Impact of Financial Sector Parameters on Optimal Haircuts** 

In this section, we consider a number of parameter sets that will illustrate some of the key results of our model. Figure 2 shows the parameterization of the various cases considered, whereby the remaining parameters are fixed at: 𝐸= 100, 𝐵= 20, 𝐷= 27, 𝑃= 2, 𝑄= 1, σθ = 1. 

> 6 Given the assumptions outlined above, the change in the value of the stock of real assets, 𝔼(Δ), can be expressed through a closed form formula and is driven by the relation between costs of default and the positive expected value of reoccurring asset value shocks. Moreover, 𝔼(Δ) can be shown to be both a monotonic and non-monotonic function of the haircut level ℎ, depending on the interplay of the various parameters describing the state of the financial system (for example, costs of default, volatilities of idiosyncratic and systemic liquidity and asset value shocks etc.). For details on these calculations, see the working paper version of this essay, Bindseil and Jabłecki (2013). 


[FIGURE id=vol5_iss3_1_f2 type=diagram label="Figure 2" file=figure_2.png caption="Model Specifications Considered"]
### **Figure 2: Model Specifications Considered**

||||||
|---|---|---|---|---|
|||Parameter Specifications|||
||**I**|**II**|**III**|**IV**|
|𝛔𝟐<br>𝛈𝟏,𝟐<br>Variance across companies’ performance|2|0/4/16|2|2|
|𝜷<br>Information content of liquidity shocks<br>with regard to companies’performance|1|1|0.1/0.2/1|1|
|𝒙<br>Cost of default|1|1|1|0/1/15/25|



_Source: Authors’ calculations._ 

We consider four specifications: baseline (I), varying volatility of asset value shocks (II), changing information content of liquidity shocks with respect to solvency shocks (III); and increasing cost of default (IV). Each specification features a number of sub-cases that allow us to analyze the relationship between the chosen collateral policy (as captured by the level of haircuts ℎ[7] ) and central bank risk-taking and economic performance in different environments. Since the central bank loss function is not available in closed form, we derive its distribution using a Monte Carlo simulation, focusing on three risk measures: the expected loss, the unexpected loss (standard deviation of the loss distribution), and the 99% value at risk (VaR; that is, the 99th percentile of the loss distribution).[8] 

We start with a baseline specification (I) featuring both key drivers of economic performance, namely firm-specific asset value shocks and costs of default (Figure 3). 

> 7 The upper bound for haircut levels has to be such that banks can at least finance their structural liquidity deficit, stemming from society’s demand for banknotes, that is, such that 𝐵< (𝐵+ 𝐷+ 𝑄)(1 −ℎ). 

> 8 Since all risk curves have similar shapes, for ease of presentation, the remaining specifications feature only the expected loss. 


[FIGURE id=vol5_iss3_1_f3 type=figure label="Figure 3" file=figure_3.png caption="Economic Performance and Central Bank Risk-Taking in the Baseline Specification"]
### **Figure 3: Economic Performance and Central Bank Risk-Taking in the Baseline Specification**
![Figure 3](assets/vol5_iss3_1/figure_3.png)




_Source: Authors’ calculations._ 

Consider first the shape of the economic performance function (left-hand panel). Initially— under the most liberal haircut framework—the economy stagnates, as low haircuts and the associated overly supportive liquidity provision contributes to zombification. Increasing haircuts allows the sifting out of underperforming businesses, which fuels growth. However, as default frequency increases, costs of default kick in and begin to weigh on the values of productive assets. Ultimately, this generates a hump-shaped curve with a local maximum for ℎ= 0.48. The number itself has no direct interpretation, given that the model is not calibrated, but it illustrates that in normal times (baseline scenario) a fairly conservative collateral policy may be necessary to prevent zombification and support economic growth. Turning to the central bank, Figure 3 (right-hand panel) shows that all risk measures decrease monotonically with the degree of restrictiveness of the haircut policy, and as a result, the risk management problem of the central bank is dominated by elements similar to those applicable to any commercial bank with little systemic impact. Consequently, by ℎ= 0.48, the balance sheet of the central bank is already fully protected, as all risk measures approach zero. We will see that such alignment of central bank’s risk management actions with economic performance is not universally true. 

To verify the robustness of the baseline specification (I), we now investigate what happens to economic performance and central bank losses when the variance of idiosyncratic asset 


value shocks first drops to zero and subsequently rises to 16 (Figure 4). Once again, these numbers are not calibrated and are simply meant to describe in model terms a situation in which: (i) deposit shift shock is completely random, with no relation to the soundness of either bank’s loan portfolio which in any way remains constant (η1 = η2 = 0); and (ii) there is considerable uncertainty regarding banks’ loan portfolios, which is reflected in interbank deposit flows (σ[2] η1[= σ][2] η2[= 16][).  ] 

[FIGURE id=vol5_iss3_1_f4 type=figure label="Figure 4" file=figure_4.png caption="Specification II—The Impact of Changing Volatility of Asset Value Shocks"]
### **Figure 4: Specification II—The Impact of Changing Volatility of Asset Value Shocks**
![Figure 4](assets/vol5_iss3_1/figure_4.png)




_Source: Authors’ calculations._ 

When there are no firm-specific asset value shocks, deposit outflows—which force banks to reach out to the central bank for funding—are purely “whimsical.” As a result, cutting off banks’ access to liquidity through higher haircuts will be economically wasteful, as reflected in the monotonically decreasing gray line in the left-hand panel of Figure 4. In contrast, with high volatility of asset value shocks, economic performance of corporates (and thus the quality of banks’ loan portfolios) may differ substantially, and so increasing haircuts—while keeping the cost of default constant—has the potential to filter out the productive, highgrowth companies. Thus, the economic performance curve for σ[2] η1[= σ][2] η2[= 16][ is ] consistently higher than in other cases. Turning to the central bank (Figure 4, right-hand panel), higher volatility of asset value shocks clearly produces higher expected losses, on account of both higher bank default probabilities and more prevalent higher adverse shocks to corporate assets (when ση1 = ση2 = 0, the central bank is not expected to suffer any losses). 


Specification III allows us to analyze the impact of information content of liquidity shocks on economic performance. Here, we see an effect similar to that observed when ση1 = ση2 = 0, namely the more “whimsical” deposit flows are (that is, the lower the β), the more wasteful it is in the model to limit banks’ access to liquidity through higher haircuts (Figure 5, lefthand panel). 

[FIGURE id=vol5_iss3_1_f5 type=figure label="Figure 5" file=figure_5.png caption="Specification III—Varying Information Content of Liquidity Shocks"]
### **Figure 5: Specification III—Varying Information Content of Liquidity Shocks**
![Figure 5](assets/vol5_iss3_1/figure_5.png)




_Source: Authors’ calculations._ 

Interestingly, the central bank’s expected loss curve is largely unaffected in this case (Figure 5, right-hand panel). This is because the key loss driver—that is, volatility of asset value shocks—remains unchanged and the cost of default (𝑥= 1) can still be absorbed by corporate and bank equity. Thus, in this specification, the risk management conclusion is to keep the haircut unchanged, even though economic performance concerns (for example, for 𝛽= 0.1) suggest loosening the collateral framework. 

Finally, in Specification IV, we investigate the impact of the cost of default on both economic performance and central bank’s losses. We run the simulations for four different levels of the cost of default, which increases in steps from 0 to 1 (4% of asset value), to 15 (60% of asset value), and 25 (100% of asset value). 

For 𝑥= 0, 𝔼(Δ) is monotonically increasing and reaches the maximum for the highest haircut level consistent with accommodating ‘the structural need to supply liquidity to banks via 


central bank credit operations (Figure 6). Intuitively, more restrictive haircuts ensure that more unsound business projects can be filtered out and wound down with a net gain for the society. As 𝑥 increases, however, gains from killing loss-making businesses (zombies) are offset by the cost of restructuring, and the economic growth curve changes from hump shaped (𝑥= 1) to monotonically decreasing (𝑥= 15.25) as the negative externalities of default easily outweigh any positive effects of discontinuing wasteful projects. Overall, the greater the cost of default, the lower the optimal haircut from the point of view of economic performance. 

[FIGURE id=vol5_iss3_1_f6 type=figure label="Figure 6" file=figure_6.png caption="Specification IV—Varying Cost of Default"]
### **Figure 6: Specification IV—Varying Cost of Default**
![Figure 6](assets/vol5_iss3_1/figure_6.png)




_Source: Authors’ calculations._ 

Turning to the central bank, Figure 6 (right-hand panel) shows that when 𝑥= 0, expected losses decrease monotonically with the degree of restrictiveness of the haircut policy. Intuitively, the zero cost of default reflects the flexibility and resilience of the financial system, which can always reorganize without disruptions. Therefore, the system can cope even with a very conservative framework without being systemically destabilized. In such an environment, the central bank’s risk management problem can be likened to that of a “granular” commercial bank that strives for the highest haircut possible to effectively mitigate credit risk. However, when default-related asset value destruction is 60% or higher, the central bank’s expected loss curve changes from monotonically decreasing to “U” shaped, whereby expected losses fall as the central bank moves from a very liberal framework (ℎ= 0%) to a moderate one (ℎ= 30%– 40%) but pick up again beyond that point. As the cost of 


default increases to 25, in which case reorganization entails almost total destruction of corporate assets (for example, selling highly sophisticated machinery as metal junk), the losses expected in the most restrictive framework skyrocket. 

Intuitively, these results reflect the fact that when the economy is not flexible and resilient— as reflected, for example, by the high cost of default—the central bank can no longer be considered to have the same risk management problem as a granular market participant: the elasticity of its liquidity provision impacts the risk parameters of its counterparties with dramatic consequences for its balance sheet. Excessive risk protection can be self-defeating, as it increases default probabilities and expected default-related losses for the central bank. The policy conclusion is that, unlike in Specification I, when the cost of default needs to be factored into the analysis, a very restrictive haircut policy may neither be in the interest of society nor minimize central bank risk-taking. Instead, the optimal haircut level—that is, one that allows striking the right balance between letting a viable bank default for liquidity reasons and preventing the default of a bank that is misallocating resources—is a moderate one. 

## **4. Conclusions** 

A careful study of past episodes of liquidity crises and banking sector panics (such as following the default of Lehman Brothers, or more recently the cases of SVB and Credit Suisse) indicates that as much as central banks seem to be conscious of their role as lenders of last resort, their actions in such cases are sometimes perceived as controversial, risky, economically wasteful, and promoting moral hazard and zombification. In this paper, we revisit this controversy by analyzing the key trade-offs the central bank needs to consider in limiting the elasticity of its credit provision through collateral eligibility rules and haircuts. 

Specifically, we formalize the insight that central bank collateral policies affect economic growth by, broadly speaking, considering the LOLR as a need to respond practically to a signal extraction problem, namely minimizing the sum of the damage to growth resulting from allowing the survival of economic underperformers (zombies) and the damage due to illiquidity-induced defaults of high-growth, competitive companies (which are not saved from the consequences of a funding liquidity crisis by being granted sufficient supply of central bank funding). Our main conclusion is that both growth and central bank risk-taking can be non-monotonic functions of haircuts, and therefore be either upward or downward sloping for a specific decision to change haircuts. This finding means that, depending on economic and financial circumstances, increasing haircuts can either increase or decrease the stock of productive assets and thereby economic growth. More surprisingly, in stressed market conditions, characterized by high negative externalities of default—such as, for example, those after the collapse of Lehman Brothers and during severe dislocations in money and capital markets as at the outbreak of the COVID-19 pandemic—central bank losses can sometimes increase with the level of haircuts. Hence, we argue that, paradoxically, extending the collateral framework in central bank operations—as the Fed, the Eurosystem, and many other central banks have done during recent periods of market stress—can be 


perfectly consistent with prudent risk management. The merits of doing so increase with the costs of company defaults, whereby these costs are likely to be higher for very sophisticated economies in which the average asset specificity (in the sense of Williamson 1985) is high and if labor and other factor mobility is low (as in less flexible advanced economies subject to high regulation, such as some European Union jurisdictions). Central banks in such areas should pursue a more supportive LOLR policy than central banks in less advanced and more flexible jurisdictions. 

Our conclusion is consistent with the insight that financial sector risk is endogenous with respect to the central bank’s emergency liquidity support. For example, if the funding stress of banks, together with other macroeconomic factors, leads to a continued credit crunch and economic downward spiral affecting collateral values, counterparties’ solvency will deteriorate over time and default probabilities will increase, eventually increasing also the central bank’s financial risks. To the extent that the central bank’s emergency liquidity operations manage to overcome the negative feedback loops characteristic of a systemic financial turmoil, these actions should then also reduce the central bank’s long-term risk exposure. 

These considerations are illustrated formally using a simple model based on a comprehensive system of financial accounts, and capturing solvency, liquidity, and the interaction between the two. The model demonstrates that under parameter changes that are consistent with a financial crisis, that is, when costs of default increase and liquidity shocks become more erratic and carry less information on solvency, the central bank should increase the total post-haircut amount of collateral. 

Thus, over and above explaining central banks’ actions during the recent crises, our model can also be helpful in addressing the critiques of central banks’ extension of collateral frameworks. The first type of the critique, namely that LOLR policies are economically wasteful and promote zombification and moral hazard, is one-sided, as it ignores the fact that in the real world of incomplete information, there is no way for the central bank to perfectly assess in a financial crisis the healthiness of firms with funding stress. Therefore, the central bank faces a trade-off, and ignoring one side of this trade-off—letting fundamentally sound banks and corporates default due to illiquidity—will lead to wrong conclusions. The second type of the critique, namely that the policies of central banks aimed at broadening their collateral sets necessarily imply more risk-taking, overlooks the fact that risks are endogenous with respect to the policies of a highly systemic player like the central bank in times of financial crises. 


## **5. References** 

Aliber, Robert Z., and Charles P. Kindleberger. 2015. _Manias, Panics, and Crashes: A History of Financial Crises_ , 7th ed. Basingstoke: Palgrave Macmillan. 

Ashcraft, Adam, Nicolae Gârleanu, and Lasse H. Pedersen. 2010. “Two Monetary Tools: Interest Rates and Haircuts.” _NBER Macroeconomics Annual_ 25: 143–80. https://www.journals.uchicago.edu/doi/full/10.1086/657530 

Bagehot, Walter. 1873. _Lombard Street: A Description of the Money Market_ , 4th ed. London: Henry S. King & Co. 

Bank for International Settlements Markets Committee (BIS Markets Committee). 2013. “Central Bank Collateral Frameworks and Practices.” Report by a Study Group chaired by Guy Debelle and established by the BIS Markets Committee, March 2013. https://www.bis.org/publ/mktc06.pdf 

Bindseil, Ulrich, and Juliusz Jabłecki. 2013. “Central Bank Liquidity Provision, Risk-Taking and Economic Efficiency.” ECB Working Paper No. 1542, May 2013. www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1542.pdf 

Bindseil, Ulrich, and Edoardo Lanari. 2022. “Fire Sales, the LOLR, and Bank Runs with Continuous Asset Liquidity.” _Journal of Financial Crises_ 4, no. 4: 77–102. https://elischolar.library.yale.edu/journal-of-financial-crises/vol4/iss4/3/ 

Brunnermeier, Markus, Andrew Crockett, Charles A. Goodhart, Avinash D. Persaud, and Hyun Shin. 2009. _The Fundamental Principles of Financial Regulation_ . Geneva Reports on the World Economy No. 11. Geneva: ICMB, International Center for Monetary and Banking Studies. www.princeton.edu/~markus/research/papers/Geneva11.pdf 

Brunnermeier, Markus, and Arvind Krishnamurthy. 2020. “Corporate Debt Overhang and Credit Policy.” Brookings Papers on Economic Activity 2020, no. 2 (Summer): 447–88. https://www.brookings.edu/articles/corporate-debt-overhang-and-credit-policy/ 

Caballero, Ricardo J., Takeo Hoshi, and Anil K. Kashyap. 2008. “Zombie Lending and Depressed Restructuring in Japan.” _American Economic Review_ 98, no. 5: 1943–77. https://www.aeaweb.org/articles?id=10.1257/aer.98.5.1943 

Chapman, James T.E., Jonathan Chiu, and Miguel Molico. 2011. “Central Bank Haircut Policy.” Annals of Finance 7, no. 3: 319–48. 

https://link.springer.com/article/10.1007/s10436-010-0171-5 

Committee for the Global Financial System (CGFS). 2017. “Designing Frameworks for Central Bank Liquidity Assistance: Addressing New Challenges.” Bank for International Settlements, CGFS Paper No. 58, April 2017. 

https://www.bis.org/publ/cgfs58.htm 


Davydenko, Sergei A., Ilya A. Strebulaev, and Xiaofei Zhao. 2012. “A Market-Based Study of the Cost of Default.” _Review of Financial Studies_ 25, no. 10: 2959–99. https://doi.org/10.1093/rfs/hhs091 

Diamond, Douglas W., and Peter H. Dybvig. 1983. “Bank Runs, Deposit Insurance, and Liquidity.” _Journal of Political Economy_ 91, no. 3: 401–19. https://www.journals.uchicago.edu/doi/10.1086/261155 

European Central Bank (ECB). 2011. “ECB Announces Measures to Support Bank Lending and Money Market Activity.” Press release, December 8, 2011. https://www.ecb.europa.eu/press/pr/date/2011/html/pr111208_1.en.html 

———. 2020. “ECB Announces Package of Temporary Collateral Easing Measures.” Press release, April 7, 2020. 

https://www.ecb.europa.eu/press/pr/date/2020/html/ecb.pr200407~2472a8ccda.en.ht ml 

Ewerhart, Christian, and Jens Tapking. 2008. “Repo Markets, Counterparty Risk, and the 2007/2008 Liquidity Crisis.” ECB Working Paper No. 909, June 2008. www.ecb.europa.eu/pub/pdf/scpwps/ecbwp909.pdf 

Federal Reserve Board of Governors (Fed). 2023. “Federal Reserve Board Announces It Will Make Available Additional Funding to Eligible Depository Institutions to Help Assure Banks Have the Ability to Meet the Needs of All Their Depositors.” Press release, March 12, 2023. https://www.federalreserve.gov/newsevents/pressreleases/monetary20230312a.htm 

Freixas, Xavier, Curzio Giannini, Glenn Hoggarth, and Farouk Soussa. 2000. “Lender of Last Resort: What Have We Learned Since Bagehot?” _Journal of Financial Services Research_ 18, no. 1: 63–84. https://link.springer.com/article/10.1023/A:1026527607455 

Freixas, Xavier, Jean-Charles Rochet, and Bruno M. Parigi. 2004. “The Lender of Last Resort: A Twenty-First Century Approach.” _Journal of the European Economic Association_ 2, no. 6: 1085–115. https://onlinelibrary.wiley.com/doi/10.1162/1542476042813841 

Goodhart, Charles A.E. 1999. “Myths about the Lender of Last Resort.” _International Finance_ 2, no. 3: 339–60. https://onlinelibrary.wiley.com/doi/full/10.1111/1468-2362.00033 

Jordan, Thomas. 2023. “Price and Financial Stability – A Demanding Year for the Swiss National Bank.” Speech delivered at the 115th Ordinary General Meeting of Shareholders of the Swiss National Bank, Berne, Switzerland, April 28, 2023. https://www.bis.org/review/r230427i.htm 


Laeven, Luc, Glenn Schepens, and Isabel Schnabel. 2020. “Zombification in Europe in Times of Pandemic.” ECONtribute Policy Brief No. 11, October 2020. 

www.econtribute.de/RePEc/ajk/ajkpbs/ECONtribute_PB_011_2020.pdf 

Noonan, Laura, Stephen Morris, James Fontanella-Kahn, Arash Massoudi, and Owen Walker. 2023. “Switzerland Prepares Emergency Measures to Deliver UBS Takeover of Credit Suisse.” _Financial Times_ , March 18, 2023. 

https://www.ft.com/content/5746165a-3a0c-42c7-9a2e-cb7cf5f33f46 

Standard and Poor’s (S&P). 2023. “Default, Transition, and Recovery: 2022 Annual Global Corporate Default and Rating Transition Study.” February 2023. 

https://www.spglobal.com/ratings/en/research/articles/230425-default-transition-andrecovery-2022-annual-global-corporate-default-and-rating-transition-study-12702145 

Surane, Jennifer. 2023. “Citi CEO’ Fraser Warns Mobile Money Is ‘Game Changer’ for Bank Runs.” Bloomberg News, March 22, 2023. 

https://www.bloomberg.com/news/articles/2023-03-23/citi-s-fraser-warns-mobilemoney-is-game-changer-for-bank-runs 

Swiss National Bank (SNB). 2023. “Swiss National Bank Provides Substantial Liquidity Assistance to Support UBS Takeover of Credit Suisse.” Press release, March 19, 2023. https://www.snb.ch/en/mmr/reference/pre_20230319/source/pre_20230319.en.pdf 

Williamson, Oliver E. 1985. _The Economic Institutions of Capitalism_ . New York: Free Press. 

This open access article is distributed under the terms of the CC-BY-NC-ND 4.0 license, which allows sharing of this work provided the original author and source are cited. The work may not be changed or used commercially.
