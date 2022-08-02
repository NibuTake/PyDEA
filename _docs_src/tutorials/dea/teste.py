"""
This is my example script
=========================

This example doesn't do much, it just makes a simple plot
"""

# %%
# This is a section header
# ------------------------
# This is the first section!
# The `#%%` signifies to Sphinx-Gallery that this text should be rendered as
# rST and if using one of the above IDE/plugin's, also signifies the start of a
# 'code block'.

# This line won't be rendered as rST because there's a space after the last block.
myvariable = 2
print("my variable is {}".format(myvariable))

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 4 * np.pi, 301)
y1 = np.sin(x)
y2 = np.cos(x)

plt.figure()
plt.plot(x, y1, label="sin")
plt.plot(x, y2, label="cos")
plt.legend()
plt.show()
# This is the end of the 'code block' (if using an above IDE). All code within
# this block can be easily executed all at once.

# %%
# This is another section header
# ------------------------------
#
# In the built documentation, it will be rendered as rST after the code above!
# This is also another code block.

print("my variable plus 2 is {}".format(myvariable + 2))
