#######################################################
###   00 · INSTALL PACKAGES (run once per computer)  ###
#######################################################
# A package only needs to be installed ONCE on each computer.
# After that, you just load it with library() each time you open R.
#
# --- OPTION 1: Click (no code) --------------------------------------
# In RStudio, go to the Packages tab (bottom-right panel) -> Install
# -> type:  ggplot2, dplyr, tidyr  -> click Install.
#
# --- OPTION 2: Run the line below -----------------------------------
# Put your cursor on the line and press Cmd + Return (Mac) or Ctrl + Enter (Windows).

install.packages(c("ggplot2", "dplyr", "tidyr"))

# If R asks "Do you want to install from sources...?" type  n  and press Enter.


#######################################################
###          CHECK: did it work?                     ###
#######################################################
# If these run with no red "Error" message, you're ready.
library(ggplot2)
library(dplyr)
library(tidyr)


#######################################################
###     OPTIONAL (not needed for class)              ###
#######################################################
# ggrepel: keeps text labels from overlapping (used in the volcano plot solution)
# install.packages("ggrepel")