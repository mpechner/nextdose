# Nextdose
New mag tag project. Lets me know if I took my insulin

I have had way too many times I have skipped my morning insulin. Now in the morning I have a new daily I cannot skip. 

The pills for the week holders are a great reminder. have not seen an equivilent for syringes.
I could 3d print a holder with spots to hold 2 syringes per day for mon-sun. But my tinkercad skills are non-existant, and pissed at my PRUSA.

Simple diplay: Next dose MONTH DAY {AM|PM}
- button 1: took dose - For the PM will advance to next day.  If pressed multiple times will do nothing.  For AM. will just change PM instead of AM.
- button 2: undo - reverts to previous state.
- button 3: refresh - redisplay current state.

On power up if current state is not set will display AM message for the day. Otherwise will display current state.

In flash store current state and previous state.

Hit the undo and it display previous state.  If last state empty, do nothing.
