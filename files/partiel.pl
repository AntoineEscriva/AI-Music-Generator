myst2(List,LR) :-myst(List, [] ,LR). 
myst([] ,Acc,Acc). 
myst([HIT] ,Acc,LR) :-
	yamyst(H,T,Ll,L2), 
	myst(L1,Acc,LR1) ,myst(L2, [l!ILRl] ,LR).
yamyst (_, [] , [] , [] ) . 
yamyst(H, [XIT], [XIL] ,G) :-X=<H,yamys (H,T,L,C). yamyst(H, [XIT] ,L, [XIG]) :-X>H,yamyst(H,T,L,C)
