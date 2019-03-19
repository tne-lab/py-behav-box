from scipy.stats import linregress
import matplotlib.pyplot as plt
import numpy as np

def abline(slope, intercept):
    """Plot a line from slope and intercept"""
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals, 'k--')

x = [-10,-4,-2, 29,1,17,1,16,18,23,14,
16,19,20,21,26,26,0,0,6]
y = [-0.005,.02,.03,.07,.005,.04,-.01,0.01,.02,.03,0,-.005,-.01,-.01,0,0.005,0,-.05,-.1,-.1]
print(len(x))
print(len(y))
plt.plot(x,y,'o')
axes = plt.gca()
axes.set_ylim([-.20,.15])
plt.xlabel('Discrimination Scale')
plt.ylabel('mPFC-BLA Theta Coherence')
plt.title('CS+ - CS- Subtraction')


x = linregress(x,y)
print(x)
plt.text(20,-.15,'R = ' + str(round(x.rvalue,5)))
plt.text(20,-.17,'p = ' + str(round(x.pvalue,5)))
abline(x.slope,x.intercept)


plt.show()
