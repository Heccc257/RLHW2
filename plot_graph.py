import matplotlib.pyplot as plt

def plot_results(lines, labels):
    plt.figure(figsize=(10, 6))
    for line, label in zip(lines, labels):
        x = range(len(line))
        plt.draw(x, line, label=label)
    plt.legend()
    plt.show()