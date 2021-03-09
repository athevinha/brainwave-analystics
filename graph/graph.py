import matplotlib.pyplot as plt
import random
while True:
    total_1 = random.randint(0, 8)
    total_2 = random.randint(0, 8)
    plt.plot([total_1], [total_2], "go-", label="Ngoc Minh")
    plt.show()
