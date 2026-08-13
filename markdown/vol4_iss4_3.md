## **Fire Sales, the LOLR, and Bank Runs with Continuous Asset Liquidity[1]** 

_Ulrich Bindseil[2 ] and Edoardo Lanari_[3] 

## **Abstract** 

Banks’ asset fire sales and recourse to central bank credit are modeled with continuous asset liquidity, allowing us to derive the liability structure of a bank. Both asset sales liquidity and the central bank collateral framework are modeled as power functions within the unit interval. Funding stability is captured as a strategic bank run game in pure strategies between depositors. Fire sale liquidity and the central bank collateral framework determine jointly the ability of the banking system to deliver maturity transformation without endangering financial stability. The model also explains why banks tend to use the least liquid eligible collateral with the central bank and why a sudden unanticipated reduction of asset liquidity, or a tightening of the collateral framework, can trigger a bank run. The model also shows that the collateral framework can be understood, beyond its aim to protect the central bank, as a financial stability and unconventional monetary policy instrument. 

**Keywords:** asset liquidity, bank intermediation spreads, bank run, capital structure, collateral, fire sales, lender of last resort 

**JEL Classifications:** C61, E43, E58, G21, G32, G33 

> 1 Opinions expressed are those of the authors. We wish to thank Stefano Corradin, Philipp Harms, Florian Heider, Slobodan Jelic, Simone Manganelli, Andrés Manzanares, Fernando Monar, Ken Nyholm, Isabel Schnabel, Leo von Thadden, and an anonymous referee. The second named author gratefully acknowledges the support of Praemium Academiae of M. Markl and RVO:67985840. 

> 2 Ulrich Bindseil, director general, Market Infrastructure and Payments, European Central Bank, ulrich.bindseil@ecb.europa.eu. 

> 3 Edoardo Lanari, quantitative researcher, Capital Fund Management, Paris, edoardo.lanari.el@gmail.com. 


## **1. Introduction** 

The model proposed in this paper sheds new light on how asset liquidity and the central bank collateral framework affect the liability structure of banks, financial stability, and monetary policy. The Global Financial Crisis of 2007–2009 (GFC) is said to also have been triggered by the insufficient asset liquidity buffers of banks relative to their short-term liabilities. These insufficient buffers would have led to an (at least temporarily) excessive reliance on central bank funding (BCBS 2013). The economic trade-offs between the efficiency of the banking system in delivering maturity transformation and financial stability is also crucial when assessing the net benefits of regulation for society. In the words of the _Turner Review_ : 

[T]here is a tradeoff to be struck. Increased maturity transformation delivers bene- fits to the non-bank sectors of the economy and produces term structures of interest rates more favorable to long-term investment. But the greater the aggregate degree of maturity transformation, the more the systemic risks and the greater the extent to which risks can only be offset by the potential for central bank liquidity assistance. (FSA 2009) 

Although the central bank collateral framework has drawn relatively limited attention in academic writing, it is one of the most complex and economically significant elements of monetary policy implementation (for example, Bindseil, Corsi et al. 2017; Bindseil, Dragu et al. 2017; Nyborg 2016). Unencumbered central bank eligible collateral is potential liquidity, as it can, in principle, be swapped into central bank money. It is therefore not an exaggeration to argue that the collateral framework must be an important ingredient of any theory of liquidity crises (as noted in Bagehot 1873) and of any monetary theory. The Markets Committee of the Bank for International Settlements (BIS) summarizes various measures central banks took during the Lehman Brothers crisis: 

During the height of the financial crisis in 2008–09, a number of central banks introduced, to varying degrees, crisis management measures such as a temporary acceptance of additional types of collateral, a temporary lowering of the minimum rating requirements of existing eligible collateral or a temporary relaxation of haircut standards. (BIS Markets Committee 2013, 8–9) 

The COVID-19 crisis again led central banks to relax their collateral frameworks, despite the fact that credit quality of issuers and counterparties did not improve. The European Central Bank (ECB) announced an “unprecedented” package on April 7, 2020: 

The Governing Council of the European Central Bank (ECB) today adopted a package of temporary collateral easing measures to facilitate the availability of eligible collateral for Eurosystem counterparties to participate in liquidity providing operations . . . the Eurosystem is increasing its risk tolerance to support the provision of credit via its refinancing operations, particularly by lowering collateral valuation haircuts for all assets consistently. . . . [T]he Governing Council decided to temporarily increase its risk tolerance level in credit operations through a general reduction of collateral valuation haircuts by a fixed factor of 20%. (ECB 2020) 


Three strands of academic literature are relevant to the present paper. First, Rochet and Vives (2004) is close to the present paper in the sense that it also models the role of fire sales and the central bank lender-of-last-resort (LOLR) function for banks’ funding stability, liquidity, and solvency. The model of Rochet and Vives, however, takes strong simplifying assumptions regarding asset liquidity (only two types of assets are distinguished: cash and nonliquid assets). Beyond Rochet and Vives, there is an extensive more general multiple funding equilibrium literature such as represented, for example, by Morris and Shin (2001) under the headline of “global games.” This literature uses more general and sophisticated equilibrium concepts than the present paper, which limits itself to pure and dominant strategies of investors/depositors, and to the existence or not of a strict Nash equilibrium in the sense of Fudenberg and Tirole (1991). Again, none of these papers, however, models explicitly fire sales and the central bank LOLR together, nor do they allow us to derive the bank’s liability structure from this modeling. Finally, there is a relatively recent bank run literature integrating bank runs and the LOLR into macroeconomic models, such as Gertler and Kiyotaki (2015) and De Fiore, Hoerova, and Uhlig (2021). These models are more ambitious in terms of integrating bank runs in a general equilibrium macro context, but the modeling of the limits of banks to issue short-term deposits is rather ad hoc (a moral hazard problem of the bank manager is postulated to limit deposit issuance; namely, bank managers would be able to divert assets from the bank to enrich themselves personally). In contrast, - in the model proposed here, the bank’s ability to issue short term deposits follows endogenously from the threat of a bank run. 

Second, Ashcraft, Garleanu, and Pedersen (2010) relates to the present model in the sense that central bank haircut policies are identified and modeled as a monetary policy instrument (see also Chapman, Chiu, and Molico 2011). Ashcraft, Garleanu, and Pedersen assumes that banks refinance assets at the central bank and that the haircut determines the leverage ratio and thus the funding costs of assets, being a weighted average of the risk-free rate and the shadow cost of equity (see also Brunnermeier and Pedersen 2009). 

Third, the present paper explains the spread between the risk-free rate (which is close to the rate of central bank credit operations and the rate of remuneration of overnight deposits of households with the banking system) and the actual funding costs of the real economy (or the effective monetary conditions for the economy). In this sense, the paper contributes to enrich the analysis of monetary policy in particular by capturing more explicitly the spread between the central bank credit operations rate and the actual monetary conditions as they are felt by participants in the real economy when seeking bank or market funding. Indeed, the present paper shows that a drop in bank asset liquidity and/or an increase in central bank haircuts both tighten effective monetary conditions in the sense that they reduce the ability of the banking system to undertake maturity transformation, and hence, everything else equal, will increase the share of “expensive” bank funding sources such as long-term bonds and equity, implying that also the lending rates that a competitive banking system is able to offer have to increase. 

Empirical evidence of the different degrees of banks’ asset liquidity, focusing on the case of the euro area, is provided by Bindseil, Dragu et al. (2017). The paper provides a cross-section analysis of liquidity properties and central bank collateral haircuts of the euro area fixed- 


income universe. That asset liquidity is continuous, and that it fluctuates over time, has been described empirically in the finance literature, such as recently in Dötz and Weth (2019), which also argues that liquidation will be carried out in a liquidity pecking order style and that marginal liquidation costs increase in redemptions (9–11), that is, as assumed in the present paper. The authors construct a sample of corporate bond fund asset liquidity data covering the 80 months before June 2016, referring to about 700,000 security holdings positions (12). The liquidity measure consists of monthly averages of bid-ask spreads. Figure 1 shows continuous portfolio liquidity, put at any moment in time in a “liquidity pecking order” (that is, securities ranked from the most to the least liquid). Obviously, the least liquid assets held by a corporate bond fund will still be more liquid than many other bank assets, such as in particular loan portfolios. Still, Dötz and Weth illustrates the idea of continuous asset liquidity and the changes of asset liquidity over time. 

[FIGURE id=vol4_iss4_3_f1 type=diagram label="Figure 1" file=figure_1.png caption="Liquidity Structure of Corporate Bond Funds across Time"]
### **Figure 1: Liquidity Structure of Corporate Bond Funds across Time**
![Figure 1](assets/vol4_iss4_3/figure_1.png)


Note: Bid-ask spread in basis points. 

_Source: Dötz and Weth 2019._ 

The paper also sheds new light on related debates. For example, first, Acosta-Smith et al. (2019), which studies the relationship between bank capital and liquidity transformation, finds that “banks engage in less liquidity transformation when they have higher capital,” but our paper suggests that there are alternative causalities that could explain this empirical pattern. Second, the literature on fire sales, as summarized by Shleifer and Vishny (2011), generally regards fire sales as entailing “systemic risk and significant [negative] externalities (43). Our paper models potential fire sales as being an integral part of maturity transformation by banks, whereby indeed, actual fire sales would not materialize in the absence of negative shocks on asset liquidity or asset values. Third, the present model provides further insights into empirical phenomena, such as those observed by Boyson, Helwege, and Jindra (2014), which investigates “which factor, liquidity or solvency, is more important for financial crisis.” Several further empirical hypotheses supported in that paper are captured also in our model, and therefore are supported by additional theoretical 


explanations. Finally, the paper also sheds new light on why both liquidity regulation and the lender of last resort are needed, extending the work of Carlson, Duygan-Bump, and Nelson (2015), among others. 

## **2. A Model of Funding Stability with Continuous Asset Liquidity and Haircuts** 

Throughout this paper, the following stylized bank balance sheet is assumed, with total length set to unit. Assets are heterogeneous in a continuous sense, while there are three types of liabilities that are each separately homogenous equity (e), long-term debt (t), and short-term deposits held by two depositors (each depositor holding therefore (1 − t − e)/2 short-term deposits), with e, t ≥ 0, e + t ∈ [0, 1]. 

[FIGURE id=vol4_iss4_3_f2 type=figure label="Figure 2" file=figure_2.png caption="Stylized Bank Balance Sheet"]
### **Figure 2: Stylized Bank Balance Sheet**

|**Assets**|**Liabilities**|
|---|---|
|Assets<br>1|Short-term debt 1<br>(1 – t – e)/2<br>Short-term debt 2<br>(1 – t – e)/2<br>Long-term debt (“term funding”)<br>t<br>Equity<br>e|



_Source: Created by the authors._ 

Short-term deposits can be subject to a bank run (Diamond and Dybvig 1983, 15). Banks could address this by not relying, or at least not extensively relying, on short-term funding. However, in general, investors prefer to hold short-term debt instruments over long-term debt instruments, and hence face a higher interest rate on long-term debt. In other words, long-term debt is associated with higher funding costs for the bank. Banks could also hold sufficient amounts of liquid assets, both in the sense of being able to liquidate these assets in case of need and to be able to pledge them with the central bank at limited haircuts. However, on average, liquid assets generate lower returns than illiquid ones. We next consider in more detail the different balance sheet positions. 

## **2.1 Bank Assets** 

Assets are continuous with regard to two liquidity characteristics: (i) Asset liquidity as measured by the “fire sale” discount to be accepted if an asset is to be sold in the short run; (ii) valuation haircut if submitted as central bank collateral. 

## _Bank Assets as Central Bank Collateral_ 

Assume that assets are ranked from those the central bank considers will require the lowest haircuts to those requiring the highest ones. The central bank collateral haircut function is 


set to be from the asset unit interval [0 _,_ 1] into the possible haircut unit interval [0, 1]. Assume that it has the following functional form with δ ≥ 0: 




The power function in the unit interval captures broadly the properties of a typical central bank haircut framework: haircuts for the most liquid assets will be close to zero, while haircuts for the least liquid assets accepted will be high, and an often-significant part of assets will not be accepted at all, which is equivalent to a 100% haircut. If δ is close to 0, then the haircuts increase and converge quickly towards 1. If in contrast δ is large (say 10) then haircuts stay at close to zero for a while and only start to increase in a convex manner when approaching the least liquid assets. The total haircut (and the average haircut) if all assets are pledged is 𝛿+1[1] ~~,~~ and hence potential central bank credit is 𝛿+1[𝛿] . This is obtained from the integration rule 𝒥 𝑥[𝛿] 𝑑𝑥= 𝛿+11 𝑥[𝛿+1] . For example, in the case of the Eurosystem, out of EUR 30 trillion of aggregated bank assets, the value of central bank eligible collateral after haircuts that could be used at any moment in time is about EUR 5 trillion. The eligibility criteria and haircut matrices are provided by the ECB, and one can match this information in principle with an informed guess of banks’ assets holdings. This implies that the effective average haircut applied by the Eurosystem to (the entirety of) bank assets is about 83% (EUR 25 trillion/EUR 30 trillion), and central bank refinancing power is about 17% of eligible assets, which approximately implies, if one assumes a power function as done above, a parameter value δ = 0.2. ECB (2015, 31) provides an overview of the ECB’s haircut scheme. 

## _Liquidity of Bank Assets_ 

Now consider asset liquidity in the sense of the ability of banks to sell assets in the short term without this inflicting a loss for the bank. Assume again that assets are ranked from the most liquid to the least liquid, and that the fire sale discount function is a function from [0 _,_ 1] to [0 _,_ 1] with the following function form, for _Θ_ ≥ 0: 




The smaller _Θ_ , the faster fire sale losses increase toward 100% when moving from the most liquid to the least liquid assets. If a certain share _x_ of the assets has to be sold, then the fire sale discounts will have to be booked as a loss and reduce equity. Assuming that the bank 1 starts with the most liquid assets, the loss will be 𝑥[Θ+1] . Empirical estimates of default Θ+1 costs in the corporate finance literature vary between 10% and 44% (see, for example, Davydenko, Strebulaev, and Zhao 2011; and Glover 2016). This cost can be interpreted as the liquidation cost of assets, captured in the parameter _Θ_ . Liquidation of all assets will lead to a damage of 1, so the remaining asset value will be _Θ_ . If default cost is 10%, this would mean that _Θ_ = 9, and if default cost is 44%, then Θ = 1.27. For a value of default costs in the middle of the empirical estimates of say 25%, one obtains _Θ_ = 3. 


## **2.2 Bank Liabilities** 

Four types of liabilities are distinguished: (i) _Short-term liabilities_ are equally split to two ex ante identical depositors; (ii) _Long-term debt_ does not mature within the period considered and is ranked pari passu with short-term debt; (iii) _Equity_ is junior to all other liabilities and cannot flow out either; and (iv) _Central bank borrowing_ is zero initially but can substitute for outflows of short-term liabilities in case of need. It is collateralized, and therefore the central bank acquires in case of default ownership of the assets pledged as collateral. Apart from this, the central bank claim ranks pari passu; that is, remaining claims after collateral liquidation are treated in the same way as an initial unsecured deposit. 

## **2.3 Timeline** 

The model is based on the following timeline: 

- Initially, the bank has the balance sheet composition as shown in Figure 1. 

- Short-term depositors/investors play a strategic game with two alternative actions: to run or not to run. “Running” means to withdraw deposits. If successful, the value of claims is afterwards equal to the initial value minus a small cost, _E_ , capturing the transaction cost of withdrawing the deposits. 

- It is not to be taken for granted that depositors can withdraw all their funds. Outflows need to be funded by the bank in some way: (i) recourse to central bank credit, assuming that the bank has sufficient eligible collateral; (ii) quick liquidation of assets (“fire sales”); or (iii) if it is impossible to pay out the depositors that want to withdraw their deposits, illiquidity-induced default will occur. In such case, all (remaining) assets need to be liquidated and corresponding default-related losses occur. 

- If the bank is not closed due to illiquidity, still its solvency needs verification after it undertakes fire sales. If capital is negative, the bank is resolved. Again, it is assumed in this case that the full costs of immediately liquidating all assets materialize. 

## **2.4 Strict Nash No-Run (SNNR) Equilibrium** 

The decision set of depositor _i (i =_ 1, 2 _)_ from which he will choose his decision _Di_ consists of _{Ki, Ri}_ , whereby “ _K_ ” stands for “keeping” deposits and “ _R_ ” stands for “run.” Let _Ui = Ui (D1, D2)_ be the payoff function of depositor _i._ Note that the strategic game is symmetric, that is: _U_ 1( _K_ 1 _, K_ 2) = _U_ 2( _K_ 1 _, K_ 2) _, U_ 1( _K_ 1 _, R_ 2) = _U_ 2( _R_ 1 _, K_ 2) _, U_ 1( _R_ 1 _, K_ 2) = _U_ 2( _K_ 1 _, R_ 2) _, U_ 1( _R_ 1 _, R_ 2) = _U_ 2( _R_ 1 _, R_ 2). This allows us in the rest of the paper to express conditions with reference to only one of the two players, say depositor 1. A strict Nash equilibrium is defined as a strategic game in which each player has a unique best response to the other players’ strategies (see Fudenberg and Tirole 1991). A strict Nash no-run (SNNR) equilibrium in the run game is therefore one in which the no-run choice dominates the “run” choice regardless of what the other depositors decide, that is, an SNNR equilibrium is defined by: 


## **3. Pure Reliance on Either Central Bank Credit or Asset Fire Sales** 

## **3.1Pure Reliance on Central Bank Funding** 

Assume first that asset liquidation is not an option, say, because markets are totally frozen, that is, Θ = 0. In this case, the analysis can focus on the sufficiency or not of buffers for central bank credit. The following proposition states the necessary condition for funding stability of banks in this case. 

**Proposition 3.1.** If Θ = 0, and assuming a small transaction cost _E_ of withdrawing 𝛿 1−𝑡−𝑒 deposits, an SNNR equilibrium prevails if and only if ≥ ~~,~~ that is, the liquidity 𝛿+1 2 buffer based on recourse to the central bank is not smaller than one-half of the short-2 term deposits. 

_Proof._ To prove this result (and similar subsequent propositions), it is sufficient to calculate through the payoffs for the alternative decisions of depositors under the possible parameter combinations and establish the frontiers of parameter combinations under which the conditions of an SNNR equilibrium apply. We now distinguish the three possible cases: (1 − 𝛿 (1−𝑡−𝑒) 𝛿 𝑡−𝑒) < (which we will denote by (1)), < < (1 −𝑡−𝑒) (which we will denote 𝛿+1 2 𝛿+1 𝛿 (1−𝑡−𝑒) by (2)), and < (denoted by (3)). These represent, respectively, the cases in which 𝛿+1 2 liquidity buffers provided by central bank collateral are sufficient to compensate for the withdrawal of all deposits, for the withdrawal of (not more than) one depositor, or for not even the withdrawal of one depositor. It may be noted that in the case assumed here that Θ = 0, illiquidity of the bank means complete destruction of asset value as the liquidation value of assets is assumed to be zero. The proposition follows from verifying the condition _U_ 1( _K_ 1 _, K_ 2) _> U_ 1( _R_ 1 _, K_ 2) and _U_ 1( _K_ 1 _, R_ 2) _> U_ 1( _R_ 1 _, R_ 2) for the three different cases distinguished above. One obtains the scenarios shown in Figure 3. 


[FIGURE id=vol4_iss4_3_f3 type=figure label="Figure 3" file=figure_3.png caption="Payoffs of Depositors in Three Cases (see Proof of Proposition 3.1)"]
### **Figure 3: Payoffs of Depositors in Three Cases (see Proof of Proposition 3.1)**

|Case||_U_1(_K_1_, K_2)||_U_1(_R_1_, K_2)|_U_1(_R_1_, K_2)||_U_1(_K_1_, R_2)||_U_1(_R_1_, R_2)|
|---|---|---|---|---|---|---|---|---|---|
|**(1)**||(1 −𝑡−𝑒)<br>2||(1 −𝑡−𝑒)<br>2<br>−𝐸|||(1 −𝑡−𝑒)<br>2||(1 −𝑡−𝑒)<br>2<br>−𝐸|
|**(2)**||(1 −𝑡−𝑒)<br>2||(1 −𝑡−𝑒)<br>2<br>−𝐸|||(1 −𝑡−𝑒)<br>2||1<br>2<br>𝛿<br>𝛿+ 1|
|||||||||||
|**(3)**||(1 −𝑡−𝑒)<br>2|||𝛿<br>𝛿+ 1||0||1<br>2<br>𝛿<br>𝛿+ 1|



_Source: Authors’ calculations._ 

It is easily verified that the conditions for an SNNR equilibrium are given if and only if (1−𝑡−𝑒) 𝛿 < ~~.~~ 2 𝛿+1 

## **3.2 Pure Reliance on Asset Fire Sales** 

Now consider the case in which the central bank does not offer any credit to banks, that is, accepts no collateral at all. In this case, _δ_ = 0, such that addressing deposit outflows will have to rely exclusively on asset liquidation. Assume that the bank does whatever it takes in terms of asset liquidation to avoid illiquidity-induced default. The total amount of liquidity that the Θ bank can generate through asset fire sales is . With full reliance on central bank lending, Θ+1 the question was whether the related liquidity buffers would be sufficient. In the present case, two default-triggering events need to be considered. Indeed, even if the bank has survived a liquidity withdrawal, it may afterwards be assessed as insolvent and thus be liquidated at the request of the bank supervisor. As noted above, for a given liquidity 1 withdrawal _x_ , the fire sale related loss is 𝑥[Θ+1] . The latter default event occurs if this loss Θ+1 exceeds initial equity.[4] 

**Proposition 3.2.** If _δ_ = 0, an SNNR equilibrium exists if and only if: 




The proposition can be verified by again establishing the strategic game payoffs and showing under which circumstances the SNNR conditions are met. The proof has been provided elsewhere (Bindseil 2013). In sum, to ensure financial stability in the case of absence of central bank credit, minimum liquidity and capital buffers are needed in some appropriate 

> 4 Note that it is assumed that equity is never sufficient to absorb the losses resulting from a bank default; that is, it is assumed that _e ≤ 1/(Θ + 1)_ . Of course, one could also calculate through the opposite case, but it is omitted here as it does not seem to match reality. 


combination to ensure the stability of a given amount of short-term funding. The lower the asset liquidity, the lower the amount of short-term funding that can be sustained for a given level of equity. 

## **4. Cases in Which the Banks Rely on Both Types of Liquidity Buffers** 

Now we consider the cases in which both _Θ, δ > 0_ . It is assumed that the ordering of assets is the same for both forms of liquidity generation; that is, if asset i is subject to lower fire sale discounts than asset j, then also asset i will have a lower central bank collateral haircut than asset j. Proposition 4.1 narrows the actual range of mixed cases, or cases in which both liquidity sources play a role in the planning of the bank. 

**Proposition 4.1.** If either _δ_ ≥ _Θ_ , or both _Θ > δ_ and _δ/(δ + 1)_ ≥ _(1- t- e)/2_ are satisfied, then banks will only rely on central bank credit to address possible deposit withdrawals, and hence the conditions established in Proposition 3.1 apply to the existence of an SNNR equilibrium. 

Taking recourse to the central bank does not cause a loss, while fire sales cause one. If, in addition, central bank recourse yields more liquidity (that is, _δ > Θ_ ), then central bank credit strictly dominates asset fire sales as a source of emergency liquidity. If _Θ > δ_ and central bank liquidity buffers allow us to address liquidity outflows relating to one depositor, that is, _δ/(δ + 1) (1- t- e)/2_ , which, as shown previously, allows us to sustain the SNNR equilibrium, then again relying only on central bank credit dominates strategies that rely on both sources. 

The cases in which the bank wants to rely potentially on both funding sources therefore appear to be limited to the ones in which _Θ > δ_ and _(1- t - e)/2 > δ/(δ + 1)_ . Again, a number of cases have to be distinguished. There will generally be a trade-off between the maximum liquidity generation and the ability to avoid losses, under the optimal use of the two funding sources. For example, the maximum generation of liquidity is achieved through fire sales only and will be equal to _Θ/(1 + Θ)_ . However, this also leads to the highest possible fire sales losses and damage to equity, _1/(1 + Θ)_ , and it is realistic to assume that this extent of losses would exceed equity. Regardless, if all the assets of the bank are sold, it has ceased to exist. The lowest generation of liquidity is achieved if all assets are pledged through central bank credit, and in this case, liquidity generation is _δ/(1 + δ)_ and fire sale losses are 0. Between these two extreme pairs of liquidity generation and fire sale losses, the set of efficient combinations of the two can be calculated. The following proposition addresses the question of whether the bank’s strategy should foresee the need to fire sale the most liquid assets and pledge the rest with the central bank, or the other way around. 

**Proposition 4.2.** In funding strategies to address withdrawals of short-term deposits rely on both funding sources, the bank should always foresee the need to fire sale the most liquid assets and pledge the less liquid assets. 


The proof of this proposition is provided in Bindseil (2013). The proof relies on showing that with the strategy to fire sale the most liquid assets and pledge the rest, the bank can achieve combinations of liquidity generation and fire sale cost, which are always superior to the combinations under the reverse strategy. The following Proposition 4.3 provides the condition in the case of strategies relying on both funding sources for an SNNR equilibrium, depending on the initial liability structure of the bank and the parameters Θ and δ. 

**Proposition 4.3.** Let z ∈ [0, 1] determine which share of its assets is foreseen by the bank to be used for fire sales (that is, the less liquid share _1 – z_ of assets is foreseen for pledging with the central bank). Let _k = h(z)_ be the fire sale losses from fire selling the _z_ most liquid assets and let _y = f (z)_ be the total liquidity generated from fire selling the most liquid assets _z_ and from pledging the least liquid assets _1 − z_ . Then, an SNNR equilibrium exists if and only if ∃ _z_ ∈ [0, 1], such that: 




The proof of this proposition is provided Bindseil (2013). Figure 3 illustrates the generation of liquidity and fire sale losses under strategy _z_ . The figure reflects that the bank plans to fire sale the most liquid part of its assets _z_ , and pledge with the central bank the least liquid part of assets _1 − z_ . Therefore, total liquidity y that could be generated corresponds to the sum of y1, the surface above the fire sale loss curve 𝑥[𝛩] up to z, and y2, the surface above the haircut curve _x[δ]_ , starting at _z_ . Fire sale losses _k_ will be equal to the surface below the fire sale loss curve between 0 and _z._ 


[FIGURE id=vol4_iss4_3_f4 type=figure label="Figure 4" file=figure_4.png caption="Liquidity Generation and Fire Sale Losses If Most Liquid Assets (from 0 to z) Are Sold, while Least Liquid Assets (from z to 1) Are Pledged with Central Bank"]
### **Figure 4: Liquidity Generation and Fire Sale Losses If Most Liquid Assets (from 0 to z) Are Sold, while Least Liquid Assets (from z to 1) Are Pledged with Central Bank**
![Figure 4](assets/vol4_iss4_3/figure_4.png)


_Source: Created by the authors._ 

## **5. Stable Funding Structure with the Lowest Possible Cost** 

In the previous sections, it was assumed that the initial bank balance sheet was given and the conditions for stability of short-term funding were established. It was shown that, depending on the bank’s liability structure, the haircut δ, and asset liquidity _Θ_ , short-term bank funding was stable or not. This section makes the liability structure endogenous in a simple setting. It is assumed that different liabilities require different remuneration rates but are at these rates perfectly elastic. For given, deterministic _δ_ and _Θ_ , competing banks can be assumed to choose the cheapest possible liability structure as determined by the conditions in the strategic depositor game, such that the single no-run equilibrium applies. Assume that the cost of remuneration of the three asset types are re for equity, rt for term funding, and 0 for short term deposits. Also assume that _re > rt > 0_ , and that _Θ > δ_ . In this setting, what will be the composition of the banks’ liabilities? The objective of the liability structure will be to minimize the average funding cost subject to maintaining a stable shortterm funding basis. 

- One strategy could be to rely only on central bank credit and thus aim to have _δ/(δ + 1) ≥ (1 – e – t)/2_ , such that fire sales will not be needed at all as backstop. If fire sales 


are not needed, then term funding is superior to equity and equity will be set to zero; that is, liabilities will consist only in term funding t and short-term deposits s = 1 – t. Therefore, the condition for stable short-term funding will be _δ/(δ + 1) ≥ (1 t)/2_ , which implies _t_[∗] _= 1 – 2δ/(δ + 1)_ . The average remuneration rate of bank funding will be _t_[∗] _rt_ . 

- A second strategy would be to rely only on the fire sales approach but to hold the necessary equity. This would mean that the two minimum conditions to be fulfilled are _z − z[Θ] /(1 +Θ) ≥ (1 − t − e)/2_ and _e ≥ (z[(1+Θ)] /(1 +Θ)_ . The funding costs _trt + ere_ can be minimized subject to these two constraints to obtain a unique optimum _t_[∗] _(Θ, re, rt_ ) and _e_[∗] _(Θ, re, rt)_ , to obtain the minimum average funding costs of the bank liabilities _t_[∗] _rt + e_[∗] _re_ . This case corresponds to _δ = 0_ in the following more general formulation. 

- A third, general strategy is to rely on both sources of funding, to plan to fire sell the most liquid assets from 0 to _z_ , and to pledge the least liquid assets from _z_ to 1, as described in Propositions 4.2 and 4.3 and in the following optimization problem. 

**Problem 5.1** . Suppose a bank relies on both sources of liquidity. The general problem of optimal liquidity management is to minimize through the choice of t, e, z ∈ [0, 1], with t + e ∈ [0, 1] the average remuneration rate of the banks’ liabilities t∗rt + e∗re, and with parameters subject to the two constraints: 







We provide the mathematical solution to this optimization problem in the Appendix. Figure 4 illustrates the functional relationships among the given parameters (Θ, δ, re, rt), and the optimum values of _e_ ∗, _t_ ∗, _s_ ∗, _z_ ∗, and _r_ ∗ (with _s_ ∗ =1 – _e_ ∗ – _t_ ∗ being the implied share of shortterm funding). Key findings are: the minimum bank intermediation cost _r_ ∗ falls monotonously in _Θ_ and in _δ_ before reaching zero (Figure 4.a). Both the share of assets foreseen for fire selling, _z_ ∗, and the equity ratio fall monotonously in _δ_ , but both first increase and then decrease again in _Θ_ (unless _δ_ is high enough to allow for _z_ ∗ = 0 and _e_ ∗ = 0) (Figure 4.b and 4.c). The share of long-term debt, _t_ ∗, falls monotonously in _Θ_ and in _δ_ before reaching zero (Figure 4.d). The share of short-term deposits, s∗, increases monotonously in _Θ_ and in _δ_ before reaching 100% (Figure 4.e). 


[FIGURE id=vol4_iss4_3_f5 type=chart label="Figure 5" file=figure_5.png caption="Minimum Funding Costs (** _**r**_ ***), Cost-Minimizing Liquidity-Generating Strategy (** _**z**_ **), and Liability Mix (** _**e**_ ***,** _**t**_ ***,** _**s**_ ***), as Functions of** _**δ**_ **and** _**Θ**_ **, for** _**rt**_ **= 5%,** _**re**_ **= 10%"]
### **Figure 5: Minimum Funding Costs (** _**r**_ ***), Cost-Minimizing Liquidity-Generating Strategy (** _**z**_ **), and Liability Mix (** _**e**_ ***,** _**t**_ ***,** _**s**_ ***), as Functions of** _**δ**_ **and** _**Θ**_ **, for** _**rt**_ **= 5%,** _**re**_ **= 10%**
![Figure 5](assets/vol4_iss4_3/figure_5.png)


- a. Minimum bank intermediation cost _r*_ as function of _θ_ and _δ_ 


[FIGURE id=vol4_iss4_3_f6 type=figure label="Exhibit 6" file=exhibit_6.png caption=""]
![Exhibit 6](assets/vol4_iss4_3/exhibit_6.png)


- c. Funding-cost minimizing share of equity funding, e*, as function of _θ_ and _δ_ 


[FIGURE id=vol4_iss4_3_f7 type=figure label="Exhibit 7" file=exhibit_7.png caption=""]
![Exhibit 7](assets/vol4_iss4_3/exhibit_7.png)


- b. Funding-cost minimizing share of assets foreseen for fire sales, _z*_ , as function of _θ_ , _δ_ 


[FIGURE id=vol4_iss4_3_f8 type=figure label="Exhibit 8" file=exhibit_8.png caption=""]
![Exhibit 8](assets/vol4_iss4_3/exhibit_8.png)


d. Funding-cost minimizing share of long-term funding, _t*_ , as function of _θ_ and _δ_ 


[FIGURE id=vol4_iss4_3_f9 type=figure label="Exhibit 9" file=exhibit_9.png caption=""]
![Exhibit 9](assets/vol4_iss4_3/exhibit_9.png)


e. Funding-cost minimizing share of short-term funding, _s*_ , as function of _θ_ and _δ_ 

_Source: Created by the authors._ 


[FIGURE id=vol4_iss4_3_f10 type=chart label="Figure 6" file=figure_6.png caption="a shows how the liability mix minimizing the funding cost evolves as a function of asset liquidity _Θ_ , for given collateral liquidity _δ_ = 0.2 (and again _rt_ = 5%, _re_ = 10%). It illustrates that the optimal equity share is not a monotonous function of the asset liquidity but reaches a maximum for about _Θ_ = 0.9. In contrast, the optimal long- and short-term funding shares decline monotonously with an improving asset liquidity (Figure 6.b shows the same relations, but for _δ_ = 0). Figure 6.c illustrates how the liability mix minimizing funding cost evolves as function of the equity premium _re_ , for a given term funding premium _rt_ = 2%, for given _(Θ, δ)_ = (0.5, 0.2). The equity share _e_ ∗ falls monotonously in the equity premium _r_ e, while the share of long-term debt _t_ ∗ increases monotonously in _r_ e. The share of short-term funding _s_ ∗ also declines monotonously in _re_ . Figure 6.d shows the same relationships for δ = 0."]
### **Figure 6: a shows how the liability mix minimizing the funding cost evolves as a function of asset liquidity _Θ_ , for given collateral liquidity _δ_ = 0.2 (and again _rt_ = 5%, _re_ = 10%). It illustrates that the optimal equity share is not a monotonous function of the asset liquidity but reaches a maximum for about _Θ_ = 0.9. In contrast, the optimal long- and short-term funding shares decline monotonously with an improving asset liquidity (Figure 6.b shows the same relations, but for _δ_ = 0). Figure 6.c illustrates how the liability mix minimizing funding cost evolves as function of the equity premium _re_ , for a given term funding premium _rt_ = 2%, for given _(Θ, δ)_ = (0.5, 0.2). The equity share _e_ ∗ falls monotonously in the equity premium _r_ e, while the share of long-term debt _t_ ∗ increases monotonously in _r_ e. The share of short-term funding _s_ ∗ also declines monotonously in _re_ . Figure 6.d shows the same relationships for δ = 0.**


[FIGURE id=vol4_iss4_3_f11 type=figure label="Figure 6" file=figure_6.png caption="Cheapest Stable Funding Mix (** _**e**_ ***,** _**t**_ ***,** _**s**_ ***), Depending on Asset Liquidity, Access to the Central Bank, and Relative Size of Equity Premium"]
### **Figure 6: Cheapest Stable Funding Mix (** _**e**_ ***,** _**t**_ ***,** _**s**_ ***), Depending on Asset Liquidity, Access to the Central Bank, and Relative Size of Equity Premium**
![Figure 6](assets/vol4_iss4_3/figure_6.png)


a. ( _e*_ , _t*_ , _s*_ ) as functions of _Θ_ , for _δ_ = 0.2; _rt_ = 5%, _re_ = 10%. X-axis: value of _Θ_ ; Y-axis: liability composition 


[FIGURE id=vol4_iss4_3_f12 type=figure label="Exhibit 12" file=exhibit_12.png caption=""]
![Exhibit 12](assets/vol4_iss4_3/exhibit_12.png)


b. ( _e*_ , _t*_ , _s*_ ) as functions of _Θ_ , for _δ_ = 0; _rt_ = 5%; _re_ = 10%. X-axis: value of _Θ_ ; Y-axis: liability composition 


[FIGURE id=vol4_iss4_3_f13 type=figure label="Exhibit 13" file=exhibit_13.png caption=""]
![Exhibit 13](assets/vol4_iss4_3/exhibit_13.png)


c. ( _e*_ , _t*_ , _s*_ ) as functions of _re_ , for _rt_ = 2%, and ( _Θ_ , δ) = (0.5, 0.2). X-axis: value of _re_ ; Y-axis: liability composition 


[FIGURE id=vol4_iss4_3_f14 type=figure label="Exhibit 14" file=exhibit_14.png caption=""]
![Exhibit 14](assets/vol4_iss4_3/exhibit_14.png)


d. ( _e*_ , _t*_ , _s*_ ) as functions of _re_ , for _rt_ = 2%, and ( _Θ_ , _δ_ ) = (0.5, 0). X-axis: value of _re_ ; Y-axis: liability composition 

_Source: Created by the authors._ 

## **6. The Central Bank Collateral Framework as a Policy Tool** 

Although the primary purpose of the central bank collateral framework is risk protection, the observed collateral policy measures of central banks during the GFC and in 2020 raise the question of what exactly the intentions of the central banks have been to widen collateral availability (and hence potential central bank recourse), in particular in a context of deteriorating asset liquidity. The model proposed in this paper allows interpreting the relaxation of the collateral framework as a policy measure: 


- (1) First, when _Θ_ (asset liquidity) suddenly declines, increasing _δ_ (by decreasing haircuts and broadening collateral eligibility) is a way to preserve the no-run equilibrium (the SNNR) and thereby is a necessary condition to prevent increases in central bank reliance, fire sales, and/or defaults. In this sense, it benefits all banks and financial stability in general, and not only those banks that already experience a run. Moreover, it may be noted that the model provides support to Bagehot’s “inertia principle,” according to which, the central bank should not tighten its collateral framework in a financial crisis as a reaction to the deterioration of asset liquidity: “If it is known that the Bank of England is freely advancing on what in ordinary times is reckoned a good security—on what is then commonly pledged and easily convertible—the alarm of the solvent merchants and bankers will be stayed . . . ” (Bagehot 1873). Lowering _δ_ when _Θ_ declines anyway would mean decreasing particularly strongly the amount of sustainable short-term funding and thereby maximizing the probability of a destabilization of bank funding, contributing, instead of preventing, large central bank recourse and fire sales of assets. 

- (2) Second, assuming that a deterioration of _Θ_ can be anticipated as a crisis is building, one could imagine that banks can adjust their liability structures in time. It would come at a high cost because, in such a context, investors also will have a strong preference for short-term assets and the collective attempt of all banks to increase the maturity of their liabilities will therefore lead to a steep increase of bank funding costs (and hence of bank lending rates). This would be procyclical, and an adjustment of the collateral framework parameter _δ_ could be seen as a policy tool to prevent such a steep increase of funding costs. 

- (3) Third, although the effect described in the previous point could in theory also be addressed by conventional monetary policy, that is, a lowering of central bank interest rates, this has limits as far as the zero lower bound is reached (as it was the case for most central banks in 2020). When this limit is reached, a widening of collateral availability may become relevant as an alternative approach to lowering effective bank funding costs or at least preventing their increase. 

In the context of the model, assume that _(Θ1_ , _δ1)_ are the pre-crisis asset parameters and (for a given equity and term funding premia _rt_ , _re_ ) the minimum funding cost is _r1_[∗] _= r_[∗] _(Θ1_ , _δ1)_ , and the related liability composition is _e1[*] = e_[∗] _(Θ1, δ1), t1_[∗] _= t_[∗] _(Θ1, δ1), s_[∗] _1 = s_[∗] _(Θ1_ , _δ1)_ . Assume that a market liquidity crisis materializes with Θ shifting from Θ1 to Θ2 < Θ1. This implies that _r2_[∗] = _r_[∗] _(Θ2_ , _δ1)_ > _r_ 1[∗] . Moreover, for _(Θ2_ , _δ1)_ , the funding structure _e_[∗] 1, _t_[∗] 1, _s_[∗] 1 does not allow for a single no-run equilibrium, but the banks are now in the multiple equilibrium case in which a bank run can occur. Now call _δ2_ the value of _δ_ for which _r_[∗] _(Θ2, δ2) = r1_[∗] . In other words, and assuming that the central bank is constrained by the zero lower bound, the collateral framework δ2 is the one that allows us to restore the monetary conditions (in the sense of the bank funding costs, and thus the bank lending rates) that prevailed before the liquidity crisis—however, only under the assumption that the banks can rapidly adjust their funding structures toward _e_[∗] 2 = _e_[∗] _(Θ2_ , _δ2), t_[∗] _2 = t_ ∗ _(Θ2_ , _δ2), s_[∗] 2 = _s_ ∗ _(Θ2_ , _δ2)._ Then, monetary conditions and financial stability have been restored. Alternatively, the central bank may immediately want to restore the single no-run equilibrium and not take the risk of a run in the possibly 


lengthy process of the adjustment of banks’ liability structures. This will require choosing another value of _δ_ , _δ2_ . Call _δ3_ the collateral framework that is obviously sufficient to restore immediately a no-run equilibrium, in the sense that _e_[∗] 1 ≤ _e_[∗] _(Θ2, δ3), t_[∗] 1 ≤ _t_[∗] ( _Θ2, δ3_ ), _s_[∗] 1 ≥ _s_[∗] ( _Θ2_ , _δ3_ ). However, _δ3_ is not strictly necessary for restoring a single no-run equilibrium. Call _δ4_ the smallest value of _δ_ for which the funding structure ( _e_[∗] 1, _t_[∗] 1, _s_[∗] 1) implies a no-run equilibrium for _(Θ2_ , _δ4)_ , that is, for which the sufficient equity condition (5) and the sufficient liquidity condition (4) are both fulfilled, whereby banks can of course recalibrate the parameter _z_ without any delay. 

In what follows, we refer the reader to the example Figure 7, with _rt_ = 5% and _re_ = 10%. Short-term funding costs are set at 0%, consistent with the idea that the zero lower bound is constraining. Figure 7 shows, for these given funding cost parameters, how the optimum values _r_[∗] , _z_[∗] , _e_[∗] , _t_[∗] , and _s_[∗] depend on the asset fire sale liquidity parameter _Θ_ and the collateral framework parameter _δ_ . 

Assume that ( _Θ1_ , _δ1_ ) = (0.7, 0.2) and that the banks have chosen the cheapest sustainable funding structures. Following Figure 7, we have ( _e_[∗] _1_ , _t_[∗] _1_ , _s_[∗] _1_ ) = (67%, 15%, 19%), to obtain funding costs of _r1_ ∗ = 2.5%. Let the crisis-related asset liquidity be _Θ2_ = 0.2. The table indicates that _δ2_ = 0.4, as _r_[∗] ( _Θ2_ , _δ2_ ) = 2.2% ≤ _r1_[∗] . A more radical move by the central bank to δ _3_ = 0.7 also obviously and immediately solves the issue of the bank run, as the optimal and thus sustainable funding mix for ( _Θ2_ , _δ3_ ) = (0.2, 0.7) is less demanding for sure than the precrisis funding mix, since the table indicates that _e_[∗] 1 ≤ _e_[∗] ( _Θ2, δ3_ ), _t_ ∗ _1_ ≤ _t_[∗] ( _Θ2, δ3_ ), _s_[∗] _1_ ≥ _s_[∗] ( _Θ2, δ3_ ). Finally, one may check if _δ_ = 0.6 or even _δ_ = 0.5 would also ensure the fulfilment of the sufficient equity and sufficient liquidity conditions (5) and (4). Note that for _(Θ1, δ1)_ , _z_[∗] = 44%, while for ( _Θ2_ , _δ3_ ), like for any ( _Θ, δ_ ) with _Θ ≤ δ_ , _z_[∗] = 0. It turns out that the bank simply needs to set _z_ = 0 and both _δ4_ = 0.6 and _δ4_ = 0.5 become sufficient from a funding stability perspective, while _δ4_ = 0.4 is indeed insufficient. Therefore, to immediately restore both an accommodative monetary policy stance and financial stability, after the liquidity crisis (after the deterioration of _Θ_ from 0.7 to 0.2), the central bank in this case should move its collateral framework _δ_ from 0.2 to 0.5. If this would be too accommodating from the monetary policy perspective, then the central bank could of course raise the short-term risk-free interest rate. 


[FIGURE id=vol4_iss4_3_f15 type=chart label="Figure 7" file=figure_7.png caption="Optimum Values of** _**r**_ ***,** _**s**_ ***,** _**e**_ ***,** _**t**_ ***, and** _**z**_ *** for** _**δ**_ **and** _**θ**_ **Each Taking Values {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8}, in %, with** _**rt**_ **= 5% and** _**re**_ **= 10%"]
### **Figure 7: Optimum Values of** _**r**_ ***,** _**s**_ ***,** _**e**_ ***,** _**t**_ ***, and** _**z**_ *** for** _**δ**_ **and** _**θ**_ **Each Taking Values {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8}, in %, with** _**rt**_ **= 5% and** _**re**_ **= 10%**

|**_r*_ (minimum funding cost)**|**δ = 0.1**|**δ = 0.2**|**δ = 0.3**|**δ = 0.4**|**δ = 0.5**|**δ = 0.6**|**δ = 0.7**|<br>**δ = 0.8**|
|---|---|---|---|---|---|---|---|---|
|**θ = 0.1**|4,1%|3,3%|2,7%|2,2%|1,7%|1,3%|0,9%|0,6%|
|**θ = 0.2**|4,1%|3,3%|2,8%|2,2%|1,7%|1,3%|0,9%|0,6%|
|**θ = 0.3**|3,9%|3,3%|2,7%|2,2%|1,7%|1,3%|0,9%|0,6%|
|**θ = 0.4**|3,7%|3,2%|2,7%|2,2%|1,7%|1,3%|0,9%|0,6%|
|**θ = 0.5**|3,3%|3,0%|2,6%|2,1%|1,7%|1,3%|0,9%|0,6%|
|**θ = 0.6**|2,9%|2,7%|2,4%|2,1%|1,7%|1,3%|0,9%|0,6%|
|**θ = 0.7**|2,6%|2,4%|2,2%|2,0%|1,6%|1,3%|0,9%|0,6%|
|**θ = 0.8**|2,2%|2,1%|1,9%|1,8%|1,5%|1,2%|0,9%|0,6%|
|**_s*_ (short-term funding**|**δ = 0.1**|**δ = 0.2**|**δ = 0.3**|**δ = 0.4**|**δ = 0.5**|**δ = 0.6**|**δ = 0.7**|<br>**δ = 0.8**|
|**ratio)**|||||||||
|**θ = 0.1**|18%|33%|46%|57%|67%|75%|82%|89%|
|**θ = 0.2**|20%|33%|46%|57%|67%|75%|82%|89%|
|**θ = 0.3**|27%|34%|46%|57%|67%|75%|83%|89%|
|**θ = 0.4**|38%|40%|47%|57%|67%|75%|83%|89%|
|**θ = 0.5**|49%|49%|51%|58%|67%|75%|82%|89%|
|**θ = 0.6**|58%|58%|58%|61%|67%|75%|82%|89%|
|**θ = 0.7**|67%|67%|66%|67%|69%|75%|82%|89%|
|**θ = 0.8**|75%|74%|74%|74%|75%|77%|82%|89%|
|**_e*_ (equity ratio)**|**δ = 0.1**|**δ = 0.2**|**δ = 0.3**|**δ = 0.4**|**δ = 0.5**|**δ = 0.6**|**δ = 0.7**|<br>**δ = 0.8**|
|**θ = 0.1**|0%|0%|0%|0%|0%|0%|0%|0%|
|**θ = 0.2**|2%|0%|0%|0%|0%|0%|0%|0%|
|**θ = 0.3**|6%|0%|0%|0%|0%|0%|0%|0%|
|**θ = 0.4**|11%|4%|1%|0%|0%|0%|0%|0%|
|**θ = 0.5**|15%|9%|3%|1%|0%|0%|0%|0%|
|**θ = 0.6**|17%|12%|7%|4%|0%|0%|0%|0%|
|**θ = 0.7**|19%|15%|11%|7%|2%|0%|0%|0%|
|**θ = 0.8**|20%|16%|13%|9%|5%|1%|0%|0%|
|**_t*_ (long-term funding**|**δ = 0.1**|**δ = 0.2**|**δ = 0.3**|**δ = 0.4**|**δ = 0.5**|**δ = 0.6**|**δ = 0.7**|<br>**δ = 0.8**|
|**ratio)**|||||||||
|**θ = 0.1**|82%|67%|54%|43%|33%|25%|18%|11%|
|**θ = 0.2**|78%|67%|54%|43%|33%|25%|18%|11%|
|**θ = 0.3**|68%|66%|54%|43%|33%|25%|17%|11%|
|**θ = 0.4**|51%|56%|53%|43%|33%|25%|17%|11%|
|**θ = 0.5**|37%|42%|46%|42%|33%|25%|18%|11%|
|**θ = 0.6**|24%|30%|34%|35%|33%|25%|18%|11%|
|**θ = 0.7**|14%|19%|23%|26%|29%|25%|18%|11%|
|**θ = 0.8**|5%|9%|13%|17%|20%|22%|17%|11%|
|**_z*_ (assets for fire sales)**|**δ = 0.1**|**δ = 0.2**|**δ = 0.3**|**δ = 0.4**|**δ = 0.5**|**δ = 0.6**|**δ = 0.7**|<br>**δ = 0.8**|
|**θ = 0.1**|0%|0%|0%|0%|0%|0%|0%|0%|
|**θ = 0.2**|5%|0%|0%|0%|0%|0%|0%|0%|
|**θ = 0.3**|13%|2%|0%|0%|0%|0%|0%|0%|
|**θ = 0.4**|26%|13%|3%|0%|0%|0%|0%|0%|
|**θ = 0.5**|36%|26%|13%|4%|0%|0%|0%|0%|
|**θ = 0.6**|44%|36%|26%|16%|4%|0%|0%|0%|
|**θ = 0.7**|51%|44%|36%|27%|13%|3%|0%|0%|
|**θ = 0.8**|56%|51%|44%|36%|26%|13%|3%|0%|



Note: Numbers in gray fields are those referred to in text. 

_Source: Created by the authors._ 


## **7. Conclusion** 

This paper provides a model of the role of the central bank collateral framework for the LOLR, bank intermediation costs, banks’ optimal funding structure, and monetary policy at the zero lower bound. Its innovation relative to the existing literature consists in specifying asset liquidity and the collateral framework as continuous functions in the unit interval, which allows building an integrated model encompassing all these dimensions and deriving an analytical solution of this model. We have shown how broadening the collateral framework, such as a number of central banks did in, for example, during the GFC and in 2020, can be considered to restore financial stability and adequate monetary conditions after a negative asset liquidity shock. Bank asset liquidity and the central bank collateral framework jointly determine financial stability and the ability of the banking system to deliver maturity transformation, which is one of its key functions. The model also shows that a widening of the central bank collateral set can prevent large recourse to central bank credit by banks suffering from a deterioration of asset liquidity. In this sense, the paper provides further illustration of Bagehot’s conjecture that only the “brave plan” of the 19th century Bank of England would be a “safe” plan. In other words, by being “brave” and increasing _δ_ after an exogenous drop of _Θ_ , the central bank will preserve the banks’ funding stability and thereby minimize the recourse of stressed banks to its credit facilities, and hence be on the “safe” side also in terms of financial exposures. The model also allows us to identify the impact of asset liquidity and of the central bank collateral framework on funding costs of banks and thereby on monetary policy conditions: first, policymakers need to be aware that a tightening of any of the two emergency liquidity sources of banks needs to be, everything else unchanged, compensated by a lowering of the monetary policy interest rate to maintain unchanged funding costs of the real economy. Second, when the central bank has reached the zero lower bound, and therefore cannot use standard interest rate policies any longer, it can consider using its collateral framework to counteract a further increase of actual funding costs of banks (and hence of the real economy depending on banks), which would otherwise result from the deteriorated asset liquidity because of the implied more expensive funding structure. 


## **8. References** 

Acosta-Smith, Jonathan, Guillaume Arnould, Kristoffer Milonas, and Quynh-Anh Vo. 2019. “Capital and Liquidity Interaction in Banking.” Bank of England. Staff Working Paper No. 840, December 2019. https://www.bankofengland.co.uk/working-paper/2019/capital-and-liquidityinteraction-in-banking 

Ashcraft, Adam, Nicolae Garleanu, and Lasse Heje Pedersen. 2010. “Two Monetary Tools: Interest Rates and Haircuts.” _NBER Macroeconomics Annual_ 25: 143–80. Chicago: University of Chicago Press. 

Bagehot, Walter. 1873. _Lombard Street: A Description of the Money Market_ . London: Henry S. King & Co. 

Bank for International Settlements Markets Committee (BIS Markets Committee). 2013. “Central Bank Collateral Frameworks and Practices.” Report by a Study Group chaired by Guy Debelle and established by the BIS Markets Committee. March 2013. https://www.bis.org/publ/mktc06.pdf 

Basel Committee on Banking Supervision (BCBS). 2013. “Basel III: The Liquidity Coverage Ratio and Liquidity Risk Monitoring Tools.” Bank for International Settlements, January 2013. 

https://www.bis.org/publ/bcbs238.pdf 

Bindseil, Ulrich. 2013. “Central Bank Collateral, Asset Fire Sales, Regulation and Liquidity.” ECB Working Paper Series, No. 1610, November 2013. https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp1610.pdf 

Bindseil, Ulrich, Marco Corsi, Benjamin Sahel, and Ad Visser. 2017. “The ECB Collateral Framework Explained.” ECB Occasional Paper, No. 189, May 2017. https://www.ecb.europa.eu/pub/pdf/scpops/ecb.op189.en.pdf 

Bindseil, Ulrich, Georgiana Dragu, Alexander Düring, and Julian von Landesberger. 2017. “Asset Liquidity, Central Bank Collateral, and Banks’ Liability Structure.” Unpublished working paper available at SSRN, October 2017. 

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3049792 

Boyson, Nicole, Jean Helwege, and Jan Jindra. 2014. “Crises, Liquidity Shocks, and Fire Sales at Commercial Banks.” _Financial Management_ 43, no. 4: 857–84. https://www.jstor.org/stable/43280207 

Brunnermeier, Markus, and Lars H. Pedersen. 2009. “Market Liquidity and Funding Liquidity.” _Review of Financial Studies_ 22, no. 6: 2201–38. https://www.princeton.edu/~markus/research/papers/liquidity.pdf 


Carlson, Mark, Burcu Duygan-Bump, and William R. Nelson. 2015. “Why Do We Need Both Liquidity Regulations and a Lender of Last Resort? A Perspective from Federal Reserve Lending during the 2007–09 US financial crisis.” Bank for International Settlements Working Paper No. 493, February 2015 _._ 

https://www.bis.org/publ/work493.pdf 

Chapman, James T., Jonathan Chiu, and Miguel Molico. 2011. “Central Bank Haircut Policy.” _Annals of Finance_ 7: 319–48. 

https://link.springer.com/article/10.1007/s10436-010-0171-5 

Davydenko, Sergei A., Ilya A. Strebulaev, and Xiaofei Zhao. 2011. “A Market-Based Study of the Cost of Default.” _Review of Financial Studies_ 25, no. 10: 2959–99. https://doi.org/10.1093/rfs/hhs091 

De Fiore, Fiorella, Marie Hoerova, and Harald Uhlig. 2021. “Money Markets, Collateral and Monetary Policy.” University of Chicago, Becker-Friedman Institute Working Paper No. 2018-79, December 2021. 

https://bfi.uchicago.edu/working-paper/money-markets-collateral-and-monetary-policy/ 

Diamond, Douglas W., and Peter H. Dybvig. 1983. “Bank Runs, Deposit Insurance, and liquidity.” _Journal of Political Economy_ 91, no. 3: 401–19. https://www.journals.uchicago.edu/doi/10.1086/261155 

Dötz, Nico, and Mark Weth. 2019. “Redemptions and Asset Liquidations in Corporate Bond Funds.” Deutsche Bundesbank Discussion Paper No. 11/2019, May 2019. https://www.bundesbank.de/resource/blob/793226/73de76968a7fc1046d1ddcb0f9800 c11/mL/2019-04-05-dkp-11-data.pdf 

European Central Bank (ECB). 2015. “The Financial Risk Management of the Eurosystem’s Monetary Policy Operations.” ECB Brochure, July 2015. 

https://www.ecb.europa.eu/pub/pdf/other/financial_risk_management_of_eurosystem_m onetary_policy_operations_201507.en.pdf 

———. 2020. “ECB Announces Package of Temporary Collateral Easing Measures.” Press release, April 7, 2020. 

https://www.ecb.europa.eu/press/pr/date/2020/html/ecb.pr200407~2472a8ccda.en.ht ml 

Financial Services Authority (FSA). 2009. _The Turner Review: A Regulatory Response to the Global Banking Crisis_ . London: Financial Services Authority. 

http://www.actuaries.org/CTTEES_TFRISKCRISIS/Documents/turner_review.pdf 

Fudenberg, Drew, and Jean Tirole. 1991. _Game Theory._ Cambridge, MA: MIT Press. 

Gertler, Mark, and Nobuhiro Kiyotaki. 2015. “Banking, Liquidity, and Bank Runs in an Infinite Horizon Economy.” _American Economic Review_ 105, no. 7, 2011–43. https://www.aeaweb.org/articles?id=10.1257/aer.20130665 


Glover, Brent. 2016. “The Expected Costs of Default.” _Journal of Financial Economics_ 119, no 2: 284–99. https://doi.org/10.1016/j.jfineco.2015.09.007 

Morris, Stephen, and Hyun Song Shin. 2001. “Global Games: Theory and Applications.” Cowles Foundation Discussion Paper No. 1275R, August 2001. https://cowles.yale.edu/publications/cfdp/cfdp-1275r 

Nyborg, Kjell. 2016. _Collateral Frameworks: The Open Secret of Central Banks._ Cambridge: Cambridge University Press. 

Rochet, Jean-Charles, and Xavier Vives. 2004. “Coordination Failures and the Lender of Last Resort: Was Bagehot Right after All?” _Journal of the European Economic Association_ 2, no. 6: 1116–47. https://academic.oup.com/jeea/article/2/6/1116/2280850 

Shleifer, Andrew, and Robert Vishny. 2011. “Fire Sales in Finance and Macroeconomics.” _Journal of Economic Perspectives_ 25, no. 1: 29–48. https://www.aeaweb.org/articles?id=10.1257/jep.25.1.29 


## **9. Appendix: Solution to Problem 5.1** 

The problem we want to solve consists of minimizing the function 𝑟: (𝑡, 𝑒) 

𝑟𝑡𝑡+ 𝑟𝑒𝑒 for given parameters 𝑟𝑒 ≥𝑟𝑡, over the subspace of triples (𝑡, 𝑒, 𝑧) ∈[0,1][3] , subject to the following constraints: 


[FIGURE id=vol4_iss4_3_f16 type=figure label="Exhibit 16" file=exhibit_16.png caption=""]
![Exhibit 16](assets/vol4_iss4_3/exhibit_16.png)


where 𝛩 > 𝛿≥0 are given parameters. 

Let 𝑊⊂[0,1][3] be the domain of admissible triples (𝑡, 𝑒, 𝑧). Clearly, 𝑊 is a compact subspace of 𝑅[3] ; therefore, 𝑟: 𝑊→𝑅 admits a minimum. Since the gradient ∇𝑟= (𝑟𝑡, 𝑟𝑒, 0) is nonvanishing everywhere on 𝑊, the minimum point lies on the boundary 𝜕𝑊. We now analyze the behavior of 𝑟 over a decomposition of such a boundary. Note that 𝜕𝑊=∪[5] 𝑖=1[𝑊] 𝑖[, where ] we set: 
















Let’s study 𝑟 on 𝑊1. If 𝑒= 0, then necessarily 𝑧= 0, which implies: 




1−𝛿 1−𝛿 If 𝛿≤1, we minimize _W_ by choosing (𝑡[∗] , 𝑒[∗] , 𝑧[∗] ) = , 0,0, which yields 𝑟[∗] = 𝑟𝑡 ~~.~~ Note that 1+𝛿 1+𝛿 in this case, 𝑡≤1, and equality holds if and only if 𝛿= 1. If instead 𝛿> 1, then (𝑡[∗] , 𝑒[∗] , 𝑧[∗] ) = (0,0,0) is admissible, so we obtain 𝑟[∗] = 0. From now on, we will assume 𝛿< 1 to avoid the trivial solution. 








We have ℎ(0) < 0, ℎ(1) > 0, and ℎ[′] (𝑧) > 0 for every 𝑧∈[0,1]. Therefore, ∃! 𝑧[∗] ∈[0,1] with 𝑧[Θ + 1] ℎ(𝑧[∗] ) = 0. By construction, 𝑧[∗] is the smallest value of 𝑧 for which 0, , 𝑧 satisfies all Θ + 1 (𝑧[∗] )[Θ + 1] (𝑧[∗] )[Θ + 1] constraints. Thus, we get a candidate triple 0, , 𝑧[∗] , which yields 𝑟[∗] = 𝑟𝑒 ~~.~~ Finally, Θ + 1 Θ + 1 𝑧= 0 can be reduced to an already analyzed case. 

On 𝑊2 and 𝑊3, it is easy to prove there is no better contribution from any possible 𝑧[Θ + 1] configuration. Turning to 𝑊4, we have 𝑒= ~~,~~ and 𝑡 is subject to the constraint: Θ + 1 




𝑧[Θ + 1] To minimize, we set 𝑡= −ℎ(𝑧), and we study 𝑟= 𝜑(𝑧) = −𝑟𝑡ℎ(𝑧) + 𝑟𝑒 . By solving Θ + 1 𝜑[′] (𝑧) = 0, we see that 𝜑 has a minimum at: 


[FIGURE id=vol4_iss4_3_f17 type=figure label="Exhibit 17" file=exhibit_17.png caption=""]
![Exhibit 17](assets/vol4_iss4_3/exhibit_17.png)


𝑧̅[Θ + 1] If ℎ(𝑧̅) ≤0, we have a new candidate triple (𝑡[∗] , 𝑒[∗] , 𝑧[∗] ) = −ℎ(𝑧̅), , 𝑧̅. Finally, the case of Θ + 1 𝑊5 can be reconducted to this last one, so the analysis is complete. The solution to the original problem is obtained by comparing the two (or three, depending on the cases) candidates selected by the algorithm we have just described. 

_Remark_ . If we fix 𝛿 and let Θ vary, we can observe that: 

𝛿−1 𝑧[𝛿+1] (1) 𝑧[∗] (Θ) ≤z[∗] (Θ[′] ) if Θ > Θ′, where 𝑧[∗] (Θ) denotes the unique solution to + 2 − 𝛿+1 𝛿+1 𝑧[Θ + 1] = 0 over [0,1] Θ + 1 




Thus, for Θ −δ big enough, we obtain 𝑧̅(Θ) > z[∗] (Θ), which forces us to pick (𝑡[∗] , 𝑒[∗] , 𝑧[∗] ) = 𝑧[∗] (Θ) 𝑧̅[Θ + 1] 0, , 𝑧[∗] (Θ) over (𝑡[∗] , 𝑒[∗] , 𝑧[∗] ) = −ℎ(𝑧̅), , 𝑧̅. On the other hand, for Θ close enough to 𝛿, Θ+1 Θ + 1 𝑧̅[Θ + 1] 𝑧[∗] (Θ) we have that (𝑡[∗] , 𝑒[∗] , 𝑧[∗] ) = −ℎ(𝑧̅), , 𝑧̅ is admissible, so that (𝑡[∗] , 𝑒[∗] , 𝑧[∗] ) = 0, , 𝑧[∗] (Θ) no Θ + 1 Θ+1 longer runs among candidates for the minimization of 𝑟. 


This open access article is distributed under the terms of the CC-BY-NC-ND 4.0 license, which allows sharing of this work provided the original author and source are cited. The work may not be changed or used commercially.
